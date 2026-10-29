from __future__ import annotations
from collections import deque
import copy
import json
import time

from BaseClasses import Region
from rule_builder.rules import And
from worlds.Files import APAutoPatchInterface

from .en import ConnectionNotes, DoLRegionNames, OptionsLocalization
from .data import DoLOptionFilters, DoLRules

from typing import TYPE_CHECKING, Any, Literal
if TYPE_CHECKING: 
    from .world import DoLWorld
    from .en import _NoteDetail
    from rule_builder.rules import Rule
    from .data import ROptionFilter

def create_and_connect_regions(world:DoLWorld):
    player = world.player
    multiworld = world.multiworld
    options = world.options

    class AreaConnection:
        """
        Container for a connection. Takes this area this connection leads to and the list of rules it needs to connect. 

        Note on connection_type: This can be simiplified to just a bool, however its kept as 'exit', 'entrance', ''
        to make it easier to organize. Internally their regions are just seen as 'parent' and 'child, so the connections
        won't change depending on how its assigned. You shouldn't add both an entrance and exit of the same line
        to 2 regions however, as that would create duplicates

        To Simplify it:

        `oxfordstreet(AreaConnection(forestlake, connection_type="exit"))` = oxfordstreet -> forestlake
        `beach(AreaConnection(prison, connection_type="entrance"))` = prison -> beach

        However if you wanted to keep all connections to and from the prison, you could move it
        so its the other way around (swap beach, prison and change connection_type to exit)

        :param area: Area which this connection is bridging to
        :param rules: List of world Rules that this connection requires
        :param connection_type: (optional) 'exit' or 'entrance', exit would be where this region leads
        to, entrance would be where another region comes in from.
        :param note: Adds a note to connection, giving the user more info on the connection
        :param generation_rules: Rules that can stop a connection from generating
        """

        def __init__(self, area:Area, rules:list[Rule[Any]] | None = None, connection_type:Literal['entrance', 'exit', ''] | None = "", 
                            note:ConnectionNotes | None = None):
            self.initsubarea = area
            self.rules = rules if rules is not None else []
            self.connection_type:Literal['entrance', 'exit', ''] | None = connection_type
            self.note = note
            self.relationship:dict[str, Area]

        def program(self, parent):
            """
            Function that fleshes out this connection, to be called whenever
            a Area is init'd, extended, or appended to.

            This sets the parent region, outgoing region correctly based on 
            connection_type, to help with randomization and connection notes

            It will be called inside Area whenever extended, appended, or init'd, so
            no need to call this on your own, unless you want loose AreaConnections
            that aren't a part of an Area but still attached to one
            """
            match(self.connection_type):
                case("entrance"):
                    # Entrance:
                    # Init region (region passed to AreaConnection) has the exit
                    # to the parent region
                    self.relationship = {"parent": self.initsubarea, "child": parent}
                case _:
                    self.relationship = {"parent": parent, "child": self.initsubarea}


    class Area:
        """
        ### Description:
        
        This class contains takes a name of a region, and the regions it wishes to connect to via the AreaConnection class

        When making this class, you do have the option to add regions in the init, however it may be better
        to make the connections after init'ing all regions, so its easier to make and order connections
        
        ### Usage:
        
        To add to multiworld, when you make this Area class add it to a list, call connect() on every region, \
            then call add_to_multiworld() on every Area        
                
        :param StrEnum region_name: Name of the region, cross referenced to the StrEnum class for your world. \
            Example: regionnames.foo
        
        :param AreaList sub_regions: List of AreaConnection that will this region will connect to when running connect() \
            Example: `[AreaConnection(regionnames.bar), AreaConnection(regionnames.baz, rules.1)]`
        
        ### Functions:

        - append(): Adds an AreaConnection to the list of connections

        - extend(): Extends the list of connections with a list of AreaConnection

        - add_to_multiworld(): Adds the Region to the world. Run this before .connect()

        - connect(): Connects regions defined in sub_regions lists with this region. Run this to finalize the region after add_to_multiworld()

        - check_connection_similarity(): Checks if this Area connects to an Area other than itself
        """

        def __init__(self, region_name:DoLRegionNames, sub_regions:list[AreaConnection] | None = None):
            self.region_name = region_name
            self.sub_regions = sub_regions if sub_regions is not None else []
            for i in self.sub_regions: i.program(self)

            self.self_region = Region(self.region_name.value, player, multiworld)

        def add_to_multiworld(self):
            """
            Adds the region to the multiworld. 

            - Run this before running connect()
            """
            # print(f"Adding '{self.region_name}' with connections '{self.self_region.entrances}'")
            multiworld.regions.append(self.self_region)

        def connect(self):
            """
            Adds all connections to the Region for this Area. 
            
            Run this after running add_to_multiworld() and randomizing its pool if needed
            """
            for connection in self.sub_regions:
                self.designate_connections(connection)

        def designate_connections(self, connection:AreaConnection):
            """
            Add a connection to this Area's Region

            Ran by .connect()
            """

            def region_connect(parent:Region, child:Region, note:str, rules:list[Rule[Any]]):
                en = parent.connect(child, note, And(*rules))
                # Since the regions contain very few rules, this
                # isn't a huge issue to add indirect conditions
                # to every region with rules, however a better
                # implementation should be added later
                if len(rules) > 0: multiworld.register_indirect_condition(parent, en)


            if connection.note == None or isinstance(connection.note, str):
                connection_note = f"{connection.relationship['parent'].region_name} -> {connection.relationship['child'].region_name}"
                connection_note_flip = f"{connection.relationship['child'].region_name} -> {connection.relationship['parent'].region_name}"
            elif isinstance(connection.note.value, str):
                connection_note = f"{connection.relationship['parent'].region_name} -> {connection.relationship['child'].region_name} | {connection.note.value}"
                connection_note_flip = f"{connection.relationship['child'].region_name} -> {connection.relationship['parent'].region_name} | {connection.note.value}"
            else:
                connection_note = f"{connection.relationship['parent'].region_name} -> {connection.relationship['child'].region_name} | {connection.note.value.resolve()}"
                connection_note_flip = f"{connection.relationship['child'].region_name} -> {connection.relationship['parent'].region_name} | {connection.note.value.resolve(True)}"

            region_connect(
                connection.relationship['parent'].self_region,
                connection.relationship['child'].self_region,
                connection_note,
                connection.rules
            )
            if connection.connection_type not in {"entrance", "exit"}:
                region_connect( # Swap parent and child and connect if connection is twoway
                    connection.relationship['child'].self_region,
                    connection.relationship['parent'].self_region,
                    connection_note_flip,
                    connection.rules
                )

        def extend(self, connection_list:list[AreaConnection]):
            """
            Extends the connection list with list[AreaConnection]
            """
            # removelater = []
            # for connect in connection_list:
            #     removelater.append(connect.area.region_name)
            # print(f"{self.name()} got {removelater} connections")
            for i in connection_list: i.program(self)
            self.sub_regions.extend(connection_list)

        def append(self, connection:AreaConnection):
            """
            Adds to the connection list
            """
            # print(f"{self.name()} got {connection.area.region_name} connection")
            connection.program(self)
            self.sub_regions.append(connection)

        def check_connection_similarity(self):
            """
            Check if all connections are circular
            (all lead into the current region)

            returns True if there exists a connection that does
            not have None as an areaname and is not equal to this
            region's name

            otherwise returns False
            """
            for conn in self.sub_regions:
                match(conn.connection_type):
                    case("entrance"):
                        conntype = "parent"
                    case _:
                        conntype = "child"
                if ((conn.relationship[conntype].region_name != self.region_name) and 
                    (conn.relationship[conntype].region_name is not None)):
                    return True
            return False

    world_regions: list[Area] = []
    badends: list[Area] = []
    shops: list[Area] = []
    debug: list[Area] = []
    

    # Outside Town
        
    # forest_shop not a world region due to shop randomization
    shops.append(forest_shop := Area(DoLRegionNames.forest_shop))
    world_regions.append(forest_lake := Area(DoLRegionNames.forest_lake))
    world_regions.append(forest := Area(DoLRegionNames.forest))
    
    
    # Ocean
    world_regions.append(ocean := Area(DoLRegionNames.ocean))

    # Outskirts
    # Farmlands
        # Maze Key: long fighting event in a domus house knock encounter
    world_regions.append(maze := Area(DoLRegionNames.maze))
    world_regions.append(alex_farm := Area(DoLRegionNames.alex_farm))
    world_regions.append(riding_school := Area(DoLRegionNames.riding_school))
    world_regions.append(meadow := Area(DoLRegionNames.meadow))
    world_regions.append(manors := Area(DoLRegionNames.manors))
    world_regions.append(farmlands_road := Area(DoLRegionNames.farmlands_road))
    world_regions.append(farmlands := Area(DoLRegionNames.farmlands))

    # Moor
    world_regions.append(remy_estate := Area(DoLRegionNames.remy_estate))
    world_regions.append(moor := Area(DoLRegionNames.moor))
    world_regions.append(bog := Area(DoLRegionNames.bog))


    # Inside Town
    # Note: for every street, connections to other streets are not connected
    # this is because the walkable town randomization rule

    # Other
    world_regions.append(park := Area(DoLRegionNames.park))
    world_regions.append(beach := Area(DoLRegionNames.beach))
    # the area slice on beach includes every mini area on the waters around the beach
    # then if you go any further into the ocean, that counts as ocean


    # Drainage
    world_regions.append(old_sewers := Area(DoLRegionNames.old_sewers))
    world_regions.append(residential_drain := Area(DoLRegionNames.residential_drain))
    world_regions.append(commercial_drain := Area(DoLRegionNames.commercial_drain))
    world_regions.append(industrial_drain := Area(DoLRegionNames.industrial_drain))

    # Alleyways
    world_regions.append(residential_alleyways := Area(DoLRegionNames.residential_alleyways))
    world_regions.append(commercial_alleyways := Area(DoLRegionNames.commercial_alleyways))
    world_regions.append(industrial_alleyways := Area(DoLRegionNames.industrial_alleyways))


    # Residential
    # Danube Street
    world_regions.append(spa := Area(DoLRegionNames.spa))
    world_regions.append(avery_mansion := Area(DoLRegionNames.avery_mansion))
    world_regions.append(danube_houses := Area(DoLRegionNames.danube_houses))
    world_regions.append(danube_street := Area(DoLRegionNames.danube_street))


    # Barb Street
    # do not append to world regions because user might have disabled tentacles
    world_regions.append(hookah_parlour := Area(DoLRegionNames.hookah_parlour))
    world_regions.append(flats := Area(DoLRegionNames.flats))
    world_regions.append(dance_studio := Area(DoLRegionNames.dance_studio))
    world_regions.append(police_station := Area(DoLRegionNames.police_station))
    world_regions.append(barb_street := Area(DoLRegionNames.barb_street))


    # Domus Street  
    # NOTE: not connecting tentacle plains here due to randomization
    world_regions.append(orphanage := Area(DoLRegionNames.orphanage))
    world_regions.append(domus_houses := Area(DoLRegionNames.domus_houses))
    world_regions.append(domus_street := Area(DoLRegionNames.domus_street))

    # Commercial
    # Connudatus Street
    world_regions.append(strip_club := Area(DoLRegionNames.strip_club))
    world_regions.append(connudatus_street := Area(DoLRegionNames.connudatus_street))

    # Starfish Street
    world_regions.append(arcade := Area(DoLRegionNames.arcade))
    world_regions.append(chalets := Area(DoLRegionNames.chalets))
    world_regions.append(dog_pound := Area(DoLRegionNames.dog_pound))
    world_regions.append(starfish_street := Area(DoLRegionNames.starfish_street))


    # Cliff Street
    world_regions.append(mayors_office := Area(DoLRegionNames.mayors_office))
    world_regions.append(cafe := Area(DoLRegionNames.cafe))
    world_regions.append(cliff_street := Area(DoLRegionNames.cliff_street))


    # High Street
    world_regions.append(shopping_centre_rooftop := Area(DoLRegionNames.shopping_centre_rooftop))
    shops.append(shopping_centre_hairdressers := Area(DoLRegionNames.shopping_centre_hairdressers))
    shops.append(shopping_centre_petshop := Area(DoLRegionNames.shopping_centre_petshop))
    shops.append(shopping_centre_tattooparlour := Area(DoLRegionNames.shopping_centre_tattooparlour))
    shops.append(shopping_centre_furnitureshop := Area(DoLRegionNames.shopping_centre_furnitureshop))
    shops.append(shopping_centre_supermarket := Area(DoLRegionNames.shopping_centre_supermarket))
    shops.append(shopping_centre_clothingshop := Area(DoLRegionNames.shopping_centre_clothingshop))
    shops.append(shopping_centre_tailor := Area(DoLRegionNames.shopping_centre_tailor))
    shops.append(shopping_centre_cosmeticsshop := Area(DoLRegionNames.shopping_centre_cosmeticsshop))
    shops.append(shopping_centre_toystore := Area(DoLRegionNames.shopping_centre_toystore))
    world_regions.append(shopping_centre := Area(DoLRegionNames.shopping_centre))
    world_regions.append(office_building := Area(DoLRegionNames.office_building))
    world_regions.append(high_street := Area(DoLRegionNames.high_street))


    # Nightingale Street
    shops.append(pharmacy := Area(DoLRegionNames.pharmacy))
    world_regions.append(hospital := Area(DoLRegionNames.hospital))
    world_regions.append(photography_studio := Area(DoLRegionNames.photography_studio))
    world_regions.append(nightingale_street := Area(DoLRegionNames.nightingale_street))


    # Wolf Street
    world_regions.append(temple := Area(DoLRegionNames.temple))
    world_regions.append(soup_kitchen := Area(DoLRegionNames.soup_kitchen))
    world_regions.append(wolf_street := Area(DoLRegionNames.wolf_street))


    # Oxford Street
    world_regions.append(school := Area(DoLRegionNames.school))
    world_regions.append(museum := Area(DoLRegionNames.museum))
    world_regions.append(oxford_street := Area(DoLRegionNames.oxford_street))
    
    # Industrial
    # Harvest Street
    world_regions.append(brothel := Area(DoLRegionNames.brothel))
    world_regions.append(pub := Area(DoLRegionNames.pub))
    world_regions.append(bus_station := Area(DoLRegionNames.bus_station))
    world_regions.append(factory := Area(DoLRegionNames.factory))
    world_regions.append(harvest_street := Area(DoLRegionNames.harvest_street))

    # Mer Street
    world_regions.append(docks := Area(DoLRegionNames.docks))
    world_regions.append(coastal_path := Area(DoLRegionNames.coastal_path))
    world_regions.append(mer_street := Area(DoLRegionNames.mer_street))

    # Elk Street
    world_regions.append(landfill := Area(DoLRegionNames.landfill))
    world_regions.append(adult_shop := Area(DoLRegionNames.adult_shop))
    world_regions.append(compound := Area(DoLRegionNames.compound))
    world_regions.append(elk_street := Area(DoLRegionNames.elk_street))


    # -- Badends
    badends.append(prison := Area(DoLRegionNames.prison))
    badends.append(pirate_ship := Area(DoLRegionNames.pirate_ship))
    badends.append(island := Area(DoLRegionNames.island))
    badends.append(underground_brothel := Area(DoLRegionNames.underground_brothel))
    badends.append(asylum := Area(DoLRegionNames.asylum))
    badends.append(dog_pound_ending := Area(DoLRegionNames.dog_pound_ending))
    badends.append(mines := Area(DoLRegionNames.mines))
    badends.append(eden_cabin := Area(DoLRegionNames.eden_cabin))
    badends.append(kylar_manor := Area(DoLRegionNames.kylar_manor))
    badends.append(bird_tower := Area(DoLRegionNames.bird_tower))
    badends.append(remy_farm := Area(DoLRegionNames.remy_farm))
        
    wolf_cave = Area(DoLRegionNames.wolf_cave)
    if (OptionsLocalization.toggle_bestiality.value in options.gameworld_options or OptionsLocalization.toggle_monsterpeople.value in options.gameworld_options):
        badends.append(wolf_cave)


    # Tentacle Plains and Tentacle Forest
    tentacle_plains = Area(DoLRegionNames.tentacle_plains)
    tentacle_forest = Area(DoLRegionNames.tentacle_forest)


    # Debug
    # These regions are not regions that exist ingame but
    # are many connections that will not be randomized to ease connections
    debug.append(in_town := Area(DoLRegionNames.in_town))
    debug.append(events_street := Area(DoLRegionNames.events_street))
    debug.append(jail := Area(DoLRegionNames.jail))
    debug.append(ambulance := Area(DoLRegionNames.ambluance))
    debug.append(moneymaker := Area(DoLRegionNames.moneymaker))




    # -------- Region Connections  --------

    # -- Outside Town
    # danube, wolf, and nightingale street enter forest
    # don't connect forest shop here incase shop randomizer, we don't want the
    # connection to be inside the world_regions pool
    forest.append(
        AreaConnection(forest_lake, note=ConnectionNotes.forest_forestlake)
        # Entrance to bog
    )
    forest_shop.append(
        AreaConnection(forest, note=ConnectionNotes.forest_forestshop)
    )
    ocean.append(
        AreaConnection(beach, note=ConnectionNotes.beach_ocean)
    )
    
    # -- Outskirts
    # Farmlands
    farmlands.extend([
        AreaConnection(manors, note=ConnectionNotes.farmlands_manors), 
        AreaConnection(meadow, note=ConnectionNotes.farmlands_meadow), 
        AreaConnection(riding_school, note=ConnectionNotes.farmlands_ridingschool), 
        AreaConnection(alex_farm, note=ConnectionNotes.farmlands_alexfarm), 
        AreaConnection(farmlands_road, note=ConnectionNotes.farmlands_farmlandsroad),
        AreaConnection(maze, [DoLRules.has_mazekey.value], note=ConnectionNotes.farmlands_maze)
    ])

    # Moor
    # don't connect badends because badend rando rules
    moor.append(
        AreaConnection(remy_estate, 
                       [DoLRules.access_remyestate_rules.value], 
                       note=ConnectionNotes.moor_remyestate)
    )

    # -- Other Areas
    # bog connects forest to moor, but not back
    # moor to bog requires discovery in forest first

    # INFO Brook Access
    # Requires one of:
    # 1. historytrait gte 4, sciencetrait gte 2, tending gte 200
    # 2. Failing a swiming check in Forest Event River
    # 3. Talking to winter at the Lake Office
    #
    # Since 1 is a failable check, I'm going to code
    # being able to fail purposefully to get this, so only rules
    # will just be access forest (parent region, no rule)
    bog.extend([
        AreaConnection(moor, 
                       [DoLRules.access_forest.value], 
                       note=ConnectionNotes.bog_moor), 
        AreaConnection(forest, 
                       connection_type="entrance", 
                       note=ConnectionNotes.bog_forest)
    ])

    # Drainage
    old_sewers.append(
        AreaConnection(beach, note=ConnectionNotes.oldsewers_beach)
    )
    residential_drain.append(
        AreaConnection(old_sewers, note=ConnectionNotes.oldsewers_residentialdrain)
    )
    commercial_drain.extend([
        AreaConnection(residential_drain, note=ConnectionNotes.residentialdrain_commercialdrain),
        AreaConnection(old_sewers, note=ConnectionNotes.oldsewers_commercialdrain)
    ])
    industrial_drain.extend([
        AreaConnection(commercial_drain, note=ConnectionNotes.commercialdrain_industrialdrain),
        AreaConnection(old_sewers, note=ConnectionNotes.oldsewers_industrialdrain)
    ])

    # Alleyways
    residential_alleyways.append(
        AreaConnection(residential_drain, note=ConnectionNotes.residentialdrain_residentialalleyways)
    )
    commercial_alleyways.extend([
        AreaConnection(commercial_drain, note=ConnectionNotes.commercialdrain_commercialalleyways), 
        AreaConnection(residential_alleyways, note=ConnectionNotes.residentialalleyways_commercialalleyways),
        AreaConnection(park, note=ConnectionNotes.park_commercialalleyways)
    ])
    industrial_alleyways.extend([
        AreaConnection(industrial_drain, note=ConnectionNotes.industrialdrain_industrialalleyways), 
        AreaConnection(commercial_alleyways, note=ConnectionNotes.commercialalleyways_industrialalleyways),
        AreaConnection(park, note=ConnectionNotes.park_industrialalleyways)
    ])

    # -- Town
    # Danube Street
    # avery_mansion.extend() # TODO: links to this
    danube_street.extend([
        AreaConnection(spa, note=ConnectionNotes.danubestreet_spa), 
        AreaConnection(avery_mansion, 
                        [DoLRules.has_adoptionpapers.value, DoLRules.access_orphanage.value], 
                        note=ConnectionNotes.danubestreet_averymansion), 
        AreaConnection(danube_houses, note=ConnectionNotes.danubestreet_danubehouses), 
        AreaConnection(forest, note=ConnectionNotes.danubestreet_forest), 
        AreaConnection(residential_alleyways, note=ConnectionNotes.danubestreet_residentialalleyways), 
        AreaConnection(residential_drain, note=ConnectionNotes.danubestreet_residentialdrain)
    ])


    # Barb Street
    flats.append(
        AreaConnection(hookah_parlour, note=ConnectionNotes.flats_hookahparlour)
    )
    barb_street.extend([
        AreaConnection(dance_studio, note=ConnectionNotes.barbstreet_dancestudio), 
        AreaConnection(police_station, note=ConnectionNotes.barbstreet_policestation), 
        AreaConnection(flats, note=ConnectionNotes.barbstreet_flats), 
        AreaConnection(residential_alleyways, note=ConnectionNotes.barbstreet_residentialalleyway), 
        AreaConnection(residential_drain, note=ConnectionNotes.barbstreet_residentialdrain)
    ])


    # Domus Street
    orphanage.append(
        AreaConnection(residential_alleyways, note=ConnectionNotes.orphanage_residentialalleyways)
    )
    domus_street.extend([
        AreaConnection(orphanage, note=ConnectionNotes.domusstreet_orphanage), 
        AreaConnection(domus_houses, note=ConnectionNotes.domusstreet_domushouses), 
        AreaConnection(residential_alleyways, note=ConnectionNotes.domusstreet_residentialalleyways),
        AreaConnection(residential_drain, note=ConnectionNotes.domusstreet_residentialdrain)
    ])


    # Connudatus Street
    connudatus_street.extend([
        # Strip Club: no req since daytime no requirement
        AreaConnection(strip_club, note=ConnectionNotes.connudatusstreet_stripclub), 
        AreaConnection(commercial_drain, note=ConnectionNotes.connudatusstreet_commercialdrain), 
        AreaConnection(residential_alleyways, note=ConnectionNotes.connudatusstreet_residentialalleyways), 
        AreaConnection(commercial_alleyways, note=ConnectionNotes.connudatusstreet_commercialalleyways)
    ])


    # Starfish Street
    starfish_street.extend([
        AreaConnection(arcade, note=ConnectionNotes.starfishstreet_arcade), 
        AreaConnection(chalets, note=ConnectionNotes.starfishstreet_chalets), 
        AreaConnection(dog_pound, note=ConnectionNotes.starfishstreet_dogpound), 
        AreaConnection(beach, note=ConnectionNotes.starfishstreet_beach), 
        AreaConnection(park, note=ConnectionNotes.starfishstreet_park), 
        AreaConnection(commercial_drain, note=ConnectionNotes.starfishstreet_commercialdrain)
    ])


    # Cliff Street
    cliff_street.extend([
        AreaConnection(mayors_office, note=ConnectionNotes.cliffstreet_mayoroffice), 
        AreaConnection(cafe, note=ConnectionNotes.cliffstreet_cafe), 
        AreaConnection(beach, note=ConnectionNotes.cliffstreet_beach), 
        AreaConnection(commercial_drain, note=ConnectionNotes.cliffstreet_commercialdrain), 
        AreaConnection(commercial_alleyways, note=ConnectionNotes.cliffstreet_commercialalleyways)
    ])


    # High Street
    shopping_centre_rooftop.append(
        AreaConnection(commercial_alleyways, note=ConnectionNotes.shoppingcentrerooftop_ladder)
    )
    shopping_centre.append(
        AreaConnection(shopping_centre_rooftop, note=ConnectionNotes.shoppingcentre_rooftop)
    )
    # Connections inside shops because shop rando
    shopping_centre_hairdressers.append(AreaConnection(shopping_centre, note=ConnectionNotes.shoppingcentre_hairdressers))
    shopping_centre_petshop.append(AreaConnection(shopping_centre, note=ConnectionNotes.shoppingcentre_petshop))
    shopping_centre_tattooparlour.append(AreaConnection(shopping_centre, note=ConnectionNotes.shoppingcentre_tattooparlour))
    shopping_centre_furnitureshop.append(AreaConnection(shopping_centre, note=ConnectionNotes.shoppingcentre_furnitureshop))
    shopping_centre_supermarket.append(AreaConnection(shopping_centre, note=ConnectionNotes.shoppingcentre_supermarket))
    shopping_centre_clothingshop.append(AreaConnection(shopping_centre, note=ConnectionNotes.shoppingcentre_clothingshop))
    shopping_centre_tailor.append(AreaConnection(shopping_centre, note=ConnectionNotes.shoppingcentre_tailor))
    shopping_centre_cosmeticsshop.append(AreaConnection(shopping_centre, note=ConnectionNotes.shoppingcentre_cosmeticsshop))
    shopping_centre_toystore.append(AreaConnection(shopping_centre, note=ConnectionNotes.shoppingcentre_toystore))

    high_street.extend([
        AreaConnection(office_building, note=ConnectionNotes.highstreet_officebuilding), 
        AreaConnection(shopping_centre, note=ConnectionNotes.highstreet_shoppingcentre), 
        AreaConnection(park, note=ConnectionNotes.highstreet_park), 
        AreaConnection(commercial_drain, note=ConnectionNotes.highstreet_commercialdrain), 
        AreaConnection(commercial_alleyways, note=ConnectionNotes.highstreet_commercialalleyways)
    ])


    # Nightingale Street
    nightingale_street.extend([
        AreaConnection(hospital, note=ConnectionNotes.nightingalestreet_hospital), 
        # studio just requires 3000 total fame or doing chef stuff
        AreaConnection(photography_studio, note=ConnectionNotes.nightingalestreet_photographystudio), 
        AreaConnection(forest, note=ConnectionNotes.nightingalestreet_forest), 
        AreaConnection(park, note=ConnectionNotes.nightingalestreet_park), 
        AreaConnection(commercial_drain, note=ConnectionNotes.nightingalestreet_commercialdrain), 
        AreaConnection(commercial_alleyways, note=ConnectionNotes.nightingalestreet_commercialalleyways)
    ])
    # Connection inside pharmacy because shop rando
    pharmacy.append(AreaConnection(hospital, note=ConnectionNotes.hospital_pharmacy))


    # Wolf Street
    wolf_street.extend([
        AreaConnection(temple, note=ConnectionNotes.wolfstreet_temple), 
        AreaConnection(soup_kitchen, note=ConnectionNotes.wolfstreet_soupkitchen), 
        AreaConnection(forest, note=ConnectionNotes.wolfstreet_forest), 
        AreaConnection(commercial_drain, note=ConnectionNotes.wolfstreet_commercialdrain), 
        AreaConnection(commercial_alleyways, note=ConnectionNotes.wolfstreet_commercialalleyways)
    ])

    # Oxford Street
    school.extend([
        AreaConnection(park, [DoLRules.science_1.value], note=ConnectionNotes.school_park),
        AreaConnection(industrial_alleyways, note=ConnectionNotes.school_industrialalleyways), 
        AreaConnection(commercial_drain, 
                        [DoLRules.history_3.value],
                        note=ConnectionNotes.school_commercialdrain)
    ])
    oxford_street.extend([
        AreaConnection(school, note=ConnectionNotes.oxfordstreet_school), 
        AreaConnection(museum, note=ConnectionNotes.oxfordstreet_museum), 
        AreaConnection(commercial_alleyways, note=ConnectionNotes.oxfordstreet_commercialalleyways),
        AreaConnection(commercial_drain, note=ConnectionNotes.oxfordstreet_commercialdrain), 
        AreaConnection(industrial_alleyways, note=ConnectionNotes.oxfordstreet_industrialalleyways), 
        AreaConnection(park, note=ConnectionNotes.oxfordstreet_park),
        AreaConnection(forest_lake, 
                        connection_type="exit", 
                        note=ConnectionNotes.oxfordstreet_forestlake), # student walking to lake
        AreaConnection(orphanage, 
                        connection_type="exit",
                        note=ConnectionNotes.oxfordstreet_orphanage), # :: Robin Walk School 
    ])


    # Harvest Street
    # TODO: NOTE abnormal connection?
    pub.append(
        AreaConnection(forest, note=ConnectionNotes.pub_forest)
    )
    harvest_street.extend([
        AreaConnection(brothel, [DoLRules.access_brothel_rules.value], note=ConnectionNotes.harveststreet_brothel), 
        AreaConnection(pub, note=ConnectionNotes.harveststreet_pub), 
        AreaConnection(bus_station, note=ConnectionNotes.harveststreet_bustation), 
        AreaConnection(factory, note=ConnectionNotes.harveststreet_factory), 
        AreaConnection(industrial_drain, note=ConnectionNotes.harveststreet_industrialdrain), 
        AreaConnection(industrial_alleyways, note=ConnectionNotes.harveststreet_industrialalleyways),
        AreaConnection(farmlands_road, note=ConnectionNotes.harveststreet_farmlandsroad)
    ])

    # Mer Street
    docks.append(
        AreaConnection(beach, # the Docks part of the Beach, not technically ocean
                        [DoLRules.skulduggery_4.value], 
                        "exit",
                        ConnectionNotes.docks_beach)
    )
    coastal_path.append(
        AreaConnection(meadow,
                        [DoLRules.history_4.value], 
                        note=ConnectionNotes.costalpath_meadow)
    )
    mer_street.extend([
        # this is two-way because fishing can bring you to the waters sometimes
        AreaConnection(beach, note=ConnectionNotes.docks_beach),
        AreaConnection(docks, note=ConnectionNotes.merstreet_docks), 
        AreaConnection(coastal_path, 
                        [DoLRules.history_3.value],
                        note=ConnectionNotes.merstreet_costalpath), 
        AreaConnection(industrial_alleyways, note=ConnectionNotes.merstreet_industrialalleyways), 
        AreaConnection(industrial_drain, note=ConnectionNotes.merstreet_industrialdrain),
    ])

    # Elk Street
    elk_street.extend([
        AreaConnection(landfill, 
                        [DoLRules.access_landfill_rules.value], 
                        note=ConnectionNotes.elkstreet_landfill), 
        AreaConnection(adult_shop, note=ConnectionNotes.elkstreet_adultshop), # no rules (don't need to build it to go there)
        AreaConnection(compound, 
                        [DoLRules.access_compound_rules.value], 
                        note=ConnectionNotes.elkstreet_compound),
        AreaConnection(industrial_alleyways, note=ConnectionNotes.elkstreet_industrialalleyways), 
        AreaConnection(industrial_drain, note=ConnectionNotes.elkstreet_industrialdrain)
    ])


    # -- Bad Ends

    # prison: 1
    prison.extend([
        # Entrances
        AreaConnection(jail, connection_type="entrance", note=ConnectionNotes.police_prison), # :: Police Prison Intro
        
        # Exits
        AreaConnection(orphanage, connection_type="exit", note=ConnectionNotes.prison_orphanage), # :: Prison End Car Silent, Prison End Car Thank, Prison End Car Angry
        AreaConnection(docks, connection_type="exit", note=ConnectionNotes.prison_docks), # :: Prison Kylar Escape Ask, Prison Kylar Escape Nod, Prison Wren Escape 3
        # NOTE: 2 ocean connections, however one doesn't require swimming 10
        AreaConnection(ocean, [DoLRules.swimming_10.value], "exit", ConnectionNotes.prison_oceanswim), # :: Prison Escape
        AreaConnection(ocean, connection_type="exit", note=ConnectionNotes.prison_oceanpassout), # ::Passout Rut 2
        AreaConnection(beach, [DoLRules.tfrule_flight.value], "exit", ConnectionNotes.prison_beach), # :: Prison Soar Escape
    ])

    # pirate_ship: 2
    # exit to island is already an entrance from island, so it does not need to be included
    pirate_ship.extend([
        # Entrances
        AreaConnection(ocean, connection_type="entrance", note=ConnectionNotes.ocean_pirateship),  # :: Pirate Intro (Passout Pirates Hot Cold, Passout Pirate)
        AreaConnection(old_sewers, [DoLRules.access_temple.value], "entrance", ConnectionNotes.oldsewers_pirateship),  # :: Smuggler Pub Zephyr
    
        # Exits
        #AreaConnection(island, connection_type="exit", note="via: On the Pirate Ship, passout or become a mate and asking Zephyr"), # :: Pirate Passout Wake, Pirate End Run, Pirate End Islanders
        AreaConnection(ocean, connection_type="exit", note=ConnectionNotes.pirateship_ocean), # :: Pirate Railing Dive Night, Pirate Railing Dive Day
        AreaConnection(mer_street, connection_type="exit", note=ConnectionNotes.pirateship_merstreet) # :: Pirate Return
    ])

    # island: 3
    island.extend([
        # Entrances
        AreaConnection(pirate_ship, connection_type="entrance", note=ConnectionNotes.pirateship_island), # :: Pirate Passout Wake, Pirate End Run, Pirate End Islanders))
    
        # Exits
        AreaConnection(pirate_ship, connection_type="exit", note=ConnectionNotes.island_pirateship), # :: Islander End Hand
        AreaConnection(mer_street, connection_type="exit", note=ConnectionNotes.island_merstreet), # :: Island Sail
        AreaConnection(ocean, connection_type="exit", note=ConnectionNotes.island_ocean), # :: Islander End Swim, Islander End Throw, Islander Enforce (req: Angel tf)
    ])

    # underground_brothel: 4
    # entrances:
    # :: Underground Intro
    # :: Briar Hack Fail can be included but can become impossible,
    #    just make sure to send this passage / add purpose fail
    # TODO: CODE add this entrance and recode to allow fail
    underground_brothel.extend([
        # Entrances
        AreaConnection(orphanage, connection_type="entrance", note=ConnectionNotes.bailey_undergroundbrothel), # :: Rent Intro ($rentsale)
        AreaConnection(hospital, connection_type="entrance", note=ConnectionNotes.police_undergroundbrothel), # :: Hospital Arrest Molestation Finish
    
        # Exits
        AreaConnection(ocean, connection_type="exit", note=ConnectionNotes.undergroundbrothel_ocean), # :: Underground Lake
        AreaConnection(forest, connection_type="exit", note=ConnectionNotes.undergroundbrothel_forest) # :: Underground Presentation Molestation Finish, Underground Hunt, Underground Cell Sneak, widget "undergroundEscapeForestStart"
    ])

    # asylum: 5
    # faints can lead to hospital leading to asylum
    asylum.extend([
        # Entrances
        AreaConnection(hospital, connection_type="entrance", note=ConnectionNotes.harper_asylum), # :: Asylum Intro
    
        # Exits
        AreaConnection(forest, connection_type="exit", note=ConnectionNotes.asylum_forest), # :: Asylum Escape, Tentacle Escape, Tentacle Wolf Escape, Eden Asylum Rescue
        AreaConnection(orphanage, connection_type="exit", note=ConnectionNotes.asylum_orphanage), # :: Asylum Return, Pregnancy Birth Asylum End (req: preg), Tentacle Plains Resist
    ])

    # dog_pound_ending: 6
    # require wolf TF for Pound Abduction
    dog_pound_ending.extend([
        # Entrances
        AreaConnection(dog_pound, connection_type="entrance", note=ConnectionNotes.dogpound_dogpoundbadend),  # :: Pound Assault Caught
    
        # Exits
        AreaConnection(starfish_street, connection_type="exit", note=ConnectionNotes.dogpoundbadend_starfishstreet), # :: Pound Escape Front, Pound Escape Free Dress, Pound Escape Free No Dress
    ])
    # Extra Entrance
    if OptionsLocalization.toggle_animaltransformations.value in options.randomization_target_requirements:
        dog_pound_ending.append(AreaConnection(in_town, [DoLRules.tfrule_wolf_full_appear.value], "entrance", ConnectionNotes.wolfabudction_dogpoundbadend))


    # mines: 7
    mines.extend([
        # Entrances
        AreaConnection(flats, connection_type="entrance", note=ConnectionNotes.flats_mines), # :: Flats Auction 8
    
        # Exits
        AreaConnection(residential_drain, connection_type="exit", note=ConnectionNotes.mines_residentialdrain), # :: Mines Guards Escape, Mines Passout Warn 3, Mines Passout Run 2
        AreaConnection(flats, connection_type="exit", note=ConnectionNotes.mines_flats) # :: Mines Escape
    ])

    # eden_cabin: 8
    eden_cabin.extend([
        # Entrances
        AreaConnection(forest, connection_type="entrance", note=ConnectionNotes.eden_edencabin), # :: Forest Hunter Molestation Finish
        AreaConnection(orphanage, connection_type="entrance", note=ConnectionNotes.bailey_edencabin),  # :: rentsale ($rentsale 1) via widget"rentEdenTrade"
    
        # Exits
        AreaConnection(forest, connection_type="exit", note=ConnectionNotes.edencabin_forest) # :: Cabin Night Escape, Eden Cabin Escape, widget"clearingactions" above Eden Cabin Escape
    ])

    # kylar_manor: 9
    # entrance: requires meeting kylar so school required
    # exit:
    # NOTE: Kylar Abduction Stockholm End (one time event) leads to the park
    # TODO: CODE abnormal exit ^
    # :: Kylar Abduction Release 4, Kylar Abduction Free Rescue [Thank, Angry, Silent, Reassure, Mock], Kylar Abduction Free Leave 2
    kylar_manor.extend([
        # Entrances
        AreaConnection(school, connection_type="entrance", note=ConnectionNotes.kylar_kylarmanor), # :: Kylar Abduction Intro via widget"kylarwatched"
    
        # Exits
        AreaConnection(danube_street, connection_type="exit", note=ConnectionNotes.kylarmanor_danubestreet) 
    ])

    # bird_tower: 10
    # (leaving -> "castle" -> moor), Bird Tower [Farmlands, Forest, Town]
    bird_tower.extend([
        # Entrances
        AreaConnection(moor, connection_type="entrance", note=ConnectionNotes.greathawk_birdtower), # :: Bird Capture, Moor Bird Wake
    
        # Exits
        AreaConnection(farmlands, [DoLRules.tfrule_flight.value], "exit", note=ConnectionNotes.birdtower_farmlands), # :: Bird Tower Farmlands
        AreaConnection(moor, connection_type="exit", note=ConnectionNotes.birdtower_moor) # :: Bird Tower Rope Escape, Bird Tower Base Leave, Bird Tower Glide ['', 2]
    ])

    # remy_farm: 11
    # TODO: CODE remy_farm entrances go through '::Street Van Journey'
    # NOTE: all entrances lead to Livestock Intro, however badendtracking starts beforehand on passages below,
    # meaning badendtracking for this may have to be redone and placed in livestock intro
    #
    # Street Van Journey -> Street Van Fight Finish / Street Van Submit -> Livestock Intro
    #
    # CHEAT REQUIREMENT, do not include: bus station -> Street Van Journey
    #
    # eden escape -> eden cabin possible, but requires access to eden regardless
    # (plus would be weird to randomize)
    remy_farm.extend([
        # Entrances
        AreaConnection(orphanage, connection_type="entrance", note=ConnectionNotes.bailey_remyfarm),  # :: Street Van Bailey
        AreaConnection(moor, connection_type="entrance", note=ConnectionNotes.moor_remyfarm),       # :: Moor Abduction Remy Wake
        AreaConnection(remy_estate, connection_type="entrance", note=ConnectionNotes.remyestate_remyfarm),  # :: Passout Estate Remy Hot Cold, widget"blackjackCaughtCheatingSurrender"
        AreaConnection(cliff_street, [DoLRules.access_cafe.value], "entrance", ConnectionNotes.cliffstreet_remyfarm),  # :: Chef Blackmail Livestock 2
        AreaConnection(pub, connection_type="entrance", note=ConnectionNotes.pub_remyfarm), # :: Pub White Pill Van
        AreaConnection(in_town, connection_type="entrance", note=ConnectionNotes.intown_remyfarm), # TODO: this entrance
    
        # Exits
        AreaConnection(forest, connection_type="exit", note=ConnectionNotes.remyfarm_forest) # all lead to :: Livestock Escape Town
    ])

    # wolf_cave: 12
    if (OptionsLocalization.toggle_bestiality.value in options.gameworld_options or OptionsLocalization.toggle_monsterpeople.value in options.gameworld_options):
        wolf_cave.append(
            AreaConnection(forest, connection_type="entrance", note=ConnectionNotes.forest_wolfcave) # :: Forest Wolf Cave Intro
        )

    # -- Tentacle Plains/Forest
    # if disabled tentacle plains will just not have connections to/from
    if OptionsLocalization.animal_tentacles.value in options.gameanimal_options:
        # NOTE: we don't want logic to think orphanage -> tentacle plains -> asylum is possible
        # so tentacle plains are enter only
        tentacle_plains.extend([
            AreaConnection(asylum, connection_type="entrance", note=ConnectionNotes.asylum_tentacleplains),
            AreaConnection(orphanage, [DoLRules.deviancy_5.value], "entrance", ConnectionNotes.orphanage_tentacleplains)
        ])
        tentacle_forest.append(AreaConnection(hookah_parlour, note=ConnectionNotes.hookahparlour_tentacleforest))

    # Any place that can exist in town, and therefore
    # gets events that would happen on a town street
    in_town.extend([
        AreaConnection(danube_street, connection_type="entrance", note=ConnectionNotes.note_town),
        AreaConnection(barb_street, connection_type="entrance", note=ConnectionNotes.note_town),
        AreaConnection(domus_street, connection_type="entrance", note=ConnectionNotes.note_town),
        AreaConnection(starfish_street, connection_type="entrance", note=ConnectionNotes.note_town),
        AreaConnection(cliff_street, connection_type="entrance", note=ConnectionNotes.note_town),
        AreaConnection(high_street, connection_type="entrance", note=ConnectionNotes.note_town),
        AreaConnection(nightingale_street, connection_type="entrance", note=ConnectionNotes.note_town),
        AreaConnection(wolf_street, connection_type="entrance", note=ConnectionNotes.note_town),
        AreaConnection(connudatus_street, connection_type="entrance", note=ConnectionNotes.note_town),
        AreaConnection(oxford_street, connection_type="entrance", note=ConnectionNotes.note_town),
        AreaConnection(harvest_street, connection_type="entrance", note=ConnectionNotes.note_town),
        AreaConnection(mer_street, connection_type="entrance", note=ConnectionNotes.note_town),
        AreaConnection(elk_street, connection_type="entrance", note=ConnectionNotes.note_town),
    ])

    # the <<eventsstreet>> macro
    events_street.extend([
        AreaConnection(in_town, connection_type="entrance", note=ConnectionNotes.note_eventsstreet),
        AreaConnection(residential_alleyways, connection_type="entrance", note=ConnectionNotes.note_eventsstreet),
        AreaConnection(commercial_alleyways, connection_type="entrance", note=ConnectionNotes.note_eventsstreet),
        AreaConnection(industrial_alleyways, connection_type="entrance", note=ConnectionNotes.note_eventsstreet),
        AreaConnection(park, connection_type="entrance", note=ConnectionNotes.note_eventsstreet),
    ])

    # Fainting Connections via <<ambluance>>
    ambulance.extend([
        AreaConnection(pub, connection_type="entrance"),                            # like every town passout
        AreaConnection(bog, connection_type="entrance"),                            # passout bog
        AreaConnection(forest, connection_type="entrance"),                         # churchyard, forest : passoutcatacombs, passoutforest
        AreaConnection(forest_lake, connection_type="entrance"),                    # passoutlake
        AreaConnection(farmlands_road, connection_type="entrance"),                 # passoutfarmroad
        AreaConnection(moor, connection_type="entrance"),                           # passout_moor
        AreaConnection(residential_alleyways, connection_type="entrance"),          # start - passoutalley
        AreaConnection(commercial_alleyways, connection_type="entrance"),
        AreaConnection(industrial_alleyways, connection_type="entrance"),
        AreaConnection(shopping_centre_rooftop, connection_type="entrance"),        # end - passoutalley
        AreaConnection(arcade, connection_type="entrance"),                         # passoutarcade
        AreaConnection(beach, connection_type="entrance"),                          # passoutbeach, passoutcave
        AreaConnection(docks, connection_type="entrance"),                          # event or straight to ambulance
        AreaConnection(flats, connection_type="entrance"),                          # passout_flats
        AreaConnection(office_building, connection_type="entrance"),                # officepassout
        AreaConnection(park, connection_type="entrance"),                           # passoutpark
        AreaConnection(school, connection_type="entrance"),                         # straight to ambluance or school passout to ambluance
        AreaConnection(ocean, connection_type="entrance"),                          # passoutsea
        AreaConnection(brothel, connection_type="entrance"),                        # start - passout shop
        AreaConnection(cafe, connection_type="entrance"),
        AreaConnection(dance_studio, connection_type="entrance"),
        AreaConnection(dog_pound, connection_type="entrance"),
        AreaConnection(strip_club, connection_type="entrance"),
        AreaConnection(spa, connection_type="entrance"),
        AreaConnection(shopping_centre_hairdressers, connection_type="entrance"),
        AreaConnection(shopping_centre_petshop, connection_type="entrance"),
        AreaConnection(shopping_centre_tattooparlour, connection_type="entrance"),
        AreaConnection(shopping_centre_furnitureshop, connection_type="entrance"),
        AreaConnection(shopping_centre_supermarket, connection_type="entrance"),
        AreaConnection(shopping_centre_clothingshop, connection_type="entrance"),
        AreaConnection(shopping_centre_tailor, connection_type="entrance"),
        AreaConnection(shopping_centre_cosmeticsshop, connection_type="entrance"),
        AreaConnection(shopping_centre_toystore, connection_type="entrance"),       # end - passout shop
        AreaConnection(in_town, connection_type="entrance"),                        # passoutstreet
        AreaConnection(temple, connection_type="entrance"),                         # passouttemple
        AreaConnection(residential_drain, connection_type="entrance"),              # start - passoutdrain
        AreaConnection(commercial_drain, connection_type="entrance"),
        AreaConnection(industrial_drain, connection_type="entrance"),               # end - passoutdrain

        AreaConnection(hospital, connection_type="exit", note=ConnectionNotes.hospital_fainting)
    ])
    
    if OptionsLocalization.toggle_pregnancy.value in options.randomization_target_requirements:
        island.append(AreaConnection(hospital, connection_type="exit", note=ConnectionNotes.island_hospital)) # :: Pregnancy Island
    
    
    # Not sure yet if I want to randomize arresting
    # All possible arresting location:
    #   Brothel Raid 
    #   Beach Phallus Science Project (pros req)
    #   Cliff Street Chef Mad
    #   Docks Skul (skul req)
    #   Flats Skul Event (skul req)
    #   Hospital Rent
    #   Hospital
    #   Park Exhb
    #   Bondage Event
    #   Car Entrap
    #   Streetevent
    #   Kylar Basement

    # Kylar Basement:
    #   Ambluance
    #   Passing out in school (combined with ambluance)
    
    jail.extend([ # TODO: police connections
        AreaConnection(brothel),
        AreaConnection(cliff_street, [DoLRules.access_cafe.value]),
        AreaConnection(docks, [DoLRules.skulduggery_4.value]),
        AreaConnection(flats, [DoLRules.skulduggery_2.value]),
        AreaConnection(hospital),
        AreaConnection(park),
        # AreaConnection(), # TODO: bondage
        # AreaConnection(), # TODO: maybe combine streetevent and car entrap
        # AreaConnection(), # ^
        AreaConnection(ambulance, [DoLRules.access_school.value], note=ConnectionNotes.arrested_kylarambluance), # kylar basement event
    ])
    if OptionsLocalization.req_seasonal.value in options.randomization_target_requirements:
        jail.append(AreaConnection(beach))

    # TODO: moneymaker
    moneymaker.extend([
        AreaConnection(spa, [], "entrance"), # hands req
        AreaConnection(alex_farm, [DoLRules.access_produesell.value], "entrance"),
        AreaConnection(cafe), 
    ])



    # -- END Connections

    def build_region_map(start:Area, subzone:dict[DoLRegionNames, list[Area]] | None = None):
        """
        Returns a set of every region name that can be connected to this region, using
        the world_map

        subzone is a zone map from build_zone_map that this function will prioritize
        if the value is found, if not or None is provided it will use the world_map instead
        """
        visited:set[DoLRegionNames] = {start.region_name}
        queue:deque[Area] = deque([start])
    
        def fill(node:Area, _map:dict[DoLRegionNames, list[Area]]):
            for reg in _map[node.region_name]:
                for child in reg.sub_regions:
                    nextnode_child = child.relationship['child']
                    nextnode_parent = child.relationship['parent']
                    if not nextnode_child.region_name in visited:
                        visited.add(nextnode_child.region_name)
                        queue.append(nextnode_child)
                    if child.connection_type not in {"entrance", "exit"}:
                        if not nextnode_parent.region_name in visited:
                            visited.add(nextnode_parent.region_name)
                            queue.append(nextnode_parent)

        while queue:
            node = queue.popleft()
            if subzone is None:
                fill(node, world_map)
            elif node.region_name in subzone:
                fill(node, subzone)
            elif node.region_name in world_map:
                fill(node, world_map)
            else: 
                print(node.region_name)
                raise ValueError("Area not found in maps")
        return visited

    def build_zone_map(zone:list[Area]):
        """
        Builds a dictionary of 'regionname : all connections of each region' from a list of Area
        """
        zone_map:dict[DoLRegionNames, list[Area]] = {}
        for reg in zone:
            for connection in reg.sub_regions:
                child = connection.relationship['child']
                parent = connection.relationship['parent']
                zone_map.setdefault(parent.region_name, []).append(child)

                # Also add child to parent if connection is twoway
                if connection.connection_type not in {"exit", "entrance"}:
                    zone_map.setdefault(child.region_name, []).append(parent)
                elif parent.region_name not in zone_map:
                    zone_map[parent.region_name] = []
            # if it had no connections add it to map
            if reg.region_name not in zone_map:
                zone_map[reg.region_name] = []
        return zone_map

    def rebuild_maps():
        """
        Rebuild all_combined_regions and world_map. 
        Automatically called before randomization

        These values can be used outside this, but mainly used
        for testing of randomization
        """
        nonlocal all_combined_regions
        nonlocal world_map
        all_combined_regions = list(world_regions) + list(shops) + list(debug) + list(badends)
        world_map.clear()
        world_map.update(build_zone_map(all_combined_regions))

    class RandomizationPool:
        """
        Helper class to randomize a list of regions

        To use, do RandomizationPool(pool).run()

        :param pool: List of Area
        :param notest: Variable if you don't want to test that the regions in the region pool are reachable.
                       Used for if the areas in the area pool don't connect to each other
        """
        # Randomization System:
        # 1. go through every area passed as a list, and take its
        # connections regions, remove them, and add it to a pool
        # 2. world.random.shuffle that pool
        # 3. add all regions back, keeping intact their to rules, number of connections for the area, 
        # and its connection note to make it easier to see where you have to come from

        # reason for implementation of connections rules like this:
        # since we're gonna just be changing the destination, the requirements to reach the destination still need to be in place
        # for example:
        #   index0: ocean -> beach  [none]          note="leaving the ocean"
        #   index1: prisn -> ocean  [flight]        note="flying away"
        #   index2: cabin -> forst  [skul 5, dev 5] note="adopting a dog"
        # needs to turn to
        #   index0: ocean -> ocean  [none]          note="leaving the ocean"
        #   index1: prisn -> forst  [flight]        note="flying away"
        #   index2: cabin -> beach  [skul 5, dev 5] note="adopting a dog"

        def __init__(self, largearealist:list[Area], notest = False):
            self.arealist = largearealist
            self.notest = notest
    
        def strip(self, pool:list[Area]):
            """
            Takes a list of regions and then converts it to a single pool
            of all their connections destinations
                                 
            If pool_onewayconnections option is disabled, all connection types
            will be registered as twoway
            Otherwise their types will either be 'twoway', 'entrance' or 'exit'
            """
            pool_relationship:dict[str, list[Area]] = {'twoway': [], 'entrance': [], 'exit': []}

            # zone_map:dict[DoLRegionNames, list[Area]] = {}
            # zone_map.setdefault(parent.region_name, []).append(child)


            def addtopool(area:Area, contype:str):
                if options.pool_onewayrandomization:
                    pool_relationship[contype].append(area)
                else:
                    pool_relationship['twoway'].append(area)
        
            for area in pool:
                for connection in area.sub_regions:
                    # print(f"Adding to Pool: {connection.relationship['parent'].region_name} : {connection.relationship['child'].region_name} : type: {connection.connection_type}")
                    match(connection.connection_type):
                        case("entrance"):
                            addtopool(connection.relationship['parent'], "entrance")
                        case("exit"):
                            addtopool(connection.relationship['child'], "exit")
                        case _:
                            addtopool(connection.relationship['child'], "twoway")
            # print("\n\n")
            return pool_relationship
        
        def shuffleback(self, pool_relationships:dict[str, list[Area]]):
            """
            Used after .strip() or .seperate(), this shuffles the list of relationships and
            then replaces each releationship in the connection pool

            For a full shuffle of a pool of Area, you should do self.shuffleback(*self.strip(pool))

            :params pool_connections: A list of all area connections the pool has
            :params pool_regions: A list of all regions in the pool
            :params pool_size: A list of all regions size (number of AreaConnection)
            :params pool_children: A list of the children each connection has
            """

            # A --> B
            # C <-- D
            # E <-> F
            #
            # E needs to replace B            
            # F Needs to replace C
            #
            # Relationship of A -> B is Exit
            # Relationship of C <- D is Entrance
            #
            # C is considered 'Child'
            # B is considered 'Child'
            #
            # E is considered 'Parent'
            # F is considered 'Child'
            #
            # Steps:
            #
            # We go through the list of Areas (A, C, E)
            #
            # We add their exits to the pool (B, C, F)
            # then shuffle this list
            # 
            # Go through the list of Areas again (A, C, E)
            #
            # Replace their exits with the shuffled list
            #
            # Finished
            #
            # Var Details:
            #
            # pool_relationships is each area we need to connect
            # to for each region sorted by connection type of
            # the original connection, if pool_oneway is off then
            # all connections will be twoway
            #
            # pool_relationships already has either the parent or
            # child depending on what the connection originally had
            # for a connectiontype, so it just contains a list
            # of all outgoing connections
            #
            # Our 'replacelist' is the pool_relationships
            # post being shuffled and tested


            def testconnections():
                """
                Simulates the world regions and tests if they can all be reached
                """
                
                to_replace_regions:list[Area] = []
                test_world:dict[str, Area] = {} # {RegionName: Area}

                # Go over every region that exists in the pool
                # Make a copy of it and copies of its connections
                # Replace the copied connections in the copied region
                # with our area_connections list taking their original from our copies
                # Build a map using it to see if all regions
                #   in the pool are able to be reached

                # Populate a test world with the regions we wish to randomize
                for region in self.arealist:
                    # print(f"adding region {region.region_name} : {len(region.sub_regions)}")
                    to_replace_regions.append(copiedregion := Area(region.region_name))
                    test_world.setdefault(copiedregion.region_name, copiedregion)

                # Populate the regions that don't exist in the pool
                # so we can test the world with their connections
                for region in all_combined_regions:
                    if region.region_name not in test_world:
                        copiedregion = Area(region.region_name)
                        test_world.setdefault(copiedregion.region_name, copiedregion)

                # Create copies of their connections basing off the
                # copies of the regions
                for region in all_combined_regions:
                    for og_conn in region.sub_regions:
                        cop_conn = AreaConnection(test_world[og_conn.initsubarea.region_name], None, og_conn.connection_type, og_conn.note)
                        test_world[region.region_name].append(cop_conn)

                # Replace the connections of the copied regions
                conn_num = {"twoway": 0, "entrance": 0, "exit": 0}
                for region in to_replace_regions: # use our copied list instead of self.arealist
                    # print(f"\n{region.region_name} Test: Size = {len(region.sub_regions)}")

                    # Preventitive measures for full circles
                    # this will apply to the final connections
                    # so no need to be duplicated
                    reg_entrance_placed = 0
                    reshuffles = 0
                    reg_entrance_num = 0
                    for og_conn in region.sub_regions:
                        if og_conn.connection_type != "exit":
                            reg_entrance_num += 1

                    # Start the test replace
                    for og_conn in region.sub_regions:

                        # set contype to the type of connection we need
                        if options.pool_onewayrandomization:
                            if og_conn.connection_type in {"exit", "entrance"}: 
                                contype = og_conn.connection_type
                            else: contype = "twoway"
                        else: contype = "twoway"

                        # Get the connection we need
                        new_reg = pool_relationships[contype][conn_num[contype]]

                        # Prevent full circles by modifying the list if needed
                        if reg_entrance_placed == reg_entrance_num and reg_entrance_num != 0 and og_conn.connection_type != "exit":
                            match(og_conn.connection_type):
                                case("entrance"): compare_area = og_conn.relationship['parent']
                                case _: compare_area = og_conn.relationship['child']
                            while compare_area.region_name == new_reg.region_name:
                                if len(pool_relationships[contype]) < reshuffles + conn_num[contype]: 
                                    print(f"Degrees of Lewdity: Detected Full Circle with no regions left for {region.region_name}, reshuffling")
                                    return False
                                else:
                                    print(f"Degrees of Lewdity: Detected Full Circle for {region.region_name}, moving list around")
                                    pool_relationships[contype].append(pool_relationships[contype].pop(conn_num[contype]))
                                    new_reg = pool_relationships[contype][conn_num[contype]]
                                    reshuffles += 1

                        # Update numbers after full circle detection
                        conn_num[contype] += 1
                        if og_conn.connection_type != "exit":
                            reg_entrance_placed += 1

                        # Replace that connections parent or child
                        # depending on the type of connection the original is
                        # print(f"Applying AreaConnection: Cur Type: {contype}, Con Type: {og_conn.connection_type}, Parent: {og_conn.relationship['parent'].region_name}, Child: {og_conn.relationship['child'].region_name}")
                        match(og_conn.connection_type):
                            case("entrance"):
                                # print(f"\t{og_conn.relationship['parent'].region_name} -> {new_reg.region_name}")
                                og_conn.relationship['parent'] = test_world[new_reg.region_name]
                            case _:
                                # print(f"\t{og_conn.relationship['child'].region_name} -> {new_reg.region_name}")
                                og_conn.relationship['child'] = test_world[new_reg.region_name]

                # Test run WalkableTown settings if
                # the regions exist in the pool
                if options.walkable_town:
                    simulated_domus = test_world[DoLRegionNames.domus_street]
                    simulated_barb = test_world[DoLRegionNames.barb_street]
                    simulated_danube = test_world[DoLRegionNames.danube_street]
                    simulated_connudatus = test_world[DoLRegionNames.connudatus_street]
                    simulated_cliff = test_world[DoLRegionNames.cliff_street]
                    simulated_wolf = test_world[DoLRegionNames.wolf_street]
                    simulated_high = test_world[DoLRegionNames.high_street]
                    simulated_starfish = test_world[DoLRegionNames.starfish_street]
                    simulated_nightingale = test_world[DoLRegionNames.nightingale_street]
                    simulated_oxford = test_world[DoLRegionNames.oxford_street]
                    simulated_mer = test_world[DoLRegionNames.mer_street]
                    simulated_elk = test_world[DoLRegionNames.elk_street]
                    simulated_harvest = test_world[DoLRegionNames.harvest_street]
                    simulated_domus.extend([        AreaConnection(simulated_barb),         AreaConnection(simulated_danube)])
                    simulated_barb.extend([         AreaConnection(simulated_cliff),        AreaConnection(simulated_connudatus)])
                    simulated_danube.extend([       AreaConnection(simulated_wolf),         AreaConnection(simulated_connudatus)])
                    simulated_connudatus.extend([   AreaConnection(simulated_cliff),        AreaConnection(simulated_wolf)])
                    simulated_cliff.extend([        AreaConnection(simulated_starfish),     AreaConnection(simulated_high)])
                    simulated_wolf.extend([         AreaConnection(simulated_nightingale),  AreaConnection(simulated_high)])
                    simulated_high.extend([         AreaConnection(simulated_starfish),     AreaConnection(simulated_nightingale)])
                    simulated_starfish.extend([     AreaConnection(simulated_oxford),       AreaConnection(simulated_mer)])
                    simulated_nightingale.extend([  AreaConnection(simulated_oxford),       AreaConnection(simulated_elk)])
                    simulated_oxford.extend([       AreaConnection(simulated_mer),          AreaConnection(simulated_elk)])
                    simulated_mer.extend([          AreaConnection(simulated_harvest)])
                    simulated_elk.extend([          AreaConnection(simulated_elk)])
                    # simulated_harvest.extend([])

                # Build the map and see if all regions in the pool exist
                zonemap = build_zone_map([reg for reg in test_world.values()])
                # print(zonemap)
                testregionmap = build_region_map(test_world[DoLRegionNames.orphanage], zonemap)
                # print({reg: [conname.region_name for conname in con] for reg, con in zonemap.items()})
                # print(testregionmap)
                for reg in self.arealist:
                    if not (reg.region_name in testregionmap):
                        # print(json.dumps({key: [regname.region_name for regname in reg] for key, reg in zonemap.items()}))
                        print(f"Degrees of Lewdity: {reg.region_name} is unreachable, Reshuffling")
                        # time.sleep(20)
                        return False
                # print("\n\nTests Finished\n\n")
                return True

            def keepshuffling():
                """
                Function that keeps shuffling pool_releationships
                until it reaches a state where every             
                area in the area_pool can be reached by the world
                """
                for pool in pool_relationships.values(): world.random.shuffle(pool)
                
                # Test that all regions are reachable
                if not testconnections(): return False
                return True

            # Create Replacement Regions
            while not keepshuffling(): continue

            # Replace the connections
            conn_num = {"twoway": 0, "entrance": 0, "exit": 0}
            for region in self.arealist:
                # print(f"\n{region.region_name} Actual")
                for og_conn in region.sub_regions:

                    # set contype to the type of connection we need
                    if options.pool_onewayrandomization:
                        if og_conn.connection_type in {"exit", "entrance"}: 
                            contype = og_conn.connection_type
                        else: contype = "twoway"
                    else: contype = "twoway"

                    # Get the conn of the contype we need
                    new_reg = pool_relationships[contype][conn_num[contype]]
                    conn_num[contype] += 1

                    # Replace that connections parent or child
                    # depending on the type of connection the original is
                    # print(f"Applying AreaConnection: Cur Type: {contype}, Con Type: {og_conn.connection_type}, Parent: {og_conn.relationship['parent'].region_name}, Child: {og_conn.relationship['child'].region_name}")
                    match(og_conn.connection_type):
                        case("entrance"):
                            # print(f"\t{og_conn.relationship['parent'].region_name} -> {new_reg.region_name}")
                            og_conn.relationship['parent'] = new_reg
                        case _:
                            # print(f"\t{og_conn.relationship['child'].region_name} -> {new_reg.region_name}")
                            og_conn.relationship['child'] = new_reg
            print(f"Degrees of Lewdity: Shuffle Finished Successfully\nConnections Made: {conn_num} : Total: {[len(item) for item in pool_relationships.values()]}")

        def run(self):
            """
            Runs through a list of Areas passed to the init of this class, and then returns that list shuffled

            If the onewayrandomization option is enabled, seperates the pools first and 
            shuffles them inbetween themselves
            """
            rebuild_maps()
            # print(f"Randomization pool started randomization containing {self.arealist[0].name()}")
            self.shuffleback(self.strip(self.arealist))

    def walkabletown_connections():
        """
        Function for street to street connections, incase we don't
        want to randomize them
        """
        # includes connections backwards aswell as forwards
        # this does mean it would be possible to have connections that lead into themselves, but should be funny
        
        # -- Column 1
        domus_street.extend([
            # Left:

            # Right:
            AreaConnection(barb_street, note=ConnectionNotes.domusstreet_barbstreet), 
            AreaConnection(danube_street, note=ConnectionNotes.domusstreet_danubestreet)
        ])
        
        # -- Column 2
        barb_street.extend([ 
            # Left:
            # AreaConnection(domus_street),
            # Right:
            AreaConnection(cliff_street, note=ConnectionNotes.barbstreet_cliffstreet), 
            AreaConnection(connudatus_street, note=ConnectionNotes.barbstreet_connudatusstreet)
        ]) 
        danube_street.extend([ 
            # Left:
            # AreaConnection(domus_street),
            # Right:
            AreaConnection(wolf_street, note=ConnectionNotes.danubestreet_wolfstreet), 
            AreaConnection(connudatus_street, note=ConnectionNotes.danubestreet_connudatusstreet)
        ])
        
        # -- Column 3
        connudatus_street.extend([
            # Left:
            # AreaConnection(danube_street), AreaConnection(barb_street),
            # Right
            AreaConnection(cliff_street, note=ConnectionNotes.connudatusstreet_cliffstreet), 
            AreaConnection(wolf_street, note=ConnectionNotes.connudatusstreet_wolfstreet)
        ]) 
        
        # -- Column 4
        cliff_street.extend([
            # Left:
            #AreaConnection(barb_street), AreaConnection(connudatus_street),
            # Right:
            AreaConnection(starfish_street, note=ConnectionNotes.cliffstreet_starfishstreet), 
            AreaConnection(high_street, note=ConnectionNotes.cliffstreet_highstreet)
        ]) 
        wolf_street.extend([
            # Left:
            #AreaConnection(danube_street), AreaConnection(connudatus_street),
            # Right:
            AreaConnection(nightingale_street, note=ConnectionNotes.wolfstreet_nightingalestreet), 
            AreaConnection(high_street, note=ConnectionNotes.wolfstreet_highstreet)
        ])
        
        # -- Column 5
        high_street.extend([
            # Left:
            #AreaConnection(cliff_street), AreaConnection(wolf_street),
            # Right:
            AreaConnection(starfish_street, note=ConnectionNotes.highstreet_starfishstreet), 
            AreaConnection(nightingale_street, note=ConnectionNotes.highstreet_nightingalestreet)
        ]) 
        
        # -- Column 6
        starfish_street.extend([
            # Left:
            #AreaConnection(cliff_street), AreaConnection(high_street),
            # Right:
            AreaConnection(oxford_street, note=ConnectionNotes.starfishstreet_oxfordstreet), 
            AreaConnection(mer_street, note=ConnectionNotes.starfishstreet_merstreet)
        ]) 
        nightingale_street.extend([
            # Left:
            # AreaConnection(wolf_street), AreaConnection(high_street),
            # Right:
            AreaConnection(oxford_street, note=ConnectionNotes.nightingalestreet_oxfordstreet), 
            AreaConnection(elk_street, note=ConnectionNotes.nightingalestreet_elkstreet)
        ])
        
        # -- Column 7
        oxford_street.extend([
            # Left:
            #AreaConnection(starfish_street), AreaConnection(nightingale_street),
            # Right:
            AreaConnection(mer_street, note=ConnectionNotes.oxfordstreet_merstreet), 
            AreaConnection(elk_street, note=ConnectionNotes.oxfordstreet_elkstreet)
        ])
        
        # -- Column 8
        mer_street.extend([
            # Left:
            #AreaConnection(starfish_street), AreaConnection(oxford_street), 
            # Right:
            AreaConnection(harvest_street, note=ConnectionNotes.merstreet_harvestreet)
        ]) 
        elk_street.extend([
            # Left:
            #AreaConnection(nightingale_street), AreaConnection(oxford_street), 
            # Right:
            AreaConnection(harvest_street, note=ConnectionNotes.elkstreet_harvestreet)
        ])
        
        # -- Column 9
        # harvest_street.extend([
        #     # Left:
        #     AreaConnection(mer_street), 
        #     AreaConnection(elk_street),
        #     # Right:
        # ])


    # -------- Start: Randomization --------

    all_combined_regions:list[Area] = []
    world_map:dict[DoLRegionNames, list[Area]] = {}
    rebuild_maps()
    

    # Connections between streets
    if not options.walkable_town: 
        walkabletown_connections()
    # .extend Shops
    if options.shop_locations == options.shop_locations.option_anywhere: 
        world_regions.extend(shops)
        shops.clear()
    # .extend Badends
    if options.randomize_badends == options.randomize_badends.option_anywhere:
        world_regions.extend(badends)
        badends.clear()
    # .append Tentacle Areas (they can exist in region list even if tent disabled)
    if options.randomize_tentacleareas and OptionsLocalization.animal_tentacles.value in options.gameanimal_options:
        world_regions.append(tentacle_forest)
        world_regions.append(tentacle_plains)

    # Run Randomize
    if options.randomize_entrances: 
        RandomizationPool(world_regions).run()

    #print([f"{regcon.relationship['parent'].region_name} : {regcon.relationship['child'].region_name} : type: {regcon.connection_type}" for reg in world_regions for regcon in reg.sub_regions])

    # -------- Post: World Randomization --------

    # Run Randomize & .extend(): Shop (if not done above)
    if options.shop_locations == options.shop_locations.option_between_themselves: 
        RandomizationPool(shops).run()
        world_regions.extend(shops)
        shops.clear()

    # Run Randomize & .extend(): Bad Ends (if not done above)
    if options.randomize_badends == options.randomize_badends.option_between_themelves:
        RandomizationPool(badends).run()
        world_regions.extend(badends)
        badends.clear()


    # -------- Post: Randomization --------

    # -- Add non-randomized loose regions
    world_regions.extend(debug)
    debug.clear()

    # -- Final Connections
    # Connections between streets (if not done above)
    if options.walkable_town: 
        walkabletown_connections()
    # .extend Shops (if not done above)
    if options.shop_locations == options.shop_locations.option_disabled: 
        world_regions.extend(shops)
        shops.clear()
    # .extend Badends (if not done above)
    if options.randomize_badends == options.randomize_badends.option_disabled: 
        world_regions.extend(badends)
        badends.clear()

    # -- No Connection Areas
    # These areas still need to be in the region pool (for rules)
    # however they won't have any connections to anything
   
    # .append Tentacle Areas (if not done above)
    if not options.randomize_tentacleareas or not(OptionsLocalization.animal_tentacles.value in options.gameanimal_options): 
        world_regions.append(tentacle_forest)
        world_regions.append(tentacle_plains)

    if not (OptionsLocalization.toggle_bestiality.value in options.gameworld_options or OptionsLocalization.toggle_monsterpeople.value in options.gameworld_options):
        world_regions.append(wolf_cave)

    # -- Final test
    double_test_zone_map = build_zone_map(world_regions)
    double_test_map = build_region_map(orphanage, double_test_zone_map)
    for reg in world_regions:
        if reg.region_name == DoLRegionNames.wolf_cave and not (OptionsLocalization.toggle_bestiality.value in options.gameworld_options or OptionsLocalization.toggle_monsterpeople.value in options.gameworld_options):
            continue
        elif reg.region_name in {DoLRegionNames.tentacle_forest, DoLRegionNames.tentacle_plains} and not (OptionsLocalization.animal_tentacles.value in options.gameanimal_options):
            continue
        if reg.region_name not in double_test_map:
            print({reg: [conname.region_name for conname in con] for reg, con in double_test_zone_map.items()})
            print("\n\nRelevant Error Info Above\n")
            raise Exception(f"Degrees of Lewdity: Noticed missing region post-randomization ({reg.region_name}), raising error to prevent an unaccessable region in world")


    # -- Create World Map Dictionary
    connection_dictionary:dict[ConnectionNotes, Area] = {}
    # Note of Connection: Area to replace

    # TODO: will need to make a file localizing the name
    # of each connection to the actual value it in ingame

    # Afterwards we can do a large switch case based off note (note == note)
    # to make the file that we can send to the user

    for region in world_regions:
        for conn in region.sub_regions:
            if conn.note == None or conn.note == "":
                continue
            match(conn.connection_type):
                case("entrance"):
                    connection_dictionary.setdefault(conn.note, conn.relationship['parent'])
                case _:
                    connection_dictionary.setdefault(conn.note, conn.relationship['child'])

    # -- World Map
    # Convert this to a file in the spoiler log eventually

    in_global = Area(DoLRegionNames.in_global)
    for reg in world_regions: in_global.append(AreaConnection(reg, connection_type="entrance", note=ConnectionNotes.note_world)) 
    world_regions.append(in_global)


    # -- Finalize


    # You must add_to_multiworld all regions before running .connect 
    for reg in world_regions:
        reg.add_to_multiworld()

    for reg in world_regions:
        # subareas = [sub.area.region_name.value for sub in reg.sub_regions]
        # print(f"attempting to connect {reg.name()} with connections {subareas}")
        reg.connect()

    return connection_dictionary
