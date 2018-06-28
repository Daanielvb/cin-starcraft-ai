#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
Generic terran bot class
"""

import sc2

from core.bot import generic_bot


class GenericTerranBot(generic_bot.GenericBot):
    """ A generic terran bot class """

    async def on_step(self, iteration):
        pass

    def __init__(self):
        super(GenericTerranBot, self).__init__(race_type=sc2.Race.Terran)

    def on_start(self):
        """ Allows initializing the bot when the game data is available """
        raise NotImplementedError

    def default_behavior(self, bot_player):
        """ The default_behavior for the class that are not the player
        :param core.bot.generic_bot.GenericBot bot_player: The instance of the player
        """
        raise NotImplementedError
