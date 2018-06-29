#!/usr/bin/env python
# -*- coding: utf-8 -*-


class Info(object):
    """ Information """

    def __init__(self, iteration, bot, request, status, unit=None):
        """
        :param int iteration:
        :param bot:
        :param request:
        :param str status:
        :param unit:
        """
        self._iteration = iteration
        self._bot = bot
        self._request = request
        self._status = status
        self._unit = unit

    @property
    def iteration(self):
        """
        :return int:
        """
        return self._iteration

    @property
    def bot(self):
        """
        :return :
        """
        return self._bot

    @property
    def request(self):
        """
        :return :
        """
        return self._request

    @property
    def status(self):
        """
        :return :
        """
        return self._status

    @status.setter
    def status(self, status):
        """
        :return :
        """
        self._status = status

    @property
    def unit(self):
        """
        :return :
        """
        return self._unit

    @unit.setter
    def unit(self, unit):
        """
        :return :
        """
        self._unit = unit
