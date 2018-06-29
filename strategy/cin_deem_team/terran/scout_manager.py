#!/usr/bin/env python
# -*- coding: utf-8 -*-

from core.bot.generic_bot_non_player import GenericBotNonPlayer
from core.bot.terran.scout.scout import Scout


class ScoutManager(GenericBotNonPlayer):
    """ Scout manager class """

    def __init__(self, bot_player):
        """
        :param core.bot.generic_bot_player.GenericBotPlayer bot_player:
        """
        super(ScoutManager, self).__init__(bot_player)
        self.add_bot(Scout(bot_player))

    async def default_behavior(self, iteration):
        """ The default behavior of the bot
        :param int iteration: Game loop iteration
        """
        for bot in self.bots.values():
            if iteration == 0:
                bot.set_cmd_center()
                bot.set_scout()
            elif iteration == 1:
                await bot.visit_enemy()
            else:
                if bot.get_found_enemy_base():
                    if iteration % 30 == 0:
                        await bot.visit_middle()
                    elif iteration % 80 == 0:
                        await bot.visit_base()
                # TODO: Implement nearby friends logic and warn
                # elif bot.found_enemies_nearby():
                    # await bot.visit_base()
                else:
                    await bot.default_behavior(iteration)