#!/usr/bin/env python
# -*- coding: utf-8 -*-

import sc2

from core.config import maps


# All bots inherit from sc2.BotAI
class WorkerRushBot(sc2.BotAI):

    # The on_step function is called for every game step
    # It is defined as async because it calls await functions
    # It takes current game state and current iteration
    async def on_step(self, iteration):

        if iteration == 0: # If this is the first frame

            for worker in self.workers:

                # Attack to the enemy base with this worker
                # (Assumes that there is only one possible starting location
                # for the opponent, which depends on the map)
                await self.do(worker.attack(self.enemy_start_locations[0]))


if __name__ == '__main__':
    sc2.run_game(sc2.maps.get(maps.Simple64), [
        sc2.player.Human(sc2.Race.Terran),
        sc2.player.Bot(sc2.Race.Zerg, WorkerRushBot())
    ], realtime=True)