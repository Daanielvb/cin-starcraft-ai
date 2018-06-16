#!/usr/bin/env python
# -*- coding: utf-8 -*-

from core.bot.terran.generic_terran_bot import GenericTerranBot


class SCV(GenericTerranBot):

    async def on_step(self, iteration):
        # TODO: Implement default behavior for SCV unit(s)

        # TODO: IDEA. PLEASE EVALUATE IT.
        # This aims to give to us a direct translation of our spreadsheet / doc with the planning,
        # where we wrote the "Decisions". "When" it would happen, "Who" will perform it and "What" would be
        # the conditions to this execution.
        #
        # Simplifying:
        # (1) Bot class are characters. They can have a method to set its behavior
        # (2) Observation class that would brings any environment information
        # (3) Step class that use this Observation class to decide when the logic will be performed
        #
        # Once we have all characters, observations and steps needed, we could have a Strategy class
        # For this level, Strategy will use more general Observations for long-term decision.
        # (1) Strategy class would holds Observation classes to verify the environment
        # (2) The "Strategy" in itself will be a step-by-step workflow counted by interactions to slice its progress
        # (2.1) e.g: Game starts. For interaction 0 to 200, the base should have 2 barracks...
        # (2.2) The code into Strategy will compile all needed steps to each this goal
        #
        # In a more upper level, we could have a Plan class, that will holds all chosen Strategies to handle
        # all situation described in our Spreadsheet / DOC.
        #
        # I just got this idea when I was writting this SCV code. I still do not know how to implement.
        # For this point point, I just know the sc2.bot_ai.BotAI class runs the on_step() for each interaction
        # Once our Bot class extends it, we can set and re-set this method with other methods (Python Rocks!)
        # To allow the Bot to changes its behavior depends on the Strategy given for a give Pla
        #
        # I am looking for a way to get the environment observation.
        # Once I found it, we can encapsulate all observations needed and all described above can be done
        # in a way that will be simple to split the code-writte work. Each of us could focus in a small peace
        # of the Plan (aka Strategy) and implement it. If the Strategy is complex, it could have as much as needed
        # minnor levels creating sub-classes of the Strategy, put everyone into a list and lets the API runs
        #
        pass
