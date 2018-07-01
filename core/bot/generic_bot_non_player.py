#!/usr/bin/env python
# -*- coding: utf-8 -*-

from sc2.ids.unit_typeid import UnitTypeId

from core.bot.generic_bot import GenericBot


class GenericBotNonPlayer(GenericBot):
    """ Generic bot non-player class, which cannot observer and operate the environment """

    def __init__(self, bot_player):
        """
        :param core.bot.generic_bot_player.GenericBotPlayer bot_player:
        """
        super(GenericBotNonPlayer, self).__init__(bot_player.race_type)
        self._bot_player = bot_player
        self._requests = list()

    @property
    def bot_player(self):
        """
        :return core.bot.generic_bot_player.GenericBotPlayer:
        """
        return self._bot_player

    @property
    def requests(self):
        """
        :return list[core.register_board.request.Request]
        """
        return self._requests

    def find_request(self):
        """ Implements the logic to find the requests that should be handled by the bot
        :return list[core.register_board.request.Request]
        """
        raise NotImplementedError

    async def requests_handler(self, iteration):
        """ Logic to go through the bot requests
        :param int iteration: Game loop iteration
        """
        raise NotImplementedError

    def requests_status_update(self):
        """ Logic to update the requests status """
        raise NotImplementedError

    async def default_behavior(self, iteration):
        """ The default behavior of the bot
        :param int iteration: Game loop iteration
        """
        await self.requests_handler(iteration)
        self.requests_status_update()

    def sync_requests(self):
        """ Update the requests that should be handled by the bot
        :return list[core.register_board.request.Request]
        """
        self._requests = self.find_request()

    def get_scvs_unit_from_bord_info(self):
        """
        :return list[sc2.unit.Unit]:
        """
        scvs = []

        for info in self.bot_player.board_info.board:
            scv = self.bot_player.get_current_scv_unit(info.unit_tag)

            if scv.type_id == UnitTypeId.SCV:
                scvs.append(scv)
        return scvs

    def find_available_scvs_units(self):
        """ Look for SCVs unit on board info that is not performing any request
        :return list[sc2.unit.Unit]:
        """
        available_scvs = None
        all_scvs = self.bot_player.workers[:]

        if not self.bot_player.board_info.board:
            available_scvs = all_scvs

        else:
            scvs_from_board_info = self.get_scvs_unit_from_bord_info()
            available_scvs = list(set(all_scvs) - set(scvs_from_board_info))

        return available_scvs
