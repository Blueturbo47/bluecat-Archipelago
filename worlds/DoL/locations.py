from __future__ import annotations
from enum import StrEnum

from typing import TYPE_CHECKING

from BaseClasses import ItemClassification, Location

from . import items

if TYPE_CHECKING:
    from .world import DoLWorld

class DoLLocationNames(StrEnum):
    # Antiques
        # Churchyard Catacombs
    antique_ivorystatuette = "antique Ivory Statuette : Churchyard"
    antique_silvercoin = "antique Silver Crown : Churchyard or Moor"
    antique_crystal = "antique Crystal : Churchyard"
    antique_silverblade = "antique Silver Blade : Churchyard"
    antique_coppercoin = "antique Copper Coin : Churchyard"
    antique_silvergoblet = "antique Silver Goblet : Churchyard"
    antique_fetish = "antique Fetish : Churchyard"
    antique_goldcoin = "antique Gold Coin : Churchyard"

        # Forest
    antique_forestdagger = "antique Dagger : Forest"
    antique_forestgem = "antique Forest Gem : Forest"
    antique_arrow = "antique Arrow : Forest"

        # Lake
    antique_ivorynecklace = "antique Ivory Necklace : Lake"
    antique_ivorybox = "antique Ivory Box : Lake"
    antique_silverring = "antique Silver Ring : Lake"
    antique_goldnecklace = "antique Gold Necklace : Lake"
    antique_chastitybelt = "antique Chastity Belt : Lake"

        # Meadow
    antique_stonetalisman = "antique Stone Talisman : Meadow"

        # Maze
    antique_horn = "antique Horn : Maze or Sewers"
    antique_snuffer = "antique Snuffer : Maze"
    antique_bucket = "antique Bucket : Maze"
    antique_silvermanacle = "antique Silver Manacle : Maze"
    antique_whip = "antique Whip : Maze"

        # Moor
    antique_goldring = "antique Gold Ring : Moor"
    # antique_silvercoin = "" also found in churchyard
    antique_bell = "antique Bell : Moor"
    antique_bullet = "antique Bullet : Moor or Great Hawk"
    antique_artilleryshell = "antique Artillery Shell : Moor"

        # Riding School
    antique_grenade = "antique Grenade : Riding School"

        # Dance School
    antique_goldbrooch = "antique Gold Brooch : Dance School"

        # Orphanage
    antique_silverbrooch = "antique Silver Brooch : Orphange"

        # Island
    antique_islanderarrow = "antique Islander Arrow : Island"
    antique_islandermask = "antique Islander Mask : Island"
    antique_obsidiandisc = "antique Obsidian Disc : Island"
    antique_trilobitefossil = "antique Trilobite Fossil : Island"

        # Landfill
    antique_baileyminesign = "antique Bailey Mine Sign : Landfill"
    antique_incenseburner = "antique Incense Burner : Landfill"
    antique_cup = "antique Cup : Landfill"

        # Museum
    antique_silvermask = "antique Silver Mask : Museum"

        # Bird Tower
    # antique_bullet = "" also found in moor

        # Manors
    antique_silveramulet = "antique Silver Amulet : Manors"

        # Compound
    antique_hourglass = "antique Hourglass : Compound"

        # Pirate Ship
    antique_swordcane = "antique Sword Cane : Pirate Ship"
    antique_chocolate = "antique Chocolate : Pirate Ship"
    antique_teacaddy = "antique Tea Caddy : Pirate Ship"
    antique_woodenfigurine = "antique Wooden Figurine : Pirate Ship"
    antique_copperring = "antique Copper Ring : Pirate Ship"
    antique_goldcompass = "antique Gold Compass : Pirate Ship"

        # Ocean
    antique_coppercompass = "antique Copper Compass : Ocean"
    antique_coralring = "antique Coral Ring : Ocean"
    antique_diamond = "antique Diamond : Ocean"

        # Temple
    antique_brassstatuette = "antique Brass Statuette : Temple"

        # Avery Mansion
    antique_golddagger = "antique Gold Dagger : Avery's Mansion"
    antique_goldamulet = "antique Gold Amulet : Avery's Mansion"
    antique_goldmask = "antique Gold Mask : Avery's Mansion"

        # Beach Cave
    antique_silvercompass = "antique Silver Compass : Beach Cave"
    antique_leathermap = "antique Leather Map : Beach Cave"
    antique_cutlass = "antique Cutlass : Beach Cave"
    antique_silverdagger = "antique Silver Dagger : Beach Cave"
    antique_rustedcutlass = "antique Rusted Cutlass : Beach Cave"

        # Sewers
    antique_pinkcrystal = "antique Pink Crystal : Sewers"
    antique_candlestick = "antique Candlestick : Sewers"
    antique_dildo = "antique Dildo : Sewers"
    # antique_horn = "" also found in maze
    antique_watch = "antique Watch : Sewers"
    
    

    

