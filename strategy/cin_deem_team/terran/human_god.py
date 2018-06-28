#!/usr/bin/env python
# -*- coding: utf-8 -*-

from sc2 import Race

from core.bot.generic_bot_player import GenericBotPlayer
from strategy.cin_deem_team.terran.worker_manager import WorkerManager
from strategy.cin_deem_team.terran.scout_manager import ScoutManager


class HumanGod(GenericBotPlayer):
    """ The player class of the game match """

    def __init__(self):
        super(HumanGod, self).__init__(race_type=Race.Terran)

    def on_start(self):
        """ Allows initializing the bot when the game data is available """
        self.add_bot(WorkerManager(bot_player=self))
        self.add_bot(ScoutManager(bot_player=self))

    async def default_behavior(self, iteration):
        """ The default behavior of the bot
        :param int iteration: Game loop iteration
        """
        for bot in self.bots.values():
            await bot.default_behavior(iteration)
