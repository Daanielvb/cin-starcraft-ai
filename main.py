#!/usr/bin/env python
# -*- coding: utf-8 -*-

""" Entry point """

from sc2 import Race
from sc2 import player
from sc2 import run_game
from sc2 import maps as sc2_maps

from config import maps
from strategy.cin_deem_team.terran.human_god import HumanGod


if __name__ == '__main__':
    players = [
        # player.Human(Race.Zerg),
        HumanGod().build_bot_player(),
        HumanGod().build_bot_player()
    ]

    run_game(
        map_settings=sc2_maps.get(maps.MAP_SIMPLE64),
        players=players,
        realtime=False
    )
