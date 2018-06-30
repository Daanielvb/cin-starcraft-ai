#!/usr/bin/env python
# -*- coding: utf-8 -*-

from core.bot.generic_bot import GenericBot
from core.exceptions import NotAddingNonPlayerBotException


class GenericBotNonPlayer(GenericBot):
    """ Generic bot non-player class, which cannot observer and operate the environment """

    def __init__(self, bot_player):
        """
        :param core.bot.generic_bot_player.GenericBotPlayer bot_player:
        """
        super(GenericBotNonPlayer, self).__init__(bot_player.race_type)
        self._bot_player = bot_player
        self._requests = list()

    @property
    def bot_player(self):
        """
        :return core.bot.generic_bot_player.GenericBotPlayer:
        """
        return self._bot_player

    @property
    def requests(self):
        """
        :return list[core.register_board.request.Request]
        """
        return self._requests

    def add_bot(self, bot):
        """
        :param core.bot.generic_bot_non_player.GenericBotNonPlayer bot:
        :raise NotAddingNonPlayerBot:
        """
        if not isinstance(bot, GenericBotNonPlayer):
            raise NotAddingNonPlayerBotException()

        self._bots[str(bot)] = bot

    def on_start(self):
        """ Allows initializing the bot when the game data is available """
        # No needed for non-players bot
        pass

    async def default_behavior(self, iteration):
        """ The default behavior of the bot
        :param int iteration: Game loop iteration
        """
        raise NotImplementedError

    def read_requests(self):
        """ Update the requests that should be handled by the bot
        :return list[core.register_board.request.Request]
        """
        self._requests.extend(self.find_request())

    def find_request(self):
        """ Implements the logic to find the requests that should be handled by the bot
        :return list[core.register_board.request.Request]
        """
        raise NotImplementedError
