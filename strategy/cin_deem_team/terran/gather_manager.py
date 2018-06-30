#!/usr/bin/env python
# -*- coding: utf-8 -*-

from core.bot.generic_bot_non_player import GenericBotNonPlayer
from core.bot.terran.worker.gather import Gather
from core.register_board.constants import OperationTypeId, RequestStatus
from strategy.cin_deem_team.terran.build_dependencies import *


class GatherManager(GenericBotNonPlayer):
    """ Build manager class """

    def __init__(self, bot_player):
        """
        :param core.bot.generic_bot_player.GenericBotPlayer bot_player:
        """
        super(GatherManager, self).__init__(bot_player)
        self.gather_class = Gather(bot_player)

    def find_request(self):
        """ Implements the logic to find the requests that should be handled by the bot
        :return list[core.register_board.request.Request]
        """

        allow_train = self.bot_player.board_request.search_request_by_operation_id(OperationTypeId.TRAIN_SCV_ALLOW)
        deny_train = self.bot_player.board_request.search_request_by_operation_id(OperationTypeId.TRAIN_SCV_DENY)
        return allow_train + deny_train

    async def default_behavior(self, iteration):
        """ The default behavior of the bot
        :param int iteration: Game loop iteration
        """
        for request in self.requests:
            print("REQUEST OK!!")
            if request.operation_type_id == OperationTypeId.TRAIN_SCV_ALLOW:
                await self.toggle_train_scv(True)
            else:
                await self.toggle_train_scv(False)
            self.bot_player.board_request.remove(request)

        await self.update_gather(iteration)

    async def toggle_train_scv(self, should_train):
        #gather_bot = self.bots.get(Gather.__name__)

        await self.gather_class.toggle_train_scv(should_train)

    async def update_gather(self, iteration):
        """
        :param int iteration: Game loop iteration
        """
       # gather_bot = self.bots.get(Gather.__name__)

        if iteration > 0:
            await self.gather_class.default_behavior(iteration)
