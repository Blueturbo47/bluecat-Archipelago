from __future__ import annotations
from enum import StrEnum, Enum

from typing import TYPE_CHECKING

from BaseClasses import ItemClassification, Location

from . import items
from .data import DoLRegion_Names

if TYPE_CHECKING:
    from .world import DoLWorld

class DoLLocationTypes(StrEnum):
    artifact = "Artifact"

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

LOCATION_DATA:dict[DoLLocationNames, tuple[int, DoLLocationTypes, list[DoLRegion_Names]]] = {
    # Antiques
    DoLLocationNames.antique_ivorystatuette: (100, DoLLocationTypes.artifact, [
                    DoLRegion_Names.temple
                ]),

    DoLLocationNames.antique_silvercoin: (101, DoLLocationTypes.artifact, [
                    DoLRegion_Names.temple,
                    DoLRegion_Names.moor
                ]),

    DoLLocationNames.antique_crystal: (102, DoLLocationTypes.artifact, [
                    DoLRegion_Names.temple
                ]),

    DoLLocationNames.antique_silverblade: (103, DoLLocationTypes.artifact, [
                    DoLRegion_Names.temple
                ]),

    DoLLocationNames.antique_coppercoin: (104, DoLLocationTypes.artifact, [
                    DoLRegion_Names.temple
                ]),

    DoLLocationNames.antique_silvergoblet: (105, DoLLocationTypes.artifact, [
                    DoLRegion_Names.temple
                ]),

    DoLLocationNames.antique_fetish: (106, DoLLocationTypes.artifact, [
                    DoLRegion_Names.temple
                ]),

    DoLLocationNames.antique_goldcoin: (107, DoLLocationTypes.artifact, [
                    DoLRegion_Names.temple
                ]),

    DoLLocationNames.antique_forestdagger: (108, DoLLocationTypes.artifact, [
                    DoLRegion_Names.forest
                ]),

    DoLLocationNames.antique_forestgem: (109, DoLLocationTypes.artifact, [
                    DoLRegion_Names.forest
                ]),

    DoLLocationNames.antique_arrow: (110, DoLLocationTypes.artifact, [
                    DoLRegion_Names.forest
                ]),

    DoLLocationNames.antique_ivorynecklace: (111, DoLLocationTypes.artifact, [
                    DoLRegion_Names.forest_lake
                ]),

    DoLLocationNames.antique_ivorybox: (112, DoLLocationTypes.artifact, [
                    DoLRegion_Names.forest_lake
                ]),

    DoLLocationNames.antique_silverring: (113, DoLLocationTypes.artifact, [
                    DoLRegion_Names.forest_lake
                ]),

    DoLLocationNames.antique_goldnecklace: (114, DoLLocationTypes.artifact, [
                    DoLRegion_Names.forest_lake
                ]),

    DoLLocationNames.antique_chastitybelt: (115, DoLLocationTypes.artifact, [
                    DoLRegion_Names.forest_lake
                ]),

    DoLLocationNames.antique_stonetalisman: (116, DoLLocationTypes.artifact, [
                    DoLRegion_Names.meadow
                ]),

    DoLLocationNames.antique_horn: (117, DoLLocationTypes.artifact, [
                    DoLRegion_Names.moor, # maze
                    DoLRegion_Names.residential_drain, # lower sewers 
                    DoLRegion_Names.commercial_drain, # TODO: replace with deep sewers location?
                    DoLRegion_Names.industrial_drain
                ]),

    DoLLocationNames.antique_snuffer: (118, DoLLocationTypes.artifact, [
                    DoLRegion_Names.moor, # maze
                ]),

    DoLLocationNames.antique_bucket: (119, DoLLocationTypes.artifact, [
                    DoLRegion_Names.moor, # maze
                ]),

    DoLLocationNames.antique_silvermanacle: (120, DoLLocationTypes.artifact, [
                    DoLRegion_Names.moor, # maze
                ]),

    DoLLocationNames.antique_whip: (121, DoLLocationTypes.artifact, [
                    DoLRegion_Names.moor, # maze
                ]),

    DoLLocationNames.antique_goldring: (122, DoLLocationTypes.artifact, [
                    DoLRegion_Names.moor
                ]),

    DoLLocationNames.antique_bell: (123, DoLLocationTypes.artifact, [
                    DoLRegion_Names.moor
                ]),

    DoLLocationNames.antique_bullet: (124, DoLLocationTypes.artifact, [
                    DoLRegion_Names.moor,
                    DoLRegion_Names.bird_tower
                ]),

    DoLLocationNames.antique_artilleryshell: (125, DoLLocationTypes.artifact, [
                    DoLRegion_Names.moor
                ]),

    DoLLocationNames.antique_grenade: (126, DoLLocationTypes.artifact, [
                    DoLRegion_Names.riding_school
                ]),

    DoLLocationNames.antique_goldbrooch: (127, DoLLocationTypes.artifact, [
                    DoLRegion_Names.dance_studio
                ]),

    DoLLocationNames.antique_silverbrooch: (128, DoLLocationTypes.artifact, [
                    DoLRegion_Names.orphanage
                ]),

    DoLLocationNames.antique_islanderarrow: (129, DoLLocationTypes.artifact, [
                    DoLRegion_Names.island
                ]),

    DoLLocationNames.antique_islandermask: (130, DoLLocationTypes.artifact, [
                    DoLRegion_Names.island
                ]),

    DoLLocationNames.antique_obsidiandisc: (131, DoLLocationTypes.artifact, [
                    DoLRegion_Names.island
                ]),

    DoLLocationNames.antique_trilobitefossil: (132, DoLLocationTypes.artifact, [
                    DoLRegion_Names.island
                ]),

    DoLLocationNames.antique_baileyminesign: (133, DoLLocationTypes.artifact, [
                    DoLRegion_Names.landfill
                ]),

    DoLLocationNames.antique_incenseburner: (134, DoLLocationTypes.artifact, [
                    DoLRegion_Names.landfill
                ]),

    DoLLocationNames.antique_cup: (135, DoLLocationTypes.artifact, [
                    DoLRegion_Names.landfill
                ]),

    DoLLocationNames.antique_silvermask: (136, DoLLocationTypes.artifact, [
                    DoLRegion_Names.manors
                ]),

    DoLLocationNames.antique_silveramulet: (137, DoLLocationTypes.artifact, [
                    DoLRegion_Names.compound
                ]),

    DoLLocationNames.antique_hourglass: (138, DoLLocationTypes.artifact, [
                    DoLRegion_Names.pirate_ship
                ]),

    DoLLocationNames.antique_swordcane: (139, DoLLocationTypes.artifact, [
                    DoLRegion_Names.pirate_ship
                ]),

    DoLLocationNames.antique_chocolate: (140, DoLLocationTypes.artifact, [
                    DoLRegion_Names.pirate_ship
                ]),

    DoLLocationNames.antique_teacaddy: (141, DoLLocationTypes.artifact, [
                    DoLRegion_Names.pirate_ship
                ]),

    DoLLocationNames.antique_woodenfigurine: (142, DoLLocationTypes.artifact, [
                    DoLRegion_Names.pirate_ship
                ]),

    DoLLocationNames.antique_copperring: (143, DoLLocationTypes.artifact, [
                    DoLRegion_Names.pirate_ship
                ]),

    DoLLocationNames.antique_goldcompass: (144, DoLLocationTypes.artifact, [
                    DoLRegion_Names.pirate_ship
                ]),

    DoLLocationNames.antique_coppercompass: (145, DoLLocationTypes.artifact, [
                    DoLRegion_Names.ocean
                ]),

    DoLLocationNames.antique_coralring: (146, DoLLocationTypes.artifact, [
                    DoLRegion_Names.ocean
                ]),

    DoLLocationNames.antique_diamond: (147, DoLLocationTypes.artifact, [
                    DoLRegion_Names.ocean
                ]),

    DoLLocationNames.antique_brassstatuette: (148, DoLLocationTypes.artifact, [
                    DoLRegion_Names.temple
                ]),

    DoLLocationNames.antique_golddagger: (149, DoLLocationTypes.artifact, [
                    DoLRegion_Names.avery_mansion
                ]),

    DoLLocationNames.antique_goldamulet: (150, DoLLocationTypes.artifact, [
                    DoLRegion_Names.avery_mansion
                ]),

    DoLLocationNames.antique_goldmask: (151, DoLLocationTypes.artifact, [
                    DoLRegion_Names.avery_mansion
                ]),

    DoLLocationNames.antique_silvercompass: (152, DoLLocationTypes.artifact, [
                    DoLRegion_Names.beach
                ]),

    DoLLocationNames.antique_leathermap: (153, DoLLocationTypes.artifact, [
                    DoLRegion_Names.beach
                ]),

    DoLLocationNames.antique_cutlass: (154, DoLLocationTypes.artifact, [
                    DoLRegion_Names.beach
                ]),

    DoLLocationNames.antique_silverdagger: (155, DoLLocationTypes.artifact, [
                    DoLRegion_Names.beach
                ]),

    DoLLocationNames.antique_rustedcutlass: (156, DoLLocationTypes.artifact, [
                    DoLRegion_Names.beach
                ]),

    DoLLocationNames.antique_pinkcrystal: (157, DoLLocationTypes.artifact, [
                    DoLRegion_Names.commercial_drain,
                    DoLRegion_Names.industrial_drain, # TODO: replace with deep sewers location?
                    DoLRegion_Names.residential_drain,
                ]),

    DoLLocationNames.antique_candlestick: (158, DoLLocationTypes.artifact, [
                    DoLRegion_Names.commercial_drain,
                    DoLRegion_Names.industrial_drain, # TODO: replace with deep sewers location?
                    DoLRegion_Names.residential_drain,
                ]),

    DoLLocationNames.antique_dildo: (159, DoLLocationTypes.artifact, [
                    DoLRegion_Names.commercial_drain,
                    DoLRegion_Names.industrial_drain, # TODO: replace with deep sewers location?
                    DoLRegion_Names.residential_drain,
                ]),

    DoLLocationNames.antique_watch: (160, DoLLocationTypes.artifact, [
                    DoLRegion_Names.commercial_drain,
                    DoLRegion_Names.industrial_drain, # TODO: replace with deep sewers location?
                    DoLRegion_Names.residential_drain,
                ]),

}


