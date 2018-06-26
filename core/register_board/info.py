#!/usr/bin/env python
# -*- coding: utf-8 -*-


class Info(object):
    """ Information """

    def __init__(self, location, timestamp, info_origin):
        """
        :param sc2.position.Point2 location:
        :param datetime.time timestamp:
        """
        self._info_id = None
        self._location = location
        self._info_origin = info_origin
        self._timestamp = timestamp

    @property
    def info_id(self):
        """
        :return int:
        """
        return self._info_id

    @info_id.setter
    def info_id(self, info_id):
        """
        :param int info_id:
        """
        self._info_id = info_id

    @property
    def info_origin(self):
        """
        :return int:
        """
        return self._info_origin
