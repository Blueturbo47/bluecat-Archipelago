from typing import TYPE_CHECKING
from BaseClasses import Entrance, Region
from enum import StrEnum
from rule_builder import rules
from rules import DoLRules
import entrance_rando

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
        Container for a connection, the area it wants to connect to and the list of rules it needs to connect 
        
        Not needed unless you want to define a connection used after definition of Area outside of just adding it to an Area

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

        def change_connectionType(self, connection_type:str):
            self.connection_type = connection_type

        def extend_rules(self, rules:list[DoLRules]):
            self.rules.extend(rules)

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
        
        This class contains takes a name of a region, and the regions it wishes to connect to via the AreaConnection class, \
            which hold the rules for the connections and the areas it wishes to connect to

        
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

            connection_type: None (normal connection), 'exit', or 'entrance'
            """
            self.sub_regions.extend(connection_list)

        def append(self, connection:AreaConnection):
            """
            Adds to the connection list

            connection_type: None (normal connection), 'exit', or 'entrance'
            """
            self.sub_regions.append(connection)

        def return_region(self):
            return self.self_region

    
            

    world_regions: list[Area] = []
    
    # Soft Bad Ends
        # Tentacle Plains
    world_regions.append(tentacle_plains := Area(DoLRegion_Names.tentacle_plains)) # not a bad end, but needs to be before asylum
        # Refer to logic where entrances/exits are
    world_regions.append(pirate_ship := Area(DoLRegion_Names.pirate_ship))
    world_regions.append(prison := Area(DoLRegion_Names.prison))
    world_regions.append(island := Area(DoLRegion_Names.island))
    world_regions.append(underground_brothel := Area(DoLRegion_Names.underground_brothel))
    world_regions.append(asylum := Area(DoLRegion_Names.asylum ))
    world_regions.append(kylar_manor := Area(DoLRegion_Names.kylar_manor))
    world_regions.append(mines := Area(DoLRegion_Names.mines))
    world_regions.append(bird_tower := Area(DoLRegion_Names.bird_tower))
    world_regions.append(remy_farm := Area(DoLRegion_Names.remy_farm))
    world_regions.append(wolf_cave := Area(DoLRegion_Names.wolf_cave))

    # Outside Town
        
    # Forest (danube, wolf, and nightingale street enter forest)
    world_regions.append(forest_shop := Area(DoLRegion_Names.forest_shop))
    world_regions.append(forest_lake := Area(DoLRegion_Names.forest_lake))
    world_regions.append(eden_cabin := Area(DoLRegion_Names.eden_cabin)) # not connecting here because its a soft bad end to not randomize it
    world_regions.append(forest := Area(DoLRegion_Names.forest, [
                AreaConnection(forest_shop), 
                AreaConnection(forest_lake)]))
    
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
    world_regions.append(dog_pound_ending := Area(DoLRegion_Names.dog_pound_ending))
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
    world_regions.append(shopping_centre := Area(DoLRegion_Names.shopping_centre, [
                AreaConnection(shopping_centre_clothingshop), 
                AreaConnection(shopping_centre_furnitureshop), 
                AreaConnection(shopping_centre_cosmeticsshop),
                AreaConnection(shopping_centre_hairdressers), 
                AreaConnection(shopping_centre_petshop), 
                AreaConnection(shopping_centre_rooftop),
                AreaConnection(shopping_centre_supermarket), 
                AreaConnection(shopping_centre_tailor), 
                AreaConnection(shopping_centre_tattooparlour),
                AreaConnection(shopping_centre_toystore)]))
    
    world_regions.append(office_building := Area(DoLRegion_Names.office_building))
    world_regions.append(
            high_street := Area(DoLRegion_Names.high_street, [
                AreaConnection(office_building), 
                AreaConnection(shopping_centre), 
                AreaConnection(park), 
                AreaConnection(commercial_drain), 
                AreaConnection(commercial_alleyways)]))

        # Nightingale Street
    world_regions.append(hospital := Area(DoLRegion_Names.hospital))
    world_regions.append(photography_studio := Area(DoLRegion_Names.photography_studio))
    world_regions.append(nightingale_street := Area(DoLRegion_Names.nightingale_street, [
                AreaConnection(hospital), 
                AreaConnection(photography_studio, ["TODO: photgraphy studio discovery"]), 
                AreaConnection(forest), 
                AreaConnection(park), 
                AreaConnection(commercial_drain), 
                AreaConnection(commercial_alleyways)]))

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
    for i in in_town:
        in_town_connections.append(AreaConnection(i))

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
    # cliff_street -> remy_farm : if chef is met and high sus but not rage



    # "town" isn't a real place, however this makes it easier for me to connect every single walkable point
    # since if you're in town, you have access to the bus, therefore have access to every stop in town
    town = Area(DoLRegion_Names.town, in_town_connections)

    badends = [prison, island, underground_brothel, asylum, 
            dog_pound_ending, mines, eden_cabin, kylar_manor, 
            pirate_ship, bird_tower, remy_farm, wolf_cave]

    # Running through world options
    def badend_connections():
        # [[connection], [[extra rule location], [extra rule]]]
        badend_connect_list_entrances:list[list[AreaConnection]] = [

                # prison: 1
                # logic is hospital for high arrest chance
            [AreaConnection(hospital, connection_type="entrance")], # :: Police Prison Intro

                # island:
                #
            [AreaConnection(pirate_ship, connection_type="entrance")], # :: Pirate Passout Wake, Pirate End Run, Pirate End Islanders

                # underground_brothel: 3 (:: Underground Intro)
                # :: Briar Hack Fail can be included but can become impossible
            [AreaConnection(orphanage, connection_type="entrance"), # :: Rent Intro ($rentsale)
            AreaConnection(hospital, connection_type="entrance")], # :: Hospital Arrest Molestation Finish

                # asylum: 4 
                # faints can lead to hospital leading to asylum
            [AreaConnection(hospital)], # :: Asylum Intro

                # dog_pound_ending: 5
                # require wolf TF for Pound Abduction
                # **if add, fix extend**
            [AreaConnection(dog_pound, connection_type="entrance"), # :: Pound Assault Caught
            ].extend(in_town_connections), # :: Pound Abudction
                
                # mines: 6 
                # 
            [AreaConnection(flats, connection_type="entrance")], # :: Flats Auction 8

                # eden_cabin: 7
                #
            [AreaConnection(forest, connection_type="entrance"), # :: Forest Hunter Molestation Finish
            AreaConnection(orphanage, connection_type="entrance")], # :: rentsale ($rentsale 1) - widget"rentEdenTrade"

                # kylar_manor: 8
                # requires meeting kylar so school required
            [AreaConnection(school, connection_type="entrance")], # :: Kylar Abduction Intro via widget"kylarwatched"

                # pirate_ship 9
                # TODO: check if can go back to mainland if so where
            [AreaConnection(ocean, connection_type="entrance"), # :: Pirate Intro, Passout Pirates Hot Cold
            AreaConnection(pub, ["TODO: rule temple access"], "entrance")], # :: Smuggler Pub Zephyr

                # bird_tower 10
                #
            [AreaConnection(moor, connection_type="entrance")], # :: Bird Capture, Moor Bird Wake

                # remy_farm 11 (:: Moor Abduction Remy Wake, Livestock Intro)
                # TODO: extend town, rng toggle option
            [AreaConnection(moor, connection_type="entrance")],

                # wolf_cave 12 ()
                # TODO: connections
            [AreaConnection(forest, connection_type="entrance")] # :: Forest Wolf Cave Intro
        ]

        badend_connect_list_exits = [ # TODO: finish out exits
                # prison: 1 
            [AreaConnection(orphanage, connection_type="exit"), # :: Prison End Car Silent, Prison End Car Thank, Prison End Car Angry
            AreaConnection(docks, connection_type="exit"), # :: Prison Kylar Escape Ask, Prison Kylar Escape Nod, Prison Wren Escape 3
            AreaConnection(ocean, [DoLRules.swimming_10], "exit"), # :: Prison Escape, Passout Rut 2
            AreaConnection(beach, [DoLRules.flight], "exit")], # :: Prison Soar Escape
            
                # island: 2
            [AreaConnection(pirate_ship, connection_type="exit"), # :: Islander End Hand
            AreaConnection(mer_street, connection_type="exit"), # :: Island Sail
            AreaConnection(ocean, connection_type="exit"), # :: Islander End Swim, Islander End Throw, Islander Enforce (req: Angel tf) : (min req: none)
            AreaConnection(hospital, [DoLRules.pregnancy_toggle], "exit")], # :: Pregnancy Island
            
                # underground_brothel: 3
            [AreaConnection(ocean, connection_type="exit"), # :: Underground Lake
            AreaConnection(forest, connection_type="exit")], # :: Underground Presentation Molestation Finish, Underground Hunt, Underground Cell Sneak, widget "undergroundEscapeForestStart"
            
                # asylum: 4
            [AreaConnection(forest, connection_type="exit"), # :: Asylum Escape, Tentacle Escape, Tentacle Wolf Escape, Eden Asylum Rescue
            AreaConnection(orphanage, connection_type="exit")], # :: Asylum Return, Pregnancy Birth Asylum End (req: preg), Tentacle Plains Resist : (min req: none)
            
                # dog_pound_ending: 5 
            [AreaConnection(starfish_street, connection_type="exit")], # :: Pound Escape Front, Pound Escape Free Dress, Pound Escape Free No Dress
            
                # mines: 6
            [AreaConnection(residential_drain, connection_type="exit"), # :: Mines Guards Escape, Mines Passout Warn 3, Mines Passout Run 2
            AreaConnection(flats, connection_type="exit")], # :: Mines Escape
            
                # eden_cabin: 7 (weirdly boring number of escape options)
            [AreaConnection(forest, connection_type="exit")], # :: Cabin Night Escape, TODO: non escape
            
                # kylar_manor: 8 note: Kylar Abduction Stockholm End (one time event) leads to the park
            [AreaConnection(danube_street, connection_type="exit")], # :: Kylar Abduction Release 4, Kylar Abduction Free Rescue [Thank, Angry, Silent, Reassure, Mock], Kylar Abduction Free Leave 2, TODO: non escape
            
                # pirate_ship 9 ()
            [AreaConnection(island, connection_type="exit"), # :: Pirate End Run, Pirate End Wait
            AreaConnection(ocean, connection_type="exit"),  # :: Pirate Railing Dive Night, Pirate Railing Dive Day
            AreaConnection(mer_street, connection_type="exit")], # :: Pirate Return
            
                # bird_tower 10
            [AreaConnection(moor, connection_type="exit")], # :: Bird Tower Rope Escape (leaving -> "castle" -> moor), TODO: non escape

                # remy_farm 11 (eden escape possible, but requires access to eden regardless)
            [AreaConnection(forest, connection_type="exit")], # all lead to :: Livestock Escape Town

                # wolf_cave 12
            [AreaConnection(forest, connection_type="exit"), # :: Forest Wolf Cave Rape End, Forest Wolf Cave Escape
            AreaConnection(ocean, connection_type="exit")] # :: Wolf Cave Descent
        ]

        for i in badend_connect_list_entrances[4][1:]: #adding wolf rules to in_town_connections
            i.append_rules(DoLRules.wolf_tf)


        # make 2 lists of pool sizes (num of exits/entrances)
        # add the connection list lists to 2 big lists containing them all unsorted
        # shuffle the big lists
        # add connections
        if world.options.randomize_badends:
            poolsize_badend_entrances:list[int] = []
            poolsize_badend_exits:list[int] = []
            pool_badend_entrances:list[AreaConnection] = []
            pool_badend_exits:list[AreaConnection] = []
            for i, nul in enumerate(badend_connect_list_entrances):
                poolsize_badend_entrances.append(len(badend_connect_list_entrances[i]))
                poolsize_badend_exits.append(len(badend_connect_list_exits[i]))
                pool_badend_entrances.extend(badend_connect_list_entrances[i])
                pool_badend_exits.extend(badend_connect_list_exits[i])
            
            world.random.shuffle(pool_badend_entrances)
            world.random.shuffle(pool_badend_exits)

            def pooltime(poolsizes, bigpool):
                i = 0
                for poolnum, poolsize in enumerate(poolsizes):
                    badends[poolnum].extend(bigpool[i:i + poolsize])
                    i += poolsize
            
            pooltime(poolsize_badend_exits, pool_badend_exits)
            pooltime(poolsize_badend_entrances, pool_badend_entrances)


    def tentacle_connections():
        asylum.append(
            AreaConnection(tentacle_plains, [DoLRules.tentacles_toggle], "exit"))
        hookah_parlour.append(
            AreaConnection(tentacle_forest, [DoLRules.tentacles_toggle]))

    if world.options.randomize_tentacleareas:
        tentacle_connections()

    if world.options.randomize_entrances:
        if world.options.randomize_entrances_badends:
            badend_connections()
        
        if not world.options.walkable_town:
            # column 1
            domus_street.extend([AreaConnection(barb_street), AreaConnection(danube_street)])
            # column 2
            barb_street.extend([AreaConnection(cliff_street), AreaConnection(connudatus_street)]) 
            danube_street.extend([AreaConnection(wolf_street), AreaConnection(connudatus_street)])
            # column 3
            connudatus_street.extend([AreaConnection(cliff_street), AreaConnection(wolf_street)]) 
            # column 4
            cliff_street.extend([AreaConnection(starfish_street), AreaConnection(high_street)]) 
            wolf_street.extend([AreaConnection(nightingale_street), AreaConnection(high_street)])
            # column 5
            high_street.extend([AreaConnection(starfish_street), AreaConnection(nightingale_street)]) 
            # column 6
            starfish_street.extend([AreaConnection(oxford_street), AreaConnection(mer_street)]) 
            nightingale_street.extend([AreaConnection(oxford_street), AreaConnection(elk_street)])
            # column 7
            oxford_street.extend([AreaConnection(mer_street), AreaConnection(elk_street)])
            # column 8
            mer_street.append(AreaConnection(harvest_street)) 
            elk_street.append(AreaConnection(harvest_street))
            # column 9
            # harvest_street.extend() 
        
        print("TODO: randomization")

    # Post-Randomization

    for reg in in_town:
        if reg.name() != DoLRegion_Names.nightingale_street:
            reg.append(AreaConnection(hospital))
   
    if not world.options.randomize_entrances_badends:
        badend_connections()

    if not world.options.randomize_tentacleareas:
        tentacle_connections()

    # TODO: import and add rules and items here

    for reg in world_regions:
        reg.add_to_multiworld()

    if world.options.walkable_town:
        town.add_to_multiworld()