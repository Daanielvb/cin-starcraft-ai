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
                # TODO: Daniel, remember to split the scout() into minor methods and call all these
                # minor methods into scout(). It will allow to trigger the scout() into 1 iteration
                await bot.default_behavior(iteration)
