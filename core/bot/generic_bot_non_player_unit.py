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

    def get_current_scout(self):
        """ Get current scout unit from Workers
        :return sc2.unit.Unit
        """
        # TODO: The unit might be dead. (Remember to test a scenario to validate it and handle it)
        for unit in self.bot_player.workers:
            if unit.tag == self.unit_tag:
                return unit

    def is_idle(self):
        """
        :return bool:
        """
        return self.get_current_scout().is_idle

    async def default_behavior(self, iteration):
        """ The default behavior of the bot
        :param int iteration: Game loop iteration
        """
        raise NotImplementedError
