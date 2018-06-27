#!/usr/bin/env python
# -*- coding: utf-8 -*-
import sc2

from core.bot.terran.generic_terran_bot import GenericTerranBot
from core.bot.util import *


class Scout(GenericTerranBot):

    def __init__(self):
        super(Scout, self).__init__()

        self.cmd_center = None
        self.current_scout = None
        self.found_enemy_base = False
        self.enemy_start_position = None
        self.enemy_location_counter = 0
        self.mean_location = None
        self.is_enemy_coming = False
        self.current_idle_units = None
        self.patrol = True

    async def move_scout_to(self, position, observer):
        await observer.do(self.current_scout.move(position))

    def set_scout(self, observer):
        if self.current_scout is None:
            self.current_scout = observer.workers[0]

    def set_cmd_center(self, observer):
        if self.cmd_center is None:
            self.cmd_center = observer.units.structure[0]

    def set_enemy_position(self, observer):
        self.enemy_start_position = observer.known_enemy_structures[0].position
        self.found_enemy_base = True

    def on_start(self):
        pass

    async def default_on_step(self, iteration, observer):
        self.log("HERE!!!")

        if self.cmd_center is None:
            self.set_cmd_center(observer)
            self.mean_location = get_mean_location(observer.start_location, observer.enemy_start_locations[0])
            # Select worker to be the scouter
        elif self.current_scout is None:
            self.set_scout(observer)
            await self.move_scout_to(observer, observer.enemy_start_locations[self.enemy_location_counter])
        else:
            if observer.known_enemy_structures and not self.found_enemy_base:
                self.set_enemy_position(observer)

            # If scout is idle
            if observer.units.idle.not_structure and contains_unit(self.current_scout, observer.units.idle.not_structure):
                # Found enemy location, go back to base
                if self.found_enemy_base:
                    # current scout position is not being updated, so this approach doesn't work
                    # dist_to_middle = distance(self.current_scout.position, self.mean_location)
                    # dist_to_base = distance(self.current_scout.position, self.cmd_center)
                    # Patrolling not working yet
                    if self.patrol:
                        await self.move_scout_to(observer, self.cmd_center)
                        self.patrol = False
                    if not self.patrol:
                        await self.move_scout_to(observer, self.mean_location)
                        self.patrol = True

                        # await observer.do(self.current_scout.move(observer.start_location))
                else:
                    # Haven't found enemy yet, go to next location
                    self.enemy_location_counter += 1
                    # await observer.do(self.current_scout.move(observer.enemy_start_locations[self.enemy_location_counter]))
