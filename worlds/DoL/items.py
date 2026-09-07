from __future__ import annotations

from typing import TYPE_CHECKING

from BaseClasses import Item, ItemClassification

if TYPE_CHECKING:
    from .world import DoLWorld

ITEM_NAME_TO_ID = {
    # TODO: Add Checks
}

DEFAULT_ITEM_CLASSIFICATIONS = {
    "": ItemClassification.progression,
    "": ItemClassification.progression | ItemClassification.useful,
    "": ItemClassification.progression,
    "": ItemClassification.progression,
    "": ItemClassification.useful,
    "": ItemClassification.filler,
    "Force Combat Encounter Trap": ItemClassification.trap, # TBA
    "Force Stalk Encounter Trap": ItemClassification.trap, # TBA
    "Teleportion Trap": ItemClassification.trap, # TBA
}

class DoLItem(Item):
    game = "Degrees of Lewdity"


def get_random_filler_item_name(world: DoLWorld) -> str:
    if world.random.randint(0, 99) < world.options.trap_chance:
        return "" # TODO: replace with traps
    return "" # TODO: replace with money?


def create_item_with_correct_classification(world: DoLWorld, name: str) -> DoLItem:
    classification = DEFAULT_ITEM_CLASSIFICATIONS[name]
    return DoLItem(name, classification, ITEM_NAME_TO_ID[name], world.player)


def create_all_items(world: DoLWorld) -> None:

    itempool: list[Item] = [
        world.create_item(""),
        world.create_item(""),
        world.create_item(""),
        world.create_item(""),
        world.create_item(""),
    ]

    # itempool size example
    number_of_items = len(itempool)

    # unfilled locations example
    # Just calling len(world.get_locations()) would report an incorrect number, because of our *event locations*.
    number_of_unfilled_locations = len(world.multiworld.get_unfilled_locations(world.player))
    needed_number_of_filler_items = number_of_unfilled_locations - number_of_items
    itempool += [world.create_filler() for _ in range(needed_number_of_filler_items)]

    # submit our apworld items to the pool
    world.multiworld.itempool += itempool

    # # precollected item example via world.push_precollected().
    # if world.options.start_with_one_confetti_cannon:
    #     starting_confetti_cannon = world.create_item("Confetti Cannon")
    #     world.push_precollected(starting_confetti_cannon)
