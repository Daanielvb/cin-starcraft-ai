#!/usr/bin/env python
# -*- coding: utf-8 -*-

from core.bot.generic_bot_non_player import GenericBotNonPlayer
from core.bot.terran.scout.scout import Scout
from core.register_board.constants import OperationTypeId
from core.register_board.request import RequestStatus


class ScoutManager(GenericBotNonPlayer):
    """ Scout manager class """

    def __init__(self, bot_player):
        """
        :param core.bot.generic_bot_player.GenericBotPlayer bot_player:
        """
        super(ScoutManager, self).__init__(bot_player)
        self._scout_unit = None

    def find_request(self):
        """ Implements the logic to find the requests that should be handled by the bot
        :return list[core.register_board.request.Request]
        """
        return self.bot_player.board_request.search_request_by_operation_id(OperationTypeId.SCOUT)

    async def requests_handler(self, iteration):
        """ Logic to go through the bot requests
        :param int iteration: Game loop iteration
        """
        for request in self.requests:
            if not self._scout_unit:
                available_scvs = self.find_available_scvs_units()

                if available_scvs:
                    self._scout_unit = Scout(
                        bot_player=self.bot_player,
                        iteration=iteration,
                        request=request,
                        unit_tag=available_scvs[0].tag
                    )

                    await self.perform_scout(iteration, self._scout_unit)

    def requests_status_update(self):
        """ Logic to update the requests status """
        if self._scout_unit:
            if not self._scout_unit.info.request.status == RequestStatus.DONE:
                if self._scout_unit.is_idle():
                    self.bot_player.board_request.remove(self._scout_unit.info.request)
                    self._scout_unit.info.status = RequestStatus.DONE

    @staticmethod
    async def perform_scout(iteration, scout):
        """
        :param int iteration: Game loop iteration
        :param core.bot.terran.scout.scout.Scout scout:
        """
        await scout.default_behavior(iteration)

        if scout.get_found_enemy_base():

            if iteration % 30 == 0:
                await scout.visit_middle()

            elif iteration % 80 == 0:
                await scout.visit_base()

        # TODO: Implement nearby friends logic and warn
        # elif bot.found_enemies_nearby():
            # await bot.visit_base()
