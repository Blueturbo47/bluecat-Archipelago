from __future__ import annotations
from enum import StrEnum

from BaseClasses import Item, ItemClassification

from .data import LOCATION_DATA, DoLLocationTypes, DoLItemNames

from typing import TYPE_CHECKING
if TYPE_CHECKING:
    from .world import DoLWorld


ITEM_NAME_TO_ID = {
    # items types are grouped in 500's starting 
    # from 100 to help organization

    # Misc
    DoLItemNames.money_100: 100,
    # Traps
    # DoLItemNames.trap: 300,

    # Skill Ranks
    DoLItemNames.progressive_skulduggery_rank: 500,
    DoLItemNames.progressive_dancing_rank: 501,
    DoLItemNames.progressive_swimming_rank: 502,
    DoLItemNames.progressive_athletics_rank: 503,
    DoLItemNames.progressive_tending_rank: 504,
    DoLItemNames.progressive_housekeeping_rank: 505,
    DoLItemNames.progressive_seduction_rank: 506,
    DoLItemNames.progressive_oral_rank: 507,
    DoLItemNames.progressive_chest_rank: 508,
    DoLItemNames.progressive_hands_rank: 509,
    DoLItemNames.progressive_buttocks_rank: 510,
    DoLItemNames.progressive_privates_rank: 511,
    DoLItemNames.progressive_anal_rank: 512,
    DoLItemNames.progressive_thighs_rank: 513,
    DoLItemNames.progressive_feet_rank: 514,
    DoLItemNames.progressive_science_rank: 515,
    DoLItemNames.progressive_math_rank: 516,
    DoLItemNames.progressive_english_rank: 517,
    DoLItemNames.progressive_history_rank: 518,
    DoLItemNames.progressive_willpower_rank: 519,
    DoLItemNames.progressive_physique_rank: 520,
    DoLItemNames.progressive_promiscuity_rank: 521,
    DoLItemNames.progressive_exhibitionism_rank: 522,
    DoLItemNames.progressive_deviancy_rank: 523,

    # Antiques
    DoLItemNames.antique_ivorystatuette: 1001,
    DoLItemNames.antique_silvercoin: 1002,
    DoLItemNames.antique_silvercrown: 1003,
    DoLItemNames.antique_crystal: 1004,
    DoLItemNames.antique_silverblade: 1005,
    DoLItemNames.antique_coppercoin: 1006,
    DoLItemNames.antique_silvergoblet: 1007,
    DoLItemNames.antique_fetish: 1008,
    DoLItemNames.antique_goldcoin: 1009,
    DoLItemNames.antique_forestdagger: 1010,
    DoLItemNames.antique_forestgem: 1011,
    DoLItemNames.antique_arrow: 1012,
    DoLItemNames.antique_ivorynecklace: 1013,
    DoLItemNames.antique_ivorybox: 1014,
    DoLItemNames.antique_silverring: 1015,
    DoLItemNames.antique_goldnecklace: 1016,
    DoLItemNames.antique_chastitybelt: 1017,
    DoLItemNames.antique_stonetalisman: 1018,
    DoLItemNames.antique_horn: 1019,
    DoLItemNames.antique_snuffer: 1020,
    DoLItemNames.antique_bucket: 1021,
    DoLItemNames.antique_silvermanacle: 1022,
    DoLItemNames.antique_whip: 1023,
    DoLItemNames.antique_goldring: 1024,
    DoLItemNames.antique_bell: 1025,
    DoLItemNames.antique_bullet: 1026,
    DoLItemNames.antique_artilleryshell: 1027,
    DoLItemNames.antique_grenade: 1028,
    DoLItemNames.antique_goldbrooch: 1029,
    DoLItemNames.antique_silverbrooch: 1030,
    DoLItemNames.antique_islanderarrow: 1031,
    DoLItemNames.antique_islandermask: 1032,
    DoLItemNames.antique_obsidiandisc: 1033,
    DoLItemNames.antique_trilobitefossil: 1034,
    DoLItemNames.antique_baileyminesign: 1035,
    DoLItemNames.antique_incenseburner: 1036,
    DoLItemNames.antique_cup: 1037,
    DoLItemNames.antique_silvermask: 1038,
    DoLItemNames.antique_bullet: 1039,
    DoLItemNames.antique_silveramulet: 1040,
    DoLItemNames.antique_hourglass: 1041,
    DoLItemNames.antique_swordcane: 1042,
    DoLItemNames.antique_chocolate: 1043,
    DoLItemNames.antique_teacaddy: 1044,
    DoLItemNames.antique_woodenfigurine: 1045,
    DoLItemNames.antique_copperring: 1046,
    DoLItemNames.antique_goldcompass: 1047,
    DoLItemNames.antique_coppercompass: 1048,
    DoLItemNames.antique_coralring: 1049,
    DoLItemNames.antique_diamond: 1050,
    DoLItemNames.antique_brassstatuette: 1051,
    DoLItemNames.antique_golddagger: 1052,
    DoLItemNames.antique_goldamulet: 1053,
    DoLItemNames.antique_goldmask: 1054,
    DoLItemNames.antique_silvercompass: 1055,
    DoLItemNames.antique_leathermap: 1056,
    DoLItemNames.antique_cutlass: 1057,
    DoLItemNames.antique_silverdagger: 1058,
    DoLItemNames.antique_rustedcutlass: 1059,
    DoLItemNames.antique_pinkcrystal: 1060,
    DoLItemNames.antique_candlestick: 1061,
    DoLItemNames.antique_dildo: 1062,
    DoLItemNames.antique_watch: 1063,

    
}

