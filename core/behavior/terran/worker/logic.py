#!/usr/bin/env python
# -*- coding: utf-8 -*-

from sc2.ids.unit_typeid import UnitTypeId


async def scv_logic(obj, iteration, observer):
    """
    :param core.bot.terran.worker.scv.SCV obj:
    :param int iteration:
    :param core.bot.generic_bot.GenericBot observer: The supreme observer
    """
    obj.log("Starting SCV Logic!")
    if obj.supply_left < 5 and obj.supply_cap < 200 \
            and obj.can_afford(UnitTypeId.SUPPLYDEPOT) and not obj.already_pending(
        UnitTypeId.SUPPLYDEPOT):
        # FIXME: Bring the get_depot_build_location()
        #  precisa construir um Supply Depot
        build_location = await obj.get_depot_build_location()
        print(build_location)
        if build_location is not None:
            scv = obj.select_build_worker(build_location, True)
            await obj.do(scv.build(UnitTypeId.SUPPLYDEPOT, build_location))

    elif obj.units(UnitTypeId.REFINERY).amount < 2 and obj.can_afford(
            UnitTypeId.REFINERY) and not obj.already_pending(UnitTypeId.REFINERY):
        build_location = obj.state.vespene_geyser.closest_to(obj.start_location)
        if build_location is not None:
            scv = obj.select_build_worker(build_location, True)
            await obj.do(scv.build(UnitTypeId.REFINERY, build_location))

    elif obj.units(UnitTypeId.COMMANDCENTER).amount < 3 and obj.can_afford(
            UnitTypeId.COMMANDCENTER):
        # precisa criar outro Command Center
        await obj.expand_now()

    elif obj.units(UnitTypeId.BARRACKS).amount < 2 and obj.can_afford(UnitTypeId.BARRACKS):
        # FIXME: Bring the get_depot_build_location()
        build_location = await obj.get_depot_build_location()
        if build_location is not None:
            scv = obj.select_build_worker(build_location, True)
            await obj.do(scv.build(UnitTypeId.BARRACKS, build_location))