#!/usr/bin/env python
# -*- coding: utf-8 -*-
from core.bot import util
from core.bot.generic_bot_non_player_unit import GenericBotNonPlayerUnit
from core.register_board.constants import RequestStatus, InfoType


class DefenseBot(GenericBotNonPlayerUnit):
    """  A defense units bot class """

    def __init__(self, bot_player, iteration, request, unit_tags):
        """
        :param core.bot.generic_bot_player.GenericBotPlayer bot_player:
        :param int iteration:
        :param core.register_board.request.Request request:
        :param list(int) unit_tags:
        """
        super(DefenseBot, self).__init__(
            bot_player=bot_player, iteration=iteration, request=request, unit_tags=unit_tags
        )

        self.cmd_center = None
        self.is_enemy_coming = False

    async def default_behavior(self, iteration):
        """ The default behavior of the bot
        :param int iteration: Game loop iteration
        """
        self.log("Executing {}".format(self._info.request))
        self.info.status = RequestStatus.ON_GOING
        await self.defend()

    async def move_units_to(self, position):
        self.log("Moving Defense units")
        units = self.bot_player.get_current_units(self._info.unit_tags)
        if units:
            for unit in units:
                await self.bot_player.do(unit.move(position))
        else:
            self.info.request.status = RequestStatus.FAILED

    async def attack_target(self, target):
        self.log("Attacking target")
        units = self.bot_player.get_current_units(self._info.unit_tags)
        for unit in units:
            await self.do(unit.attack(target))

    def get_attack_position(self):
        request_position = self.bot_player.board_info.search_request_by_type(InfoType.ENEMY_POSITION)
        if len(request_position) < 0:
            return self.bot_player.enemy_start_locations[0]
        else:
            return request_position[0].value

    async def perform_attack(self):
        position = self.get_attack_position()
        await self.move_units_to(position)

    async def visit_middle(self):
        self.log("Visiting middle")
        await self.move_units_to(util.get_mean_location(
            self.bot_player.start_location, self.bot_player.enemy_start_locations[0]))

    async def defend(self):
        self.log("Defending")
        target = self.select_enemy_target()
        if target:
            await self.attack_target(target)

    def select_enemy_target(self):
        self.log("Setting target")
        target = self.bot_player.known_enemy_units
        if len(target) > 0:
            return target.random.position