DEFAULT_ITEM_CLASSIFICATIONS = {
    #"": ItemClassification.progression | ItemClassification.useful,
    #"": ItemClassification.useful,
    #"": ItemClassification.filler,
    #"": ItemClassification.trap


    # Progression
    DoLItemNames.progressive_skulduggery_rank: ItemClassification.progression, 
    DoLItemNames.progressive_dancing_rank: ItemClassification.progression, 
    DoLItemNames.progressive_swimming_rank: ItemClassification.progression, 
    DoLItemNames.progressive_athletics_rank: ItemClassification.progression, 
    DoLItemNames.progressive_tending_rank: ItemClassification.progression, 
    DoLItemNames.progressive_housekeeping_rank: ItemClassification.progression, 
    DoLItemNames.progressive_seduction_rank: ItemClassification.progression, 
    DoLItemNames.progressive_oral_rank: ItemClassification.progression, 
    DoLItemNames.progressive_chest_rank: ItemClassification.progression, 
    DoLItemNames.progressive_hands_rank: ItemClassification.progression, 
    DoLItemNames.progressive_buttocks_rank: ItemClassification.progression, 
    DoLItemNames.progressive_privates_rank: ItemClassification.progression, 
    DoLItemNames.progressive_anal_rank: ItemClassification.progression, 
    DoLItemNames.progressive_thighs_rank: ItemClassification.progression, 
    DoLItemNames.progressive_feet_rank: ItemClassification.progression, 
    DoLItemNames.progressive_science_rank: ItemClassification.progression, 
    DoLItemNames.progressive_math_rank: ItemClassification.progression, 
    DoLItemNames.progressive_english_rank: ItemClassification.progression, 
    DoLItemNames.progressive_history_rank: ItemClassification.progression, 
    DoLItemNames.progressive_willpower_rank: ItemClassification.progression, 
    DoLItemNames.progressive_physique_rank: ItemClassification.progression, 
    DoLItemNames.progressive_promiscuity_rank: ItemClassification.progression, 
    DoLItemNames.progressive_exhibitionism_rank: ItemClassification.progression, 
    DoLItemNames.progressive_deviancy_rank: ItemClassification.progression, 


    # Useful

    # artifacts are useful because the silver mask artifact
    # requires 20 artifacts to get first
    DoLItemNames.antique_ivorystatuette: ItemClassification.useful | ItemClassification.progression,
    DoLItemNames.antique_silvercoin: ItemClassification.useful | ItemClassification.progression,
    DoLItemNames.antique_silvercrown: ItemClassification.useful | ItemClassification.progression,
    DoLItemNames.antique_crystal: ItemClassification.useful | ItemClassification.progression,
    DoLItemNames.antique_silverblade: ItemClassification.useful | ItemClassification.progression,
    DoLItemNames.antique_coppercoin: ItemClassification.useful | ItemClassification.progression,
    DoLItemNames.antique_silvergoblet: ItemClassification.useful | ItemClassification.progression,
    DoLItemNames.antique_fetish: ItemClassification.useful | ItemClassification.progression,
    DoLItemNames.antique_goldcoin: ItemClassification.useful | ItemClassification.progression,
    DoLItemNames.antique_forestdagger: ItemClassification.useful | ItemClassification.progression,
    DoLItemNames.antique_forestgem: ItemClassification.useful | ItemClassification.progression,
    DoLItemNames.antique_arrow: ItemClassification.useful | ItemClassification.progression,
    DoLItemNames.antique_ivorynecklace: ItemClassification.useful | ItemClassification.progression,
    DoLItemNames.antique_ivorybox: ItemClassification.useful | ItemClassification.progression,
    DoLItemNames.antique_silverring: ItemClassification.useful | ItemClassification.progression,
    DoLItemNames.antique_goldnecklace: ItemClassification.useful | ItemClassification.progression,
    DoLItemNames.antique_chastitybelt: ItemClassification.useful | ItemClassification.progression,
    DoLItemNames.antique_stonetalisman: ItemClassification.useful | ItemClassification.progression,
    DoLItemNames.antique_horn: ItemClassification.useful | ItemClassification.progression,
    DoLItemNames.antique_snuffer: ItemClassification.useful | ItemClassification.progression,
    DoLItemNames.antique_bucket: ItemClassification.useful | ItemClassification.progression,
    DoLItemNames.antique_silvermanacle: ItemClassification.useful | ItemClassification.progression,
    DoLItemNames.antique_whip: ItemClassification.useful | ItemClassification.progression,
    DoLItemNames.antique_goldring: ItemClassification.useful | ItemClassification.progression,
    DoLItemNames.antique_bell: ItemClassification.useful | ItemClassification.progression,
    DoLItemNames.antique_bullet: ItemClassification.useful | ItemClassification.progression,
    DoLItemNames.antique_artilleryshell: ItemClassification.useful | ItemClassification.progression,
    DoLItemNames.antique_grenade: ItemClassification.useful | ItemClassification.progression,
    DoLItemNames.antique_goldbrooch: ItemClassification.useful | ItemClassification.progression,
    DoLItemNames.antique_silverbrooch: ItemClassification.useful | ItemClassification.progression,
    DoLItemNames.antique_islanderarrow: ItemClassification.useful | ItemClassification.progression,
    DoLItemNames.antique_islandermask: ItemClassification.useful | ItemClassification.progression,
    DoLItemNames.antique_obsidiandisc: ItemClassification.useful | ItemClassification.progression,
    DoLItemNames.antique_trilobitefossil: ItemClassification.useful | ItemClassification.progression,
    DoLItemNames.antique_baileyminesign: ItemClassification.useful | ItemClassification.progression,
    DoLItemNames.antique_incenseburner: ItemClassification.useful | ItemClassification.progression,
    DoLItemNames.antique_cup: ItemClassification.useful | ItemClassification.progression,
    DoLItemNames.antique_silvermask: ItemClassification.useful | ItemClassification.progression,
    DoLItemNames.antique_bullet: ItemClassification.useful | ItemClassification.progression,
    DoLItemNames.antique_silveramulet: ItemClassification.useful | ItemClassification.progression,
    DoLItemNames.antique_hourglass: ItemClassification.useful | ItemClassification.progression,
    DoLItemNames.antique_swordcane: ItemClassification.useful | ItemClassification.progression,
    DoLItemNames.antique_chocolate: ItemClassification.useful | ItemClassification.progression,
    DoLItemNames.antique_teacaddy: ItemClassification.useful | ItemClassification.progression,
    DoLItemNames.antique_woodenfigurine: ItemClassification.useful | ItemClassification.progression,
    DoLItemNames.antique_copperring: ItemClassification.useful | ItemClassification.progression,
    DoLItemNames.antique_goldcompass: ItemClassification.useful | ItemClassification.progression,
    DoLItemNames.antique_coppercompass: ItemClassification.useful | ItemClassification.progression,
    DoLItemNames.antique_coralring: ItemClassification.useful | ItemClassification.progression,
    DoLItemNames.antique_diamond: ItemClassification.useful | ItemClassification.progression,
    DoLItemNames.antique_brassstatuette: ItemClassification.useful | ItemClassification.progression,
    DoLItemNames.antique_golddagger: ItemClassification.useful | ItemClassification.progression,
    DoLItemNames.antique_goldamulet: ItemClassification.useful | ItemClassification.progression,
    DoLItemNames.antique_goldmask: ItemClassification.useful | ItemClassification.progression,
    DoLItemNames.antique_silvercompass: ItemClassification.useful | ItemClassification.progression,
    DoLItemNames.antique_leathermap: ItemClassification.useful | ItemClassification.progression,
    DoLItemNames.antique_cutlass: ItemClassification.useful | ItemClassification.progression,
    DoLItemNames.antique_silverdagger: ItemClassification.useful | ItemClassification.progression,
    DoLItemNames.antique_rustedcutlass: ItemClassification.useful | ItemClassification.progression,
    DoLItemNames.antique_pinkcrystal: ItemClassification.useful | ItemClassification.progression,
    DoLItemNames.antique_candlestick: ItemClassification.useful | ItemClassification.progression,
    DoLItemNames.antique_dildo: ItemClassification.useful | ItemClassification.progression,
    DoLItemNames.antique_watch: ItemClassification.useful | ItemClassification.progression,


    # Filler
    DoLItemNames.money_100: ItemClassification.filler,


    # Trap
    #"Force Combat Encounter Trap": ItemClassification.trap, # TBA
    #"Force Stalk Encounter Trap": ItemClassification.trap, # TBA
    #"Teleportion Trap": ItemClassification.trap, # TBA
}


