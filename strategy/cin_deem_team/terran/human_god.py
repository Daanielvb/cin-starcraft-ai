#!/usr/bin/env python
# -*- coding: utf-8 -*-

from sc2 import Race
from sc2.ids.unit_typeid import UnitTypeId

from core.bot.generic_bot_player import GenericBotPlayer
from core.register_board.constants import RequestPriority
from core.register_board.constants import OperationTypeId
from core.register_board.request import Request
from strategy.cin_deem_team.terran.gather_manager import GatherManager
from strategy.cin_deem_team.terran.builder_manager import BuildManager
from strategy.cin_deem_team.terran.scout_manager import ScoutManager


class HumanGod(GenericBotPlayer):
    """ The player class of the game match """

    def __init__(self):
        super(HumanGod, self).__init__(race_type=Race.Terran)

    def on_start(self):
        """ Allows initializing the bot when the game data is available """
        self.add_bot(ScoutManager(bot_player=self))
        self.add_bot(BuildManager(bot_player=self))
        self.add_bot(GatherManager(bot_player=self))
        self.init_request_board()

    async def default_behavior(self, iteration):
        """ The default behavior of the bot
        :param int iteration: Game loop iteration
        """
        if iteration == 0:
            scout_request = Request(
                request_priority=RequestPriority.PRIORITY_HIGHER,
                unit_type_id=UnitTypeId.SCV,
                operation_type_id=OperationTypeId.SCOUT
            )
            self.board_request.register(scout_request)

        self._sync_bot_requests()
        await self._trigger_bots_default_behavior(iteration)

    def _sync_bot_requests(self):
        """ Update the requests for each bot added """
        for bot in self.bots.values():
            bot.read_requests()

    async def _trigger_bots_default_behavior(self, iteration):
        """
        :param int iteration:
        """
        for bot in self.bots.values():
            await bot.default_behavior(iteration=iteration)

    def init_request_board(self):
        self.board_request.register(
            Request(request_priority=RequestPriority.PRIORITY_HIGHER, operation_type_id=OperationTypeId.TRAIN_SCV_ALLOW)
        )
        self.board_request.register(
            Request(request_priority=RequestPriority.PRIORITY_HIGHER, unit_type_id=UnitTypeId.SCV,
                    operation_type_id=OperationTypeId.SCOUT)
        )
        self.board_request.register(
            Request(request_priority=RequestPriority.PRIORITY_HIGHER, unit_type_id=UnitTypeId.SUPPLYDEPOT,
                    operation_type_id=OperationTypeId.BUILD)
        )
        self.board_request.register(
            Request(request_priority=RequestPriority.PRIORITY_HIGHER, unit_type_id=UnitTypeId.BARRACKS,
                    operation_type_id=OperationTypeId.BUILD)
        )
        self.board_request.register(
            Request(request_priority=RequestPriority.PRIORITY_HIGHER, unit_type_id=UnitTypeId.BARRACKSTECHLAB,
                    operation_type_id=OperationTypeId.BUILD)
        )
        self.board_request.register(
            Request(request_priority=RequestPriority.PRIORITY_HIGHER, unit_type_id=UnitTypeId.SUPPLYDEPOT,
                    operation_type_id=OperationTypeId.BUILD)
        )
        self.board_request.register(
            Request(request_priority=RequestPriority.PRIORITY_HIGHER, unit_type_id=UnitTypeId.SUPPLYDEPOT,
                    operation_type_id=OperationTypeId.BUILD)
        )
        self.board_request.register(
            Request(request_priority=RequestPriority.PRIORITY_HIGHER, unit_type_id=UnitTypeId.SUPPLYDEPOT,
                    operation_type_id=OperationTypeId.BUILD)
        )

