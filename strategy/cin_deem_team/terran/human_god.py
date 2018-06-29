#!/usr/bin/env python
# -*- coding: utf-8 -*-

from sc2 import Race
from sc2.ids.unit_typeid import UnitTypeId

from core.bot.generic_bot_player import GenericBotPlayer
from core.register_board.constants import RequestPriority
from core.register_board.constants import OperationTypeId
from core.register_board.request import Request
from strategy.cin_deem_team.terran.scout_manager import ScoutManager


class HumanGod(GenericBotPlayer):
    """ The player class of the game match """

    def __init__(self):
        super(HumanGod, self).__init__(race_type=Race.Terran)

    def on_start(self):
        """ Allows initializing the bot when the game data is available """
        self.add_bot(ScoutManager(bot_player=self))

    async def default_behavior(self, iteration, request=None):
        """ The default behavior of the bot
        :param int iteration: Game loop iteration
        :param core.register_board.request.Request request:
        """
        if iteration == 0:
            scout_request = Request(
                request_priority=RequestPriority.PRIORITY_HIGHER,
                unit_type_id=UnitTypeId.SCV,
                operation_type_id=OperationTypeId.SCOUT
            )
            self.board_request.register(scout_request)

        await self.read_requests(iteration)

    async def read_requests(self, iteration):
        for bot in self.bots.values():
            await bot.default_behavior(iteration=iteration, request=None)
