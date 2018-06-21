#!/usr/bin/env python
# -*- coding: utf-8 -*-

import sc2
from core.config import maps
import numpy as np

from sc2.position import Point2
from sc2.ids.ability_id import AbilityId
from sc2.ids.unit_typeid import UnitTypeId

def distance(unit_a, unit_b):
    return unit_a.position.to2.distance_to(unit_b.position.to2)

class BuilderBot(sc2.BotAI):

    next_depot = 0

    async def get_depot_build_location(self):
        #pega as rampas próximas da base
        depos = [
            Point2((np.median([p.x for p in d]), np.median([p.y for p in d])))
            for d in self.main_base_ramp.top_wall_depos
        ]

        num_ramps = len(depos)

        if num_ramps > 0:
            self.next_depot = self.next_depot + 1
            return await self.find_placement(UnitTypeId.SUPPLYDEPOT, list(depos)[self.next_depot % num_ramps])
        else:
            return await self.find_placement(UnitTypeId.SUPPLYDEPOT, self.start_location)

    async def scv_logic(self):
        if self.supply_left < 5 and self.supply_cap < 200\
                and self.can_afford(UnitTypeId.SUPPLYDEPOT) and not self.already_pending(UnitTypeId.SUPPLYDEPOT):
            #precisa construir um Supply Depot
            build_location = await self.get_depot_build_location()
            print(build_location)
            if build_location is not None:
                scv = self.select_build_worker(build_location, True)
                await self.do(scv.build(UnitTypeId.SUPPLYDEPOT, build_location))
        elif self.units(UnitTypeId.REFINERY).amount < 2 and self.can_afford(UnitTypeId.REFINERY) and not self.already_pending(UnitTypeId.REFINERY):
            build_location = self.state.vespene_geyser.closest_to(self.start_location)
            if build_location is not None:
                scv = self.select_build_worker(build_location, True)
                await self.do(scv.build(UnitTypeId.REFINERY, build_location))
        elif self.units(UnitTypeId.COMMANDCENTER).amount < 2 and self.can_afford(UnitTypeId.COMMANDCENTER):
            #precisa criar outro Command Center
            await self.expand_now()

        #distribui os trabalhadores
        await self.distribute_workers()

    async def depot_logic(self):
        enemies = self.known_enemy_units.not_structure
        #verifica se deve levantar a defesa
        for depot in self.units(UnitTypeId.SUPPLYDEPOTLOWERED).ready:
            for enemy in enemies:
                if distance(enemy, depot) < 12:
                    await self.do(depot(AbilityId.MORPH_SUPPLYDEPOT_RAISE))
                    break

        #verifica se deve abaixar a defesa
        for depot in self.units(UnitTypeId.SUPPLYDEPOT).ready:
            enemies_far = True
            for enemy in enemies:
                if distance(enemy, depot) < 16:
                    enemies_far = False
                    break
            if enemies_far:
                await self.do(depot(AbilityId.MORPH_SUPPLYDEPOT_LOWER))

    async def center_logic(self):
        num_idle_workers = len(self.workers.idle)
        command_centers = self.units(UnitTypeId.COMMANDCENTER).ready
        for cmd_cen in command_centers:
            if self.can_afford(UnitTypeId.SCV) and cmd_cen.noqueue:
                refinery_slots = 0
                refs = self.units(UnitTypeId.REFINERY).ready.closer_than(20, cmd_cen.position)
                for ref in refs:
                    refinery_slots += ref.ideal_harvesters - ref.assigned_harvesters

                if cmd_cen.assigned_harvesters < (cmd_cen.ideal_harvesters + refinery_slots - num_idle_workers):
                    #precisa treinar um SCV
                    await self.do(cmd_cen.train(UnitTypeId.SCV))

    async def on_step(self, iteration):
        await self.scv_logic() #logica do SCV
        await self.center_logic() #logica do COMMAND_CENTER
        await self.depot_logic() #logica do SUPPLY DEPOT
