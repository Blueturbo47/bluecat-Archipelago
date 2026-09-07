from collections.abc import Mapping
from typing import Any

from worlds.AutoWorld import World

# Imports of your world's files must be relative.
from . import items, locations, regions, rules
from . import options as dol_options  # rename due to a name conflict with World.options

from .regions import DolRegion_Names

class DoLWorld(World):
    """
    Degrees of Lewdity is a text-based RPG set inside of a town that holds many mysteries and people to engage with.
    This is a NSFW game and should not be included where participants of the multiworld do not understand the content that this game includes.
    """

    # The docstring should contain a description of the game, to be displayed on the WebHost.

    game = "Degrees of Lewdity"

    # # The WebWorld is a definition class that governs how this world will be displayed on the website.
    # web = web_world.APQuestWebWorld()

    options_dataclass = dol_options.DoLOptions
    options: dol_options.DoLOptions  #  This has to be a colon

    location_name_to_id = locations.LOCATION_NAME_TO_ID
    item_name_to_id = items.ITEM_NAME_TO_ID
    origin_region_name = DolRegion_Names.orphanage

    def randomize_start(self) -> None:
        # Starting region
        regionnum = self.options.randomize_start
        if regionnum == 1:
            regionnum = self.random.randint(2, 99)
        match(regionnum):
            case 0:  # option_dontRandomize
                self.origin_region_name = DolRegion_Names.orphanage
            case 2:  # danube_street
                self.origin_region_name = DolRegion_Names.danube_street
            case 3:  # barb_street
                self.origin_region_name = DolRegion_Names.barb_street
            case 4:  # domus_street
                self.origin_region_name = DolRegion_Names.domus_street
            case 5:  # starfish_street
                self.origin_region_name = DolRegion_Names.starfish_street
            case 6:  # cliff_street
                self.origin_region_name = DolRegion_Names.cliff_street
            case 7:  # high_street
                self.origin_region_name = DolRegion_Names.high_street
            case 8:  # nightingale_street
                self.origin_region_name = DolRegion_Names.nightingale_street
            case 9:  # wolf_street
                self.origin_region_name = DolRegion_Names.wolf_street
            case 10:  # connudatus_street
                self.origin_region_name = DolRegion_Names.connudatus_street
            case 11:  # oxford_street
                self.origin_region_name = DolRegion_Names.oxford_street
            case 12:  # harvest_street
                self.origin_region_name = DolRegion_Names.harvest_street
            case 13:  # mer_street
                self.origin_region_name = DolRegion_Names.mer_street
            case 14:  # elk_street
                self.origin_region_name = DolRegion_Names.elk_street
            case 15:  # orphanage
                self.origin_region_name = DolRegion_Names.orphanage

    def create_regions(self) -> None:
        regions.create_and_connect_regions(self)
        locations.create_all_locations(self)

    def set_rules(self) -> None:
        rules.set_all_rules(self)

    def create_items(self) -> None:
        items.create_all_items(self)

    def create_item(self, name: str) -> items.DoLWorld:
        return items.create_item_with_correct_classification(self, name)

    def get_filler_item_name(self) -> str:
        return items.get_random_filler_item_name(self)

    def fill_slot_data(self) -> Mapping[str, Any]:
        return self.options.as_dict(
            "",
        )
