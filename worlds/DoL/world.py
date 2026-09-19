from collections.abc import Mapping
from typing import Any

from worlds.AutoWorld import World

from . import items, locations, regions, rules
from . import options as dol_options

from .data import DoLRegionNames, DoLItemNames, DoLLocationTypes

class DoLWorld(World):
    """
    Degrees of Lewdity is a text-based RPG set inside of a town that holds many mysteries and people to engage with.
    This is a NSFW game and should not be included where participants of the multiworld do not understand the content that this game includes.
    """


    game = "Degrees of Lewdity"


    options_dataclass = dol_options.DoLOptions
    options: dol_options.DoLOptions  #  This has to be a colon

    location_name_to_id = {key.value: val_tuple[0] for key, val_tuple in locations.LOCATION_DATA.items()}
    item_name_to_id = {key.value: val for key, val in items.ITEM_NAME_TO_ID.items()}
    base_id = 100
    origin_region_name = DoLRegionNames.orphanage.value

    item_name_groups = {
        DoLLocationTypes.antique.value: {
            DoLItemNames.antique_ivorystatuette.value,    DoLItemNames.antique_silvercoin.value,        DoLItemNames.antique_silvercrown.value,
            DoLItemNames.antique_crystal.value,           DoLItemNames.antique_silverblade.value,       DoLItemNames.antique_coppercoin.value,
            DoLItemNames.antique_silvergoblet.value,      DoLItemNames.antique_fetish.value,            DoLItemNames.antique_goldcoin.value,
            DoLItemNames.antique_forestdagger.value,      DoLItemNames.antique_forestgem.value,         DoLItemNames.antique_arrow.value,
            DoLItemNames.antique_ivorynecklace.value,     DoLItemNames.antique_ivorybox.value,          DoLItemNames.antique_silverring.value,
            DoLItemNames.antique_goldnecklace.value,      DoLItemNames.antique_chastitybelt.value,      DoLItemNames.antique_stonetalisman.value,
            DoLItemNames.antique_horn.value,              DoLItemNames.antique_snuffer.value,           DoLItemNames.antique_bucket.value,
            DoLItemNames.antique_silvermanacle.value,     DoLItemNames.antique_whip.value,              DoLItemNames.antique_goldring.value,
            DoLItemNames.antique_bell.value,              DoLItemNames.antique_bullet.value,            DoLItemNames.antique_artilleryshell.value,
            DoLItemNames.antique_grenade.value,           DoLItemNames.antique_goldbrooch.value,        DoLItemNames.antique_silverbrooch.value,
            DoLItemNames.antique_islanderarrow.value,     DoLItemNames.antique_islandermask.value,      DoLItemNames.antique_obsidiandisc.value,
            DoLItemNames.antique_trilobitefossil.value,   DoLItemNames.antique_baileyminesign.value,    DoLItemNames.antique_incenseburner.value,
            DoLItemNames.antique_cup.value,               DoLItemNames.antique_silvermask.value,        DoLItemNames.antique_silveramulet.value,      
            DoLItemNames.antique_hourglass.value,         DoLItemNames.antique_swordcane.value,         DoLItemNames.antique_chocolate.value,         
            DoLItemNames.antique_teacaddy.value,          DoLItemNames.antique_woodenfigurine.value,    DoLItemNames.antique_copperring.value,        
            DoLItemNames.antique_goldcompass.value,       DoLItemNames.antique_coppercompass.value,     DoLItemNames.antique_coralring.value,
            DoLItemNames.antique_diamond.value,           DoLItemNames.antique_brassstatuette.value,    DoLItemNames.antique_golddagger.value,
            DoLItemNames.antique_goldamulet.value,        DoLItemNames.antique_goldmask.value,          DoLItemNames.antique_silvercompass.value,
            DoLItemNames.antique_leathermap.value,        DoLItemNames.antique_cutlass.value,           DoLItemNames.antique_silverdagger.value,
            DoLItemNames.antique_rustedcutlass.value,     DoLItemNames.antique_pinkcrystal.value,       DoLItemNames.antique_candlestick.value,
            DoLItemNames.antique_dildo.value,             DoLItemNames.antique_watch.value,
        },
    }

    def randomize_start(self) -> None:
        # Starting region
        regionnum = self.options.randomize_start
        randomizeablestarts = [
            DoLRegionNames.orphanage, DoLRegionNames.danube_street, DoLRegionNames.barb_street, 
            DoLRegionNames.domus_street, DoLRegionNames.starfish_street, DoLRegionNames.cliff_street, 
            DoLRegionNames.high_street, DoLRegionNames.nightingale_street, DoLRegionNames.wolf_street, 
            DoLRegionNames.connudatus_street, DoLRegionNames.oxford_street, DoLRegionNames.harvest_street, 
            DoLRegionNames.mer_street, DoLRegionNames.elk_street]
        if regionnum == 1:
            regionnum = self.random.randint(0, len(randomizeablestarts) - 1)
        elif regionnum != 0:
            regionnum -= 1
        self.origin_region_name = randomizeablestarts[regionnum].value
        

    def create_regions(self) -> None:
        regions.create_and_connect_regions(self)
        locations.create_all_locations(self)

    def set_rules(self) -> None:
        rules.set_all_rules(self)

    def create_items(self) -> None:
        # print(self.item_name_groups.keys())
        # print(f"Key '{DoLLocationTypes.antique.value}' == {self.item_name_groups[DoLLocationTypes.antique.value]}")
        items.create_all_items(self)

    def create_item(self, name: str) -> items.DoLItem:
        return items.create_item_with_correct_classification(self, name)

    def get_filler_item_name(self) -> str:
        return items.get_random_filler_item_name(self)

    def fill_slot_data(self) -> Mapping[str, Any]:
        return self.options.as_dict( # just add toggles here for now I guess?
            "tentacles", "pregnancy", "parasitic_pregnancy", 
            "animal_transformations", "divine_transformations", "bestiality", 
            "lactation", "softvore", "parasites", 
            "anal", "bodywriting",
        )
