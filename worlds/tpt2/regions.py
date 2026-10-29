from __future__ import annotations
from .en import TPT2RegionNames

from BaseClasses import Entrance, MultiWorld, Region

from typing import TYPE_CHECKING
if TYPE_CHECKING:
    from .world import TPT2World


def create_and_connect_regions(world: TPT2World) -> None:
    player = world.player
    multiworld = world.multiworld

    class TPT2Region(Region):
        player = world.player
        multiworld = world.multiworld

        def __init__(self, name: str, hint: str | None = None):
            super().__init__(name, player, multiworld, hint)

    town = TPT2Region(TPT2RegionNames.town.value)

    multiworld.regions.append(town)
