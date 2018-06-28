#!/usr/bin/env python
# -*- coding: utf-8 -*-

from sc2 import bot_ai

from utils import logger


class GenericBot(bot_ai.BotAI):
    """" A generic bot class """

    def __init__(self, race_type):
        """
        :param sc2.data.Race race_type:
        """
        self._race_type = race_type
        self._bots = dict()
        self._board = dict()

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
    def bots(self):
        """
        :return dict:
        """
        return self._bots

    @property
    def board(self):
        """
        :return dict:
        """
        return self._board

    def add_bot(self, bot):
        """
        :param core.bot.generic_bot.GenericBot bot:
        """
        self._bots[str(bot)] = bot

    async def on_step(self, iteration):
        """ Ran on every game step (looped in real-time mode).
        :param int iteration: Game loop iteration
        """
        self.log("Iteration #{}".format(iteration))
        await self.default_behavior(iteration)

    def on_start(self):
        """ Allows initializing the bot when the game data is available """
        raise NotImplementedError

    async def default_behavior(self, iteration):
        """ The default behavior of the bot
        :param int iteration: Game loop iteration
        """
        raise NotImplementedError

