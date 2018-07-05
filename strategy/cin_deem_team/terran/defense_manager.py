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

    async def update_barracks_rally(self):


    def find_request(self):
        """ Implements the logic to find the requests that should be handled by the bot
        :return list[core.register_board.request.Request]
        """
        self._relevant_info = self.find_info()
        army_requests = self.bot_player.board_request.search_request_by_operation_id(OperationTypeId.ARMY)
        army_requests.extend(self.bot_player.board_request.search_request_by_operation_id(OperationTypeId.DEFEND))
        army_requests.extend(self.bot_player.board_request.search_request_by_operation_id(OperationTypeId.ATTACK))
        return army_requests

    def find_info(self):
        return self.bot_player.board_info.search_request_by_type(InfoType.ENEMY_NEARBY)

    async def requests_handler(self, iteration):
        """ Logic to go through the bot requests
        :param int iteration: Game loop iteration
        """
        for request in self.requests:
            if request.status == RequestStatus.TO_BE_DONE and request.operation_type_id == OperationTypeId.ARMY:
                if request.unit_type_id == UnitTypeId.MARINE:
                    if self.find_ready_barracks():
                        await self.request_build(request, self.find_ready_barracks())
                elif request.unit_type_id == UnitTypeId.MARAUDER:
                    if self.find_ready_barracks_tech():
                        await self.request_build(request, self.find_ready_barracks_tech())

            if request.status == RequestStatus.TO_BE_DONE and request.operation_type_id == OperationTypeId.ATTACK:
                if len(self.find_available_defense_units()) >= request.amount:
                    self._defense_units = DefenseBot(
                        bot_player=self.bot_player,
                        iteration=iteration,
                        request=request,
                        unit_tags=util.get_units_tags(self.find_available_defense_units())
                    )
                    self.bot_player.board_request.register(
                        Request(request_priority=RequestPriority.PRIORITY_MEDIUM, unit_type_id=UnitTypeId.MARINE,
                                amount=15,
                                operation_type_id=OperationTypeId.ARMY)
                    )
                    await self.attack(iteration, self._defense_units)

            if not self._defense_units:
                available_defensive_units = self.find_available_defense_units()

                if available_defensive_units:
                    self._defense_units = DefenseBot(
                        bot_player=self.bot_player,
                        iteration=iteration,
                        request=request,
                        unit_tags=util.get_units_tags(available_defensive_units)
                    )

                    #await self.perform_defense(iteration, self._defense_units)
        #This was to defend from an attack, if there is an INFO that enemies are close,
        # create a DEFEND request on the position
        #for info in self._relevant_info:
                #if len(self.find_available_defense_units()) > info.value:
                    #Request(request_priority=RequestPriority.PRIORITY_HIGH, unit_type_id=UnitTypeId.MARINE,
                            #operation_type_id=OperationTypeId.DEFEND, location=info.location, value=info.value)

    async def request_build(self, request, barrack):
        if self.bot_player.can_afford(request.unit_type_id) and barrack.noqueue and request.amount >= 1:
            if self.bot_player.supply_left < 2 and self.bot_player.supply_cap < 200:
                Request(request_priority=RequestPriority.PRIORITY_HIGHER, unit_type_id=UnitTypeId.SUPPLYDEPOT,
                        operation_type_id=OperationTypeId.BUILD)
            else:
                await self.bot_player.do(barrack.train(request.unit_type_id))
                self.update_build_request(request)

    def update_build_request(self, request):
        amount = request.amount - 1
        request.amount = amount
        if request.amount == 0:
            self.bot_player.board_request.remove(request)

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

    @staticmethod
    async def attack(iteration, defense):
        """
        :param int iteration: Game loop iteration
        :param core.bot.terran.d
        """
        await defense.perform_attack()
