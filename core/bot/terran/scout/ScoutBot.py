#!/usr/bin/env python
# -*- coding: utf-8 -*-
import sc2

class Scout(sc2.BotAI):

    cmd_center = None
    current_scout = None
    found_enemy_base = False
    enemy_start_position = None
    enemy_location_counter = 0
    is_enemy_coming = False
    current_idle_units = None

    async def on_step(self, iteration):

        Scout.current_idle_units = self.units.idle.not_structure
        if Scout.cmd_center is None:
            Scout.cmd_center = self.units.structure[0]
        # Select worker to be the scouter
        if Scout.current_scout is None:
            Scout.current_scout = self.workers[0]
            await self.do(Scout.current_scout.move(self.enemy_start_locations[Scout.enemy_location_counter]))
        else:
            if self.known_enemy_structures and not Scout.found_enemy_base:
                Scout.enemy_start_position = self.known_enemy_structures[0].position
                Scout.found_enemy_base = True

            # equals isn't working...
            if Scout.current_idle_units and Scout.current_scout.tag == Scout.current_idle_units[0].tag:
                # Found enemy location, go back to base
                if Scout.found_enemy_base:
                        await self.do(Scout.current_scout.move(self.start_location))
                else:
                    # Haven't found enemy yet, go to next location
                    Scout.enemy_location_counter += 1
                    await self.do(Scout.current_scout.move(self.enemy_start_locations[Scout.enemy_location_counter]))
