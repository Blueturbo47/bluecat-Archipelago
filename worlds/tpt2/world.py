from collections.abc import Mapping
from typing import Any

from worlds.AutoWorld import World
from .data import TPT2ItemData, TPT2LocationData, TPT2OptionFilters, TPT2TypeNames
from .en import TPT2ItemNames, TPT2LocationNames, TPT2RegionNames

from . import items, locations, regions, rules, web_world
from . import options as tpt2_options  # rename due to a name conflict with World.options

class TPT2World(World):
    """
    The Perfect Tower 2 is an incremental game with many smaller minigames, centered around
    building The Perfect Tower!
    """

    game = "The Perfect Tower 2"

    # The WebWorld is a definition class that governs how this world will be displayed on the website.
    # web = web_world.APQuestWebWorld()

    options_dataclass = tpt2_options.TPT2Options
    options: tpt2_options.TPT2Options  # This has to be a colon (:), not an equals sign (=).

    location_name_to_id = {TPT2LocationNames[loc.name].value: loc.value.location_id for loc in TPT2LocationData}
    item_name_to_id = items.ITEM_NAME_TO_ID
    base_id = 100
    origin_region_name = TPT2RegionNames.town.value

    item_name_groups = {
        TPT2TypeNames.module.value: {
            TPT2ItemNames[item.name].value for item in TPT2ItemData
            if (TPT2OptionFilters.type_module.value in item.value.rules_generation)
        }
    }
    

    def create_regions(self) -> None:
        regions.create_and_connect_regions(self)
        locations.create_all_locations(self)

    def set_rules(self) -> None:
        rules.set_all_rules(self)

    def create_items(self) -> None:
        items.create_all_items(self)

    def create_item(self, name: str) -> items.TPT2Item:
        return items.create_item_with_correct_classification(self, name)

    def get_filler_item_name(self) -> str:
        return items.get_random_filler_item_name(self)

    def fill_slot_data(self) -> Mapping[str, Any]:
        return self.options.as_dict(
            "randomization_targets"
        )
