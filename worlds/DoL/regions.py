from typing import TYPE_CHECKING
from BaseClasses import Entrance, Region
from enum import StrEnum
from rule_builder import rules
from rules import DoLRules

if TYPE_CHECKING:
    from .world import DoLWorld

class DoLRegion_Names(StrEnum):
    town = "Town"

    # Residential
        # Danube Street
    danube_street = "Danube Street"
    spa = "Spa"
    kylar_manor = "Kylar's Manor"
    avery_mansion = "Avery's Mansion"
    danube_houses = "Danube Street Houses"

        # Connudatus Street
    connudatus_street = "Connudatus Street"
    strip_club = "Strip Club"

        # Barb Street
    barb_street = "Barb Street"
    dance_studio = "Dance Studio"
    police_station = "Police Station"
    flats = "Flats"
    hookah_parlour = "Hookah Parlour"
    tentacle_forest = "Tentacle Forest"

        # Domus Street  
    domus_street = "Domus Street"
    orphanage = "Orphanage" # technically correct starting location
    domus_houses = "Domus Street Houses"

        # Backalleys
    residential_alleyways = "Residential Alleyways"
    residential_drain = "Residential Drain System"

    # Commercial
        # Starfish Street
    starfish_street = "Starfish Street"
    arcade = "Arcade"
    chalets = "Chalets"
    dog_pound = "Dog Pound"

        # Cliff Street
    cliff_street = "Cliff Street"
    mayors_office = "Mayor's Office"
    cafe = "Cafe"

        # High Street
    high_street = "High Street"
    office_building = "Office Building"
    shopping_centre = "Shopping Centre"
    shopping_centre_rooftop = "Shopping Centre Rooftop"
    shopping_centre_hairdressers = "Shopping Centre Hairdressers"
    shopping_centre_petshop = "Shopping Centre Pet Shop"
    shopping_centre_tattooparlour = "Shopping Centre Tattoo Parlour"
    shopping_centre_furnitureshop = "Shopping Centre Furniture Shop"
    shopping_centre_supermarket = "Shopping Centre Supermarket"
    shopping_centre_clothingshop = "Shopping Centre Clothing Shop"
    shopping_centre_tailor = "Shopping Centre Tailor"
    shopping_centre_cosmeticsshop = "Shopping Centre Cosmetics Shop"
    shopping_centre_toystore = "Shopping Centre Toystore"

        # Nightingale Street
    nightingale_street = "Nightingale Street"
    hospital = "Hospital"
    pharmacy = "Pharmacy"
    photography_studio = "Photography Studio"

        # Wolf Street
    wolf_street = "Wolf Street"
    temple = "Temple"
    # soup kitchen requires discovery
    soup_kitchen = "Soup Kitchen"

        # Oxford Street
    oxford_street = "Oxford Street"
    school = "School"
    museum = "Museum"

        # Backalleys
    commercial_alleyways = "Commercial Alleyways"
    commercial_drain = "Commercial Drain System"

        # Other
    park = "Park"
    beach = "Beach"

    # Industrial
        # Harvest Street
    harvest_street = "Harvest Street"
    brothel = "Brothel"
    pub = "Pub"
    bus_station = "Bus Station"
    factory = "Factory"

        # Mer Street
    mer_street = "Mer Street"
    docks = "Docks"
    coastal_path = "Coastal Path"

        # Elk Street
    elk_street = "Elk Street"
    landfill = "Landfill"
    adult_shop = "Adult Shop"
    compound = "Compound"

        # Backalleys
    industrial_alleyways = "Industrial Alleyways"
    industrial_drain = "Industrial Drain System"

    # Outside Town
        # Forest
    forest = "Forest"
    forest_shop = "Forest Shop"
    forest_lake = "Forest Lake"
    wolf_cave = "Black Wolf's Cave"
    eden_cabin = "Eden's Cabin"

        # Ocean
    ocean = "Ocean"

        # Outskirts
            # Farmlands
    farmlands = "Farmlands"
    alex_farm = "Alex's Farm"
    riding_school = "Riding School"
    meadow = "Meadow"
    manors = "Manors"
    farmlands_road = "Road to the Farmlands"
            # Moor
    moor = "Moor"
    bird_tower = "Great Hawk's Tower" # include "castle" as apart of the tower
    remy_farm = "Remy's Farm"

        # Other Regions
    bog = "The Bog"
    tentacle_plains = "Tentacle Plains"

        # Soft Bad Ends
    # Prison and Island goes to ocean
        # Prison is accessable from anywhere in town you can get arrested (just town for now I guess)
    prison = "Prison"
        # Island requires getting to the pirate ship, which requires passing out in ocean or going to the smugglers pub
    island = "Island"
    # Brothel and Asylum goes to forest
        # Brothel requires failing Bailey 4 times, requires access to the orphanage
    underground_brothel = "Underground Brothel"
        # Asylum just requires passing out, just link access to town?
    asylum = "Asylum"
    # Goes to dogpound
        # Requires dogpound to enter
    dog_pound_ending = "Dog Pound Soft Bad End"
    # Goes to Residential Drain
        # Requires Flats to enter
    mines = "The Mines"
    # Goes to Ocean or Island
        # Requires Ocean or Smugglers Den to enter
    pirate_ship = "Pirate Ship"


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

        def __init__(self, area:"Area", rules:list[DoLRules] = [], connection_type:str = ""):
            self.area = area
            self.rules = rules
            self.connection_type = connection_type

        def has_rules(self):
            return True if not self.rules else False

        def append_rules(self, rule:DoLRules):
            self.rules.append(rule)

        def extend_rules(self, rules:list[DoLRules]):
            self.rules.extend(rules)

        def pop_rules(self):
            rules = self.rules
            self.rules = []
            return rules

        def change_connectionType(self, connection_type:str):
            self.connection_type = connection_type

        def return_area(self):
            return self.area

        def return_areaName(self):
            return self.area.name()

        def return_areaRegion(self):
            return self.area.return_region()

        def return_connectionType(self):
            return self.connection_type



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

        

        def __init__(self, region_name:str, sub_regions:list[AreaConnection] = []):
            self.region_name = region_name
            self.sub_regions = sub_regions

            self_region = Region(self.region_name, player, multiworld)
            self.self_region = self_region

        def name(self):
            return self.region_name

        def add_to_multiworld(self):
            """
            Adds the **finalized** region to the multiworld
            """
            multiworld.regions.append(self.self_region)

        def connect(self):
            for i in self.sub_regions:
                self.designate_connections(i)

        def designate_connections(self, connection:AreaConnection):
            """
            Leave blank for a normal connection
            connection_type (optional): 'exit' or 'entrance'
            """

            if connection.has_rules():
                # TODO: ADD RULES
                newrule = rules
            else:
                match(connection.return_connectionType()):
                    case "exit":
                        self.self_region.add_exits(connection.return_areaName()) # TODO:
                    case "entrance":
                        connection.return_areaRegion().add_exits(self.name()) # TODO:
                    case _:
                        self.self_region.connect(connection.return_areaName(), f"{connection.return_areaName()} in/at {self.name()}")
                        #outgoingRegion.connect(self.self_region, f"Leaving {outgoingRegion.name} from {self.name()}")

        def extend(self, connection_list:list[AreaConnection]):
            """
            Extends the connection lists

            connection_type: None (normal connection), "exit", or "entrance"
            """
            self.sub_regions.extend(connection_list)

        def append(self, connection:AreaConnection):
            """
            Adds to the connection list

            connection_type: None (normal connection), "exit", or "entrance"
            """
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
    world_regions.append(tentacle_plains := Area(DoLRegion_Names.tentacle_plains)) 
        # Refer to logic at bottom where entrances/exits are
    badends.append(prison := Area(DoLRegion_Names.prison))
    badends.append(island := Area(DoLRegion_Names.island))
    badends.append(underground_brothel := Area(DoLRegion_Names.underground_brothel))
    badends.append(asylum := Area(DoLRegion_Names.asylum ))
    badends.append(dog_pound_ending := Area(DoLRegion_Names.dog_pound_ending))
    badends.append(mines := Area(DoLRegion_Names.mines))
    badends.append(eden_cabin := Area(DoLRegion_Names.eden_cabin))
    badends.append(kylar_manor := Area(DoLRegion_Names.kylar_manor))
    badends.append(pirate_ship := Area(DoLRegion_Names.pirate_ship)) 
    badends.append(bird_tower := Area(DoLRegion_Names.bird_tower))
    badends.append(remy_farm := Area(DoLRegion_Names.remy_farm))
    badends.append(wolf_cave := Area(DoLRegion_Names.wolf_cave))

    # Outside Town
        
    # Forest (danube, wolf, and nightingale street enter forest)
    world_regions.append(forest_shop := Area(DoLRegion_Names.forest_shop))
    world_regions.append(forest_lake := Area(DoLRegion_Names.forest_lake))

    # Don't connect forest shop here incase shop randomizer
    world_regions.append(forest := Area(DoLRegion_Names.forest, [ 
                AreaConnection(forest_lake)]))
    shops.append(forest_shop)
    
    # Ocean
    world_regions.append(ocean := Area(DoLRegion_Names.ocean))

    # Outskirts
        # Farmlands
    world_regions.append(alex_farm := Area(DoLRegion_Names.alex_farm))
    world_regions.append(riding_school := Area(DoLRegion_Names.riding_school))
    world_regions.append(meadow := Area(DoLRegion_Names.meadow))
    world_regions.append(manors := Area(DoLRegion_Names.manors))
    world_regions.append(farmlands_road := Area(DoLRegion_Names.farmlands_road))
    world_regions.append(farmlands := Area(DoLRegion_Names.farmlands, [
                AreaConnection(manors), 
                AreaConnection(meadow), 
                AreaConnection(riding_school), 
                AreaConnection(alex_farm), 
                AreaConnection(farmlands_road)]))

        # Moor
    world_regions.append(moor := Area(DoLRegion_Names.moor))

        # Other Areas
    # bog connects forest to moor, but not back
    world_regions.append(bog := Area(DoLRegion_Names.bog, [
                AreaConnection(moor, ["TODO: moor to bog requires $bogprogress 1"]), 
                AreaConnection(forest, ["TODO: bog can be discovered in forest in a few ways"], "entrance")]))


    # Inside Town
    # Note: for every street, connections to other streets are not connected
    # this is because the walkable town randomization rule
        # Other
    world_regions.append(park := Area(DoLRegion_Names.park))
    world_regions.append(beach := Area(DoLRegion_Names.beach))

        # Drainage and Alleyways
    world_regions.append(residential_drain := Area(DoLRegion_Names.residential_drain))
    world_regions.append(commercial_drain := Area(DoLRegion_Names.commercial_drain, [
                AreaConnection(residential_drain)]))
    world_regions.append(industrial_drain := Area(DoLRegion_Names.industrial_drain, [
                AreaConnection(commercial_drain)]))

    world_regions.append(residential_alleyways := Area(DoLRegion_Names.residential_alleyways, [
                AreaConnection(residential_drain)]))
    world_regions.append(commercial_alleyways := Area(DoLRegion_Names.commercial_alleyways, [
                AreaConnection(commercial_drain), 
                AreaConnection(residential_alleyways)]))
    world_regions.append(industrial_alleyways := Area(DoLRegion_Names.industrial_alleyways, [
                AreaConnection(industrial_drain), 
                AreaConnection(commercial_alleyways)]))


    # Residential
        # Danube Street
    world_regions.append(spa := Area(DoLRegion_Names.spa))
    world_regions.append(avery_mansion := Area(DoLRegion_Names.avery_mansion)) # TODO: links to this
    world_regions.append(danube_houses := Area(DoLRegion_Names.danube_houses))
    world_regions.append(avery_mansion := Area(DoLRegion_Names.avery_mansion))
    world_regions.append(danube_street := Area(DoLRegion_Names.danube_street, [
                AreaConnection(spa), 
                AreaConnection(avery_mansion, ["TODO: requires averyMansionScore() gte 130", "TODO: orphanage access"]), 
                AreaConnection(danube_houses), 
                AreaConnection(forest), 
                AreaConnection(residential_alleyways), 
                AreaConnection(residential_drain)]))

        # Barb Street
    world_regions.append(tentacle_forest := Area(DoLRegion_Names.tentacle_forest))
    world_regions.append(hookah_parlour := Area(DoLRegion_Names.hookah_parlour))
    world_regions.append(flats := Area(DoLRegion_Names.flats, [
                AreaConnection(hookah_parlour)]))
    world_regions.append(dance_studio := Area(DoLRegion_Names.dance_studio))
    world_regions.append(police_station := Area(DoLRegion_Names.police_station))
    world_regions.append(
            barb_street := Area(DoLRegion_Names.barb_street, [
                AreaConnection(dance_studio), 
                AreaConnection(police_station), 
                AreaConnection(flats), 
                AreaConnection(residential_alleyways), 
                AreaConnection(residential_drain)]))

        # Domus Street  
    world_regions.append(orphanage := Area(DoLRegion_Names.orphanage, [
                AreaConnection(tentacle_plains, [DoLRules.deviancy_5, DoLRules.tentacle_plains])]))
    world_regions.append(domus_houses := Area(DoLRegion_Names.domus_houses))
    world_regions.append(domus_street := Area(DoLRegion_Names.domus_street, [
                AreaConnection(orphanage), 
                AreaConnection(domus_houses), 
                AreaConnection(residential_alleyways),
                AreaConnection(residential_drain)]))

    # Commercial
        # Connudatus Street
    world_regions.append(strip_club := Area(DoLRegion_Names.strip_club))
    world_regions.append(connudatus_street := Area(DoLRegion_Names.connudatus_street, [
                AreaConnection(strip_club, [DoLRules.fakeid]), 
                AreaConnection(commercial_drain), 
                AreaConnection(residential_alleyways), 
                AreaConnection(commercial_alleyways)]))

        # Starfish Street
    world_regions.append(arcade := Area(DoLRegion_Names.arcade))
    world_regions.append(chalets := Area(DoLRegion_Names.chalets))
    world_regions.append(dog_pound := Area(DoLRegion_Names.dog_pound))
    world_regions.append(starfish_street := Area(DoLRegion_Names.starfish_street, [
                AreaConnection(arcade), 
                AreaConnection(chalets), 
                AreaConnection(dog_pound), 
                AreaConnection(beach), 
                AreaConnection(park), 
                AreaConnection(commercial_drain)]))


        # Cliff Street
    world_regions.append(mayors_office := Area(DoLRegion_Names.mayors_office))
    world_regions.append(cafe := Area(DoLRegion_Names.cafe))
    world_regions.append(cliff_street := Area(DoLRegion_Names.cliff_street, [
                AreaConnection(mayors_office), 
                AreaConnection(cafe), 
                AreaConnection(beach), 
                AreaConnection(commercial_drain), 
                AreaConnection(commercial_alleyways)]))

        # High Street
    world_regions.append(shopping_centre_rooftop := Area(DoLRegion_Names.shopping_centre_rooftop))
    world_regions.append(shopping_centre_hairdressers := Area(DoLRegion_Names.shopping_centre_hairdressers))
    world_regions.append(shopping_centre_petshop := Area(DoLRegion_Names.shopping_centre_petshop))
    world_regions.append(shopping_centre_tattooparlour := Area(DoLRegion_Names.shopping_centre_tattooparlour))
    world_regions.append(shopping_centre_furnitureshop := Area(DoLRegion_Names.shopping_centre_furnitureshop))
    world_regions.append(shopping_centre_supermarket := Area(DoLRegion_Names.shopping_centre_supermarket))
    world_regions.append(shopping_centre_clothingshop := Area(DoLRegion_Names.shopping_centre_clothingshop))
    world_regions.append(shopping_centre_tailor := Area(DoLRegion_Names.shopping_centre_tailor))
    world_regions.append(shopping_centre_cosmeticsshop := Area(DoLRegion_Names.shopping_centre_cosmeticsshop))
    world_regions.append(shopping_centre_toystore := Area(DoLRegion_Names.shopping_centre_toystore))
    # don't connect here because option to determine if we want to randomize this or not
    world_regions.append(shopping_centre := Area(DoLRegion_Names.shopping_centre))
    shopping_centre_areas = [
                shopping_centre_clothingshop, 
                shopping_centre_furnitureshop, 
                shopping_centre_cosmeticsshop,
                shopping_centre_hairdressers, 
                shopping_centre_petshop, 
                shopping_centre_rooftop,
                shopping_centre_supermarket, 
                shopping_centre_tailor, 
                shopping_centre_tattooparlour,
                shopping_centre_toystore]
    shops.extend(shopping_centre_areas)
    
    world_regions.append(office_building := Area(DoLRegion_Names.office_building))
    world_regions.append(
            high_street := Area(DoLRegion_Names.high_street, [
                AreaConnection(office_building), 
                AreaConnection(shopping_centre), 
                AreaConnection(park), 
                AreaConnection(commercial_drain), 
                AreaConnection(commercial_alleyways)]))

        # Nightingale Street
    # don't connect pharmacy here because option to determine if we want to randomize this or not
    world_regions.append(pharmacy := Area(DoLRegion_Names.pharmacy))
    world_regions.append(hospital := Area(DoLRegion_Names.hospital))
    world_regions.append(photography_studio := Area(DoLRegion_Names.photography_studio))
    world_regions.append(nightingale_street := Area(DoLRegion_Names.nightingale_street, [
                AreaConnection(hospital), 
                AreaConnection(photography_studio, ["TODO: photgraphy studio discovery"]), 
                AreaConnection(forest), 
                AreaConnection(park), 
                AreaConnection(commercial_drain), 
                AreaConnection(commercial_alleyways)]))
    shops.append(pharmacy)

        # Wolf Street
    world_regions.append(temple := Area(DoLRegion_Names.temple))
    world_regions.append(soup_kitchen := Area(DoLRegion_Names.soup_kitchen))
    world_regions.append(wolf_street := Area(DoLRegion_Names.wolf_street, [
                AreaConnection(temple), 
                AreaConnection(soup_kitchen), 
                AreaConnection(forest), 
                AreaConnection(commercial_drain), 
                AreaConnection(commercial_alleyways)]))

        # Oxford Street
    world_regions.append(school := Area(DoLRegion_Names.school, [
                AreaConnection(park), 
                AreaConnection(industrial_alleyways), 
                AreaConnection(commercial_drain, [DoLRules.history_3])]))
    world_regions.append(museum := Area(DoLRegion_Names.museum))
    world_regions.append(oxford_street := Area(DoLRegion_Names.oxford_street, [
                AreaConnection(school), 
                AreaConnection(museum), 
                AreaConnection(commercial_alleyways),
                AreaConnection(commercial_drain), 
                AreaConnection(industrial_alleyways), 
                AreaConnection(park),
                AreaConnection(orphanage), # orphanage and lake are connected via student/robin fast-travel
                AreaConnection(forest_lake)]))
    
    # Industrial
        # Harvest Street
    world_regions.append(brothel := Area(DoLRegion_Names.brothel))
    world_regions.append(pub := Area(DoLRegion_Names.pub))
    world_regions.append(bus_station := Area(DoLRegion_Names.bus_station))
    world_regions.append(factory := Area(DoLRegion_Names.factory))
    world_regions.append(harvest_street := Area(DoLRegion_Names.harvest_street, [
                AreaConnection(brothel), 
                AreaConnection(pub), 
                AreaConnection(bus_station), 
                AreaConnection(factory), 
                AreaConnection(industrial_drain), 
                AreaConnection(industrial_alleyways),
                AreaConnection(farmlands_road)]))

        # Mer Street
    world_regions.append(docks := Area(DoLRegion_Names.docks, [
                AreaConnection(ocean, [DoLRules.skulduggery_4], "exit")]))
    world_regions.append(coastal_path := Area(DoLRegion_Names.coastal_path, [
                AreaConnection(meadow)]))
    world_regions.append(mer_street := Area(DoLRegion_Names.mer_street, [
                AreaConnection(docks), 
                AreaConnection(coastal_path, [DoLRules.history_4]), 
                AreaConnection(industrial_alleyways), 
                AreaConnection(industrial_drain)]))

        # Elk Street
    world_regions.append(landfill := Area(DoLRegion_Names.landfill))
    world_regions.append(adult_shop := Area(DoLRegion_Names.adult_shop))
    world_regions.append(compound := Area(DoLRegion_Names.compound))
    world_regions.append(
            elk_street := Area(DoLRegion_Names.elk_street, [
                AreaConnection(landfill, ["TODO: landfill discovery"]), 
                AreaConnection(adult_shop, ["TODO: adult shop built"]), 
                AreaConnection(compound),
                AreaConnection(industrial_alleyways), 
                AreaConnection(industrial_drain)]))


    in_town = [danube_street, barb_street, domus_street, 
            starfish_street, cliff_street, high_street,
            nightingale_street, wolf_street, connudatus_street,
            oxford_street, harvest_street, mer_street,
            elk_street]

    in_town_connections:list[AreaConnection] = []
    for street in in_town:
        in_town_connections.append(AreaConnection(street))

    # "town" isn't a real place, however this makes it easier for me to connect every single walkable point
    # since if you're in town, you have access to the bus, therefore have access to every stop in town
    # town = Area(DoLRegion_Names.town, in_town_connections)

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
    
    # police_station.extend([ 
    #
    # ])

    # TODO: connections:
    

    # Extra definitions of logic functions

    class RandomizationPool:
        def __init__(self, largearealist:list[Area]):
            self.arealist = largearealist

        def seperate(pool:list[Area]):
            """
            Takes a list of areas, removes its connections, and sorts them into 3 lists based on connection_type
            """
            newpool_normal:list[AreaConnection] = []
            newpool_exit:list[AreaConnection] = []
            newpool_entrance:list[AreaConnection] = []
            for area in pool:
                connections = area.pop_areas()
                for connect in connections:
                    match(connect.return_connectionType()):
                        case("exit"):
                            newpool_exit.append(connect)
                        case("entrance"):
                            newpool_entrance.append(connect)
                        case _:
                            newpool_normal.append(connect)
            return newpool_normal, newpool_exit, newpool_entrance
    
        def strip(self, pool:list[AreaConnection]):
            """
            Function used to strip a list of connections to:
            - A list of size of the connection
            - The list of connections
            - A list of the lists of rules each connection has
            """
            pool_size = len(pool)
            newpool:list[AreaConnection] = []
            pool_rules:list[list[DoLRules]] = []
            for connection in pool:
                # reason for implementation of connections rules like this:
                # since we're gonna just be changing the destination, the requirements to reach the destination still need to be in place
                # for example:
                #   index0: beach   [none]
                #   index1: ocean   [flight]
                #   index2: forest  [skul 5, dev 5]
                # needs to turn to
                #   index0: ocean   [none]
                #   index1: forest  [flight]
                #   index2: beach   [skul 5, dev 5]

                # pool_rules = [[rule], [rule], ...]
                
                pool_rules.append(connection.pop_rules())
                newpool.append(connection) # add the cleaned connections into the pool
            return pool_size, newpool, pool_rules

        def shuffleback(self, pool:list[AreaConnection], pool_size:list[int], pool_rules:list[list[DoLRules]]):
            """
            Takes the original list of areas, the list of connections they all have, the size of area, and the rules for the connections

            Then afterwards, shuffles the connections, and adds them back with their original rules and area size
            """
            world.random.shuffle(pool)
            for areanum, area in enumerate(self.arealist):
                i = 0
                while i < pool_size[areanum]:
                    connection = pool[i]
                    connection.extend_rules(pool_rules.pop(0))
                    area.append(connection)
                    i += 1

        def run(self):
            for pooltype in (self.seperate(self.arealist)):
                self.shuffleback(self.strip(pooltype))
            return self.arealist

    

    def badend_connections():

        # entrances:

        # prison: 1
        # logic is hospital for high arrest chance
        prison.extend([
            AreaConnection(hospital, connection_type="entrance") # :: Police Prison Intro
        ])  

        # island: 2
        island.extend([
            AreaConnection(pirate_ship, connection_type="entrance") # :: Pirate Passout Wake, Pirate End Run, Pirate End Islanders
        ])  

        # underground_brothel: 3
        # :: Underground Intro
        # :: Briar Hack Fail can be included but can become impossible,
        #    just make sure to send this passage / add purpose fail
        underground_brothel.extend([
            AreaConnection(orphanage, connection_type="entrance"),  # :: Rent Intro ($rentsale)
            AreaConnection(hospital, connection_type="entrance")     # :: Hospital Arrest Molestation Finish
        ])

        # asylum: 4
        # faints can lead to hospital leading to asylum
        asylum.extend([
            AreaConnection(hospital, connection_type="entrance") # :: Asylum Intro
        ])  

        # dog_pound_ending: 5
        # require wolf TF for Pound Abduction
        # **if add, fix extend**
        dog_pound_ending.extend([
            AreaConnection(dog_pound, connection_type="entrance")  # :: Pound Assault Caught
        ]) 
        # :: Pound Abudction
        for street in in_town:
            dog_pound_ending.append(AreaConnection(street, [DoLRules.wolf_tf], connection_type="entrance"))

        # mines: 6
        mines.extend([
            AreaConnection(flats, connection_type="entrance") # :: Flats Auction 8
        ])  

        # eden_cabin: 7
        eden_cabin.extend([
            AreaConnection(forest, connection_type="entrance"),    # :: Forest Hunter Molestation Finish
            AreaConnection(orphanage, connection_type="entrance")  # :: rentsale ($rentsale 1) via widget"rentEdenTrade"
        ])

        # kylar_manor: 8
        # requires meeting kylar so school required
        kylar_manor.extend([
            AreaConnection(school, connection_type="entrance") # :: Kylar Abduction Intro via widget"kylarwatched"
        ])

        # pirate_ship: 9
        pirate_ship.extend([
            AreaConnection(ocean, connection_type="entrance"),  # :: Pirate Intro, Passout Pirates Hot Cold
            AreaConnection(pub, ["TODO: rule temple access"], "entrance")  # :: Smuggler Pub Zephyr
        ])

        # bird_tower: 10
        bird_tower.extend([
            AreaConnection(moor, connection_type="entrance") # :: Bird Capture, Moor Bird Wake
        ])

        # remy_farm: 11
        # all lead to Livestock Intro, however badendtracking starts beforehand on passages below,
        # meaning badendtracking for this may have to be redone and placed in livestock intro
        #
        # TODO: figure out how I wanna handle these extra passages, 
        # many ways to enter from multiple places that just go through the same passage
        # bus station -> Street Van Journey
        # Pub White Pill Van -> Street Van Journey
        # intown -> Street Van Help -> Street Van Journey
        # Street Van Journey -> Street Van Fight Finish, Street Van Submit -> Livestock Intro
        remy_farm.extend([
            AreaConnection(orphanage, connection_type="entrance"),  # :: Street Van Bailey
            AreaConnection(moor, connection_type="entrance"),       # :: Moor Abduction Remy Wake
            AreaConnection("TODO: remy estate", connection_type="entrance"),  # :: Passout Estate Remy Hot Cold, widget"blackjackCaughtCheatingSurrender"
            AreaConnection(cliff_street, ["TODO: rule access cafe"], "entrance")  # :: Chef Blackmail Livestock 2
        ])

        # wolf_cave: 12
        wolf_cave.extend([
            AreaConnection(forest, connection_type="entrance") # :: Forest Wolf Cave Intro
        ])


        # exits:
        
        # prison: 1
        prison.extend([
            AreaConnection(orphanage, connection_type="exit"), # :: Prison End Car Silent, Prison End Car Thank, Prison End Car Angry
            AreaConnection(docks, connection_type="exit"), # :: Prison Kylar Escape Ask, Prison Kylar Escape Nod, Prison Wren Escape 3
            AreaConnection(ocean, [DoLRules.swimming_10], "exit"), # :: Prison Escape, Passout Rut 2
            AreaConnection(beach, [DoLRules.flight], "exit") # :: Prison Soar Escape
        ])

        # island: 2
        island.extend([
            AreaConnection(pirate_ship, connection_type="exit"), # :: Islander End Hand
            AreaConnection(mer_street, connection_type="exit"), # :: Island Sail
            AreaConnection(ocean, connection_type="exit"), # :: Islander End Swim, Islander End Throw, Islander Enforce (req: Angel tf)
            AreaConnection(hospital, [DoLRules.pregnancy_toggle], "exit") # :: Pregnancy Island
        ])

        # underground_brothel: 3
        underground_brothel.extend([
            AreaConnection(ocean, connection_type="exit"), # :: Underground Lake
            AreaConnection(forest, connection_type="exit") # :: Underground Presentation Molestation Finish, Underground Hunt, Underground Cell Sneak, widget "undergroundEscapeForestStart"
        ])

        # asylum: 4
        asylum.extend([
            AreaConnection(forest, connection_type="exit"), # :: Asylum Escape, Tentacle Escape, Tentacle Wolf Escape, Eden Asylum Rescue
            AreaConnection(orphanage, connection_type="exit") # :: Asylum Return, Pregnancy Birth Asylum End (req: preg), Tentacle Plains Resist
        ])

        # dog_pound_ending: 5
        dog_pound_ending.extend([
            AreaConnection(starfish_street, connection_type="exit") # :: Pound Escape Front, Pound Escape Free Dress, Pound Escape Free No Dress
        ])

        # mines: 6
        mines.extend([
            AreaConnection(residential_drain, connection_type="exit"), # :: Mines Guards Escape, Mines Passout Warn 3, Mines Passout Run 2
            AreaConnection(flats, connection_type="exit") # :: Mines Escape
        ])

        # eden_cabin: 7
        eden_cabin.extend([
            AreaConnection(forest, connection_type="exit") # :: Cabin Night Escape, Eden Cabin Escape, widget"clearingactions" above Eden Cabin Escape
        ])

        # kylar_manor: 8
        # note: Kylar Abduction Stockholm End (one time event) leads to the park
        # :: Kylar Abduction Release 4, Kylar Abduction Free Rescue [Thank, Angry, Silent, Reassure, Mock], Kylar Abduction Free Leave 2, TODO: non escape
        kylar_manor.extend([
            AreaConnection(danube_street, connection_type="exit") 
        ])

        # pirate_ship: 9
        pirate_ship.extend([
            AreaConnection(island, connection_type="exit"), # :: Pirate End Run, Pirate End Wait
            AreaConnection(ocean, connection_type="exit"), # :: Pirate Railing Dive Night, Pirate Railing Dive Day
            AreaConnection(mer_street, connection_type="exit") # :: Pirate Return
        ])

        # bird_tower: 10
        # (leaving -> "castle" -> moor), Bird Tower [Farmlands, Forest, Town]
        bird_tower.extend([
            AreaConnection(farmlands, [DoLRules.flight], "exit"), # :: Bird Tower Farmlands
            AreaConnection(moor, connection_type="exit") # :: Bird Tower Rope Escape, Bird Tower Base Leave, Bird Tower Glide [ , 2]
        ])

        # remy_farm: 11
        # eden escape possible, but requires access to eden regardless
        remy_farm.extend([
            AreaConnection(forest, connection_type="exit") # all lead to :: Livestock Escape Town
        ])

        # wolf_cave: 12
        wolf_cave.extend([
            AreaConnection(forest, connection_type="exit"), # :: Forest Wolf Cave Rape End, Forest Wolf Cave Escape
            AreaConnection(ocean, connection_type="exit") # :: Wolf Cave Descent
        ])

        
        # check if we want to randomize these badend connections after connecting them
        # don't randomize if we have badend entrances also just randomized, because then its just effectively doing the same thing
        if world.options.randomize_badends and not world.options.randomize_entrances_badends:
            badends = RandomizationPool(badends).run()
        # add the badends to the world pool (can now be put in logic or randomized)
        world_regions.extend(badends)

    def tentacle_connections():
        asylum.append(
            AreaConnection(tentacle_plains, [DoLRules.tentacles_toggle], "exit"))
        hookah_parlour.append(
            AreaConnection(tentacle_forest, [DoLRules.tentacles_toggle]))

    def walkabletown_connections():
        # includes connections backwards aswell as forwards
        # this does mean it would be possible to have connections that lead into themselves, but should be funny
        # column 1
        domus_street.extend([AreaConnection(barb_street), AreaConnection(danube_street)])
        # column 2
        barb_street.extend([AreaConnection(domus_street),
                            AreaConnection(cliff_street), AreaConnection(connudatus_street)]) 
        danube_street.extend([AreaConnection(domus_street),
                              AreaConnection(wolf_street), AreaConnection(connudatus_street)])
        # column 3
        connudatus_street.extend([AreaConnection(danube_street), AreaConnection(barb_street),
                                  AreaConnection(cliff_street), AreaConnection(wolf_street)]) 
        # column 4
        cliff_street.extend([AreaConnection(barb_street), AreaConnection(connudatus_street),
                             AreaConnection(starfish_street), AreaConnection(high_street)]) 
        wolf_street.extend([AreaConnection(danube_street), AreaConnection(connudatus_street),
                            AreaConnection(nightingale_street), AreaConnection(high_street)])
        # column 5
        high_street.extend([AreaConnection(cliff_street), AreaConnection(wolf_street),
                            AreaConnection(starfish_street), AreaConnection(nightingale_street)]) 
        # column 6
        starfish_street.extend([AreaConnection(cliff_street), AreaConnection(high_street),
                                AreaConnection(oxford_street), AreaConnection(mer_street)]) 
        nightingale_street.extend([AreaConnection(wolf_street), AreaConnection(high_street),
                                   AreaConnection(oxford_street), AreaConnection(elk_street)])
        # column 7
        oxford_street.extend([AreaConnection(starfish_street), AreaConnection(nightingale_street),
                              AreaConnection(mer_street), AreaConnection(elk_street)])
        # column 8
        mer_street.append(AreaConnection(starfish_street), AreaConnection(oxford_street), 
                          AreaConnection(harvest_street)) 
        elk_street.append(AreaConnection(nightingale_street), AreaConnection(oxford_street), 
                          AreaConnection(harvest_street))
        # column 9
        harvest_street.extend(AreaConnection(mer_street), AreaConnection(elk_street))

    # Running through world options

    # if we want things to be randomized we have to connect them before randomization
    if not world.options.walkable_town: walkabletown_connections()
    if world.options.randomize_entrances_badends: badend_connections()
    if world.options.randomize_tentacleareas: tentacle_connections()
    if world.options.shop_locations == 2: 
        for area in shopping_centre_areas: shopping_centre.append(AreaConnection(area))
    
    if world.options.randomize_entrances:
        # Randomization System:
        # go through every area defined in world_regions
        # remove every connection in every area in that region and add it to a pool
        # world.random.shuffle that pool
        # add all connections back, keeping intact their to rules to enter the connection, area sizes, and connection type
            # connection types are shuffled whithin themselves, 
            # so areas that are exit only only lead to other connections that are exit only
        # explained further in the RandomizationPool class
        # any areas not defined world_regions will not be randomized, and can be added after this
        world_regions = RandomizationPool(world_regions).run()

    if world.options.shop_locations == 1:
        shops = RandomizationPool(world_regions).run()
        world_regions.extend(shops)

    # Post-Randomization

    # add connections to hospital via fainting in the street
    # don't not include nightingale, because the hospital might of been randomzied away!
    for reg in in_town: reg.append(AreaConnection(hospital))

    if world.options.walkable_town: walkabletown_connections()
    if not world.options.randomize_entrances_badends: badend_connections() # check to randomize badend entrances exists in here
    if not world.options.randomize_tentacleareas: tentacle_connections()

    # TODO: import and add rules and items here

    for reg in world_regions:
        reg.add_to_multiworld()
    print("region gen finished!")