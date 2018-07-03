#!/usr/bin/env python
# -*- coding: utf-8 -*-

from enum import Enum


class OperationTypeId(Enum):
    """
    Operation Type Id
    """
    ATTACK = 'ATTACK'
    BUILD = 'BUILD'
    DEFEND = 'DEFEND'
    PATROL = 'PATROL'
    RESEARCH_TECHNOLOGY = 'RESEARCH_TECHNOLOGY'
    SCOUT = 'SCOUT'
    TRAIN_SCV_ALLOW = 'ALLOW SCV'
    TRAIN_SCV_DENY = 'DENY SCV'
    WARN = 'WARN'


class RequestStatus(Enum):
    """
    Request Status
    """
    TO_BE_DONE = "TO BE DONE"
    ON_GOING = "ON GOING"
    DONE = "DONE"
    DISMISSED = "DISMISSED"
    FAILED = "FAILED"


class RequestPriority(Enum):
    """
    Request Priority
    """
    PRIORITY_HIGHER = 0
    PRIORITY_HIGH = 1
    PRIORITY_MEDIUM = 2
    PRIORITY_LOW = 3
    PRIORITY_LOWER = 4


class InfoType(Enum):
    ENEMY_POSITION = 'ENEMY_POSITION'
    ENEMY_NEARBY = 'ENEMY_NEARBY'
