from __future__ import annotations
from typing import TYPE_CHECKING
from BaseClasses import Entrance, Region

from .rules import DoLRules
from .data import DoLRegionNames

if TYPE_CHECKING:
    from .world import DoLWorld




def create_and_connect_regions(world: DoLWorld) -> None:
    player = world.player
    multiworld = world.multiworld

    class AreaConnection:
        """
        Container for a connection. Takes this area this connection leads to and the list of rules it needs to connect. 
        
        :param area: Area which this connection is bridging to
        :param rules: List of world Rules that this connection requires
        :param connection_type: (optional) 'exit' or 'entrance'
        """

        def __init__(self, area:Area, rules:list[DoLRules] | None = None, connection_type:str = "", note:str = ""):
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
            return self.rules


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

        def set_note(self, newnote:str):
            self.note = newnote

    class Area:
        """
        ### Description:
        
        This class contains takes a name of a region, and the regions it wishes to connect to via the AreaConnection class
        
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

        - connect(): connects regions defined in the sub_regions lists with this region. Run this to finalize the region

        - append(): adds a connection to the list of connections

        - extend(): adds multiple connections in a list to the list of connections

        - add_to_multiworld(): adds the finalized region to the world
        """

        def __init__(self, region_name:DoLRegionNames, sub_regions:list[AreaConnection] | None = None):
            self.region_name = region_name
            self.sub_regions = sub_regions if sub_regions is not None else []

            self.self_region = Region(self.region_name, player, multiworld)

            # removelater = []
            # for connect in self.sub_regions:
            #     removelater.append(connect.return_areaName())
            # print(f"{self.region_name} generated with {removelater} connections")

        def name(self):
            return self.region_name

        def add_to_multiworld(self):
            """
            Adds the **finalized** region to the multiworld
            """
            # print(f"Adding '{self.region_name}' with connections '{self.self_region.entrances}'")
            multiworld.regions.append(self.self_region)

        def connect(self):
            """
            Adds all connections to the Region for this Area. Run this before running add_to_multiworld()
            """
            for connection in self.sub_regions:
                self.designate_connections(connection)

        def designate_connections(self, connection:AreaConnection):
            """
            Leave blank for a normal connection
            connection_type (optional): 'exit' or 'entrance'
            """

            connectiontype = connection.return_connectionType()

            # TODO: rules for connections
            if (connectiontype == "entrance" or connectiontype == None or connectiontype == ""):
                connection.return_areaRegion().connect(self.self_region, f"{connection.return_areaName()} -> {self.self_region.name} | {connection.note}")

            if (connectiontype == "exit" or connectiontype == None or connectiontype == ""):
                self.self_region.connect(connection.return_areaRegion(), f"{self.self_region.name} -> {connection.return_areaName()} | {connection.note}")

        def extend(self, connection_list:list[AreaConnection]):
            """
            Extends the connection lists

            connection_type: None (normal connection), "exit", or "entrance"
            """
            # # TODO: remove debug
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
    
    # Soft Bad Ends
        # Tentacle Plains (not a bad end, but needs to be before asylum)
    world_regions.append(tentacle_plains := Area(DoLRegionNames.tentacle_plains)) 
        # Refer to logic at bottom where entrances/exits are
    badends.append(prison := Area(DoLRegionNames.prison))
    badends.append(island := Area(DoLRegionNames.island))
    badends.append(underground_brothel := Area(DoLRegionNames.underground_brothel))
    badends.append(asylum := Area(DoLRegionNames.asylum ))
    badends.append(dog_pound_ending := Area(DoLRegionNames.dog_pound_ending))
    badends.append(mines := Area(DoLRegionNames.mines))
    badends.append(eden_cabin := Area(DoLRegionNames.eden_cabin))
    badends.append(kylar_manor := Area(DoLRegionNames.kylar_manor))
    badends.append(pirate_ship := Area(DoLRegionNames.pirate_ship)) 
    badends.append(bird_tower := Area(DoLRegionNames.bird_tower))
    badends.append(remy_farm := Area(DoLRegionNames.remy_farm))
    badends.append(wolf_cave := Area(DoLRegionNames.wolf_cave))

    # Outside Town
        
    # Forest (danube, wolf, and nightingale street enter forest)
    # forest_shop not a world region due to shop randomization
    shops.append(forest_shop := Area(DoLRegionNames.forest_shop))
    world_regions.append(forest_lake := Area(DoLRegionNames.forest_lake))

    # don't connect forest shop here incase shop randomizer, we don't want the
    # connection to be inside the world_regions pool
    world_regions.append(forest := Area(DoLRegionNames.forest, [ 
                AreaConnection(forest_lake, note="via Forest Lake from Forest")]))
    # we need connection to be after decleration
    forest_shop.append(AreaConnection(forest, note="via Forest Shop from Forest"))
    
    # Ocean
    world_regions.append(ocean := Area(DoLRegionNames.ocean))

    # Outskirts
    # Farmlands
    world_regions.append(alex_farm := Area(DoLRegionNames.alex_farm))
    world_regions.append(riding_school := Area(DoLRegionNames.riding_school))
    world_regions.append(meadow := Area(DoLRegionNames.meadow))
    world_regions.append(manors := Area(DoLRegionNames.manors))
    world_regions.append(farmlands_road := Area(DoLRegionNames.farmlands_road))
    world_regions.append(farmlands := Area(DoLRegionNames.farmlands, [
                AreaConnection(manors, note="via Manors from the Farmlands"), 
                AreaConnection(meadow, note="via Meadow from the Farmlands"), 
                AreaConnection(riding_school, note="via Riding School from the Farmlands"), 
                AreaConnection(alex_farm, note="via Alex's Farm from the Farmlands"), 
                AreaConnection(farmlands_road, note="via Town Road from the Farmlands")]))

    # Moor
    world_regions.append(moor := Area(DoLRegionNames.moor))

        # Other Areas
    # bog connects forest to moor, but not back
    world_regions.append(bog := Area(DoLRegionNames.bog, [
                AreaConnection(moor, 
                                ["TODO: moor to bog requires $bogprogress 1"], 
                                note="via Moor from the Bog"), 
                AreaConnection(forest, 
                                ["TODO: bog can be discovered in forest in a few ways"], 
                                "entrance", 
                                "via Bog from the Forest")]))


    # Inside Town
    # Note: for every street, connections to other streets are not connected
    # this is because the walkable town randomization rule

    # Other
    world_regions.append(park := Area(DoLRegionNames.park))
    world_regions.append(beach := Area(DoLRegionNames.beach))


    # Drainage and Alleyways
    world_regions.append(residential_drain := Area(DoLRegionNames.residential_drain))
    world_regions.append(commercial_drain := Area(DoLRegionNames.commercial_drain, [
                AreaConnection(residential_drain, note="via Residential Drain from the Commercial Drain")]))
    world_regions.append(industrial_drain := Area(DoLRegionNames.industrial_drain, [
                AreaConnection(commercial_drain, note="via Commercial Drain from the Industrial Drain")]))

    world_regions.append(residential_alleyways := Area(DoLRegionNames.residential_alleyways, [
                AreaConnection(residential_drain, note="via Residential Drain from its Alleyways")]))
    world_regions.append(commercial_alleyways := Area(DoLRegionNames.commercial_alleyways, [
                AreaConnection(commercial_drain, note="via Commercial Drain from its Alleyways"), 
                AreaConnection(residential_alleyways, note="via Residential Alleyways from the Commercial Alleyways")]))
    world_regions.append(industrial_alleyways := Area(DoLRegionNames.industrial_alleyways, [
                AreaConnection(industrial_drain, note="via Industrial Drain from its Alleyways"), 
                AreaConnection(commercial_alleyways, note="via Commercial Alleyways from the Industrial Alleyways")]))


    # Residential
    # Danube Street
    world_regions.append(spa := Area(DoLRegionNames.spa))
    world_regions.append(avery_mansion := Area(DoLRegionNames.avery_mansion)) # TODO: links to this
    world_regions.append(danube_houses := Area(DoLRegionNames.danube_houses))
    world_regions.append(danube_street := Area(DoLRegionNames.danube_street, [
                AreaConnection(spa, note="via the Spa from Danube Street"), 
                AreaConnection(avery_mansion, 
                               ["TODO: requires averyMansionScore() gte 130", "TODO: orphanage access"], 
                               note="via Avery's Mansion from Danube Street"), 
                AreaConnection(danube_houses, note="via Danube Houses from Danube Street"), 
                AreaConnection(forest, note="via Forest from Danube Street"), 
                AreaConnection(residential_alleyways, note="via Residential Alleyways from Danube Street"), 
                AreaConnection(residential_drain, note="via Residential Drain from Danube Street")]))


    # Barb Street
    world_regions.append(tentacle_forest := Area(DoLRegionNames.tentacle_forest))
    world_regions.append(hookah_parlour := Area(DoLRegionNames.hookah_parlour))
    world_regions.append(flats := Area(DoLRegionNames.flats, [
                AreaConnection(hookah_parlour, note="via Hookah Parlour from the Flats")]))
    world_regions.append(dance_studio := Area(DoLRegionNames.dance_studio))
    world_regions.append(police_station := Area(DoLRegionNames.police_station))
    world_regions.append(barb_street := Area(DoLRegionNames.barb_street, [
                AreaConnection(dance_studio, note="via Dance Studio from Barb Street"), 
                AreaConnection(police_station, note="via Police Station from Barb Street"), 
                AreaConnection(flats, note="via Flats from Barb Street"), 
                AreaConnection(residential_alleyways, note="via Residential Alleyway from Barb Street"), 
                AreaConnection(residential_drain, note="via Residential Drain from Barb Street")]))


    # Domus Street  
    # note: not connecting tentacle plains here due to randomization
    world_regions.append(orphanage := Area(DoLRegionNames.orphanage))
    world_regions.append(domus_houses := Area(DoLRegionNames.domus_houses))
    world_regions.append(domus_street := Area(DoLRegionNames.domus_street, [
                AreaConnection(orphanage, note="via Orphanage from Domus Street"), 
                AreaConnection(domus_houses, note="via Domus Houses from Domus Street"), 
                AreaConnection(residential_alleyways, note="via Residential Alleyways from Domus Street"),
                AreaConnection(residential_drain, note="via Residential Drain from Domus Street")]))

    # Commercial
    # Connudatus Street
    world_regions.append(strip_club := Area(DoLRegionNames.strip_club))
    world_regions.append(connudatus_street := Area(DoLRegionNames.connudatus_street, [
                AreaConnection(strip_club, 
                               [DoLRules.fakeid],
                               note="via Strip Club from Connudatus Street"), 
                AreaConnection(commercial_drain, note="via Commercial Drain from Connudatus Street"), 
                AreaConnection(residential_alleyways, note="via Residential Alleyways from Connudatus Street"), 
                AreaConnection(commercial_alleyways, note="via Commercial Alleyways from Connudatus Street")]))

        # Starfish Street
    world_regions.append(arcade := Area(DoLRegionNames.arcade))
    world_regions.append(chalets := Area(DoLRegionNames.chalets))
    world_regions.append(dog_pound := Area(DoLRegionNames.dog_pound))
    world_regions.append(starfish_street := Area(DoLRegionNames.starfish_street, [
                AreaConnection(arcade, note="via Arcade from Starfish Street"), 
                AreaConnection(chalets, note="via Chalets from Starfish Street"), 
                AreaConnection(dog_pound, note="via Dog Pound from Starfish Street"), 
                AreaConnection(beach, note="via Beach from Starfish Street"), 
                AreaConnection(park, note="via Park from Starfish Street"), 
                AreaConnection(commercial_drain, note="via Commercial Drain from Starfish Street")]))


    # Cliff Street
    world_regions.append(mayors_office := Area(DoLRegionNames.mayors_office))
    world_regions.append(cafe := Area(DoLRegionNames.cafe))
    world_regions.append(cliff_street := Area(DoLRegionNames.cliff_street, [
                AreaConnection(mayors_office, note="via Mayor's Office from Cliff Street"), 
                AreaConnection(cafe, note="via Cafe from Cliff Street"), 
                AreaConnection(beach, note="via Beach from Cliff Street"), 
                AreaConnection(commercial_drain, note="via Commercial Drain from Cliff Street"), 
                AreaConnection(commercial_alleyways, note="via Commercial Alleyways from Cliff Street")]))


    # High Street
    world_regions.append(shopping_centre_rooftop := Area(DoLRegionNames.shopping_centre_rooftop)) # TODO: rooftop connections
    shops.append(shopping_centre_hairdressers := Area(DoLRegionNames.shopping_centre_hairdressers))
    shops.append(shopping_centre_petshop := Area(DoLRegionNames.shopping_centre_petshop))
    shops.append(shopping_centre_tattooparlour := Area(DoLRegionNames.shopping_centre_tattooparlour))
    shops.append(shopping_centre_furnitureshop := Area(DoLRegionNames.shopping_centre_furnitureshop))
    shops.append(shopping_centre_supermarket := Area(DoLRegionNames.shopping_centre_supermarket))
    shops.append(shopping_centre_clothingshop := Area(DoLRegionNames.shopping_centre_clothingshop))
    shops.append(shopping_centre_tailor := Area(DoLRegionNames.shopping_centre_tailor))
    shops.append(shopping_centre_cosmeticsshop := Area(DoLRegionNames.shopping_centre_cosmeticsshop))
    shops.append(shopping_centre_toystore := Area(DoLRegionNames.shopping_centre_toystore))
    # don't put shopping_centre_x in world_regions because option to determine if we want to randomize its connections or not
    # we can put shopping_centre in however because we will not be hosting the connections there
    world_regions.append(shopping_centre := Area(DoLRegionNames.shopping_centre, [
                AreaConnection(shopping_centre_rooftop, note="via Rooftop from Shopping Centre")]))
    
    # need connections after decleration
    shopping_centre_hairdressers.append(AreaConnection(shopping_centre, note="via Hairdressers from Shopping Centre"))
    shopping_centre_petshop.append(AreaConnection(shopping_centre, note="via Pet Shop from Shopping Centre"))
    shopping_centre_tattooparlour.append(AreaConnection(shopping_centre, note="via Tattoo Parlour from Shopping Centre"))
    shopping_centre_furnitureshop.append(AreaConnection(shopping_centre, note="via Furniture Shop from Shopping Centre"))
    shopping_centre_supermarket.append(AreaConnection(shopping_centre, note="via Supermarket from Shopping Centre"))
    shopping_centre_clothingshop.append(AreaConnection(shopping_centre, note="via Clothing Shop from Shopping Centre"))
    shopping_centre_tailor.append(AreaConnection(shopping_centre, note="via Tailor from Shopping Centre"))
    shopping_centre_cosmeticsshop.append(AreaConnection(shopping_centre, note="via Cosmetics Shop from Shopping Centre"))
    shopping_centre_toystore.append(AreaConnection(shopping_centre, note="via Toy Store from Shopping Centre"))

        
    world_regions.append(office_building := Area(DoLRegionNames.office_building))
    world_regions.append(high_street := Area(DoLRegionNames.high_street, [
                AreaConnection(office_building, note="via Office Building from High Street"), 
                AreaConnection(shopping_centre, note="via Shopping Centre from High Street"), 
                AreaConnection(park, note="via Park from High Street"), 
                AreaConnection(commercial_drain, note="via Commercial Drain from High Street"), 
                AreaConnection(commercial_alleyways, note="via Commercial Alleyways from High Street")]))


    # Nightingale Street
    # don't connect pharmacy here because option to determine if we want to randomize this or not
    shops.append(pharmacy := Area(DoLRegionNames.pharmacy))
    world_regions.append(hospital := Area(DoLRegionNames.hospital))
    world_regions.append(photography_studio := Area(DoLRegionNames.photography_studio))
    world_regions.append(nightingale_street := Area(DoLRegionNames.nightingale_street, [
                AreaConnection(hospital, note="via Hospital from Nightingale Street"), 
                AreaConnection(photography_studio, 
                               ["TODO: photgraphy studio discovery"],
                               note="via Photography Studio from Nightingale Street"), 
                AreaConnection(forest, note="via Forest from Nightingale Street"), 
                AreaConnection(park, note="via Park from Nightingale Street"), 
                AreaConnection(commercial_drain, note="via Commercial Drain from Nightingale Street"), 
                AreaConnection(commercial_alleyways, note="via Commercial Alleyways from Nightingale Street")]))
    pharmacy.append(AreaConnection(hospital, note="via Pharmacy in Hospital"))


    # Wolf Street
    world_regions.append(temple := Area(DoLRegionNames.temple))
    world_regions.append(soup_kitchen := Area(DoLRegionNames.soup_kitchen))
    world_regions.append(wolf_street := Area(DoLRegionNames.wolf_street, [
                AreaConnection(temple, note="via Temple from Wolf Street"), 
                AreaConnection(soup_kitchen, note="via Soup Kitchen from Wolf Street"), 
                AreaConnection(forest, note="via Forest from Wolf Street"), 
                AreaConnection(commercial_drain, note="via Commercial Drain from Wolf Street"), 
                AreaConnection(commercial_alleyways, note="via Commercial Alleyways from Wolf Street")]))


    # Oxford Street
    world_regions.append(school := Area(DoLRegionNames.school, [
                AreaConnection(park, note="via Park from School"), 
                AreaConnection(industrial_alleyways, note="via Industrial Alleyways from School"), 
                AreaConnection(commercial_drain, 
                               [DoLRules.history_3],
                               note="via Commercial Drain from School Toilets")]))
    world_regions.append(museum := Area(DoLRegionNames.museum))
    world_regions.append(oxford_street := Area(DoLRegionNames.oxford_street, [
                AreaConnection(school, note="via School from Oxford Street"), 
                AreaConnection(museum, note="via Museum from Oxford Street"), 
                AreaConnection(commercial_alleyways, note="via Commercial Alleyways from Oxford Street"),
                AreaConnection(commercial_drain, note="via Commercial Drain from Oxford Street"), 
                AreaConnection(industrial_alleyways, note="via Industrial Alleyways from Oxford Street"), 
                AreaConnection(park, note="via Park from Oxford Street"),
                AreaConnection(forest_lake, 
                               connection_type="entrance", 
                               note="via Forest Lake from Oxford Street Afterschool Students"), # student walking to lake
                AreaConnection(orphanage, 
                               connection_type="entrance",
                               note="via Orphanage from Oxford Street Afterschool Robin"), # :: Robin Walk School 
                ]))
    
    # Industrial
    # Harvest Street
    world_regions.append(brothel := Area(DoLRegionNames.brothel))
    world_regions.append(pub := Area(DoLRegionNames.pub))
    world_regions.append(bus_station := Area(DoLRegionNames.bus_station))
    world_regions.append(factory := Area(DoLRegionNames.factory))
    world_regions.append(harvest_street := Area(DoLRegionNames.harvest_street, [
                AreaConnection(brothel, note="via Brothel from Harvest Street"), 
                AreaConnection(pub, note="via Pub from Harvest Street"), 
                AreaConnection(bus_station, note="via Bus Station from Harvest Street"), 
                AreaConnection(factory, note="via Factory from Harvest Street"), 
                AreaConnection(industrial_drain, note="via Industrial Drain from Harvest Street"), 
                AreaConnection(industrial_alleyways, note="via Industrial Alleyways from Harvest Street"),
                AreaConnection(farmlands_road, note="via Farmlands Road")]))

    # Mer Street
    world_regions.append(docks := Area(DoLRegionNames.docks, [
                AreaConnection(ocean, 
                               [DoLRules.skulduggery_4], 
                               "exit",
                               "via Ocean from Docks")]))
    world_regions.append(coastal_path := Area(DoLRegionNames.coastal_path, [
                AreaConnection(meadow, note="via Meadow from Costal Path")]))
    world_regions.append(mer_street := Area(DoLRegionNames.mer_street, [
                AreaConnection(docks, note="via Docks from Mer Street"), 
                AreaConnection(coastal_path, 
                               [DoLRules.history_4],
                               note="via Costal Path from Mer Street"), 
                AreaConnection(industrial_alleyways, note="via Industrial Alleyways from Mer Street"), 
                AreaConnection(industrial_drain, note="via Industrial Drain from Mer Street")]))

    # Elk Street
    world_regions.append(landfill := Area(DoLRegionNames.landfill)) #
    world_regions.append(adult_shop := Area(DoLRegionNames.adult_shop))
    world_regions.append(compound := Area(DoLRegionNames.compound))
    world_regions.append(
            elk_street := Area(DoLRegionNames.elk_street, [
                AreaConnection(landfill, 
                               ["TODO: landfill discovery"], 
                               note="via Landfill from Mer Street"), 
                AreaConnection(adult_shop, 
                               ["TODO: adult shop built"],
                               note="via Adult Shop from Mer Street"), 
                AreaConnection(compound,
                               ["TODO: compound discovery"],
                               note="via Compound from Mer Street"),
                AreaConnection(industrial_alleyways,
                               note="via Industrial Alleyways from Mer Street"), 
                AreaConnection(industrial_drain,
                               note="via Industrial Drain from Mer Street")]))


    in_town_regions = [danube_street, barb_street, domus_street, 
            starfish_street, cliff_street, high_street,
            nightingale_street, wolf_street, connudatus_street,
            oxford_street, harvest_street, mer_street,
            elk_street]

    in_town_connections:list[AreaConnection] = []
    for street in in_town_regions:
        in_town_connections.append(AreaConnection(street))


    # All possible arresting location:
        # beach, if you do the beach fallus for science project, you can get arrested for it if you pick a cop, evil logic
        # via brothel raid (straight to cell) (:: Brothel Raid)
        # via docks (hospital arrest) (:: Docks Caught)
        # $bus to hospital in orphanage (hospital arrest)
        # hospital: stay from trauma/faint, stay overnight, winning fight against bailey (hospital arrest)
        # via bondage event (:: Bondage Police Willing)
        # voa cliff street if the chef hates you and have crime built up (:: Cliff Street, Chef Police Journey)
        # random cop street car prostitution (:: Street Car Sex Police (widget "streetProstitutionProposition"))
        # connudatus? street widget "streetpolice"
        # cliff street if chef is met and high sus and rage (hospital arrest) 
    
    # police_station.extend([ # TODO: police connections
    #
    # ])
    

    # Extra definitions of logic functions

    class RandomizationPool:
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
            print(f"Randomization pool started randomization containing {self.arealist[0].name()}")
            if world.options.pool_onewayrandomization:
                for pooltype in self.seperate(self.arealist):
                    self.shuffleback(self.strip(pooltype))
            else:
                self.shuffleback(self.strip(self.arealist))
            return self.arealist

    

    def badend_connections():

        # entrances:

        # prison: 1
        # logic is hospital for high arrest chance
        prison.extend([
            AreaConnection(hospital, connection_type="entrance", note="via Being caught by Police or Turning yourself in with >=5000 Crime Score") # :: Police Prison Intro
        ])  

        # island: 2
        island.extend([
            AreaConnection(pirate_ship, connection_type="entrance", note="via: On the Pirate Ship, passout or become a mate and asking Zephyr") # :: Pirate Passout Wake, Pirate End Run, Pirate End Islanders
        ])  

        # underground_brothel: 3
        # :: Underground Intro
        # :: Briar Hack Fail can be included but can become impossible,
        #    just make sure to send this passage / add purpose fail
        underground_brothel.extend([
            AreaConnection(orphanage, connection_type="entrance", note="via Failing to pay Bailey"), # :: Rent Intro ($rentsale)
            AreaConnection(hospital, connection_type="entrance", note="via Failing to run from the Hospital Police") # :: Hospital Arrest Molestation Finish
        ])

        # asylum: 4
        # faints can lead to hospital leading to asylum
        asylum.extend([
            AreaConnection(hospital, connection_type="entrance", note="via Harper abduction") # :: Asylum Intro
        ])  

        # dog_pound_ending: 5
        # require wolf TF for Pound Abduction
        # **if add, fix extend**
        dog_pound_ending.extend([
            AreaConnection(dog_pound, connection_type="entrance", note="via Having 'fun' with the Dog Pound Dogs, often close to closing time")  # :: Pound Assault Caught
        ]) 
        for street in in_town_regions: # :: Pound Abudction
            dog_pound_ending.append(AreaConnection(street, [DoLRules.wolf_tf], connection_type="entrance", note="via Abduction with Wolf Appearance"))

        # mines: 6
        mines.extend([
            AreaConnection(flats, connection_type="entrance", note="via Abduction in the Flats") # :: Flats Auction 8
        ])  

        # eden_cabin: 7
        eden_cabin.extend([
            AreaConnection(forest, connection_type="entrance", note="via Meeting Eden in the Forest"), # :: Forest Hunter Molestation Finish
            AreaConnection(orphanage, connection_type="entrance", note="via Failing to pay Bailey")  # :: rentsale ($rentsale 1) via widget"rentEdenTrade"
        ])

        # kylar_manor: 8
        # requires meeting kylar so school required
        kylar_manor.extend([
            AreaConnection(school, connection_type="entrance", note="via Kylar Abduction") # :: Kylar Abduction Intro via widget"kylarwatched"
        ])

        # pirate_ship: 9
        pirate_ship.extend([
            AreaConnection(ocean, connection_type="entrance", note="via Passing out in the ocean"),  # :: Pirate Intro (Passout Pirates Hot Cold, Passout Pirate)
            AreaConnection(pub, ["TODO: rule temple access"], "entrance", "via Meeting Zephyr in the Pub, knowing about the Spear")  # :: Smuggler Pub Zephyr
        ])

        # bird_tower: 10
        bird_tower.extend([
            AreaConnection(moor, connection_type="entrance", note="via Abduction from the Great Hawk") # :: Bird Capture, Moor Bird Wake
        ])

        # remy_farm: 11
        # all lead to Livestock Intro, however badendtracking starts beforehand on passages below,
        # meaning badendtracking for this may have to be redone and placed in livestock intro
        #
        # TODO: figure out how I wanna handle these extra passages, 
        # many ways to enter from multiple places that just go through the same passage
        # CHEAT REQUIREMENT, do not include: bus station -> Street Van Journey
        # Pub White Pill Van -> Street Van Journey
        # intown -> Street Van Help -> Street Van Journey
        #
        # Street Van Journey -> Street Van Fight Finish, Street Van Submit -> Livestock Intro
        remy_farm.extend([
            AreaConnection(orphanage, connection_type="entrance", note="via Failing to pay Bailey"),  # :: Street Van Bailey
            AreaConnection(moor, connection_type="entrance", note="via Abduction in the Moor"),       # :: Moor Abduction Remy Wake
            AreaConnection(remy_farm, # TODO: remy estate
                           connection_type="entrance", note="via Passing out or losing blackjack in Remy's Estate"),  # :: Passout Estate Remy Hot Cold, widget"blackjackCaughtCheatingSurrender"
            AreaConnection(cliff_street, ["TODO: rule access cafe"], "entrance", "via Making Sam mad and being on Cliff Street"),  # :: Chef Blackmail Livestock 2
            AreaConnection(pub, ["TODO: rng entrance"], "entrance", "via Getting drunk at the pub, someone taking you home, then taking their White Pill")
        ])
        for street in in_town_regions:
            remy_farm.append(AreaConnection(street, ["TODO: rng entrance"], "entrance", "via Abduction while helping someone unload their Van"))


        # wolf_cave: 12
        # unable to enter if monster people or bestiality are disabled
        if world.options.bestiality:
            wolf_cave.extend([
                AreaConnection(forest, connection_type="entrance", note="via Wolves in the Forest") # :: Forest Wolf Cave Intro
            ])


        # exits:
        
        # prison: 1
        prison.extend([
            AreaConnection(orphanage, connection_type="exit", note="via Leaving the Prison normally"), # :: Prison End Car Silent, Prison End Car Thank, Prison End Car Angry
            AreaConnection(docks, connection_type="exit", note="via Leaving the Prion with the Boat"), # :: Prison Kylar Escape Ask, Prison Kylar Escape Nod, Prison Wren Escape 3
            # note: 2 ocean connections, however one doesn't require swimming 10
            AreaConnection(ocean, [DoLRules.swimming_10], "exit", "via Swimming away the Prison"), # :: Prison Escape
            AreaConnection(ocean, connection_type="exit", note="via Passing out in the Prison's rut"), # ::Passout Rut 2
            AreaConnection(beach, [DoLRules.flight], "exit", "via Flying away from the Prison") # :: Prison Soar Escape
        ])

        # island: 2
        island.extend([
            AreaConnection(pirate_ship, connection_type="exit", note="via Handing over the spear to Zephyr"), # :: Islander End Hand
            AreaConnection(mer_street, connection_type="exit", note="via Sailing away in a Raft from the Island"), # :: Island Sail
            AreaConnection(ocean, connection_type="exit", note="via Successfully running with the Island Spear"), # :: Islander End Swim, Islander End Throw, Islander Enforce (req: Angel tf)
            AreaConnection(hospital, [DoLRules.pregnancy_toggle], "exit", note="via Leaving the Island due to Pregnancy") # :: Pregnancy Island
        ])

        # underground_brothel: 3
        underground_brothel.extend([
            AreaConnection(ocean, connection_type="exit", note="via Digging out from the Underground Brothel"), # :: Underground Lake
            AreaConnection(forest, connection_type="exit", note="via Running to the Forest from the Underground Brothel") # :: Underground Presentation Molestation Finish, Underground Hunt, Underground Cell Sneak, widget "undergroundEscapeForestStart"
        ])

        # asylum: 4
        asylum.extend([
            AreaConnection(forest, connection_type="exit", note="via Running from the Asylum"), # :: Asylum Escape, Tentacle Escape, Tentacle Wolf Escape, Eden Asylum Rescue
            AreaConnection(orphanage, connection_type="exit", note="via Leaving the Asylum to the Orphanage") # :: Asylum Return, Pregnancy Birth Asylum End (req: preg), Tentacle Plains Resist
        ])

        # dog_pound_ending: 5
        dog_pound_ending.extend([
            AreaConnection(starfish_street, connection_type="exit", note="via Escaping the Dog Pound Bad-End") # :: Pound Escape Front, Pound Escape Free Dress, Pound Escape Free No Dress
        ])

        # mines: 6
        mines.extend([
            AreaConnection(residential_drain, connection_type="exit", note="via Escaping from the Guards or Passing out in the Mines"), # :: Mines Guards Escape, Mines Passout Warn 3, Mines Passout Run 2
            AreaConnection(flats, connection_type="exit", note="via Escaping from the Mines") # :: Mines Escape
        ])

        # eden_cabin: 7
        eden_cabin.extend([
            AreaConnection(forest, connection_type="exit", note="via Running from Eden's Cabin") # :: Cabin Night Escape, Eden Cabin Escape, widget"clearingactions" above Eden Cabin Escape
        ])

        # kylar_manor: 8
        # note: Kylar Abduction Stockholm End (one time event) leads to the park
        # :: Kylar Abduction Release 4, Kylar Abduction Free Rescue [Thank, Angry, Silent, Reassure, Mock], Kylar Abduction Free Leave 2, TODO: non escape
        kylar_manor.extend([
            AreaConnection(danube_street, connection_type="exit", note="via Running or Leaving Kylar's Mansion") 
        ])

        # pirate_ship: 9
        # exit to island is already an entrance from island, so it does not need to be randomized
        pirate_ship.extend([
            #AreaConnection(island, connection_type="exit", note="via: On the Pirate Ship, passout or become a mate and asking Zephyr"), # :: Pirate Passout Wake, Pirate End Run, Pirate End Islanders
            AreaConnection(ocean, connection_type="exit", note="via Diving from the Pirate Ship"), # :: Pirate Railing Dive Night, Pirate Railing Dive Day
            AreaConnection(mer_street, connection_type="exit", note="via Having Zephyr return you to town") # :: Pirate Return
        ])

        # bird_tower: 10
        # (leaving -> "castle" -> moor), Bird Tower [Farmlands, Forest, Town]
        bird_tower.extend([
            AreaConnection(farmlands, [DoLRules.flight], "exit", note="via flying from the Great Hawk's Tower"), # :: Bird Tower Farmlands
            AreaConnection(moor, connection_type="exit", note="via leaving the Great Hawk's Tower") # :: Bird Tower Rope Escape, Bird Tower Base Leave, Bird Tower Glide ['', 2]
        ])

        # remy_farm: 11
        # eden escape possible, but requires access to eden regardless
        remy_farm.extend([
            AreaConnection(forest, connection_type="exit", note="via Escaping Remy's Farm") # all lead to :: Livestock Escape Town
        ])

        # wolf_cave: 12
        # unable to enter if monster people or bestiality are disabled
        if world.options.bestiality:
            wolf_cave.extend([
                AreaConnection(forest, connection_type="exit", note="via Running from the Wolves Cave"), # :: Forest Wolf Cave Rape End, Forest Wolf Cave Escape
                AreaConnection(ocean, connection_type="exit", note="via Digging out from the Wolves Cave") # :: Wolf Cave Descent
            ])

        
        # check if we want to randomize these badend connections after connecting them
        # don't randomize if we have badend entrances also just randomized, because then its just effectively doing the same thing
        if world.options.randomize_badends and not world.options.randomize_entrances_badends:
            badends = RandomizationPool(badends).run()

    def tentacle_connections():
        asylum.append(
            AreaConnection(tentacle_plains, [DoLRules.tentacles_toggle], "exit"))
        hookah_parlour.append(
            AreaConnection(tentacle_forest, [DoLRules.tentacles_toggle]))
        orphanage.append(
            AreaConnection(tentacle_plains, [DoLRules.deviancy_5, DoLRules.tentacle_plains]))

    def walkabletown_connections():
        # includes connections backwards aswell as forwards
        # this does mean it would be possible to have connections that lead into themselves, but should be funny
        # column 1
        domus_street.extend([
                             AreaConnection(barb_street), AreaConnection(danube_street)])
        # column 2
        barb_street.extend([ #AreaConnection(domus_street),
                            AreaConnection(cliff_street), AreaConnection(connudatus_street)]) 
        danube_street.extend([ #AreaConnection(domus_street),
                              AreaConnection(wolf_street), AreaConnection(connudatus_street)])
        # column 3
        connudatus_street.extend([ #AreaConnection(danube_street), AreaConnection(barb_street),
                                  AreaConnection(cliff_street), AreaConnection(wolf_street)]) 
        # column 4
        cliff_street.extend([ #AreaConnection(barb_street), AreaConnection(connudatus_street),
                             AreaConnection(starfish_street), AreaConnection(high_street)]) 
        wolf_street.extend([ #AreaConnection(danube_street), AreaConnection(connudatus_street),
                            AreaConnection(nightingale_street), AreaConnection(high_street)])
        # column 5
        high_street.extend([ #AreaConnection(cliff_street), AreaConnection(wolf_street),
                            AreaConnection(starfish_street), AreaConnection(nightingale_street)]) 
        # column 6
        starfish_street.extend([ #AreaConnection(cliff_street), AreaConnection(high_street),
                                AreaConnection(oxford_street), AreaConnection(mer_street)]) 
        nightingale_street.extend([ # AreaConnection(wolf_street), AreaConnection(high_street),
                                   AreaConnection(oxford_street), AreaConnection(elk_street)])
        # column 7
        oxford_street.extend([ #AreaConnection(starfish_street), AreaConnection(nightingale_street),
                              AreaConnection(mer_street), AreaConnection(elk_street)])
        # column 8
        mer_street.extend([ #AreaConnection(starfish_street), AreaConnection(oxford_street), 
                          AreaConnection(harvest_street)]) 
        elk_street.extend([ #AreaConnection(nightingale_street), AreaConnection(oxford_street), 
                          AreaConnection(harvest_street)])
        # column 9
        # harvest_street.extend([AreaConnection(mer_street), AreaConnection(elk_street)
        #                        ])
            

    # -------- Start: Randomization --------

    if not world.options.walkable_town: walkabletown_connections()
    if world.options.randomize_entrances_badends: 
        badend_connections()
        world_regions.extend(badends)
    if world.options.randomize_tentacleareas: tentacle_connections()
    if world.options.shop_locations == 2: world_regions.extend(shops)
    if world.options.randomize_entrances: world_regions = RandomizationPool(world_regions).run()

    # -------- Post: World Randomization --------

    if world.options.shop_locations == 1: shops = RandomizationPool(shops).run()

    # -------- Post: Randomization --------
    world_regions.extend(shops)

    # add connections to hospital via fainting in the street
    # don't not include nightingale, because the hospital might of been randomzied away!
    for reg in in_town_regions: 
        # print(f"adding {reg.name()}'s connection to Hospital")
        reg.append(AreaConnection(hospital, connection_type="entrance", note="via Fainting"))

    if world.options.walkable_town: walkabletown_connections()
    if not world.options.randomize_entrances_badends: 
        badend_connections()
        world_regions.extend(badends)
    if not world.options.randomize_tentacleareas: tentacle_connections()

    world_regions.append(in_town := Area(DoLRegionNames.in_town, [
        AreaConnection(domus_street), AreaConnection(barb_street), AreaConnection(danube_street),
        AreaConnection(connudatus_street), AreaConnection(cliff_street), AreaConnection(wolf_street),
        AreaConnection(high_street), AreaConnection(starfish_street), AreaConnection(nightingale_street),
        AreaConnection(oxford_street), AreaConnection(mer_street), AreaConnection(elk_street),
        AreaConnection(harvest_street)
    ])) # debug region used for some checks to determine that this character is in town

    for reg in world_regions:
        # subareas = []
        # if len(reg.sub_regions) > 0:
        #     print(reg.sub_regions[0].return_areaName())
        # for sub in reg.sub_regions:
        #     subareas.append(sub.return_areaName())
        # print(f"attempting to connect {reg.name()} with connections {subareas}")
        reg.connect()
        reg.add_to_multiworld()
    
