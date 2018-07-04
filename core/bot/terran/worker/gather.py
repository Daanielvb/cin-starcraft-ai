#!/usr/bin/env python
# -*- coding: utf-8 -*-
from sc2.ids.ability_id import AbilityId
from sc2.ids.unit_typeid import UnitTypeId

from core.bot.generic_bot_non_player import GenericBotNonPlayer
from core.bot.util import distance
from core.register_board.constants import RequestStatus
from core.register_board.info import Info


def get_workers_free_slots(unit):
    return unit.ideal_harvesters - unit.assigned_harvesters

def scv_can_gather(scv):
    orders = scv.orders
    return len(orders) < 1 or orders[0].ability.id in [AbilityId.HARVEST_GATHER, AbilityId.HARVEST_RETURN]

class Gather(GenericBotNonPlayer):
    """  A Gather bot class """

    should_train_scv = False

    def __init__(self, bot_player):
        """
        :param core.bot.generic_bot_player.GenericBotPlayer bot_player:
        """
        super(Gather, self).__init__(bot_player)
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
        else:
            await self.gather_resources()
            if self.should_train_scv:
                await self.train_scv()

    async def toggle_train_scv(self, should_train):
        self.should_train_scv = should_train

    async def gather_resources(self):
        if self.bot_player.state.mineral_field:
            await self.bot_player.distribute_workers()

    async def train_scv(self):
        num_idle_workers = len(self.bot_player.workers.idle)
        command_centers = self.bot_player.units(UnitTypeId.COMMANDCENTER).ready
        for cmd_cen in command_centers:
            if self.bot_player.can_afford(UnitTypeId.SCV) and cmd_cen.noqueue:
                refinery_slots = 0
                refs = self.bot_player.units(UnitTypeId.REFINERY).ready.closer_than(20, cmd_cen.position)
                for ref in refs:
                    refinery_slots += ref.ideal_harvesters - ref.assigned_harvesters

                if cmd_cen.assigned_harvesters < (cmd_cen.ideal_harvesters + refinery_slots - num_idle_workers):
                    #precisa treinar um SCV
                    await self.bot_player.do(cmd_cen.train(UnitTypeId.SCV))
