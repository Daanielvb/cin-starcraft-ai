#!/usr/bin/env python
# -*- coding: utf-8 -*-

from sc2.ids.ability_id import AbilityId
from sc2.ids.unit_typeid import UnitTypeId

from core.bot.generic_bot_non_player_unit import GenericBotNonPlayerUnit
from core.register_board.constants import RequestStatus


class Build(GenericBotNonPlayerUnit):
    """  A Scout bot class """

    def __init__(self, bot_player, iteration, request, unit_tags):
        """
        :param core.bot.generic_bot_player.GenericBotPlayer bot_player:
        :param int iteration:
        :param core.register_board.request.Request request:
        :param list(int) unit_tags:
        """
        super(Build, self).__init__(
            bot_player=bot_player, iteration=iteration, request=request, unit_tags=unit_tags
        )

    async def default_behavior(self, iteration):
        """ The default behavior of the bot
        :param int iteration: Game loop iteration
        """
        await self._build()
        await self.depot_behaviour()

    async def _build(self):
        """
        Build action
        """
        if self.info.request.location:
            build_type = self.info.request.unit_type_id
            scv = await self.get_builder()
            # location = self.bot_player.owned_expansions.popitem()[1].position.towards_with_random_angle(
            #     self.bot_player.game_info.map_center, 8
            # )
            if self.info.request.unit_type_id == UnitTypeId.REFINERY:
                location = self.info.request.location
            else:
                location = self.info.request.location.towards_with_random_angle(self.bot_player.game_info.map_center, 8)

            await self.bot_player.do(scv.build(build_type, location))

            self.log("########################## Request DONE: {}".format(self.info.request))
            self.info.request.status = RequestStatus.DONE


            # build_type, near=self.info.request.location.towards(self.bot_player.game_info.map_center, 8))
        else:
            self.log("Location is None to build: {}".format(self.info.request))

    async def get_builder(self):
        if not self.info.unit_tag:
            scv = self.bot_player.select_build_worker(self.info.request.location, True)
            self.info.unit_tag = scv.tag

        return self.bot_player.get_current_scv_unit(self._info.unit_tag)

    async def depot_behaviour(self):
        """
        Supply depot behaviour
        """
        for depot in self.bot_player.units(UnitTypeId.SUPPLYDEPOT).ready:
            await self.bot_player.do(depot(AbilityId.MORPH_SUPPLYDEPOT_LOWER))
