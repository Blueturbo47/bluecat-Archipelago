from __future__ import annotations

from typing import TYPE_CHECKING

from BaseClasses import Item, ItemClassification
from .data import DEFAULT_ITEM_CLASSIFICATIONS, ITEM_NAME_TO_ID, TPT2ItemData
from .en import TPT2ItemNames

if TYPE_CHECKING:
    from .world import TPT2World
    from .data import ROptionFilter

class TPT2Item(Item):
    game = "The Perfect Tower 2"

def get_random_filler_item_name(world: TPT2World) -> str:
    return TPT2ItemNames.filler_doubleresources.value

def create_item_with_correct_classification(world: TPT2World, name: str) -> TPT2Item:
    classification = DEFAULT_ITEM_CLASSIFICATIONS[name]
    id = ITEM_NAME_TO_ID[name]
    return TPT2Item(name, classification, id, world.player)

def create_all_items(world: TPT2World) -> None:
    itempool:list[Item] = []

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
        for rule in genrules:
            if type(rule) == bool:
                genrules_bools.append(rule)
                continue
            else:
                resolution = rule.resolve(world)
                genrules_bools.append(resolution)
        return genrules_bools

    for itemdata in TPT2ItemData:
        itemname = TPT2ItemNames[itemdata.name].value
        itemnumber = itemdata.value.item_multiplier
        itemgenrules = itemdata.value.rules_generation
        

        if all(convertGenRules(itemgenrules)):
            for _ in range(itemnumber):
                generateditem = world.create_item(itemname)
                itempool.append(generateditem)


    # fill rest
    number_of_items = len(itempool)
    number_of_unfilled_locations = len(world.multiworld.get_unfilled_locations(world.player))
    needed_number_of_filler_items = number_of_unfilled_locations - number_of_items
    itempool += [world.create_filler() for _ in range(needed_number_of_filler_items)]

    # submit
    world.multiworld.itempool += itempool