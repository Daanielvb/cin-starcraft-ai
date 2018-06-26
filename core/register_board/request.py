#!/usr/bin/env python
# -*- coding: utf-8 -*-
from core.register_board.constants import RequestStatus


class Request(object):
    """ Request """

    def __init__(self, request_priority, location, unit_type_id=None, operation_type_id=None):
        """
        :param core.request_board.request_priority.RequestPriority request_priority:
        :param sc2.position.Point2 location:
        :param sc2.ids.unit_typeid.UnitTypeId unit_type_id:
        :param core.request_board.operation_type_id.OperationTypeId operation_type_id:
        """
        self._request_id = None
        self._request_priority_level = request_priority
        self._location = location
        self._unit_type_id = unit_type_id
        self._operation_type_id = operation_type_id
        self._status = RequestStatus.TO_BE_DONE

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
    def operation_type_id(self):
        """
        :return sc2.ids.unit_typeid.UnitTypeId:
        """
        return self._operation_type_id

    @property
    def status(self):
        """
        :return str:
        """
        return self._status

    @status.setter
    def status(self, status):
        """
        :param str status:
        """
        self._status = status
