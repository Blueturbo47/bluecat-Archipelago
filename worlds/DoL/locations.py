from __future__ import annotations
from enum import StrEnum, Enum

from typing import TYPE_CHECKING

from BaseClasses import Location
from Options import Option

from . import items
from .data import DoLRegionNames, DoLLocationTypes, DoLLocationNames, LOCATION_DATA, LOCATION_RULES

if TYPE_CHECKING:
    from .world import DoLWorld

class DolWorldLocation(Location):
    game = "Degrees of Lewdity"

def create_all_locations(world: DoLWorld) -> None:
    create_regular_locations(world)
    create_events(world)


def create_regular_locations(world: DoLWorld) -> None:
    LOCATION_TYPE_DATA:dict[DoLLocationTypes, Option] = {
        DoLLocationTypes.antique: world.options.randomize_antiques,
        DoLLocationTypes.skill: world.options.randomize_skills
    }

    # i = {locationname : (locationid, locationtype, [locationregions])}
    for locname in LOCATION_DATA:
        loctuple = LOCATION_DATA[locname]
        locid = loctuple[0]
        loctype = loctuple[1]
        locregions = loctuple[2]
        if locname in LOCATION_RULES: locrule = LOCATION_RULES[locname]
        else: locrule = ""

        # cross reference the locationtype via locationtypedata to the world option
        # so if the world option dictates we can disable a location type
        option = LOCATION_TYPE_DATA[loctype]
        if option:
            # for regionname in locregions:
            region = world.get_region(locregions[0]) # TODO: make this work for different locations (discord said something about events, else a new region)
            region.add_locations({locname.value: locid}, DolWorldLocation)
            newloc = world.get_location(locname)
            print(f"Generated location '{newloc}' with rule '{"" if locrule == "" else locrule.value}'")
            if locrule != "":
                world.set_rule(newloc, locrule.value)



def create_events(world: DoLWorld) -> None:
    return
    # danube = world.get_region(DoLRegionNames.danube_street)
    #danube.add_event("testevent", "victory", location_type=DolWorldLocation, item_type=items.DoLItem)
    # TODO: create events