from __future__ import annotations

from BaseClasses import Item, ItemClassification

from .data import DEFAULT_ITEM_CLASSIFICATIONS, ITEM_NAME_TO_ID, DoLLocationData, DoLLocationTypes, DoLLocationNames, DoLItemNames, DoLOptionFilters, DoLRules, DoLItemData, ROptionFilter

from typing import TYPE_CHECKING
if TYPE_CHECKING: from .world import DoLWorld


class DoLItem(Item):
    game = "Degrees of Lewdity"


def get_random_filler_item_name(world: DoLWorld) -> str:
    # if world.random.randint(0, 99) < world.options.trap_chance:
    #     return "" # TODO: replace with traps
    return DoLItemNames.money_100.value


def create_item_with_correct_classification(world: DoLWorld, name: str) -> DoLItem:
    classification = DEFAULT_ITEM_CLASSIFICATIONS[name]
    id = ITEM_NAME_TO_ID[name]
    #print(f"returning dolitem with {name}, {classification}, {id}")
    return DoLItem(name, classification, id, world.player)


def create_all_items(world: DoLWorld) -> None:
    itempool: list[Item] = []

    # NOTE: avoid creating locations with multiple
    # basic generation types (ex: skill and feat)
    # in order to not create errors with this code
    #
    # if needed, create a extra rule under a new name
    
    def convertGenRules(genrules:list[ROptionFilter]):
        """
        Converts list[ROptionFilter] to list[bool]
        """
        genrules_bools = []
        # print(f"Resolving rules {genrules}")
        for rule in genrules:
            if type(rule) == bool:
                genrules_bools.append(rule)
                continue
            else:
                resolution = rule.resolve(world)
                genrules_bools.append(resolution)
        return genrules_bools

    for itemdata in DoLItemData:
        # print(f"Attempting to generate item {itemdata.name}")
        itemname = DoLItemNames[itemdata.name].value
        itemnumber = itemdata.value.item_multiplier
        itemgenrules = itemdata.value.rules_generation
        

        if all(convertGenRules(itemgenrules)):
            # print(f"Generated Item {itemname}")
            # print(f"Gen Item {itemname}, {itemnumber}")
            for _ in range(itemnumber):
                generateditem = world.create_item(itemname)
                itempool.append(generateditem)
        # else: print(f"{itemname}'s genrule prevented gen: {itemgenrules}")
        
    # filling rest of items
    number_of_items = len(itempool)
    number_of_unfilled_locations = len(world.multiworld.get_unfilled_locations(world.player))
    needed_number_of_filler_items = number_of_unfilled_locations - number_of_items
    itempool += [world.create_filler() for _ in range(needed_number_of_filler_items)]

    # submit 
    # print(itempool)
    world.multiworld.itempool += itempool