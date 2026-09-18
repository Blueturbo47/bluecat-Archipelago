from __future__ import annotations
from enum import Enum

from rule_builder.options import OptionFilter
from rule_builder.rules import Has, HasAll, Rule, CanReachRegion

from .options import *
from .data import DoLRegionNames, DoLRules

from typing import TYPE_CHECKING
if TYPE_CHECKING:
    from .world import DoLWorld
    

def set_all_rules(world: DoLWorld) -> None:
    set_all_entrance_rules(world)
    set_all_location_rules(world)
    set_completion_condition(world)

def set_all_entrance_rules(world: DoLWorld) -> None:
    return # rules done via regions.py

def set_all_location_rules(world: DoLWorld) -> None:
    return # rules done via locations.py

def set_completion_condition(world: DoLWorld) -> None:
    print("do compleition condition") # TODO: completion conditions