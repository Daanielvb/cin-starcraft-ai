#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
Basic Agent
"""

from pysc2.agents import base_agent
from pysc2.lib import actions


class Agent(base_agent.BaseAgent):
    def step(self, obs):
        super(Agent, self).step(obs)
        return actions.FunctionCall(actions.FUNCTIONS.no_op.id, [])
