#!/usr/bin/env python
# -*- coding: utf-8 -*-
from random import randint

from core.bot.generic_bot import GenericBot
from core.register_board.info import Info


class GenericBotNonPlayerUnit(GenericBot):
    """ Generic bot non-player unit class, which represents a sc2.unit.Unit on the game """

    def __init__(self, bot_player, iteration, request, unit_tags):
        """
        :param core.bot.generic_bot_player.GenericBotPlayer bot_player:
        :param int iteration:
        :param core.register_board.request.Request request:
        :param list(int) unit_tags:
        """
        super(GenericBotNonPlayerUnit, self).__init__(bot_player)
        self._bot_player = bot_player
        self._unit_tags = unit_tags
        self._info = Info(
            iteration=iteration,
            bot=self,
            request=request,
            unit_tags=self._unit_tags
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
    def request(self):
        """
        :return core.register_board.request.Request:
        """
        return self._info.request

    def set_request(self, request):
        """
        :param core.register_board.request.Request request:
        """
        self._info.request = request

    @property
    def unit_tag(self):
        """
        :return int:
        """
        return self._unit_tags

    def is_idle(self):
        """
        :return bool:
        """
        unit = self.bot_player.get_current_scv_unit(self._info.unit_tags)
        if unit:
            return unit.is_idle
        else:
            return False

    def are_idle(self):
        """
        :return bool:
        """
        result = True
        units = self.bot_player.get_current_units(self._info.unit_tags)
        if units:
            for unit in units:
                if not unit.is_idle:
                    result = False
        else:
            result = False
        return result

    async def default_behavior(self, iteration):
        """ The default behavior of the bot
        :param int iteration: Game loop iteration
        """
        raise NotImplementedError
