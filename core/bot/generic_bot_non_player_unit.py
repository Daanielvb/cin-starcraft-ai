#!/usr/bin/env python
# -*- coding: utf-8 -*-

from core.bot.generic_bot import GenericBot
from core.register_board.info import Info


class GenericBotNonPlayerUnit(GenericBot):
    """ Generic bot non-player unit class, which represents a sc2.unit.Unit on the game """

    def __init__(self, bot_player, iteration, request, unit_tag):
        """
        :param core.bot.generic_bot_player.GenericBotPlayer bot_player:
        :param int iteration:
        :param core.register_board.request.Request request:
        :param int unit_tag:
        """
        super(GenericBotNonPlayerUnit, self).__init__(bot_player)
        self._bot_player = bot_player
        self._unit_tag = unit_tag
        self._info = Info(
            iteration=iteration,
            bot=self,
            request=request,
            unit_tag=self._unit_tag
        )

        self.bot_player.board_info.register(self._info)

    @property
    def bot_player(self):
        """
        :return core.bot.generic_bot_player.GenericBotPlayer:
        """
        return self._bot_player

    @property
    def info(self):
        """
        :return core.register_board.info.Info:
        """
        return self._info

    @property
    def unit_tag(self):
        """
        :return int:
        """
        return self._unit_tag

    def is_idle(self):
        """
        :return bool:
        """
        return self.bot_player.get_current_scv_unit(self._info.unit_tag).is_idle

    async def default_behavior(self, iteration):
        """ The default behavior of the bot
        :param int iteration: Game loop iteration
        """
        raise NotImplementedError
