#!/usr/bin/env python
# -*- coding: utf-8 -*-
from numpy import random

from core.bot.generic_bot_non_player import GenericBotNonPlayer
from core.bot.terran.build.build import Build
from core.register_board.constants import OperationTypeId, RequestStatus
from strategy.cin_deem_team.terran.build_dependencies import *

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
            self.log(request)
            if not self._build_unit:
                available_scvs = self.find_available_scvs_units()
                self.log("Request to build {}".format(request.unit_type_id))
                if available_scvs:
                    self._build_unit = Build(
                        bot_player=self.bot_player,
                        iteration=iteration,
                        request=request,
                        unit_tag=available_scvs[0].tag
                    )
            elif self._build_unit and (
                    not self._build_unit.request or self._build_unit.request.status == RequestStatus.DONE):

                self.log("New request={} to unit={}".format(request.request_id, self._build_unit.unit_tag))
                self._build_unit.set_request(request)

            if self._build_unit.request.status == RequestStatus.TO_BE_DONE and await self._check_dependencies(request):
                self._set_best_location(request)
                self.log(request)
                await self._build_unit.default_behavior(iteration)

    def requests_status_update(self):
        if self._build_unit:
            if self._build_unit.info.request.status != RequestStatus.FAILED \
                    and self._build_unit.info.request.status != RequestStatus.DONE:
                if self._build_unit.is_idle():
                    self.bot_player.board_request.remove(self._build_unit.info.request)
                    self._build_unit.info.status = RequestStatus.DONE

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

    def _set_best_location(self, request):
        """
        Set best location to build
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
