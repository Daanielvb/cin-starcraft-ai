#!/usr/bin/env python
# -*- coding: utf-8 -*-
import sc2

from core.bot.util import *


class Scout(sc2.BotAI):

    cmd_center = None
    current_scout = None
    found_enemy_base = False
    enemy_start_position = None
    enemy_location_counter = 0
    mean_location = None
    is_enemy_coming = False
    current_idle_units = None
    patrol = True

    async def move_scout_to(self, position):
        await self.do(Scout.current_scout.move(position))

    def set_scout(self):
        if Scout.current_scout is None:
            Scout.current_scout = self.workers[0]

    def set_cmd_center(self):
        if Scout.cmd_center is None:
            Scout.cmd_center = self.units.structure[0]

    def set_enemy_position(self):
        Scout.enemy_start_position = self.known_enemy_structures[0].position
        Scout.found_enemy_base = True

    async def on_step(self, iteration):

        if Scout.cmd_center is None:
            Scout.set_cmd_center(self)
            Scout.mean_location = get_mean_location(self.start_location, self.enemy_start_locations[0])
        # Select worker to be the scouter
        elif Scout.current_scout is None:
            Scout.set_scout(self)
            await Scout.move_scout_to(self, self.enemy_start_locations[Scout.enemy_location_counter])
        else:
            if self.known_enemy_structures and not Scout.found_enemy_base:
                Scout.set_enemy_position(self)

            # If scout is idle
            if self.units.idle.not_structure and contains_unit(Scout.current_scout, self.units.idle.not_structure):
                # Found enemy location, go back to base
                if Scout.found_enemy_base:
                    # current scout position is not being updated, so this approach doesn't work
                    # dist_to_middle = distance(Scout.current_scout.position, Scout.mean_location)
                    # dist_to_base = distance(Scout.current_scout.position, Scout.cmd_center)
                    # Patrolling not working yet
                    if Scout.patrol:
                        await Scout.move_scout_to(self, Scout.cmd_center)
                        Scout.patrol = False
                    if not Scout.patrol:
                        await Scout.move_scout_to(self, Scout.mean_location)
                        Scout.patrol = True

                        #await self.do(Scout.current_scout.move(self.start_location))
                else:
                    # Haven't found enemy yet, go to next location
                    Scout.enemy_location_counter += 1
                    #await self.do(Scout.current_scout.move(self.enemy_start_locations[Scout.enemy_location_counter]))
