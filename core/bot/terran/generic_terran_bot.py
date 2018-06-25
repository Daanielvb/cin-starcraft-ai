#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
Generic terran bot class
"""

import sc2

from core.bot import generic_bot


class GenericTerranBot(generic_bot.GenericBot):
    """ A generic terran bot class """

    def __init__(self):
        super(GenericTerranBot, self).__init__(race_type=sc2.Race.Terran)

    def on_start(self):
        """ Allows initializing the bot when the game data is available """
        raise NotImplementedError

    async def default_on_step(self, iteration, observer):
        """ Default behavior for the bot
        :param int iteration: Game loop iteration
        :param core.bot.generic_bot.GenericBot observer: The supreme observer
        """
        raise NotImplementedError
