#!/usr/bin/env python
# -*- coding: utf-8 -*-

from numpy import random
from sc2.unit import UnitTypeId
from sc2.ids.ability_id import AbilityId
from s2clientprotocol import common_pb2

from core.register_board.request import Request
from core.bot.generic_bot_non_player import GenericBotNonPlayer
from core.bot.terran.build.build import Build, is_addon
from core.register_board.constants import OperationTypeId, RequestStatus, RequestPriority

from core.bot.util import get_mean_location


class BuildManager(GenericBotNonPlayer):
    """ Build manager class """

    current_iteration = 0

    true_start_location = None

    def __init__(self, bot_player):
        """
        :param core.bot.generic_bot_player.GenericBotPlayer bot_player:
        """
        super(BuildManager, self).__init__(bot_player)
        self._build_unit = None
        self._started_build_process = False

    def find_request(self):
        """ Implements the logic to find the requests that should be handled by the bot
        :return list[core.register_board.request.Request]
        """
        return self.bot_player.board_request.search_request_by_operation_id(OperationTypeId.BUILD)

    async def requests_handler(self, iteration):
        """ Logic to go through the bot requests
        :param int iteration: Game loop iteration
        """
        self.current_iteration = iteration



        for request in self.requests:
            if request.unit_type_id != UnitTypeId.SUPPLYDEPOT and \
                    self.bot_player.supply_left < 10 and self.bot_player.supply_cap < 200:
                Request(request_priority=RequestPriority.PRIORITY_HIGHER, unit_type_id=UnitTypeId.SUPPLYDEPOT,
                        operation_type_id=OperationTypeId.BUILD)

            if not self._build_unit:
                self.set_build_unit(iteration=iteration, request=request)

            elif self._build_unit and (not self._build_unit.request or self._build_unit.request.status == RequestStatus.DONE
                                       or self._build_unit.request.status == RequestStatus.FAILED):
                self._build_unit.set_request(request)

            if not self._started_build_process and self._build_unit.request.status in [RequestStatus.TO_BE_DONE,
                                                                                       RequestStatus.FAILED]:

                # evita treinar marines se precisar melhorar as barracas
                if is_addon(request.unit_type_id):
                    self.bot_player.board_request.register(
                        Request(request_priority=RequestPriority.PRIORITY_HIGHER,
                                operation_type_id=OperationTypeId.TRAIN_MARINE_DENY)
                    )

                self._set_best_location(request)
                await self._build_unit.default_behavior(iteration)
            break

        if self._build_unit:
            await self._build_unit.depot_behaviour()

    def building_completed(self, request):
        units = self.bot_player.units(request.unit_type_id)
        if units:
            unit = units.closest_to(request.location)
            if unit:
                if unit.is_ready and unit.distance_to(request.location) < 6:
                    return True
        return False

    def requests_status_update(self):
        """ Logic to update the requests status """

        if not self.true_start_location:
            command_centers = self.bot_player.units(UnitTypeId.COMMANDCENTER)
            if command_centers:
                self.true_start_location = command_centers[0].position

        if self._build_unit and self.bot_player.get_current_scv_unit(self._build_unit.unit_tags[0]):
            request = self._build_unit.info.request

            request_is_addon = is_addon(request.unit_type_id)

            if request_is_addon:
                if self._build_unit.build_upgraded_tag:
                    units = self.bot_player.get_current_units([self._build_unit.build_upgraded_tag])
                    if units:
                        unit = units[0]
                    else:
                        unit = None
                else:
                    unit = None
            else:
                unit = self.bot_player.get_current_scv_unit(self._build_unit.unit_tags[0])

            if unit:
                orders = unit.orders
                self._started_build_process = True

                for order in orders:
                    target_unit = self.get_target_unit(order)
                    request_status = request.status
                    self._started_build_process = False

                    if request_is_addon and order.ability.id in [AbilityId.BUILD_REACTOR,
                                                                 AbilityId.BUILD_REACTOR_BARRACKS,
                                                                 AbilityId.BUILD_REACTOR_FACTORY,
                                                                 AbilityId.BUILD_REACTOR_STARPORT,
                                                                 AbilityId.BUILD_TECHLAB,
                                                                 AbilityId.BUILD_TECHLAB_BARRACKS,
                                                                 AbilityId.BUILD_TECHLAB_FACTORY,
                                                                 AbilityId.BUILD_TECHLAB_STARPORT
                                                                 ]:
                        self.bot_player.board_request.register(
                            Request(request_priority=RequestPriority.PRIORITY_HIGHER,
                                    operation_type_id=OperationTypeId.TRAIN_MARINE_ALLOW)
                        )
                    elif target_unit and target_unit.type_id == request.unit_type_id and not target_unit.is_ready:
                        if request_status != RequestStatus.ON_GOING:
                            self.log('Starting request: {}'.format(self._build_unit.info.request))
                            request.status = RequestStatus.ON_GOING
                    elif (target_unit and target_unit.type_id == request.unit_type_id and target_unit.is_ready) or self.building_completed(request):
                        request.status = RequestStatus.DONE
                        self.bot_player.board_request.remove(request)
                    elif order.ability.id in [AbilityId.HARVEST_GATHER, AbilityId.HARVEST_RETURN] and request.status == RequestStatus.START_DOING:
                        request.status = RequestStatus.FAILED

    def get_target_unit(self, order):
        """
        :param order:
        :return:
        """
        if isinstance(order.target, common_pb2.Point):
            return self.bot_player.get_units_by_position(
                position_x=order.target.x,
                position_y=order.target.y
            )

    def set_build_unit(self, iteration, request):
        """ Sets a unit for the build unit
        :param int iteration: Game loop iteration
        :param core.register_board.request.Request request:
        """
        self.log('Setting unit to Build bot unit')
        available_scvs = self.find_available_scvs_units()

        if available_scvs:
            self._build_unit = Build(
                bot_player=self.bot_player,
                iteration=iteration,
                request=request,
                unit_tags=[available_scvs[0].tag]
            )

    def _set_best_location(self, request):
        """ Sets best location to build
        :param core.register_board.request.Request request:
        """
        if request.unit_type_id == UnitTypeId.REFINERY:
            request.location = self.bot_player.state.vespene_geyser(UnitTypeId.VESPENEGEYSER).closest_to(self.true_start_location or self.bot_player.start_location)
        else:
            our_expansion = self.bot_player.get_owned_expansions_locations()[0]
            resources_list = self.bot_player.get_resources_locations(our_expansion)
            resource_location = resources_list[random.randint(0, len(resources_list)-1)]
            # command_center = self.bot_player.units.structure[0]
            command_center = self.bot_player.owned_expansions.popitem()[1]
            request.location = get_mean_location(resource_location.position, command_center.position)
