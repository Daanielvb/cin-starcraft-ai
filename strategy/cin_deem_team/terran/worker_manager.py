#!/usr/bin/env python
# -*- coding: utf-8 -*-

from core.bot.generic_bot_non_player import GenericBotNonPlayer
from core.bot.terran.worker.scv import SCV


class WorkerManager(GenericBotNonPlayer):
    """ Worker manager class """

    def __init__(self, bot_player):
        """
        :param core.bot.generic_bot_player.GenericBotPlayer bot_player:
        """
        super(WorkerManager, self).__init__(bot_player)
        self.add_bot(SCV(bot_player))

    async def default_behavior(self, iteration):
        """ The default behavior of the bot
        :param int iteration: Game loop iteration
        """
        for bot in self.bots.values():
            if iteration == 0:
                await bot.worker_rush_attack()
