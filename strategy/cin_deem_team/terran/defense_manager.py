#!/usr/bin/env python
# -*- coding: utf-8 -*-
from sc2.ids.unit_typeid import UnitTypeId

from core.bot import util
from core.bot.generic_bot_non_player import GenericBotNonPlayer
from core.bot.terran.military.defense import DefenseBot
from core.register_board.constants import OperationTypeId, RequestStatus, InfoType, RequestPriority
from core.register_board.request import Request


class DefenseManager(GenericBotNonPlayer):
    """ Defense manager class """

    def __init__(self, bot_player):
        """
        :param core.bot.generic_bot_player.GenericBotPlayer bot_player:
        """
        super(DefenseManager, self).__init__(bot_player)
        self._defense_units = None
        self._relevant_info = None


    def find_request(self):
        """ Implements the logic to find the requests that should be handled by the bot
        :return list[core.register_board.request.Request]
        """
        self._relevant_info = self.find_info()
        return self.bot_player.board_request.search_request_by_operation_id(OperationTypeId.DEFEND)

    def find_info(self):
        return self.bot_player.board_info.search_request_by_type(InfoType.ENEMY_NEARBY)


    async def requests_handler(self, iteration):
        """ Logic to go through the bot requests
        :param int iteration: Game loop iteration
        """
        for request in self.requests:
            if not self._defense_units:
                available_defensive_units = self.find_available_defense_units()

                if available_defensive_units:
                    self._defense_units = DefenseBot(
                        bot_player=self.bot_player,
                        iteration=iteration,
                        request=request,
                        unit_tags=util.get_units_tags(available_defensive_units)
                    )

                    await self.perform_defense(iteration, self._defense_units)
            else:
                if request.status == RequestStatus.TO_BE_DONE and request.operation_type_id == OperationTypeId.DEFEND:
                    print('defend!')
                    # check if there are marines to bunker
                    # move defense units to ramp
        for info in self._relevant_info:
                if len(self.find_available_defense_units()) > info.value:
                    Request(request_priority=RequestPriority.PRIORITY_HIGH, unit_type_id=UnitTypeId.MARINE,
                            operation_type_id=OperationTypeId.DEFEND, location=info.location, value=info.value)


    def requests_status_update(self):
        """ Logic to update the requests status """
        if self._defense_units:
            if self._defense_units.info.request.status != RequestStatus.ON_GOING \
                    and self._defense_units.info.request.status != RequestStatus.DONE:
                if self._defense_units.are_idle():
                    self.bot_player.board_request.remove(self._defense_units.info.request)
                    self._defense_units.info.status = RequestStatus.DONE


    @staticmethod
    async def perform_defense(iteration, defense):
        """
        :param int iteration: Game loop iteration
        :param core.bot.terran.d
        """
        await defense.default_behavior(iteration)
