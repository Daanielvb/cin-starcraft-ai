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

    async def on_step(self, iteration):
        """ Ran on every game step (looped in real-time mode).
        :param int iteration: Game loop iteration
        """
        self.log("Iteration #{}".format(iteration))
        await self.default_behavior(iteration)

    async def default_behavior(self, iteration):
        """ The default behavior of the bot
        :param int iteration: Game loop iteration
        """
        raise NotImplementedError
