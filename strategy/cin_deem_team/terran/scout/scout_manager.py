#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
Worker manager
"""

from core.bot.terran.generic_terran_bot import GenericTerranBot
from core.bot.terran.scout.scout import Scout
from core.bot.terran.worker.scv import SCV
from core.behavior.terran.worker import attack


class ScoutManager(GenericTerranBot):
    """ Worker manager class """

    def __init__(self):
        super(ScoutManager, self).__init__()
        self.add_bot(Scout())

    def on_start(self):
        """ Allows initializing the bot when the game data is available """
        pass

    async def default_on_step(self, iteration, observer):
        """ Ran on every game step (looped in real-time mode).
        :param int iteration: Game loop iteration
        :param core.bot.generic_bot.GenericBot observer: The supreme observer
        """
        for bot in self.bots.values():
            self.log("For bot {}".format(bot))
            bot.default_on_step(iteration, observer)

