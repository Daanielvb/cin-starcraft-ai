#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
The screen is a higher resolution view of part of the map.
https://github.com/deepmind/pysc2/blob/master/docs/environment.md#screen
"""

FEATURE_SCREEN = 'feature_screen'


def get_height_map_screen(obs):
    """ Shows the terrain levels
    :param pysc2.env.environment.TimeStep obs:
    :return pysc2.lib.named_array.NamedNumpyArray:
    """
    return obs.observation.get(FEATURE_SCREEN)[0]


def get_visibility_map_screen(obs):
    """ Which part of the map are hidden, have been seen or are currently visible
    :param pysc2.env.environment.TimeStep obs:
    :return pysc2.lib.named_array.NamedNumpyArray:
    """
    return obs.observation.get(FEATURE_SCREEN)[1]


def get_creep_screen(obs):
    """ Which parts have zerg creep
    :param pysc2.env.environment.TimeStep obs:
    :return pysc2.lib.named_array.NamedNumpyArray:
    """
    return obs.observation.get(FEATURE_SCREEN)[2]


def get_power_screen(obs):
    """ Which parts have protoss power, only shows your power
    :param pysc2.env.environment.TimeStep obs:
    :return pysc2.lib.named_array.NamedNumpyArray:
    """
    return obs.observation.get(FEATURE_SCREEN)[3]


def get_player_id_screen(obs):
    """ Who owns the units, with absolute ids
    :param pysc2.env.environment.TimeStep obs:
    :return pysc2.lib.named_array.NamedNumpyArray:
    """
    return obs.observation.get(FEATURE_SCREEN)[4]


def get_player_relative_screen(obs):
    """ Which units are friendly vs hostile. Takes values in [0, 4],
    denoting [background, self, ally, neutral, enemy] units respectively.
    :param pysc2.env.environment.TimeStep obs:
    :return pysc2.lib.named_array.NamedNumpyArray:
    """
    return obs.observation.get(FEATURE_SCREEN)[5]


def get_unit_type_screen(obs):
    """ A unit type id, which can be looked up in pysc2/lib/units.py
    :param pysc2.env.environment.TimeStep obs:
    :return pysc2.lib.named_array.NamedNumpyArray:
    """
    return obs.observation.get(FEATURE_SCREEN)[6]


def get_selected_screen(obs):
    """ Which units are selected
    :param pysc2.env.environment.TimeStep obs:
    :return pysc2.lib.named_array.NamedNumpyArray:
    """
    return obs.observation.get(FEATURE_SCREEN)[7]


def get_unit_hit_points_screen(obs):
    """  How many hit points the unit has
    :param pysc2.env.environment.TimeStep obs:
    :return pysc2.lib.named_array.NamedNumpyArray:
    """
    return obs.observation.get(FEATURE_SCREEN)[8]


def get_unit_energy_screen(obs):
    """  How many hit points the unit has
    :param pysc2.env.environment.TimeStep obs:
    :return pysc2.lib.named_array.NamedNumpyArray:
    """
    return obs.observation.get(FEATURE_SCREEN)[10]


def get_unit_density_map_screen(obs):
    """  How many units are in this pixel.
    :param pysc2.env.environment.TimeStep obs:
    :return pysc2.lib.named_array.NamedNumpyArray:
    """
    return obs.observation.get(FEATURE_SCREEN)[14]
