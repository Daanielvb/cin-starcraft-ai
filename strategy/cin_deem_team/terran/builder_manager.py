#!/usr/bin/env python
# -*- coding: utf-8 -*-

from core.bot.generic_bot_non_player import GenericBotNonPlayer
from core.bot.terran.build.build import Build
from core.register_board.constants import OperationTypeId
from strategy.cin_deem_team.terran.build_dependencies import *


class BuildManager(GenericBotNonPlayer):
    """ Build manager class """

    def __init__(self, bot_player):
        """
        :param core.bot.generic_bot_player.GenericBotPlayer bot_player:
        """
        super(BuildManager, self).__init__(bot_player)
        self.add_bot(Build(bot_player, self.board_info))

    def find_request(self):
        """ Implements the logic to find the requests that should be handled by the bot
        :return list[core.register_board.request.Request]
        """
        return self.bot_player.board_request.search_request_by_operation_id(OperationTypeId.BUILD)

    async def default_behavior(self, iteration):
        """ The default behavior of the bot
        :param int iteration: Game loop iteration
        """
        for request in self.requests:
            if await self._check_dependencies(request):
                await self.perform_build(iteration)

    async def perform_build(self, iteration):
        """
        :param int iteration: Game loop iteration
        """
        build_bot = self.bots.get(Build.__name__)

        if iteration == 0:
            await build_bot.default_behavior(iteration)

    async def _check_dependencies(self, request):
        """
        Check request dependencies.
        :param core.register_board.request.Request: request
        :return bool:
        """
        requested_unit = request.unit_type_id
        request_dependencies = DEPENDENCIES.get(requested_unit)
        result = False

        if not request_dependencies:
            result = await self.bot_player.can_afford(requested_unit)

            supply_dependencies = request_dependencies[SUPPLY]
            result = await self.check_build_dependencies(supply_dependencies, result)

            tech_dependencies = request_dependencies[TECHNOLOGY]
            result = await self.check_technology_dependencies(tech_dependencies, result)

            build_dependencies = request_dependencies[BUILD]
            result = await self.check_supply_dependencies(build_dependencies, result)

        return result

    async def check_supply_dependencies(self, supply_dependencies, result):
        """
        Check supply dependencies
        :param supply_dependencies:
        :param result:
        :return:
        """
        if await self.bot_player.supply_left > supply_dependencies:
            pass
        else:
            # register needed of supply
            result = False
        return result

    async def check_technology_dependencies(self, tech_dependencies, result):
        """
        Check technology dependencies
        :param tech_dependencies:
        :param result:
        :return:
        """
        for dependency in tech_dependencies:
            if await self.bot_player.get_available_abilities(dependency).amount > 0:
                result = result and True
            else:
                # register needed technology
                result = False
                break
        return result

    async def check_build_dependencies(self, build_dependencies, result):
        """
        Check build dependencies
        :param build_dependencies:
        :param result:
        :return:
        """
        for dependency in build_dependencies:
            if await self.bot_player.units(dependency).amount > 0:
                result = result and True
            else:
                # register needed unit
                result = False
                break
        return result
