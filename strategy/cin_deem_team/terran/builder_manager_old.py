from core.bot.terran.generic_terran_bot import GenericTerranBot
from core.bot.util import distance

from enum import Enum

from sc2.ids.ability_id import AbilityId
from sc2.ids.unit_typeid import UnitTypeId


class Builder(GenericTerranBot):
    """
    Builder Bot
    """
    build_request = []

    async def on_step(self, iteration):
        await self.__builder_logic()  # builder
        await self.__depot_logic()    # suply depot

    # async def __builder_logic(self):
    #     if self.supply_left < 5 and self.supply_cap < 200 \
    #             and self.can_afford(UnitTypeId.SUPPLYDEPOT) and not self.already_pending(UnitTypeId.SUPPLYDEPOT):
    #         #precisa construir um Supply Depot
    #         build_location = await self.get_depot_build_location()
    #         print(build_location)
    #         if build_location is not None:
    #             scv = self.select_build_worker(build_location, True)
    #             await self.do(scv.build(UnitTypeId.SUPPLYDEPOT, build_location))
    #     elif self.units(UnitTypeId.REFINERY).amount < 2 and self.can_afford(UnitTypeId.REFINERY)
    #       and not self.already_pending(UnitTypeId.REFINERY):
    #         build_location = self.state.vespene_geyser.closest_to(self.start_location)
    #         if build_location is not None:
    #             scv = self.select_build_worker(build_location, True)
    #             await self.do(scv.build(UnitTypeId.REFINERY, build_location))

    async def __builder_logic(self):
        current_request = self.build_request[0]
        build_type = current_request.build_type
        if (self.can_afford(build_type) and self.units(build_type).amount < current_request.build_number_limit
                and not self.already_pending(build_type)):

            if current_request.location is not None:
                scv = self.select_build_worker(current_request.build_location, True)
                await self.do(scv.build(build_type, current_request.build_location))

            elif build_type == UnitTypeId.COMMANDCENTER:
                # Criar outro Command Center
                await self.expand_now()

    async def depot_logic(self):
        enemies = self.known_enemy_units.not_structure
        # Verifica se deve levantar a defesa suply depot
        for depot in self.units(UnitTypeId.SUPPLYDEPOTLOWERED).ready:
            for enemy in enemies:
                if distance(enemy, depot) < 12:
                    await self.do(depot(AbilityId.MORPH_SUPPLYDEPOT_RAISE))
                    break

        # Verifica se deve abaixar a defesa do suply depot
        for depot in self.units(UnitTypeId.SUPPLYDEPOT).ready:
            enemies_far = True
            for enemy in enemies:
                if distance(enemy, depot) < 16:
                    enemies_far = False
                    break
            if enemies_far:
                await self.do(depot(AbilityId.MORPH_SUPPLYDEPOT_LOWER))






