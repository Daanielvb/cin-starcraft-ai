#!/usr/bin/env python
# -*- coding: utf-8 -*-
import sc2
from sc2.constants import *
from sc2 import Race, Difficulty
from sc2.constants import *
from sc2.player import Bot, Computer
from sc2.helpers import ControlGroup

# When using heritage, debug mode isn't working
from core.bot.terran.generic_terran_bot import GenericTerranBot


class Scout(sc2.BotAI):
    current_scout = None
    found_enemy_base = False
    enemy_start_position = None
    enemy_location_counter = 0
    is_enemy_coming = False
    current_idle_units = None

    async def on_step(self, iteration):
        Scout.current_idle_units = self.units.idle.not_structure

        # Select worker to be the scouter
        if Scout.current_scout is None:
            Scout.current_scout = self.workers[0]
            await self.do(Scout.current_scout.move(self.enemy_start_locations[Scout.enemy_location_counter]))
        else:
            if self.known_enemy_structures and not Scout.found_enemy_base:
                Scout.enemy_start_position = self.known_enemy_structures[0].position
                Scout.found_enemy_base = True
            if Scout.current_idle_units and Scout.current_scout.tag == Scout.current_idle_units[0].tag:
                # Found enemy location, go back to base
                if Scout.found_enemy_base:
                    print('Should move to base now')
                    # The line below is crashing the game, must find a way to send the scouter back to base
                    # await self.do(Scout.current_scout.move(self.start_location))
                else:
                    # Haven't found enemy yet, go to next location
                    Scout.enemy_location_counter += 1
                    await self.do(Scout.current_scout.move(self.enemy_start_locations[Scout.enemy_location_counter]))
