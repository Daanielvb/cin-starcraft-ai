from pysc2.agents import base_agent
from pysc2.lib import actions
from pysc2.lib import features
from pysc2.lib.units import Terran
import math
import random

# Funcoes
FUNCTION_NO_OP = actions.FUNCTIONS.no_op.id
FUNCTION_SELECT_POINT = actions.FUNCTIONS.select_point.id
FUNCTION_MOVE_SCREEN = actions.FUNCTIONS.Move_screen.id

# Features
FEATURE_PLAYER_RELATIVE = features.SCREEN_FEATURES.player_relative.index
RELATIVE_SELF = 1
RELATIVE_NEUTRAL = 3
RELATIVE_ENEMY = 4

FEATURE_UNIT_TYPE = features.SCREEN_FEATURES.unit_type.index
UNIT_SCV = Terran.SCV
BUILDING_COMMAND_CENTER = Terran.CommandCenter

SCREEN = "feature_screen"

NOT_QUEUED = [0]
QUEUED = [1]


def is_in_range(value, begin_value, end_value):
    """
    Checks if determined value is on the screen within specified range
    :param value: to be checked on the screen
    :param begin_value: initial range to be checked on the screen
    :param end_value: final range to checked on the screen:
    :return true or false
    """
    return value >= begin_value and value < end_value

def is_on_screen(target):

    return is_in_range(target[0],0,84) and is_in_range(target[1],0,84)

def get_unit(obs, type, player):
    unit_type = obs.observation[SCREEN][FEATURE_UNIT_TYPE] == type
    unit_player = obs.observation[SCREEN][FEATURE_PLAYER_RELATIVE] == player
    unit_y, unit_x = (unit_type * unit_player).nonzero()
    numUnits = len(unit_y)
    if numUnits > 0:
        random_index = random.randrange(0, numUnits)
        return [unit_x[random_index], unit_y[random_index]]
    return None

def get_mean_position(obs, type, player):
    unit_type = obs.observation[SCREEN][FEATURE_UNIT_TYPE] == type
    unit_player = obs.observation[SCREEN][FEATURE_PLAYER_RELATIVE] == player
    unit_y, unit_x = (unit_type * unit_player).nonzero()
    numUnits = len(unit_y)
    if numUnits > 0:
        return [int(unit_x.mean()), int(unit_y.mean())]
    return None
	
class Agent(base_agent.BaseAgent):
    selected_unit = False
    def step(self, obs):
        super(Agent, self).step(obs)
        if not self.selected_unit or FUNCTION_MOVE_SCREEN not in obs.observation["available_actions"]:
            target = get_unit(obs, UNIT_SCV, RELATIVE_SELF)
            if target is None:
                return actions.FunctionCall(FUNCTION_NO_OP, [])
            else:
                self.selected_unit = True
                return actions.FunctionCall(FUNCTION_SELECT_POINT, [NOT_QUEUED, target])
        else:
            target = get_mean_position(obs, BUILDING_COMMAND_CENTER, RELATIVE_SELF)
            if target is None:
                return actions.FunctionCall(FUNCTION_NO_OP, [])
            else:
                angle = 2 * math.pi * random.random()
                radius = 20 + 4 * random.random()
                target = [target[0] + radius*math.sin(angle), target[1] + radius*math.cos(angle)]
                if is_on_screen(target):
                    self.selected_unit = False # permite selecionar outro
                    return actions.FunctionCall(FUNCTION_MOVE_SCREEN, [NOT_QUEUED, target])
                else:
                    return actions.FunctionCall(FUNCTION_NO_OP, [])
