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
        super(GenericTerranBot, self).__init__(race=sc2.Race.Terran)

    async def on_step(self, iteration):
        raise NotImplementedError