class DoLItem(Item):
    game = "Degrees of Lewdity"


def get_random_filler_item_name(world: DoLWorld) -> str:
    # if world.random.randint(0, 99) < world.options.trap_chance:
    #     return "" # TODO: replace with traps
    return DoLItemNames.money_100


def create_item_with_correct_classification(world: DoLWorld, name: str) -> DoLItem:
    classification = DEFAULT_ITEM_CLASSIFICATIONS[name]
    id = ITEM_NAME_TO_ID[name]
    #print(f"returning dolitem with {name}, {classification}, {id}")
    return DoLItem(name, classification, id, world.player)


def create_all_items(world: DoLWorld) -> None:
    itempool: list[Item] = []

    # create the items we want 1 to 1 with our locations
    # item should not be created unless we want it to
    testingvar = 0
    for i in LOCATION_DATA.items():
        locname = i[0].value
        loctype = i[1][1]
        
        # print(f"Attempting to generate {locname}")
        match(loctype):
            case(DoLLocationTypes.antique):
                if world.options.randomize_antiques:
                    print(f"Generating Artifact as Item with name '{locname[0:locname.find(":") - 1]}' type {locname.__class__}")
                    # remove the ' : location' so it equals the name of the item
                    item = world.create_item(locname[0:locname.find(":") - 1])

                    # testing stuff #TODO: uncomment
                    testingvar += 1
                    if testingvar <= 23: itempool.append(item)
                    # itempool.append(item)
            case(DoLLocationTypes.skill):
                if world.options.randomize_skills:
                    # remove the 'A+' from the rank and add progressive to the front
                    itempool.append(world.create_item(f"Progressive {locname[0:locname.find("Rank") + 4]}"))

    # filling rest of items
    number_of_items = len(itempool)
    number_of_unfilled_locations = len(world.multiworld.get_unfilled_locations(world.player))
    needed_number_of_filler_items = number_of_unfilled_locations - number_of_items
    itempool += [world.create_filler() for _ in range(needed_number_of_filler_items)]

    # submit 
    # print(itempool)
    world.multiworld.itempool += itempool