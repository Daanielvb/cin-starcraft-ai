#!/usr/bin/env python
# -*- coding: utf-8 -*-

""" Entry point """

from sc2 import Race, Difficulty
from sc2 import player
from sc2 import run_game
from sc2 import maps as sc2_maps
from sc2.player import Computer

from config import maps
from strategy.cin_deem_team.terran.human_god import HumanGod


if __name__ == '__main__':
    players = [
        HumanGod().build_bot_player(),
        player.Computer(Race.Zerg, Difficulty.VeryEasy)
    ]

    run_game(
        map_settings=sc2_maps.get(maps.MAP_SIMPLE64),
        players=players,
        realtime=False
    )
