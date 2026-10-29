from __future__ import annotations

from BaseClasses import Location, Region
from rule_builder.rules import And

from .data import DoLLocationData, DoLLocationNames, DoLOptionFilters, DoLRules, ROptionFilter

from typing import TYPE_CHECKING
if TYPE_CHECKING: from .world import DoLWorld

class DolWorldLocation(Location):
    game = "Degrees of Lewdity"

def create_all_locations(world: DoLWorld) -> None:
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

    failedantiques = 0

    # loc = {locationname : (location ID, [Location Regions], [Location Gen Rules], [Location Reach Rules])}
    for loc in DoLLocationData.__members__.values():
        locname = DoLLocationNames[loc.name].value
        locid = loc.value.location_id
        locregions = loc.value.locations
        locgenrules = loc.value.rules_generation
        locreachrules = loc.value.rules_obtain
        # print(f"\nAttempting generation for loc '{locname}'")

        # print(f"\tRules: {And(*[locrule.value for locrule in locreachrules]).to_dict()}")
        # NOTE: this print ^ is too large currently as certain feats (gwylan) rules are too large
        if not all(convertGenRules(locgenrules)):
            # print(f"{locname}'s genrules prevented gen: {loc.value.rules_generation}")
            # Reduce the ceiling on total antiques if one fails to generate
            if DoLOptionFilters.type_antiques.value in locgenrules: failedantiques += 1
            continue

        if len(locregions) > 1:
            regionname = f"{locname}: {[locarea for locarea in locregions]}"
            region = Region(regionname, world.player, world.multiworld)
            world.multiworld.regions.append(region)
            for locarea in locregions:
                world.get_region(locarea).connect(region)
        else: region = world.get_region(locregions[0])

        region.add_locations({locname: locid}, DolWorldLocation)
        newloc = world.get_location(locname)
        # print(f"Generated location '{newloc}' with rule '{"" if locrule == "" else locrule.value}'")
        for rule in locreachrules:
            # print(f"Set Rule '{rule.value}' : '{rule.value.__class__}'")
            world.set_rule(newloc, rule)

    # Fix world option if antiques set is higher than possible to generate
    world.options.completiongoal_antiques.value = min(world.options.completiongoal_antiques.range_end - failedantiques, world.options.completiongoal_antiques.value)