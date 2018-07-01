#!/usr/bin/env python
# -*- coding: utf-8 -*-

from sc2.ids.unit_typeid import UnitTypeId

BUILD = 'BUILD'
TECHNOLOGY = 'TECHNOLOGY'
SUPPLY = 'SUPPLY'

DEPENDENCIES = {
    # ==================================== UNITIES ====================================
    UnitTypeId.SCV: {
        BUILD: [UnitTypeId.COMMANDCENTER],
        TECHNOLOGY: [],
        SUPPLY: 1
    },
    UnitTypeId.MARINE: {
        BUILD: [UnitTypeId.BARRACKS],
        TECHNOLOGY: [],
        SUPPLY: 2
    },
    UnitTypeId.MARAUDER: {
        BUILD: [UnitTypeId.BARRACKS],
        TECHNOLOGY: [],
        SUPPLY: 2
    },
    UnitTypeId.REAPER: {
        BUILD: [UnitTypeId.BARRACKS],
        TECHNOLOGY: [],
        SUPPLY: 1
    },
    UnitTypeId.GHOST: {
        BUILD: [UnitTypeId.BARRACKS],
        TECHNOLOGY: [],
        SUPPLY: 2
    },
    UnitTypeId.HELLION: {
        BUILD: [UnitTypeId.FACTORY],
        TECHNOLOGY: [],
        SUPPLY: 2
    },
    UnitTypeId.SIEGETANK: {
        BUILD: [UnitTypeId.FACTORY],
        TECHNOLOGY: [],
        SUPPLY: 3
    },
    UnitTypeId.THOR: {
        BUILD: [UnitTypeId.FACTORY],
        TECHNOLOGY: [],
        SUPPLY: 6
    },
    UnitTypeId.HELLBATACGLUESCREENDUMMY: {
        BUILD: [UnitTypeId.FACTORY],
        TECHNOLOGY: [],
        SUPPLY: 2
    },
    UnitTypeId.WIDOWMINE: {
        BUILD: [UnitTypeId.FACTORY],
        TECHNOLOGY: [],
        SUPPLY: 2
    },
    UnitTypeId.CYCLONE: {
        BUILD: [UnitTypeId.FACTORY],
        TECHNOLOGY: [],
        SUPPLY: 3
    },
    UnitTypeId.VIKINGSKY_UNIT: {
        BUILD: [UnitTypeId.STARPORT],
        TECHNOLOGY: [],
        SUPPLY: 2
    },
    UnitTypeId.MEDIVAC: {
        BUILD: [UnitTypeId.STARPORT],
        TECHNOLOGY: [],
        SUPPLY: 2
    },
    UnitTypeId.RAVEN: {
        BUILD: [UnitTypeId.STARPORT],
        TECHNOLOGY: [],
        SUPPLY: 2
    },
    UnitTypeId.BANSHEE: {
        BUILD: [UnitTypeId.STARPORT],
        TECHNOLOGY: [],
        SUPPLY: 3
    },
    UnitTypeId.BATTLECRUISER: {
        BUILD: [UnitTypeId.STARPORT],
        TECHNOLOGY: [],
        SUPPLY: 6
    },
    UnitTypeId.LIBERATOR: {
        BUILD: [UnitTypeId.STARPORT],
        TECHNOLOGY: [],
        SUPPLY: 3
    },

    # ==================================== BUILDS ====================================
    UnitTypeId.SUPPLYDEPOT: {
        BUILD: [],
        TECHNOLOGY: [],
        SUPPLY: 0
    },
    UnitTypeId.REFINERY: {
        BUILD: [],
        TECHNOLOGY: [],
        SUPPLY: 0
    },
    UnitTypeId.BARRACKS: {
        BUILD: [UnitTypeId.COMMANDCENTER],
        TECHNOLOGY: [],
        SUPPLY: 0
    },
    UnitTypeId.BARRACKSTECHLAB: {
        BUILD: [UnitTypeId.BARRACKS],
        TECHNOLOGY: [],
        SUPPLY: 0
    },
    UnitTypeId.ENGINEERINGBAY: {
        BUILD: [UnitTypeId.COMMANDCENTER],
        TECHNOLOGY: [],
        SUPPLY: 0
    },
    UnitTypeId.BUNKER: {
        BUILD: [UnitTypeId.BARRACKS],
        TECHNOLOGY: [],
        SUPPLY: 0
    },
    UnitTypeId.MISSILETURRET: {
        BUILD: [UnitTypeId.ENGINEERINGBAY],
        TECHNOLOGY: [],
        SUPPLY: 0
    },
    UnitTypeId.FACTORY: {
        BUILD: [UnitTypeId.BARRACKS],
        TECHNOLOGY: [],
        SUPPLY: 0
    },
    UnitTypeId.FACTORYTECHLAB: {
        BUILD: [UnitTypeId.FACTORY],
        TECHNOLOGY: [],
        SUPPLY: 0
    },
    UnitTypeId.ARMORY: {
        BUILD: [UnitTypeId.FACTORY],
        TECHNOLOGY: [],
        SUPPLY: 0
    },
    UnitTypeId.STARPORT: {
        BUILD: [UnitTypeId.FACTORY],
        TECHNOLOGY: [],
        SUPPLY: 0
    },
    UnitTypeId.STARPORTTECHLAB: {
        BUILD: [UnitTypeId.STARPORT],
        TECHNOLOGY: [],
        SUPPLY: 0
    },
    UnitTypeId.SCIENCEFACILITY: {
        BUILD: [UnitTypeId.STARPORT],
        TECHNOLOGY: [],
        SUPPLY: 0
    }
}
