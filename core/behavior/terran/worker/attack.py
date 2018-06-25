#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
Worker Rush Attack
"""


async def worker_rush_attack(iteration, observer):
    """ Send all workers to attack the enemy base
    :param int iteration:
    :param core.bot.generic_bot.GenericBot observer: The supreme manager observer for the hierarchy
    """
    observer.log("Iteration #{}. Starting Worker Rush Attack!".format(iteration))
    for worker in observer.workers:
        await observer.do(worker.attack(observer.enemy_start_locations[0]))
