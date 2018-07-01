#!/usr/bin/env python
# -*- coding: utf-8 -*-

from sc2.ids.ability_id import AbilityId
from sc2.ids.unit_typeid import UnitTypeId

from core.bot.generic_bot_non_player_unit import GenericBotNonPlayerUnit
from core.bot.util import distance


class Build(GenericBotNonPlayerUnit):
    """  A Scout bot class """

    def __init__(self, bot_player, iteration, request, unit_tag):
        """
        :param core.bot.generic_bot_player.GenericBotPlayer bot_player:
        :param int iteration:
        :param core.register_board.request.Request request:
        :param int unit_tag:
        """
        super(Build, self).__init__(
            bot_player=bot_player, iteration=iteration, request=request, unit_tag=unit_tag
        )

    async def default_behavior(self, iteration):
        """ The default behavior of the bot
        :param int iteration: Game loop iteration
        """
        await self._build()
        # await self.depot_behaviour()

    async def _build(self):
        """
        Build action
        """
        build_type = self.info.request.unit_type_id
        scv = self.bot_player.select_build_worker(self.info.request.location, True)
        # await self.bot_player.do(scv.build(build_type, self.info.request.location))
        await self.bot_player.do(scv.build(build_type, self.info.request.location))

    async def depot_behaviour(self):
        """
        Supply depot behaviour
        """
        enemies = self.known_enemy_units.not_structure

        for depot in self.units(UnitTypeId.SUPPLYDEPOTLOWERED).ready:
            for enemy in enemies:
                if distance(enemy, depot) < 12:
                    await self.do(depot(AbilityId.MORPH_SUPPLYDEPOT_RAISE))
                    break

        for depot in self.units(UnitTypeId.SUPPLYDEPOT).ready:
            enemies_far = True
            for enemy in enemies:
                if distance(enemy, depot) < 16:
                    enemies_far = False
                    break
            if enemies_far:
                await self.do(depot(AbilityId.MORPH_SUPPLYDEPOT_LOWER))
