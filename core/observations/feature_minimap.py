#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
The minimap is a low resolution view of the entire map. It gives an overview of everything going on,
but with less detail than the screen.
https://github.com/deepmind/pysc2/blob/master/docs/environment.md#minimap
"""

FEATURE_MINIMAP = 'feature_minimap'


def get_height_map_minimap(obs):
    """ Shows the terrain levels
    :param pysc2.env.environment.TimeStep obs:
    :return pysc2.lib.named_array.NamedNumpyArray:
    """
    return obs.observation.get(FEATURE_MINIMAP)[0]


def get_visibility_map_minimap(obs):
    """ Which part of the map are hidden, have been seen or are currently visible
    :param pysc2.env.environment.TimeStep obs:
    :return pysc2.lib.named_array.NamedNumpyArray:
    """
    return obs.observation.get(FEATURE_MINIMAP)[1]


def get_creep_minimap(obs):
    """ Which parts have zerg creep
    :param pysc2.env.environment.TimeStep obs:
    :return pysc2.lib.named_array.NamedNumpyArray:
    """
    return obs.observation.get(FEATURE_MINIMAP)[2]


def get_camera_minimap(obs):
    """ Which part of the map are visible in the screen layers
    :param pysc2.env.environment.TimeStep obs:
    :return pysc2.lib.named_array.NamedNumpyArray:
    """
    return obs.observation.get(FEATURE_MINIMAP)[3]


def get_player_id_minimap(obs):
    """ Who owns the units, with absolute ids
    :param pysc2.env.environment.TimeStep obs:
    :return pysc2.lib.named_array.NamedNumpyArray:
    """
    return obs.observation.get(FEATURE_MINIMAP)[4]


def get_player_relative_minimap(obs):
    """ Which units are friendly vs hostile. Takes values in [0, 4],
    denoting [background, self, ally, neutral, enemy] units respectively
    :param pysc2.env.environment.TimeStep obs:
    :return pysc2.lib.named_array.NamedNumpyArray:
    """
    return obs.observation.get(FEATURE_MINIMAP)[5]


def get_selected_minimap(obs):
    """ Which units are selected
    :param pysc2.env.environment.TimeStep obs:
    :return pysc2.lib.named_array.NamedNumpyArray:
    """
    return obs.observation.get(FEATURE_MINIMAP)[6]
