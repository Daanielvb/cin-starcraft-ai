#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
Read the player status as minerals, vespene  gas, etc ...
"""

OBSERVATION_PLAYER = 'player'


def get_player_id(obs):
    """
    :param pysc2.env.environment.TimeStep obs:
    :return numpy.int32:
    """
    return obs.observation.get(OBSERVATION_PLAYER)[0]


def get_minerals_count(obs):
    """
    :param pysc2.env.environment.TimeStep obs:
    :return numpy.int32:
    """
    return obs.observation.get(OBSERVATION_PLAYER)[1]


def get_vespene_count(obs):
    """
    :param pysc2.env.environment.TimeStep obs:
    :return numpy.int32:
    """
    return obs.observation.get(OBSERVATION_PLAYER)[2]


def get_used_supply_count(obs):
    """
    :param pysc2.env.environment.TimeStep obs:
    :return numpy.int32:
    """
    return obs.observation.get(OBSERVATION_PLAYER)[3]


def get_max_supply_count(obs):
    """
    :param pysc2.env.environment.TimeStep obs:
    :return numpy.int32:
    """
    return obs.observation.get(OBSERVATION_PLAYER)[4]


def get_supply_army_count(obs):
    """
    :param pysc2.env.environment.TimeStep obs:
    :return numpy.int32:
    """
    return obs.observation.get(OBSERVATION_PLAYER)[5]


def get_supply_workers_count(obs):
    """
    :param pysc2.env.environment.TimeStep obs:
    :return numpy.int32:
    """
    return obs.observation.get(OBSERVATION_PLAYER)[6]


def get_idle_workers_count(obs):
    """
    :param pysc2.env.environment.TimeStep obs:
    :return numpy.int32:
    """
    return obs.observation.get(OBSERVATION_PLAYER)[7]