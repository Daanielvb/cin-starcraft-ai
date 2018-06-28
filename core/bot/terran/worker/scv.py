#!/usr/bin/env python
# -*- coding: utf-8 -*-

from core.bot.generic_bot_non_player import GenericBotNonPlayer


class SCV(GenericBotNonPlayer):
    """ A SCV bot class """

    async def default_behavior(self, iteration):
        """ The default behavior of the bot
        :param int iteration: Game loop iteration
        """
        await self.worker_rush_attack()

    async def worker_rush_attack(self):
        """ Send all workers to attack the enemy base """
        self.log("Starting Worker rush attack")
        for worker in self.bot_player.workers:
            await self.bot_player.do(worker.attack(self.bot_player.enemy_start_locations[0]))
