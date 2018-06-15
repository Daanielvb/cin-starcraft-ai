#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
Helper method for units
"""

def unit_type_is_selected(self, obs, unit_type):
    if (len(obs.observation.single_select) > 0 and
            obs.observation.single_select[0].unit_type == unit_type):
        return True

    if (len(obs.observation.multi_select) > 0 and
            obs.observation.multi_select[0].unit_type == unit_type):
        return True
    return False