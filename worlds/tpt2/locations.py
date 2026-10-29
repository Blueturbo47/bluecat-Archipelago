from __future__ import annotations

from typing import TYPE_CHECKING

from BaseClasses import ItemClassification, Location, Region
from worlds.tpt2.en import TPT2LocationNames

from . import items
from .data import TPT2LocationData

if TYPE_CHECKING:
    from .world import TPT2World
    from .data import ROptionFilter

LOCATION_NAME_TO_ID = {}


class TPT2Location(Location):
    game = "The Perfect Tower 2"

def create_all_locations(world: TPT2World) -> None:
    def convertGenRules(genrules:list[ROptionFilter]):
        """
        Converts list[ROptionFilter] to list[bool]
        """
        genrules_bools = []
        # print(f"Resolving rules {genrules}")
        for rule in genrules:
            resolution = rule.resolve(world)
            genrules_bools.append(resolution)
        return genrules_bools

    for loc in TPT2LocationData.__members__.values():
        locname = TPT2LocationNames[loc.name].value
        locid = loc.value.location_id
        locregions = loc.value.locations
        locgenrules = loc.value.rules_generation
        locreachrules = loc.value.rules_obtain

        if not all(convertGenRules(locgenrules)):
            continue

        # Create mini-region that only has entrances
        # from each region designated from our location
        # if our location has multiple regions
        if len(locregions) > 1:
            regionname = f"{locname}: {[locarea for locarea in locregions]}"
            region = Region(regionname, world.player, world.multiworld)
            world.multiworld.regions.append(region)
            for locarea in locregions:
                world.get_region(locarea).connect(region)
        else: region = world.get_region(locregions[0])

        region.add_locations({locname: locid}, TPT2Location)
        newloc = world.get_location(locname)
        for rule in locreachrules: world.set_rule(newloc, rule)
