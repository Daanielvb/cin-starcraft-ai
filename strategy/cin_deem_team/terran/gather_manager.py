#!/usr/bin/env python
# -*- coding: utf-8 -*-

from core.bot.generic_bot_non_player import GenericBotNonPlayer
from core.bot.terran.worker.gather import Gather
from core.register_board.constants import OperationTypeId, RequestStatus
from strategy.cin_deem_team.terran.build_dependencies import *


class GatherManager(GenericBotNonPlayer):
    """ Build manager class """

    processed_requests = []

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
        return self.bot_player.board_request.search_request_by_operation_ids([OperationTypeId.TRAIN_SCV_ALLOW,
                                                                              OperationTypeId.TRAIN_SCV_DENY])

    def requests_status_update(self):
        """ Logic to update the requests status """
        for request in self.processed_requests:
            self.bot_player.board_request.remove(request)
        self.processed_requests.clear()

    async def requests_handler(self, iteration):
        for request in self.requests:
            if request.operation_type_id == OperationTypeId.TRAIN_SCV_ALLOW:
                await self.toggle_train_scv(True)
            else:
                await self.toggle_train_scv(False)
            self.processed_requests = self.processed_requests + [request]

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
