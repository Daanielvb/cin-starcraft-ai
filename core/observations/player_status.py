#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
Read the player status as minerals, vespene  gas, etc ...
"""

OBSERVATION_PLAYER = 'player'


def get_minerals_status(obs):
    """
    :param pysc2.env.environment.TimeStep obs:
    :return numpy.int32:
    """
    return obs.observation.get(OBSERVATION_PLAYER)[1]


def get_vespene_status(obs):
    """
    :param pysc2.env.environment.TimeStep obs:
    :return numpy.int32:
    """
    return obs.observation.get(OBSERVATION_PLAYER)[2]


def get_current_supply_status(obs):
    """
    :param pysc2.env.environment.TimeStep obs:
    :return numpy.int32:
    """
    return obs.observation.get(OBSERVATION_PLAYER)[3]


def get_max_supply_status(obs):
    """
    :param pysc2.env.environment.TimeStep obs:
    :return numpy.int32:
    """
    return obs.observation.get(OBSERVATION_PLAYER)[4]
