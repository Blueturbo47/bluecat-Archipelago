from collections.abc import Mapping
from typing import Any

from rule_builder.rules import HasGroupUnique
from worlds.AutoWorld import World

from . import items, locations, regions, options as dol_options

from .data import DoLOptionFilters, DoLRegionNames, DoLItemNames, DoLLocationTypes, DoLLocationData, DoLLocationNames, DoLRules, DoLItemData

class DoLWorld(World):
    """
    Degrees of Lewdity is a text-based RPG set inside of a town that holds many mysteries and people to engage with.
    This is a NSFW game and should not be included where participants of the multiworld do not understand the content that this game includes.
    """

    game = "Degrees of Lewdity"


    options_dataclass = dol_options.DoLOptions
    options: dol_options.DoLOptions  #  This has to be a colon

    location_name_to_id = {DoLLocationNames[loc.name].value: loc.value.location_id for loc in DoLLocationData}
    item_name_to_id = items.ITEM_NAME_TO_ID
    base_id = 100
    origin_region_name = DoLRegionNames.orphanage.value

    item_name_groups = {
        DoLLocationTypes.antique.value: {
            DoLItemNames[item.name].value for item in DoLItemData 
            if (DoLOptionFilters.type_antiques.value in item.value.rules_generation)
        },

        DoLLocationTypes.skill.value: {
            DoLItemNames[item.name].value for item in DoLItemData 
            if (DoLOptionFilters.type_skills.value in item.value.rules_generation)
        },

        DoLLocationTypes.upgrade.value: {
            DoLItemNames[item.name].value for item in DoLItemData 
            if (DoLOptionFilters.type_upgrade.value in item.value.rules_generation)
        },

        DoLLocationTypes.transformation.value: {
            DoLItemNames[item.name].value for item in DoLItemData 
            if (DoLOptionFilters.type_transformation.value in item.value.rules_generation)
        }

        # feats are not included because they are pure locations
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
        # Rules done in regions and locations files
        
        # Completion
        
        self.set_completion_rule(HasGroupUnique(DoLLocationTypes.antique.value, self.options.completiongoal_antiques.value))
    
    def create_items(self) -> None:
        # print(self.item_name_groups)
        # print(f"Key '{DoLLocationTypes.antique.value}' == {self.item_name_groups[DoLLocationTypes.antique.value]}")
        items.create_all_items(self)

    def create_item(self, name: str) -> items.DoLItem:
        return items.create_item_with_correct_classification(self, name)

    def get_filler_item_name(self) -> str:
        return items.get_random_filler_item_name(self)

    def fill_slot_data(self) -> Mapping[str, Any]:
        return self.options.as_dict(
            "randomization_targets", "completiongoal", "completiongoal_antiques", "completiongoal_money"
        )
