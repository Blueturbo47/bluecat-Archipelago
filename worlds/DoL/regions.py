from __future__ import annotations
from BaseClasses import Region
from rule_builder.rules import And
from .en import ConnectionNotes, DoLRegionNames, OptionsLocalization

from .data import DoLOptionFilters, DoLRules

from typing import TYPE_CHECKING
if TYPE_CHECKING: 
    from .world import DoLWorld
    from .en import _NoteDetail



def create_and_connect_regions(world:DoLWorld) -> None:
    player = world.player
    multiworld = world.multiworld
    options = world.options

    class AreaConnection:
        """
        Container for a connection. Takes this area this connection leads to and the list of rules it needs to connect. 

        :param area: Area which this connection is bridging to
        :param rules: List of world Rules that this connection requires
        :param connection_type: (optional) 'exit' or 'entrance'
        :param note: Adds a note to connection, giving the user more info on the connection
        """

        def __init__(self, area:Area, rules:list[DoLRules] | None = None, connection_type:str = "", note:ConnectionNotes = None):
            self.area = area
            self.rules = rules if rules is not None else []
            self.connection_type = connection_type
            self.note = note


        def has_rules(self):
            return True if not self.rules else False

        def append_rules(self, rule:DoLRules):
            self.rules.append(rule)

        def extend_rules(self, rules:list[DoLRules]):
            self.rules.extend(rules)

        def pop_rules(self):
            rules, self.rules = self.rules, []
            return rules

        def return_rules(self):
            rules = []
            for rule in self.rules:
                rules.append(rule.value)
            return rules


        def set_connectionType(self, connection_type:str):
            self.connection_type = connection_type

        def return_connectionType(self):
            return self.connection_type


        def pop_area(self):
            area, self.area = self.area, None
            return area

        def set_area(self, area:Area):
            self.area = area

        def return_area(self):
            return self.area

        def return_areaName(self):
            return self.area.name()

        def return_areaRegion(self):
            return self.area.return_region()


        def pop_note(self):
            note, self.note = self.note, ""
            return note

        def set_note(self, newnote:_NoteDetail):
            self.note = newnote

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
            Example: [AreaConnection(regionnames.bar), AreaConnection(regionnames.baz, rules.1)]
        
        ### Functions:

        - name(): returns name

        - return_region(): returns the Region class for this Area

        - return_areas(): returns the list of connections

        - pop_areas(): returns and clears the list of connections

        - append(): adds an AreaConnection to the list of connections

        - extend(): extends the list of connections with a list of AreaConnection

        - add_to_multiworld(): adds the region to the world, run this before .connect()

        - connect(): connects regions defined in the sub_regions lists with this region. Run this to finalize the region after add_to_multiworld()
        """

        def __init__(self, region_name:DoLRegionNames, sub_regions:list[AreaConnection] | None = None):
            self.region_name = region_name
            self.sub_regions = sub_regions if sub_regions is not None else []

            self.self_region = Region(self.region_name.value, player, multiworld)

            # removelater = []
            # for connect in self.sub_regions:
            #     removelater.append(connect.return_areaName())
            # print(f"{self.region_name} generated with {removelater} connections")

        def name(self):
            return self.region_name

        def add_to_multiworld(self):
            """
            Adds the region to the multiworld. Run this before running connect()
            """
            # print(f"Adding '{self.region_name}' with connections '{self.self_region.entrances}'")
            multiworld.regions.append(self.self_region)

        def connect(self):
            """
            Adds all connections to the Region for this Area. Run this after running add_to_multiworld()
            """
            for connection in self.sub_regions:
                self.designate_connections(connection)

        def designate_connections(self, connection:AreaConnection):
            """
            Leave blank for a normal connection
            connection_type (optional): 'exit' or 'entrance'
            """

            connectiontype = connection.return_connectionType()
            selfregion = world.get_region(self.region_name.value)

            # print(f"\nConnection '{self.region_name.value}' {"->" if connectiontype == "entrance" else "<-" if connectiontype == "exit" else "<->"} '{connection.return_areaName().value}'")
            # print(f"\tNote: '{connection.note}'")
            # print(f"\tRules: {And(*connection.return_rules()).to_dict()}")


            if (connectiontype == "entrance" or connectiontype == None or connectiontype == ""):
                connection.return_areaRegion().connect(
                    selfregion, # incoming only
                    f"{connection.return_areaName()} -> {self.self_region.name} {f"| {connection.note.value.resolve()}" if connection.note is not None else ""}",
                    And(*connection.return_rules())
                )
                
            if (connectiontype == "exit" or connectiontype == None or connectiontype == ""):
                selfregion.connect(
                    connection.return_areaRegion(), # outgoing only
                    f"{self.self_region.name} -> {connection.return_areaName()} {f"| {connection.note.value.resolve()}" if connection.note is not None else ""}",
                    And(*connection.return_rules())
                )

        def extend(self, connection_list:list[AreaConnection]):
            """
            Extends the connection lists

            connection_type: None (normal connection), "exit", or "entrance"
            """
            # removelater = []
            # for connect in connection_list:
            #     removelater.append(connect.return_areaName())
            # print(f"{self.name()} got {removelater} connections")

            self.sub_regions.extend(connection_list)

        def append(self, connection:AreaConnection):
            """
            Adds to the connection list

            connection_type: None (normal connection), "exit", or "entrance"
            """
            # print(f"{self.name()} got {connection.return_areaName()} connection")

            self.sub_regions.append(connection)

        def return_region(self):
            return self.self_region

        def return_areas(self):
            return self.sub_regions

        def pop_areas(self):
            areas = self.sub_regions
            self.sub_regions = []
            return areas


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
    badends.append(wolf_cave := Area(DoLRegionNames.wolf_cave))


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
    # Ocean -- None
    
    # -- Outskirts
    # Farmlands
    farmlands.extend([
        AreaConnection(manors, note=ConnectionNotes.farmlands_manors), 
        AreaConnection(meadow, note=ConnectionNotes.farmlands_meadow), 
        AreaConnection(riding_school, note=ConnectionNotes.farmlands_ridingschool), 
        AreaConnection(alex_farm, note=ConnectionNotes.farmlands_alexfarm), 
        AreaConnection(farmlands_road, note=ConnectionNotes.farmlands_farmlandsroad),
        AreaConnection(maze, [DoLRules.has_mazekey], note=ConnectionNotes.farmlands_maze)
    ])

    # Moor
    # don't connect badends because badend rando rules
    moor.append(
        AreaConnection(remy_estate, 
                       [DoLRules.access_remyestate_rules], 
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
    # TODO: CODE bog access failing
    bog.extend([
        AreaConnection(moor, 
                       [DoLRules.access_forest], 
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
                        [DoLRules.has_adoptionpapers, DoLRules.access_orphanage], 
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
        AreaConnection(park, [DoLRules.science_1], note=ConnectionNotes.school_park),
        AreaConnection(industrial_alleyways, note=ConnectionNotes.school_industrialalleyways), 
        AreaConnection(commercial_drain, 
                        [DoLRules.history_3],
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
                        connection_type="entrance", 
                        note=ConnectionNotes.oxfordstreet_forestlake), # student walking to lake
        AreaConnection(orphanage, 
                        connection_type="entrance",
                        note=ConnectionNotes.oxfordstreet_orphanage), # :: Robin Walk School 
    ])


    # Harvest Street
    # TODO: NOTE abnormal connection?
    pub.append(
        AreaConnection(forest, note=ConnectionNotes.pub_forest)
    )
    harvest_street.extend([
        AreaConnection(brothel, [DoLRules.access_brothel_rules], note=ConnectionNotes.harveststreet_brothel), 
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
                        [DoLRules.skulduggery_4], 
                        "exit",
                        ConnectionNotes.docks_beach)
    )
    coastal_path.append(
        AreaConnection(meadow,
                        [DoLRules.history_4], 
                        note=ConnectionNotes.costalpath_meadow)
    )
    mer_street.extend([
        # this is two-way because fishing can bring you to the waters sometimes
        AreaConnection(beach, note=ConnectionNotes.docks_beach),
        AreaConnection(docks, note=ConnectionNotes.merstreet_docks), 
        AreaConnection(coastal_path, 
                        [DoLRules.history_3],
                        note=ConnectionNotes.merstreet_costalpath), 
        AreaConnection(industrial_alleyways, note=ConnectionNotes.merstreet_industrialalleyways), 
        AreaConnection(industrial_drain, note=ConnectionNotes.merstreet_industrialdrain),
    ])

    # Elk Street
    elk_street.extend([
        AreaConnection(landfill, 
                        [DoLRules.access_landfill_rules], 
                        note=ConnectionNotes.elkstreet_landfill), 
        AreaConnection(adult_shop, note=ConnectionNotes.elkstreet_adultshop), # no rules (don't need to build it to go there)
        AreaConnection(compound, 
                        [DoLRules.access_compound_rules], 
                        note=ConnectionNotes.elkstreet_compound),
        AreaConnection(industrial_alleyways, note=ConnectionNotes.elkstreet_industrialalleyways), 
        AreaConnection(industrial_drain, note=ConnectionNotes.elkstreet_industrialdrain)
    ])


    # -- Bad Ends

    # prison: 1
    # entrance logic is hospital for high arrest chance
    prison.extend([
        # Entrances
        # Entrance done below badends from jail region
        AreaConnection(hospital, connection_type="entrance", note=ConnectionNotes.police_prison), # :: Police Prison Intro
        
        # Exits
        AreaConnection(orphanage, connection_type="exit", note=ConnectionNotes.prison_orphanage), # :: Prison End Car Silent, Prison End Car Thank, Prison End Car Angry
        AreaConnection(docks, connection_type="exit", note=ConnectionNotes.prison_docks), # :: Prison Kylar Escape Ask, Prison Kylar Escape Nod, Prison Wren Escape 3
        # NOTE: 2 ocean connections, however one doesn't require swimming 10
        AreaConnection(ocean, [DoLRules.swimming_10], "exit", ConnectionNotes.prison_oceanswim), # :: Prison Escape
        AreaConnection(ocean, connection_type="exit", note=ConnectionNotes.prison_oceanpassout), # ::Passout Rut 2
        AreaConnection(beach, [DoLRules.tfrule_flight], "exit", ConnectionNotes.prison_beach), # :: Prison Soar Escape
    ])

    # pirate_ship: 2
    # exit to island is already an entrance from island, so it does not need to be included
    pirate_ship.extend([
        # Entrances
        AreaConnection(ocean, connection_type="entrance", note=ConnectionNotes.ocean_pirateship),  # :: Pirate Intro (Passout Pirates Hot Cold, Passout Pirate)
        AreaConnection(old_sewers, [DoLRules.access_temple], "entrance", ConnectionNotes.oldsewers_pirateship),  # :: Smuggler Pub Zephyr
    
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
        dog_pound_ending.append(AreaConnection(in_town, [DoLRules.tfrule_wolf_full_appear], "entrance", ConnectionNotes.wolfabudction_dogpoundbadend))


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
        AreaConnection(farmlands, [DoLRules.tfrule_flight], "exit", note=ConnectionNotes.birdtower_farmlands), # :: Bird Tower Farmlands
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
        AreaConnection(cliff_street, [DoLRules.access_cafe], "entrance", ConnectionNotes.cliffstreet_remyfarm),  # :: Chef Blackmail Livestock 2
        AreaConnection(pub, connection_type="entrance", note=ConnectionNotes.pub_remyfarm), # :: Pub White Pill Van
        AreaConnection(in_town, connection_type="entrance", note=ConnectionNotes.intown_remyfarm), # TODO: this entrance
    
        # Exits
        AreaConnection(forest, connection_type="exit", note=ConnectionNotes.remyfarm_forest) # all lead to :: Livestock Escape Town
    ])

    # wolf_cave: 12
    # unable to enter if monster people or bestiality is disabled
    if DoLOptionFilters.bestiality_or_monsterpeople.value.resolve(world):
        wolf_cave.append(
            AreaConnection(forest, connection_type="entrance", note=ConnectionNotes.forest_wolfcave) # :: Forest Wolf Cave Intro
        )

    # -- Tentacle Plains/Forest
    # if disabled tentacle plains will just not have connections to/from
    if OptionsLocalization.animal_tentacles.value in options.gameanimal_options:
        # NOTE: we don't want logic to think orphanage -> tentacle plains -> asylum is possible
        # so tentacle plains are enter only
        tentacle_plains.append(AreaConnection(asylum, connection_type="entrance", note=ConnectionNotes.asylum_tentacleplains))
        tentacle_plains.append(AreaConnection(orphanage, [DoLRules.deviancy_5], "entrance", ConnectionNotes.orphanage_tentacleplains))
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
    ])
    hospital.append(AreaConnection(ambulance, connection_type="entrance", note=ConnectionNotes.hospital_fainting))
    
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
        AreaConnection(cliff_street, [DoLRules.access_cafe]),
        AreaConnection(docks, [DoLRules.skulduggery_4]),
        AreaConnection(flats, [DoLRules.skulduggery_2]),
        AreaConnection(hospital),
        AreaConnection(park),
        # AreaConnection(), # TODO: bondage
        # AreaConnection(), # TODO: maybe combine streetevent and car entrap
        # AreaConnection(), # ^
        AreaConnection(ambulance, [DoLRules.access_school], note=ConnectionNotes.arrested_kylarambluance), # kylar basement event
    ])
    prison.append(AreaConnection(jail, connection_type="entrance", note=ConnectionNotes.police_prison)), # :: Police Prison Intro
    if OptionsLocalization.req_seasonal.value in options.randomization_target_requirements:
        police_station.append(AreaConnection(beach))



    # -- END Connections

    class RandomizationPool:
        """
        Helper class to randomize a list of regions
        """
        # Randomization System:
        # go through every area passed as a list
        # remove every connection in every area in that region and add it to a pool
        # world.random.shuffle that pool
        # add all connections back, keeping intact their to rules to enter the connection, number of connections for the area, 
        # and its connection note to make it easier to see where you have to come from
            # Note: unless you have the option to prevent this, this will make oneway connections
            # randomize into the pool. Otherwise oneway connections only randomize within themselves

        def __init__(self, largearealist:list[Area]):
            self.arealist = largearealist

        def seperate(pool:list[Area]):
            """
            Takes a list of areas, removes its connections, and sorts them into 2 lists based on connection_type
            """
            newpool_normal:list[AreaConnection] = []
            newpool_exitentrance:list[AreaConnection] = []
            for area in pool:
                connections = area.pop_areas()
                for connect in connections:
                    match(connect.return_connectionType()):
                        case("exit" | "entrance"):
                            newpool_exitentrance.append(connect)
                        case _:
                            newpool_normal.append(connect)
            return newpool_normal, newpool_exitentrance
    
        def strip(self, pool:list[AreaConnection]):
            """
            Function used to strip a list of connections to:
            - A list of size of the connection
            - The list of connections
            - A list of the lists of rules each connection has
            """
            pool_size = len(pool)
            newpool:list[AreaConnection] = []
            pool_areas:list[Area] = []
            for connection in pool:
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

                
                pool_areas.append(connection.pop_area())
                newpool.append(connection) # add the cleaned connection into the pool
            return pool_size, newpool, pool_areas

        def shuffleback(self, pool:list[AreaConnection], pool_size:list[int], pool_areas:list[Area]):
            """
            Takes the original list of areas, the list of connections they all have, the size of area, and the rules for the connections

            Then afterwards, shuffles the connections, and adds them back with their original rules and area size
            """
            world.random.shuffle(pool)
            for areanum, area in enumerate(self.arealist):
                i = 0
                while i < pool_size[areanum]:
                    connection = pool[i]
                    connection.set_area(pool_areas.pop(0))
                    area.append(connection)
                    i += 1

        def run(self):
            """
            Runs through a list of Areas passed to the init of this class, and then returns that list shuffled
            """
            # print(f"Randomization pool started randomization containing {self.arealist[0].name()}")
            if options.pool_onewayrandomization:
                for pooltype in self.seperate(self.arealist):
                    self.shuffleback(self.strip(pooltype))
            else:
                self.shuffleback(self.strip(self.arealist))
            return self.arealist

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


    # # -------- Start: Randomization --------

    # # Connections between streets
    # if not options.walkable_town: 
    #     walkabletown_connections()
    # # .extend Shops
    # if options.shop_locations == options.shop_locations.option_anywhere: 
    #     world_regions.extend(shops)
    # # .extend Badends
    # if options.randomize_badends == options.randomize_badends.option_anywhere:
    #     world_regions.extend(badends)
    # # .append Tentacle Areas (they can exist in region list even if tent disabled)
    # if options.randomize_tentacleareas: 
    #     world_regions.append(tentacle_forest)
    #     world_regions.append(tentacle_plains)

    # # Run Randomize
    # if options.randomize_entrances: 
    #     world_regions = RandomizationPool(world_regions).run()

    # # -------- Post: World Randomization --------

    # # Run Randomize & .extend(): Shop (if not done above)
    # if options.shop_locations == options.shop_locations.option_between_themselves: 
    #     shops = RandomizationPool(shops).run()
    #     world_regions.extend(shops)
    # # Run Randomize & .extend(): Bad Ends (if not done above)
    # if options.randomize_badends == options.randomize_badends.option_between_themelves:
    #     badends = RandomizationPool(badends).run()
    #     world_regions.extend(badends)


    # -------- Post: Randomization --------
    
    # non-randomized loose regions
    world_regions.extend(debug)
    walkabletown_connections()
    world_regions.extend(shops)
    world_regions.extend(badends)
    world_regions.append(tentacle_forest)
    world_regions.append(tentacle_plains)


    # # Connections between streets (if not done above)
    # if options.walkable_town: 
    #     walkabletown_connections()
    # # .extend Shops (if not done above)
    # if options.shop_locations == options.shop_locations.option_disabled: 
    #     world_regions.extend(shops)
    # # .extend Badends (if not done above)
    # if options.randomize_badends == options.randomize_badends.option_disabled: 
    #     world_regions.extend(badends)
    # # .append Tentacle Areas (they can exist in region list even if tent disabled) (if not done above)
    # if not options.randomize_tentacleareas: 
    #     world_regions.append(tentacle_forest)
    #     world_regions.append(tentacle_plains)


    in_global = Area(DoLRegionNames.in_global)
    for reg in world_regions: in_global.append(AreaConnection(reg, note=ConnectionNotes.note_world)) 
    world_regions.append(in_global)

    # You must add_to_multiworld all regions before running .connect 
    for reg in world_regions:
        reg.add_to_multiworld()

    for reg in world_regions:
        # subareas = [sub.return_areaName().value for sub in reg.sub_regions]
        # print(f"attempting to connect {reg.name()} with connections {subareas}")
        reg.connect()
