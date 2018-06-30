#!/usr/bin/env python
# -*- coding: utf-8 -*-
from sc2.ids.ability_id import AbilityId
from sc2.ids.unit_typeid import UnitTypeId

from core.bot.generic_bot_non_player import GenericBotNonPlayer
from core.bot.util import distance
from core.register_board.constants import RequestStatus
from core.register_board.info import Info


class Build(GenericBotNonPlayer):
    """  A Scout bot class """

    def __init__(self, bot_player, border):
        """
        :param core.bot.generic_bot_player.GenericBotPlayer bot_player:
        """
        super(Build, self).__init__(bot_player)
        self._border_info = border
        self._info = None

    async def default_behavior(self, iteration):
        """ The default behavior of the bot
        :param int iteration: Game loop iteration
        """
        if iteration == 0:
            # self._info = Info(iteration=iteration, bot=self, request=request, status='START')
            # self.bot_player.board_info.register(self._info)
            # await self._build(request)
            pass

    async def _build(self, request):
        """
        Build action
        :param core.register_board.request.Request request:
        """
        build_type = request.unit_type_id
        if (self.can_afford(build_type) and self.check_number_of(build_type) < 200
                and not self.already_pending(build_type)):

            if request.location is not None:
                scv = self.bot_player.select_build_worker(request.location, True)
                await self.bot_player.do(scv.build(build_type, request.location))

    def can_afford(self, type):
        return self.bot_player.can_afford(type)

    def check_number_of(self, type):
        return self.bot_player.units(type).amount

    def already_pending(self, type):
        return self.bot_player.already_pending(type)

    async def depot_behaviour(self, request):
        """
        Supply depot behaviour
        :param request:
        """
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
