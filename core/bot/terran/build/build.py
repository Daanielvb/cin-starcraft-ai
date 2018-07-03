#!/usr/bin/env python
# -*- coding: utf-8 -*-

from sc2.ids.ability_id import AbilityId
from sc2.ids.unit_typeid import UnitTypeId
from sc2.position import Point2

from core.bot.generic_bot_non_player_unit import GenericBotNonPlayerUnit
from core.register_board.constants import RequestPriority, OperationTypeId
from core.register_board.request import Request
from strategy.cin_deem_team.terran.build_dependencies import DEPENDENCIES, BUILD, TECHNOLOGY, SUPPLY


def is_addon(unit_type):
    return unit_type in [UnitTypeId.BARRACKSTECHLAB, UnitTypeId.BARRACKSREACTOR, UnitTypeId.FACTORYTECHLAB,
                         UnitTypeId.FACTORYREACTOR, UnitTypeId.STARPORTTECHLAB, UnitTypeId.STARPORTREACTOR]


class Build(GenericBotNonPlayerUnit):
    """  A Scout bot class """

    def __init__(self, bot_player, iteration, request, unit_tags):
        """
        :param core.bot.generic_bot_player.GenericBotPlayer bot_player:
        :param int iteration:
        :param core.register_board.request.Request request:
        :param list(int) unit_tags:
        """
        super(Build, self).__init__(
            bot_player=bot_player, iteration=iteration, request=request, unit_tags=unit_tags
        )

    build_upgraded_tag = None

    async def default_behavior(self, iteration):
        """ The default behavior of the bot
        :param int iteration: Game loop iteration
        """
        await self._build()

    def get_addon_location(self, addon_type, location):
        if addon_type in [UnitTypeId.BARRACKSTECHLAB, UnitTypeId.BARRACKSREACTOR]:
            barracks = self.bot_player.units(UnitTypeId.BARRACKS).prefer_close_to(location)
            for barrack in barracks:
                if not barrack.has_add_on:
                    return barrack
        elif addon_type in [UnitTypeId.FACTORYTECHLAB, UnitTypeId.FACTORYREACTOR]:
            factories = self.bot_player.units(UnitTypeId.FACTORY).prefer_close_to(location)
            for factory in factories:
                if not factory.has_add_on:
                    return factory
        elif addon_type in [UnitTypeId.STARPORTTECHLAB, UnitTypeId.STARPORTREACTOR]:
            factories = self.bot_player.units(UnitTypeId.STARPORT).prefer_close_to(location)
            for factory in factories:
                if not factory.has_add_on:
                    return factory
        return None

    def validate_location(self, location):
        ref_constructions = self.bot_player.units(UnitTypeId.BARRACKS)\
                            + self.bot_player.units(UnitTypeId.FACTORY)\
                            + self.bot_player.units(UnitTypeId.STARPORT)
        for construction in ref_constructions:
            if location.x > construction.position.x and construction.position.distance_to(location) < 15:
                return False
        return True

    async def fix_location(self, location, build_type):
        if location:
            position_ok = False
            can_move_left = True
            # garante que nao vai ocupar o espaco para Techs e Reactors
            for i in range(2):
                position_ok = await self.bot_player.can_place(build_type, location)
                if position_ok and self.validate_location(location):
                    break
                else:
                    can_move_left = False
                    location = Point2((location.x+1, location.y))
            if not position_ok:
                location = None
            else:
                # garante que tera espaco para Techs e Reactors
                if build_type in [UnitTypeId.BARRACKS, UnitTypeId.FACTORY, UnitTypeId.STARPORT]:
                    position_ok = False
                    have_right_space = await self.bot_player.can_place(build_type, Point2((location.x+1, location.y)))
                    for i in range(3):
                        position_ok = await self.bot_player.can_place(build_type, location)
                        if position_ok and have_right_space:
                            position_ok = True
                            break
                        elif can_move_left:
                            location = Point2((location.x-1, location.y))
                            have_right_space = position_ok
                            position_ok = False
                        else:
                            position_ok = False
                            break
                    if not position_ok:
                        location = None
        return location

    async def get_building_location(self, build_type):
        location = self.info.request.location.towards_with_random_angle(self.bot_player.game_info.map_center, 10)
        location = await self.bot_player.find_placement(build_type, location, max_distance=50)
        location = await self.fix_location(location, build_type)
        return location

    async def _build(self):
        """
        Build action
        """
        if self.info.request.location:
            if await self._check_dependencies(self.info.request):
                build_type = self.info.request.unit_type_id
                location = self.info.request.location

                if is_addon(build_type):
                    building = self.get_addon_location(build_type, location)
                    if building:
                        self.info.request.location = building.position
                        self.build_upgraded_tag = building.tag
                        await self.bot_player.do(building.build(build_type, building.position))
                else:
                    scv = await self.get_builder(location)
                    if scv:
                        if build_type != UnitTypeId.REFINERY:
                            location = await self.get_building_location(build_type)
                        else:
                            print(location)
                        if location:
                            await self.bot_player.do(scv.build(build_type, location))

        else:
            self.log("Location is None to build: {}".format(self.info.request))

    def get_worker(self, location):
        # versao que evita pegar o scout
        workers = self.bot_player.workers.closer_than(20, location) or self.bot_player.workers
        for worker in workers.prefer_close_to(location).prefer_idle:
            if not worker.orders or len(worker.orders) == 1\
                    and worker.orders[0].ability.id in [AbilityId.HARVEST_GATHER, AbilityId.HARVEST_RETURN]:
                return worker
        return workers.random

    async def get_builder(self, location=None):
        scv = None

        if not self.info.unit_tags:
            scv = self.get_worker(location)
            self.info.unit_tag = scv.tag
        else:
            scv = self.bot_player.get_current_scv_unit(self._info.unit_tags[0])

            if not scv and location:
                scv = self.get_worker(location)

        return scv

    async def depot_behaviour(self):
        """
        Supply depot behaviour
        """
        for depot in self.bot_player.units(UnitTypeId.SUPPLYDEPOT).ready:
            await self.bot_player.do(depot(AbilityId.MORPH_SUPPLYDEPOT_LOWER))

    async def _check_dependencies(self, request):
        """
        Check request dependencies.
        :param core.register_board.request.Request request:
        :return bool:
        """
        requested_unit = request.unit_type_id
        request_dependencies = DEPENDENCIES.get(requested_unit)
        can_build = True

        if request_dependencies:
            can_build = self.bot_player.can_afford(requested_unit)
            can_build = can_build.can_afford_minerals and can_build.can_afford_vespene

            build_dependencies = request_dependencies[BUILD]
            can_build = can_build and await self.check_build_dependencies(request, build_dependencies, can_build)

            tech_dependencies = request_dependencies[TECHNOLOGY]
            can_build = can_build and await self.check_technology_dependencies(request, tech_dependencies, can_build)

            supply_dependencies = request_dependencies[SUPPLY]
            can_build = can_build and await self.check_supply_dependencies(request, supply_dependencies, can_build)

        return can_build

    async def check_supply_dependencies(self, request, supply_dependencies, can_build):
        """
        Check supply dependencies
        :param core.register_board.request.Request request:
        :param supply_dependencies:
        :param can_build:
        :return:
        """
        if self.bot_player.supply_left > supply_dependencies:
            pass
        else:
            self.bot_player.board_request.register(
                Request(request_priority=request.request_priority_level, unit_type_id=UnitTypeId.SUPPLYDEPOT,
                        operation_type_id=OperationTypeId.BUILD)
            )
            can_build = False
        return can_build

    async def check_technology_dependencies(self, request, tech_dependencies, can_build):
        """
        Check technology dependencies
        :param core.register_board.request.Request request:
        :param tech_dependencies:
        :param can_build:
        :return:
        """
        for dependency in tech_dependencies:
            if self.bot_player.get_available_abilities(dependency).amount > 0:
                can_build = can_build and True
            else:
                self.bot_player.board_request.register(
                    Request(request_priority=request.request_priority_level, unit_type_id=dependency,
                            operation_type_id=OperationTypeId.RESEARCH_TECHNOLOGY)
                )
                can_build = False
                break
        return can_build

    async def check_build_dependencies(self, request, build_dependencies, can_build):
        """
        Check build dependencies
        :param core.register_board.request.Request request:
        :param build_dependencies:
        :param can_build:
        :return:
        """
        for dependency in build_dependencies:
            if self.bot_player.units(dependency).amount > 0:
                can_build = can_build and True
            else:
                self.bot_player.board_request.register(
                    Request(request_priority=request.request_priority_level, unit_type_id=dependency,
                            operation_type_id=OperationTypeId.BUILD)
                )
                can_build = False
                break
        return can_build