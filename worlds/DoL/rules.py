from __future__ import annotations

from typing import TYPE_CHECKING
from enum import Enum
from rule_builder.options import OptionFilter
from rule_builder.rules import Has, HasAll, Rule

if TYPE_CHECKING:
    from .world import DoLWorld

class default_rules(Enum):
    skulduggery_1 = Has("skul", 1) # TODO: fill out rules, fix this rule

def set_all_rules(world: DoLWorld) -> None:
    set_all_entrance_rules(world)
    set_all_location_rules(world)
    set_completion_condition(world)

def set_all_entrance_rules(world: DoLWorld) -> None:
    print("do rules") # TODO: entrance rules

def set_all_location_rules(world: DoLWorld) -> None:
    print("do rules") # TODO: location rules

def set_completion_condition(world: DoLWorld) -> None:
    print("do rules") # TODO: completion conditions