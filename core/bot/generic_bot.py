#!/usr/bin/env python
# -*- coding: utf-8 -*-

from sc2 import bot_ai

from core.register_board.boards import BoardInfo
from core.register_board.boards import BoardRequest
from utils import logger


class GenericBot(bot_ai.BotAI):
    """" A generic bot class """

    def __init__(self, race_type):
        """
        :param sc2.data.Race race_type:
        """
        self._race_type = race_type
        self._bots = dict()
        self._board_info = BoardInfo()
        self._board_request = BoardRequest()

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
    def board_info(self):
        """
        :return core.register_board.boards.BoardInfo:
        """
        return self._board_info

    @property
    def board_request(self):
        """
        :return core.register_board.boards.BoardRequest:
        """
        return self._board_request

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

    async def default_behavior(self, iteration, request):
        """ The default behavior of the bot
        :param int iteration: Game loop iteration
        :param core.register_board.request.Request request:
        """
        raise NotImplementedError

    def send_info(self, info):
        """
        :param info:
        """
        self._board_info.register(info)

    def send_request(self, request):
        """
        :param request:
        :return:
        """
        self._board_request.register(request)

