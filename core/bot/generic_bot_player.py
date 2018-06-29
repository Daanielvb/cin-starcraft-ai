#!/usr/bin/env python
# -*- coding: utf-8 -*-

from sc2 import player

from core.bot.generic_bot import GenericBot
from core.bot.generic_bot_non_player import GenericBotNonPlayer
from core.exceptions import NotAddingNonPlayerBotException


class GenericBotPlayer(GenericBot):
    """ Generic bot player class, which can observer and operate the environment """

    def __init__(self, race_type):
        """
        :param sc2.data.Race race_type:
        """
        super(GenericBotPlayer, self).__init__(race_type)

    def add_bot(self, bot):
        """
        :param core.bot.generic_bot_non_player.GenericBotNonPlayer bot:
        :raise NotAddingNonPlayerBot:
        """
        if not isinstance(bot, GenericBotNonPlayer):
            raise NotAddingNonPlayerBotException()

        self._bots[str(bot)] = bot

    def build_bot_player(self):
        """
        :return sc2.player.Bot
        """
        return player.Bot(race=self._race_type, ai=self)

    def on_start(self):
        """ Allows initializing the bot when the game data is available """
        raise NotImplementedError

    async def default_behavior(self, iteration, request=None):
        """ The default behavior of the bot
        :param int iteration: Game loop iteration
        :param core.register_board.request.Request request:
        """
        raise NotImplementedError

