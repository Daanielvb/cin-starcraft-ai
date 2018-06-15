from pysc2.agents import base_agent
from pysc2.env import sc2_env
from pysc2.lib import actions, features
from absl import app
from pysc2.lib.units import Terran



UNIT_SCV = Terran.SCV
TERRAN_COMMAND_CENTER = Terran.CommandCenter
_BUILD_SUPPLYDEPOT = actions.FUNCTIONS.Build_SupplyDepot_screen.id



class TerranAgent(base_agent.BaseAgent):

    #should be moved to another class, couldnt make it for now
    def unit_type_is_selected(self, obs, unit_type):
        if (len(obs.observation.single_select) > 0 and
                obs.observation.single_select[0].unit_type == unit_type):
            return True

        if (len(obs.observation.multi_select) > 0 and
                obs.observation.multi_select[0].unit_type == unit_type):
            return True
        return False

    def step(self, obs):
        super(TerranAgent, self).step(obs)


        #if command center is selected, build SCV
        if self.unit_type_is_selected(obs, TERRAN_COMMAND_CENTER):
            if (actions.FUNCTIONS.Train_SCV_quick.id in
                    obs.observation.available_actions):
                return actions.FUNCTIONS.Train_SCV_quick("now")

        #get list of cmd centers
        cmd_centers = [unit for unit in obs.observation.feature_units
                  if unit.unit_type == TERRAN_COMMAND_CENTER]

        if len(cmd_centers) > 0:
            # if there is a cmd center, get the first one and select it
            cmd_center = cmd_centers[0]

            return actions.FUNCTIONS.select_point("select_all_type", (cmd_center.x, cmd_center.y))

        return actions.FUNCTIONS.no_op()


def main(unused_argv):
    agent = TerranAgent()
    try:
        while True:

            with sc2_env.SC2Env(
                    map_name="Simple64",
                    players=[sc2_env.Agent(sc2_env.Race.terran),
                             sc2_env.Bot(sc2_env.Race.terran,
                                         sc2_env.Difficulty.very_easy)],
                    agent_interface_format=features.AgentInterfaceFormat(
                        feature_dimensions=features.Dimensions(screen=84, minimap=64),
                        use_feature_units=True),
                    step_mul=16,
                    game_steps_per_episode=0,
                    visualize=True) as env:

                agent.setup(env.observation_spec(), env.action_spec())
                timesteps = env.reset()
                agent.reset()

                while True:
                    step_actions = [agent.step(timesteps[0])]
                    if timesteps[0].last():
                        break
                    timesteps = env.step(step_actions)

    except KeyboardInterrupt:
        pass


if __name__ == "__main__":
    app.run(main)