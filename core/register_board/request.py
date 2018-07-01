#!/usr/bin/env python
# -*- coding: utf-8 -*-

from core.register_board.constants import RequestStatus


class Request(object):
    """ An action request """

    def __init__(self, request_priority, location=None, unit_type_id=None, operation_type_id=None):
        """
        :param core.register_board.constants.RequestPriority request_priority:
        :param sc2.position.Point2 location:
        :param sc2.ids.unit_typeid.UnitTypeId unit_type_id:
        :param core.register_board.constants.OperationTypeId operation_type_id:
        """
        self._request_id = None
        self._request_priority_level = request_priority
        self._location = location
        self._unit_type_id = unit_type_id
        self._operation_type_id = operation_type_id
        self._status = RequestStatus.TO_BE_DONE

    def __str__(self):
        return str(
            dict(
                request_id=self._request_id,
                operation_type_id=self._operation_type_id.name,
                unit_type_id=self._unit_type_id.name,
                request_priority_level=self._request_priority_level.name,
                status=self._status.name
            )
        )

    def __eq__(self, other):
        return isinstance(other, Request) and self._request_id == other.request_id

    @property
    def request_id(self):
        """
        :return int:
        """
        return self._request_id

    @request_id.setter
    def request_id(self, request_id):
        """
        :param int request_id:
        """
        self._request_id = request_id

    @property
    def unit_type_id(self):
        """
        :return sc2.ids.unit_typeid.UnitTypeId:
        """
        return self._unit_type_id

    @property
    def location(self):
        """
        :return sc2.position.Point2:
        """
        return self._location

    @location.setter
    def location(self, location):
        """
        :param sc2.position.Point2 location:
        """
        self._location = location

    @property
    def operation_type_id(self):
        """
        :return sc2.ids.unit_typeid.UnitTypeId:
        """
        return self._operation_type_id

    @property
    def status(self):
        """
        :return core.register_board.constants.RequestStatus:
        """
        return self._status

    @status.setter
    def status(self, status):
        """
        :param core.register_board.constants.RequestStatus status:
        """
        self._status = status
