#!/usr/bin/env python
# -*- coding: utf-8 -*-

from numpy import random
from sc2.unit import UnitTypeId
from s2clientprotocol import common_pb2

from core.bot.generic_bot_non_player import GenericBotNonPlayer
from core.bot.terran.build.build import Build
from core.register_board.constants import OperationTypeId, RequestStatus

from core.bot.util import get_mean_location


class BuildManager(GenericBotNonPlayer):
    """ Build manager class """

    def __init__(self, bot_player):
        """
        :param core.bot.generic_bot_player.GenericBotPlayer bot_player:
        """
        super(BuildManager, self).__init__(bot_player)
        self._build_unit = None

    def find_request(self):
        """ Implements the logic to find the requests that should be handled by the bot
        :return list[core.register_board.request.Request]
        """
        return self.bot_player.board_request.search_request_by_operation_id(OperationTypeId.BUILD)

    async def requests_handler(self, iteration):
        """ Logic to go through the bot requests
        :param int iteration: Game loop iteration
        """
        for request in self.requests:
            if not self._build_unit:
                self.set_build_unit(iteration=iteration, request=request)

            elif self._build_unit and (not self._build_unit.request or self._build_unit.request.status == RequestStatus.DONE):
                self._build_unit.set_request(request)

            if self._build_unit.request.status == RequestStatus.TO_BE_DONE:
                self._set_best_location(request)
                await self._build_unit.default_behavior(iteration)

    def requests_status_update(self):
        """ Logic to update the requests status """
        if self._build_unit:
            orders = self.bot_player.get_current_scv_unit(self._build_unit.unit_tags[0]).orders

            for order in orders:
                target_unit = self.get_target_unit(order)
                request_status = self._build_unit.info.request.status

                if target_unit and not target_unit.is_ready and request_status != RequestStatus.ON_GOING:
                    self.log('Starting request: {}'.format(self._build_unit.info.request))
                    self._build_unit.info.request.status = RequestStatus.ON_GOING

                elif target_unit and target_unit.is_ready:
                    self._build_unit.info.request.status = RequestStatus.DONE
                    self.bot_player.board_request.remove(self._build_unit.info.request)

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
            request.location = self.bot_player.state.vespene_geyser.closest_to(self.bot_player.start_location)
        else:
            our_expansion = self.bot_player.get_owned_expansions_locations()[0]
            resources_list = self.bot_player.get_resources_locations(our_expansion)
            resource_location = resources_list[random.randint(0, len(resources_list)-1)]
            # command_center = self.bot_player.units.structure[0]
            command_center = self.bot_player.owned_expansions.popitem()[1]
            request.location = get_mean_location(resource_location.position, command_center.position)