LOCATION_NAME_TO_ID = {
    # Antiques
    DoLLocationNames.antique_ivorystatuette: 100,
    DoLLocationNames.antique_silvercoin: 101,
    DoLLocationNames.antique_crystal: 102,
    DoLLocationNames.antique_silverblade: 103,
    DoLLocationNames.antique_coppercoin: 104,
    DoLLocationNames.antique_silvergoblet: 105,
    DoLLocationNames.antique_fetish: 106,
    DoLLocationNames.antique_goldcoin: 107,
    DoLLocationNames.antique_forestdagger: 108,
    DoLLocationNames.antique_forestgem: 109,
    DoLLocationNames.antique_arrow: 110,
    DoLLocationNames.antique_ivorynecklace: 111,
    DoLLocationNames.antique_ivorybox: 112,
    DoLLocationNames.antique_silverring: 113,
    DoLLocationNames.antique_goldnecklace: 114,
    DoLLocationNames.antique_chastitybelt: 115,
    DoLLocationNames.antique_stonetalisman: 116,
    DoLLocationNames.antique_horn: 117,
    DoLLocationNames.antique_snuffer: 118,
    DoLLocationNames.antique_bucket: 119,
    DoLLocationNames.antique_silvermanacle: 120,
    DoLLocationNames.antique_whip: 121,
    DoLLocationNames.antique_goldring: 122,
    DoLLocationNames.antique_bell: 123,
    DoLLocationNames.antique_bullet: 124,
    DoLLocationNames.antique_artilleryshell: 125,
    DoLLocationNames.antique_grenade: 126,
    DoLLocationNames.antique_goldbrooch: 127,
    DoLLocationNames.antique_silverbrooch: 128,
    DoLLocationNames.antique_islanderarrow: 129,
    DoLLocationNames.antique_islandermask: 130,
    DoLLocationNames.antique_obsidiandisc: 131,
    DoLLocationNames.antique_trilobitefossil: 132,
    DoLLocationNames.antique_baileyminesign: 133,
    DoLLocationNames.antique_incenseburner: 134,
    DoLLocationNames.antique_cup: 135,
    DoLLocationNames.antique_silvermask: 136,
    DoLLocationNames.antique_silveramulet: 137,
    DoLLocationNames.antique_hourglass: 138,
    DoLLocationNames.antique_swordcane: 139,
    DoLLocationNames.antique_chocolate: 140,
    DoLLocationNames.antique_teacaddy: 141,
    DoLLocationNames.antique_woodenfigurine: 142,
    DoLLocationNames.antique_copperring: 143,
    DoLLocationNames.antique_goldcompass: 144,
    DoLLocationNames.antique_coppercompass: 145,
    DoLLocationNames.antique_coralring: 146,
    DoLLocationNames.antique_diamond: 147,
    DoLLocationNames.antique_brassstatuette: 148,
    DoLLocationNames.antique_golddagger: 149,
    DoLLocationNames.antique_goldamulet: 150,
    DoLLocationNames.antique_goldmask: 151,
    DoLLocationNames.antique_silvercompass: 152,
    DoLLocationNames.antique_leathermap: 153,
    DoLLocationNames.antique_cutlass: 154,
    DoLLocationNames.antique_silverdagger: 155,
    DoLLocationNames.antique_rustedcutlass: 156,
    DoLLocationNames.antique_pinkcrystal: 157,
    DoLLocationNames.antique_candlestick: 158,
    DoLLocationNames.antique_dildo: 159,
    DoLLocationNames.antique_watch: 160,
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