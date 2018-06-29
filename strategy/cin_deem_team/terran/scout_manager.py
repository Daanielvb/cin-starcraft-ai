#!/usr/bin/env python
# -*- coding: utf-8 -*-

from core.bot.generic_bot_non_player import GenericBotNonPlayer
from core.bot.terran.scout.scout import Scout
from core.register_board.constants import OperationTypeId


class ScoutManager(GenericBotNonPlayer):
    """ Scout manager class """

    def __init__(self, bot_player):
        """
        :param core.bot.generic_bot_player.GenericBotPlayer bot_player:
        """
        super(ScoutManager, self).__init__(bot_player)
        self.add_bot(Scout(bot_player, self.board_info))

    async def default_behavior(self, iteration, request):
        """ The default behavior of the bot
        :param int iteration: Game loop iteration
        :param core.register_board.request.Request request:
        """
        scout_requests = self.bot_player.board_request.search_request_by_operation_id(
            OperationTypeId.SCOUT
        )

        for scout_request in scout_requests:
            await self.perform_scout(iteration, scout_request)

    async def perform_scout(self, iteration, scout_request):
        """
        :param int iteration: Game loop iteration
        :param core.register_board.request.Request scout_request:
        """
        scout_bot = self.bots.get(Scout.__name__)

        if iteration == 0:
            await scout_bot.default_behavior(iteration, scout_request)

        else:
            if scout_bot.get_found_enemy_base():

                if iteration % 30 == 0:
                    await scout_bot.visit_middle()

                elif iteration % 80 == 0:
                    await scout_bot.visit_base()

            # TODO: Implement nearby friends logic and warn
            # elif bot.found_enemies_nearby():
                # await bot.visit_base()

            else:
                await scout_bot.default_behavior(iteration, scout_request)