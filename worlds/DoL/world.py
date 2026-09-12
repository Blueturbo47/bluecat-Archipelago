from collections.abc import Mapping
from typing import Any

from worlds.AutoWorld import World

from . import items, locations, regions, rules
from . import options as dol_options

from .data import DoLRegion_Names

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

    location_name_to_id = {key.value: val_tuple[0] for key, val_tuple in locations.LOCATION_DATA.items()}
    item_name_to_id = {key.value: val for key, val in items.ITEM_NAME_TO_ID.items()}
    origin_region_name = DoLRegion_Names.orphanage

    def randomize_start(self) -> None:
        # Starting region
        regionnum = self.options.randomize_start
        randomizeablestarts = [
            DoLRegion_Names.orphanage, DoLRegion_Names.danube_street, DoLRegion_Names.barb_street, 
            DoLRegion_Names.domus_street, DoLRegion_Names.starfish_street, DoLRegion_Names.cliff_street, 
            DoLRegion_Names.high_street, DoLRegion_Names.nightingale_street, DoLRegion_Names.wolf_street, 
            DoLRegion_Names.connudatus_street, DoLRegion_Names.oxford_street, DoLRegion_Names.harvest_street, 
            DoLRegion_Names.mer_street, DoLRegion_Names.elk_street]
        if regionnum == 1:
            regionnum = self.random.randint(0, len(randomizeablestarts) - 1)
        elif regionnum != 0:
            regionnum -= 1
        self.origin_region_name = randomizeablestarts[regionnum]
        

    def create_regions(self) -> None:
        regions.create_and_connect_regions(self)
        locations.create_all_locations(self)

    def set_rules(self) -> None:
        rules.set_all_rules(self)

    def create_items(self) -> None:
        items.create_all_items(self)

    def create_item(self, name: str) -> items.DoLItem:
        return items.create_item_with_correct_classification(self, name)

    def get_filler_item_name(self) -> str:
        return items.get_random_filler_item_name(self)

    def fill_slot_data(self) -> Mapping[str, Any]:
        return self.options.as_dict( # just add toggles here for now I guess?
            "tentacles", "pregnancy", "parasitic_pregnancy", 
            "animal_transformations", "divine_transformations", "beastiality", 
            "lactation", "softvore", "parasites", 
            "anal", "bodywriting",
        )
