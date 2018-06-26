#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
Supreme master manager of the hierarchy
"""

from core.bot.terran.generic_terran_bot import GenericTerranBot
from strategy.cin_deem_team.terran.worker.worker_manager import WorkerManager


class HumanGod(GenericTerranBot):
    """ Supreme master leader of the hierarchy class """

    def on_start(self):
        """ Allows initializing the bot when the game data is available """
        self.add_bot(WorkerManager())

    async def default_on_step(self, iteration, observer):
        """ Ran on every game step (looped in real-time mode).
        :param int iteration: Game loop iteration
        :param core.bot.generic_bot.GenericBot observer: The supreme observer
        """
        for bot in self.bots.values():
            self.log("For bot {}".format(bot))
            await bot.default_on_step(iteration, observer)
