#!/usr/bin/env python
# -*- coding: utf-8 -*-

from core.bot.generic_bot_non_player import GenericBotNonPlayer
from core.bot import util
from core.register_board.info import Info

START = 'START'
STOP = 'STOP'

class Scout(GenericBotNonPlayer):
    """  A Scout bot class """

    def __init__(self, bot_player, border):
        """
        :param core.bot.generic_bot_player.GenericBotPlayer bot_player:
        """
        super(Scout, self).__init__(bot_player)

        self._border_info = border
        self.cmd_center = None
        self.current_scout = None
        self.found_enemy_base = False
        self.enemy_start_position = None
        self.enemy_location_counter = 0
        self.mean_location = None
        self.is_enemy_coming = False
        self.current_idle_units = None
        self.patrol = True
        self._info = None

    async def default_behavior(self, iteration, request):
        """ The default behavior of the bot
        :param int iteration: Game loop iteration
        :param core.register_board.request.Request request:
        """
        if iteration == 0:
            self._info = Info(iteration=iteration, bot=self, request=request, status=START)
            self.bot_player.board_info.register(self._info)
            await self.scout(request)

    async def move_scout_to(self, position):
        self.log("Moving Scout")
        await self.bot_player.do(self.current_scout.move(position))

    def set_scout(self):
        self.log("Setting Scout")
        if not self.current_scout:
            # TODO: Get free scout based on BOARD info
            # TODO: If there are not free scouts, ask the manager for one.
            self.current_scout = self.bot_player.workers[0]
            self.set_mean_location()
            self._info.unit = self.current_scout

    def set_mean_location(self):
        self.mean_location = util.get_mean_location(
            self.bot_player.start_location, self.bot_player.enemy_start_locations[0]
        )

    def set_cmd_center(self):
        self.log("Setting cmd center")
        if self.cmd_center is None:
            self.cmd_center = self.bot_player.units.structure[0]

    def set_enemy_position(self):
        self.log("Found enemy base")
        self.enemy_start_position = self.bot_player.known_enemy_structures[0].position
        self.found_enemy_base = True

    def get_found_enemy_base(self):
        return self.found_enemy_base

    def get_found_enemies_nearby(self):
        return self.found_enemies_nearby

    async def visit_enemy(self):
        await self.move_scout_to(self.bot_player.enemy_start_locations[self.enemy_location_counter])

    async def visit_base(self):
        self.log("Visiting base")
        await self.move_scout_to(self.cmd_center)

    async def visit_middle(self):
        self.log("Visiting middle")
        await self.move_scout_to(self.cmd_center)

    async def scout(self, request):
        self.log("Executing {}".format(request))
        self.set_cmd_center()
        self.set_scout()
        await self.visit_enemy()

        # Sorry :)
        # if self.bot_player.known_enemy_structures and not self.found_enemy_base:
        #     # TODO: Write this info on the BOARD
        #     self.set_enemy_position()
        #
        # # If found enemy base, go patrolling
        # if self.found_enemy_base:
        #     # current scout position is not being updated, so this approach doesn't work
        #     await self.visit_base()
