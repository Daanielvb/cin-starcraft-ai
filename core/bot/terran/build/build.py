#!/usr/bin/env python
# -*- coding: utf-8 -*-

from sc2.ids.ability_id import AbilityId
from sc2.ids.unit_typeid import UnitTypeId

from core.bot.generic_bot_non_player_unit import GenericBotNonPlayerUnit
from strategy.cin_deem_team.terran.build_dependencies import DEPENDENCIES, BUILD, TECHNOLOGY, SUPPLY


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

    async def default_behavior(self, iteration):
        """ The default behavior of the bot
        :param int iteration: Game loop iteration
        """
        await self._build()
        await self.depot_behaviour()

    async def _build(self):
        """
        Build action
        """
        if self.info.request.location:
            build_type = self.info.request.unit_type_id

            if self.info.request.unit_type_id == UnitTypeId.REFINERY:
                location = self.info.request.location
            else:
                location = self.info.request.location.towards_with_random_angle(self.bot_player.game_info.map_center, 8)

            scv = await self.get_builder(location)
            if scv and await self._check_dependencies(self.info.request):
                await self.bot_player.do(scv.build(build_type, location))

        else:
            self.log("Location is None to build: {}".format(self.info.request))

    async def get_builder(self, location=None):
        scv = None

        if not self.info.unit_tags:
            scv = self.bot_player.select_build_worker(location, True)
            self.info.unit_tag = scv.tag
        else:
            scv = self.bot_player.get_current_scv_unit(self._info.unit_tags[0])

            if not scv and location:
                scv = self.bot_player.select_build_worker(location, True)

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
        :param core.register_board.request.Request: request
        :return bool:
        """
        requested_unit = request.unit_type_id
        request_dependencies = DEPENDENCIES.get(requested_unit)
        can_build = True

        if request_dependencies:
            can_build = self.bot_player.can_afford(requested_unit)
            can_build = can_build.can_afford_minerals and can_build.can_afford_vespene

            build_dependencies = request_dependencies[BUILD]
            can_build = can_build and await self.check_build_dependencies(build_dependencies, can_build)

            tech_dependencies = request_dependencies[TECHNOLOGY]
            can_build = can_build and await self.check_technology_dependencies(tech_dependencies, can_build)

            supply_dependencies = request_dependencies[SUPPLY]
            can_build = can_build and await self.check_supply_dependencies(supply_dependencies, can_build)

        return can_build

    async def check_supply_dependencies(self, supply_dependencies, can_build):
        """
        Check supply dependencies
        :param supply_dependencies:
        :param can_build:
        :return:
        """
        if self.bot_player.supply_left > supply_dependencies:
            pass
        else:
            # register needed of supply
            can_build = False
        return can_build

    async def check_technology_dependencies(self, tech_dependencies, can_build):
        """
        Check technology dependencies
        :param tech_dependencies:
        :param can_build:
        :return:
        """
        for dependency in tech_dependencies:
            if self.bot_player.get_available_abilities(dependency).amount > 0:
                can_build = can_build and True
            else:
                # register needed technology
                can_build = False
                break
        return can_build

    async def check_build_dependencies(self, build_dependencies, can_build):
        """
        Check build dependencies
        :param build_dependencies:
        :param can_build:
        :return:
        """
        for dependency in build_dependencies:
            if self.bot_player.units(dependency).amount > 0:
                can_build = can_build and True
            else:
                # register needed unit
                can_build = False
                break
        return can_build