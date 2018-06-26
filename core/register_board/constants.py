#!/usr/bin/env python
# -*- coding: utf-8 -*-

from enum import Enum


class OperationTypeId(Enum):
    """
    Operation Type Id
    """
    ATTACK = 'ATTACK'
    SCOUT = 'SCOUT'
    DEFENSE = 'DEFENSE'


class RequestStatus(Enum):
    """
    Request Status
    """
    TO_BE_DONE = "TO BE DONE"
    ON_GOING = "ON GOING"
    DONE = "DONE"
    DISMISSED = "DISMISSED"


class RequestPriority(Enum):
    """
    Request Priority
    """
    PRIORITY_HIGHER = 0
    PRIORITY_HIGH = 1
    PRIORITY_MEDIUM = 2
    PRIORITY_LOW = 3
    PRIORITY_LOWER = 4
