#!/usr/bin/env python
# -*- coding: utf-8 -*-


class Info(object):
    """ Request information status """

    def __init__(self, bot, iteration=None, request=None, unit_tag=None, type=None, value=None):
        """
        :param int iteration:
        :param core.bot.generic_bot.GenericBot bot:
        :param core.register_board.request.Request request:
        :param int unit_tag:
        """
        self._iteration = iteration
        self._bot = bot
        self._request = request
        self._unit_tag = unit_tag
        self._type = type
        self._value = value

    @property
    def iteration(self):
        """
        :return int:
        """
        return self._iteration

    @property
    def bot(self):
        """
        :return core.bot.generic_bot.GenericBot:
        """
        return self._bot

    @property
    def request(self):
        """
        :return core.register_board.request.Request:
        """
        return self._request

    @property
    def status(self):
        """
        :return core.register_board.request.RequestStatus:
        """
        return self._request.status

    @status.setter
    def status(self, status):
        """
        :param core.register_board.request.RequestStatus status:
        """
        self._request.status = status

    @property
    def type(self):
        """
        :return core.register_board.constants.InfoType:
        """
        return self._type

    @property
    def value(self):
        """
        :return *:
        """
        return self._value

    @value.setter
    def value(self, value):
        """
        :param * value:
        """
        self._value = value

    @property
    def unit_tag(self):
        """
        :return int:
        """
        return self._unit_tag
