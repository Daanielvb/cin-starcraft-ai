#!/usr/bin/env python
# -*- coding: utf-8 -*-

from utils import logger
from core.register_board.constants import RequestPriority


class BoardRequest(object):
    """ Board for task request """

    def __init__(self):
        self._board = []
        self._requests_count = 0

    def register(self, request):
        """
        :param core.request_board.request.Request request:
        """
        logger.LOGGER('Registering request: {}'.format(request))
        request.request_id = self._requests_count
        self._board.append(request)
        self._requests_count += 1

    @property
    def board(self):
        """
        :return list[core.register_board.request.Request]:
        """
        return self._board

    def remove(self, request):
        """
        :param core.request_board.request.Request request:
        """
        # TODO: This IF is to avoid remove an already removed request and crash the match
        logger.LOGGER('Removing request: {}'.format(request))
        if request in self._board:
            self._board.remove(request)

    def search_request_by_operation_ids(self, operation_ids):
        """
        :param core.register_board.constants.OperationTypeId operation_id:
        :return list[core.register_board.request.Request]:
        """

        list_higher = []
        list_high = []
        list_medium = []
        list_low = []
        list_lower = []

        for request in self.board:
            if request.operation_type_id in operation_ids:
                if request.request_priority_level == RequestPriority.PRIORITY_HIGHER:
                    list_higher.append(request)
                elif request.request_priority_level == RequestPriority.PRIORITY_HIGH:
                    list_high.append(request)
                elif request.request_priority_level == RequestPriority.PRIORITY_MEDIUM:
                    list_medium.append(request)
                elif request.request_priority_level == RequestPriority.PRIORITY_LOW:
                    list_low.append(request)
                elif request.request_priority_level == RequestPriority.PRIORITY_LOWER:
                    list_lower.append(request)

        return list_higher + list_high + list_medium + list_low + list_lower

    def search_request_by_operation_id(self, operation_id):
        """
        :param core.register_board.constants.OperationTypeId operation_id:
        :return list[core.register_board.request.Request]:
        """

        list_higher = []
        list_high = []
        list_medium = []
        list_low = []
        list_lower = []

        for request in self.board:
            if request.operation_type_id == operation_id:
                if request.request_priority_level == RequestPriority.PRIORITY_HIGHER:
                    list_higher.append(request)
                elif request.request_priority_level == RequestPriority.PRIORITY_HIGH:
                    list_high.append(request)
                elif request.request_priority_level == RequestPriority.PRIORITY_MEDIUM:
                    list_medium.append(request)
                elif request.request_priority_level == RequestPriority.PRIORITY_LOW:
                    list_low.append(request)
                elif request.request_priority_level == RequestPriority.PRIORITY_LOWER:
                    list_lower.append(request)

        return list_higher + list_high + list_medium + list_low + list_lower


class BoardInfo(object):
    """ Board for share information between bots """

    def __init__(self):
        self._board = []
        self._info_count = 0

    def register(self, info):
        """
        :param core.register_board.info.Info info:
        """
        info.info_id = self._info_count
        self._board.append(info)
        self._info_count += 1

    @property
    def board(self):
        """
        :return list[core.register_board.info.Info]:
        """
        return self._board

    def search_request_by_type(self, info_type):
        return [info for info in self.board if info.type == info_type]
