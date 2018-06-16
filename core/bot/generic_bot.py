#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
Generic bot class
"""

from sc2 import player
from sc2 import bot_ai


class GenericBot(bot_ai.BotAI):
    """" A generic bot class """

    def __init__(self, race, on_step_method_strategy=None):
        """
        :param sc2.data.Race race:
        :param function on_step_method_strategy:
        """
        self._race = race

    @property
    def race(self):
        """
        :return int:
        """
        return self._race

    def build_bot_player(self):
        """
        :return sc2.player.Bot
        """
        return player.Bot(race=self.race, ai=self)

    async def on_step(self, iteration):
        """ Ran on every game step (looped in realtime mode). """
        raise NotImplementedError
