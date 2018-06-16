#!/usr/bin/env python
# -*- coding: utf-8 -*-

from core.bot.terran.worker.scv import SCV


class WorkerRushBot(SCV):

    async def on_step(self, iteration):
        if iteration == 0:
            for worker in self.workers:
                await self.do(worker.attack(self.enemy_start_locations[0]))