class DolWorldLocation(Location):
    game = "APQuest"

def create_all_locations(world: DoLWorld) -> None:
    create_regular_locations(world)
    create_events(world)

# def location_logic()


# based on the location type we need to
# check if that location type is banned
# if not go through every region in the location
# add the location id

def create_regular_locations(world: DoLWorld) -> None:
    LOCATION_TYPE_DATA = {
        DoLLocationTypes.artifact: world.options.randomize_artifacts
    }

    # i = {locationname : (locationid, locationtype, [locationregions])}
    for locname in LOCATION_DATA:
        loctuple = LOCATION_DATA[locname]
        locid = loctuple[0]
        loctype = loctuple[1]
        locregions = loctuple[2]
        # cross reference the locationtype via locationtypedata to the world option
        # so if the world option dictates we can disable a location type
        option = LOCATION_TYPE_DATA[loctype]
        if option:
            # for regionname in locregions:
            region = world.get_region(locregions[0]) # TODO: make this work for different locations, discord said something about events, else a new region
            region.add_locations({locname: locid}, DolWorldLocation)



def create_events(world: DoLWorld) -> None:
    danube = world.get_region(DoLRegion_Names.danube_street)
    danube.add_event("testevent", "victory", location_type=DolWorldLocation, item_type=items.DoLItem)
    # TODO: create events