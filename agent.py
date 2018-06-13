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

def isInRange(value, beginValue, endValue):
    return value >= beginValue and value < endValue

def isOnScreen(target):
    return isInRange(target[0],0,84) and isInRange(target[1],0,84)

def getUnit(obs, type, player):
    unit_type = obs.observation[SCREEN][FEATURE_UNIT_TYPE] == type
    unit_player = obs.observation[SCREEN][FEATURE_PLAYER_RELATIVE] == player
    unit_y, unit_x = (unit_type * unit_player).nonzero()
    numUnits = len(unit_y)
    if numUnits > 0:
        random_index = random.randrange(0, numUnits)
        return [unit_x[random_index], unit_y[random_index]]
    return None

def getMeanPosition(obs, type, player):
    unit_type = obs.observation[SCREEN][FEATURE_UNIT_TYPE] == type
    unit_player = obs.observation[SCREEN][FEATURE_PLAYER_RELATIVE] == player
    unit_y, unit_x = (unit_type * unit_player).nonzero()
    numUnits = len(unit_y)
    if numUnits > 0:
        return [int(unit_x.mean()), int(unit_y.mean())]
    return None
	
class Agent(base_agent.BaseAgent):
    selectedUnit = False
    def step(self, obs):
        super(Agent, self).step(obs)
        if not self.selectedUnit or FUNCTION_MOVE_SCREEN not in obs.observation["available_actions"]:
            target = getUnit(obs, UNIT_SCV, RELATIVE_SELF)
            if target is None:
                return actions.FunctionCall(FUNCTION_NO_OP, [])
            else:
                self.selectedUnit = True
                return actions.FunctionCall(FUNCTION_SELECT_POINT, [NOT_QUEUED, target])
        else:
            target = getMeanPosition(obs, BUILDING_COMMAND_CENTER, RELATIVE_SELF)
            if target is None:
                return actions.FunctionCall(FUNCTION_NO_OP, [])
            else:
                angle = 2 * math.pi * random.random()
                radius = 20 + 4 * random.random()
                target = [target[0] + radius*math.sin(angle), target[1] + radius*math.cos(angle)]
                if isOnScreen(target):
                    self.selectedUnit = False # permite selecionar outro
                    return actions.FunctionCall(FUNCTION_MOVE_SCREEN, [NOT_QUEUED, target])
                else:
                    return actions.FunctionCall(FUNCTION_NO_OP, [])
