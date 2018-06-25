#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
Generic bot class
"""

import asyncio

from sc2 import player
from sc2 import bot_ai

from utils import logger


class GenericBot(bot_ai.BotAI):
    """" A generic bot class """

    def __init__(self, race_type):
        """
        :param sc2.data.Race race_type:
        """
        self._race_type = race_type
        self._alternative_on_step = None
        self._bots = dict()

    def __str__(self):
        """
        :return str:
        """
        return self.__class__.__name__

    def log(self, msg):
        """ Prints log message
        :param msg: the message to be printed
        """
        logger.LOGGER(
            '{class_name}:{msg}'.format(class_name=self, msg=msg)
        )

    @property
    def race_type(self):
        """
        :return int:
        """
        return self._race_type

    @property
    def alternative_on_step(self):
        """
        :return coroutine:
        """
        return self._alternative_on_step

    @property
    def bots(self):
        """
        :return dict:
        """
        return self._bots

    @alternative_on_step.setter
    def alternative_on_step(self, alternative_on_step):
        """
        :param asyncio.coroutines alternative_on_step:
        """
        self._alternative_on_step = alternative_on_step

    def build_bot_player(self):
        """
        :return sc2.player.Bot
        """
        return player.Bot(race=self._race_type, ai=self)

    def add_bot(self, bot):
        """
        :param core.bot.generic_bot.GenericBot bot:
        """
        self._bots[str(bot)] = bot

    def on_start(self):
        """ Allows initializing the bot when the game data is available """
        raise NotImplementedError

    async def on_step(self, iteration):
        """ Ran on every game step (looped in real-time mode).
        :param int iteration: Game loop iteration
        """
        self.log("Iteration #{}".format(iteration))

        loop = asyncio.get_event_loop()
        tasks = []

        if self._alternative_on_step:
            self.log("Creating alternative_on_step() task")
            tasks.append(
                loop.create_task(
                    self._alternative_on_step(obj=self, iteration=iteration, observer=self)
                )
            )
        else:
            self.log("Creating default_on_step() task")
            tasks.append(
                loop.create_task(
                    self.default_on_step(iteration=iteration, observer=self)
                )
            )

        await asyncio.wait(tasks)

    async def default_on_step(self, iteration, observer):
        """ Default behavior for the bot
        :param int iteration: Game loop iteration
        :param core.bot.generic_bot.GenericBot observer: The supreme observer
        """
        raise NotImplementedError
