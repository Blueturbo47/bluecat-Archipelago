from __future__ import annotations

from typing import TYPE_CHECKING

from BaseClasses import ItemClassification, Location

from . import items

if TYPE_CHECKING:
    from .world import DoLWorld


LOCATION_NAME_TO_ID = { #example location and ids, remove later
    "": 1,
    "": 2,
    "": 3,
    "": 4,
    "": 5,
    "": 6,
    "": 10,
}

class DolWorldLocation(Location):
    game = "APQuest"


def get_location_names_with_ids(location_names: list[str]) -> dict[str, int | None]:
    return {location_name: LOCATION_NAME_TO_ID[location_name] for location_name in location_names}


def create_all_locations(world: DoLWorld) -> None:
    create_regular_locations(world)
    create_events(world)


def create_regular_locations(world: DoLWorld) -> None:
    # TODO: get regions list and add the locations
   print("todo create locations")


def create_events(world: DoLWorld) -> None:
    print("todo create events")