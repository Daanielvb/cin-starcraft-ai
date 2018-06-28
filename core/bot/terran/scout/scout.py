#!/usr/bin/env python
# -*- coding: utf-8 -*-

from core.bot.generic_bot_non_player import GenericBotNonPlayer
from core.bot import util


class Scout(GenericBotNonPlayer):
    """  A Scout bot class """

    def __init__(self, bot_player):
        """
        :param core.bot.generic_bot_player.GenericBotPlayer bot_player:
        """
        super(Scout, self).__init__(bot_player)

        self.cmd_center = None
        self.current_scout = None
        self.found_enemy_base = False
        self.enemy_start_position = None
        self.enemy_location_counter = 0
        self.mean_location = None
        self.is_enemy_coming = False
        self.current_idle_units = None
        self.patrol = True

    async def default_behavior(self, iteration):
        """ The default behavior of the bot
        :param int iteration: Game loop iteration
        """
        await self.scout()

    async def move_scout_to(self, position):
        await self.bot_player.do(self.current_scout.move(position))

    def set_scout(self):
        if self.current_scout is None:
            self.current_scout = self.bot_player.workers[0]

    def set_cmd_center(self):
        if self.cmd_center is None:
            self.cmd_center = self.bot_player.units.structure[0]

    def set_enemy_position(self):
        self.enemy_start_position = self.bot_player.known_enemy_structures[0].position
        self.found_enemy_base = True

    async def scout(self):
        self.log("Starting Scout")

        if self.cmd_center is None:
            self.set_cmd_center()
            self.mean_location = util.get_mean_location(
                self.bot_player.start_location, self.bot_player.enemy_start_locations[0]
            )

        elif self.current_scout is None:
            # Select worker to be the scouter
            self.set_scout()
            await self.move_scout_to(
                self.bot_player.enemy_start_locations[self.enemy_location_counter]
            )

        else:

            if self.bot_player.known_enemy_structures and not self.found_enemy_base:
                self.set_enemy_position()

            # If scout is idle
            if self.bot_player.units.idle.not_structure and util.contains_unit(self.current_scout, self.bot_player.units.idle.not_structure):

                # Found enemy location, go back to base
                if self.found_enemy_base:

                    # current scout position is not being updated, so this approach doesn't work
                    # dist_to_middle = distance(self.current_scout.position, self.mean_location)
                    # dist_to_base = distance(self.current_scout.position, self.cmd_center)
                    # Patrolling not working yet
                    if self.patrol:
                        await self.move_scout_to(self.cmd_center)
                        self.patrol = False

                    if not self.patrol:
                        await self.move_scout_to(self.mean_location)
                        self.patrol = True

                        # await observer.do(self.current_scout.move(observer.start_location))
                else:
                    # Haven't found enemy yet, go to next location
                    self.enemy_location_counter += 1

                    # await observer.do(self.current_scout.move(observer.enemy_start_locations[self.enemy_location_counter]))
