from typing import TYPE_CHECKING
from BaseClasses import Entrance, Region
from enum import StrEnum
from rule_builder import rules
import entrance_rando


if TYPE_CHECKING:
    from .world import DoLWorld

class DolRegion_Names(StrEnum):
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
    hawk_tower = "Great Hawk's Tower"

        # Other Regions
    bog = "The Bog"

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

    class Area:
        '''
        ### Description:
        
        This class contains takes a name of a region, the regions that you want this to connect to, \
            and any extra rules for regions that wish to connect to this region, \
            and then helps do the connection and creation of the regions.

        You **must** construct areas in **reverse order** for example, if you want to start at \
            foo and go to bar, bar = Area(region.bar) must be done first, and then foo Area(region.foo)
        
        I recommend putting all areas built with this constructor into one list, following the same principle as above \
            to make creation of regions and connections easier        

        
        ### Usage:
        
        To create: do a for loop that through the area list, and retrieve name of area with .name()
        
        - Example: for area_name in regions: world_regions.append(Region(area_name.name(), world.player, world.multiworld))
        
        To connect: do a for loop that runs .connect(). **You must create your regions first before connecting**
        
        - Example: for x in regions: x.connect()
        
                
        :param StrEnum region_name: Name of the region, cross referenced to the StrEnum class for your world. \
            Example: foobar_REGION_NAMES.foo
        
        :param AreaList sub_regions: List of Area that will this region will connect to when running connect() \
            Example: [bar, baz]

        :param AreaList sub_regions_oneway_outgoing: Same as above, but for one-way outgoing connections. Optional
        
        :param AreaList sub_regions_oneway_incoming: Same as above, but for one-way incoming connections.\
            This is useful in the case that you need to send a earlier declared region to a later region. Optional
        
        :param 3DList extra_rules: Designate a wished connection with a rule that must be followed. \
            Areas not in wished connections are ignored. Format: [[Area, Rule], ...]. Optional
        
        ### Functions:

        - name(): returns name

        - connect(): connects regions defined in the sub_regions lists with this region

        - add_connection(): lets you add connections, best used if you have connections you only want from world rules
        
        '''

        

        def __init__(self, region_name:str, sub_regions:list = [], sub_regions_oneway_outgoing:list = [], 
                    sub_regions_oneway_incoming:list = [], extra_rules:list = []):
            self.region_name = region_name
            self.sub_regions = sub_regions
            self.sub_regions_oneway_outgoing = sub_regions_oneway_outgoing
            self.sub_regions_oneway_incoming = sub_regions_oneway_incoming
            self.extra_rules = extra_rules

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
            self.designate_connections(self.sub_regions)
            if self.sub_regions_oneway_outgoing:
                self.designate_connections(self.sub_regions_oneway_outgoing, "exit")
            if self.sub_regions_oneway_incoming:
                self.designate_connections(self.sub_regions_oneway_incoming, "entrance")

        def designate_connections(self, connection_list:list, connection_type:str = ""):
            """
            Leave blank for a normal connection
            connection_type (optional): 'exit' or 'entrance'
            """

            for outgoing in self.sub_regions:
                outgoingRegion = world.get_region(outgoing.name())
                if not self.extra_rules:
                    match(connection_type):
                        case "exit":
                            self.self_region.add_exits # TODO:
                        case "entrance":
                            outgoingRegion.add_exits # TODO:
                        case _:
                            self.self_region.connect(outgoingRegion, f"{outgoing.name()} in/at {self.name()}")
                else:
                    # TODO: ADD RULES
                    newrule = rules
                    match(connection_type):
                        case "exit":
                            self.self_region.add_exits # TODO:
                        case "entrance":
                            outgoingRegion.add_exits # TODO:
                        case _:
                            self.self_region.connect(outgoingRegion, f"{outgoing.name()} in/at {self.name()}")

        def add_connection(self, connection_list:list, connection_type:str = ""):
            """
            Adds to the connection lists

            connection_type: None (normal connection), 'exit', or 'entrance'
            """
            match(connection_type):
                case "exit":
                    self.sub_regions_oneway_outgoing.extend(connection_list)
                case "entrance":
                    self.sub_regions_oneway_incoming.extend(connection_list)
                case _:
                    self.sub_regions.extend(connection_list)

    world_regions: list[Area] = []
    
    regions = DolRegion_Names

    # Soft Bad Ends
        # Pirate Ship connect to Island or Ocean
    world_regions.append(pirate_ship := Area(DolRegion_Names.pirate_ship))
        # Prison and Island connect to Ocean
    world_regions.append(prison := Area(DolRegion_Names.prison))
    world_regions.append(island := Area(DolRegion_Names.island))
        # Brothel and Asylum connect to forest
    world_regions.append(underground_brothel := Area(DolRegion_Names.underground_brothel))
    world_regions.append(asylum := Area(DolRegion_Names.asylum))
        # Kylars Manor connect to Danube Street
    world_regions.append(kylar_manor := Area(DolRegion_Names.kylar_manor))
        # Mine connect to Flats
    world_regions.append(mines := Area(DolRegion_Names.mines))
    world_regions.append(hawk_tower := Area(DolRegion_Names.hawk_tower))

    # Outside Town
        
    # Forest (danube, wolf, and nightingale street enter forest)
    world_regions.append(forest_shop := Area(DolRegion_Names.forest_shop))
    world_regions.append(forest_lake := Area(DolRegion_Names.forest_lake))
    world_regions.append(wolf_cave := Area(DolRegion_Names.wolf_cave))
    world_regions.append(eden_cabin := Area(DolRegion_Names.eden_cabin)) # not connecting here because its a soft bad end to not randomize it
    world_regions.append(
            forest := Area(DolRegion_Names.forest, [
                forest_shop, forest_lake, wolf_cave
            ]))
    
    # Ocean
    world_regions.append(ocean := Area(DolRegion_Names.ocean))

    # Outskirts
        # Farmlands
    world_regions.append(alex_farm := Area(DolRegion_Names.alex_farm))
    world_regions.append(riding_school := Area(DolRegion_Names.riding_school))
    world_regions.append(meadow := Area(DolRegion_Names.meadow))
    world_regions.append(manors := Area(DolRegion_Names.manors))
    world_regions.append(farmlands_road := Area(DolRegion_Names.farmlands_road))
    world_regions.append(
            farmlands := Area(DolRegion_Names.farmlands, [
                manors, meadow, riding_school, 
                alex_farm, farmlands_road
            ]))

        # Moor
    world_regions.append(moor := Area(DolRegion_Names.moor))

        # Other Areas
    # bog connects forest to moor, but not back
    world_regions.append(bog := Area(DolRegion_Names.bog, [moor], sub_regions_oneway_incoming=[forest], 
            extra_rules=[
                [forest, moor], 
                ["TODO: bog can be discovered in forest in a few ways", "TODO: moor to bog requires $bogprogress 1"]
            ]))


    # Inside Town
        # Other
    world_regions.append(park := Area(DolRegion_Names.park))
    world_regions.append(beach := Area(DolRegion_Names.beach))

        # Drainage and Alleyways
    world_regions.append(residential_drain := Area(DolRegion_Names.residential_drain))
    world_regions.append(commercial_drain := Area(DolRegion_Names.commercial_drain, [residential_drain]))
    world_regions.append(industrial_drain := Area(DolRegion_Names.industrial_drain, [commercial_drain]))

    world_regions.append(residential_alleyways := Area(DolRegion_Names.residential_alleyways, [residential_drain]))
    world_regions.append(commercial_alleyways := Area(DolRegion_Names.commercial_alleyways, [commercial_drain, residential_alleyways]))
    world_regions.append(industrial_alleyways := Area(DolRegion_Names.industrial_alleyways, [industrial_drain, commercial_alleyways]))


    # Residential
        # Danube Street
    world_regions.append(spa := Area(DolRegion_Names.spa))
    
    world_regions.append(avery_mansion := Area(DolRegion_Names.avery_mansion))
    world_regions.append(danube_houses := Area(DolRegion_Names.danube_houses))
    world_regions.append(avery_mansion := Area(DolRegion_Names.avery_mansion))

    world_regions.append(
            danube_street := Area(DolRegion_Names.danube_street, [
                spa, avery_mansion, 
                danube_houses, forest, residential_alleyways, 
                residential_drain
            ], extra_rules=[
                [avery_mansion],
                ["TODO: requires $avery_mansion"]
            ]))

        # Barb Street
    world_regions.append(tentacle_forest := Area(DolRegion_Names.tentacle_forest))
    world_regions.append(hookah_parlour := Area(DolRegion_Names.hookah_parlour, [tentacle_forest]))
    world_regions.append(flats := Area(DolRegion_Names.flats, [hookah_parlour]))
    
    world_regions.append(dance_studio := Area(DolRegion_Names.dance_studio))
    world_regions.append(police_station := Area(DolRegion_Names.police_station))

    world_regions.append(
            barb_street := Area(DolRegion_Names.barb_street, [
                dance_studio, police_station, flats, 
                residential_alleyways, residential_drain
            ]))

        # Domus Street  
    world_regions.append(orphanage := Area(DolRegion_Names.orphanage))
    world_regions.append(domus_houses := Area(DolRegion_Names.domus_houses))

    world_regions.append(
            domus_street := Area(DolRegion_Names.domus_street, [
                orphanage, domus_houses, residential_alleyways, 
                residential_drain
            ]))

    # Commercial
        # Connudatus Street
    world_regions.append(strip_club := Area(DolRegion_Names.strip_club))

    world_regions.append(
            connudatus_street := Area(DolRegion_Names.connudatus_street, [
                strip_club, commercial_drain, residential_alleyways, 
                commercial_alleyways
            ], extra_rules = [
                [strip_club],
                ["TODO: fake id requirement"]
            ]))

        # Starfish Street
    world_regions.append(arcade := Area(DolRegion_Names.arcade))
    world_regions.append(chalets := Area(DolRegion_Names.chalets))
    world_regions.append(dog_pound := Area(DolRegion_Names.dog_pound))
    world_regions.append(dog_pound_ending := Area(DolRegion_Names.dog_pound_ending))

    world_regions.append(
            starfish_street := Area(DolRegion_Names.starfish_street, [
                arcade, chalets, dog_pound, 
                beach, park, commercial_drain
            ]))


        # Cliff Street
    world_regions.append(mayors_office := Area(DolRegion_Names.mayors_office))
    world_regions.append(cafe := Area(DolRegion_Names.cafe))

    world_regions.append(
            cliff_street := Area(DolRegion_Names.cliff_street, [
                mayors_office, cafe, beach, 
                commercial_drain, commercial_alleyways
            ]))

        # High Street
    world_regions.append(shopping_centre_rooftop := Area(DolRegion_Names.shopping_centre_rooftop))
    world_regions.append(shopping_centre_hairdressers := Area(DolRegion_Names.shopping_centre_hairdressers))
    world_regions.append(shopping_centre_petshop := Area(DolRegion_Names.shopping_centre_petshop))
    world_regions.append(shopping_centre_tattooparlour := Area(DolRegion_Names.shopping_centre_tattooparlour))
    world_regions.append(shopping_centre_furnitureshop := Area(DolRegion_Names.shopping_centre_furnitureshop))
    world_regions.append(shopping_centre_supermarket := Area(DolRegion_Names.shopping_centre_supermarket))
    world_regions.append(shopping_centre_clothingshop := Area(DolRegion_Names.shopping_centre_clothingshop))
    world_regions.append(shopping_centre_tailor := Area(DolRegion_Names.shopping_centre_tailor))
    world_regions.append(shopping_centre_cosmeticsshop := Area(DolRegion_Names.shopping_centre_cosmeticsshop))
    world_regions.append(shopping_centre_toystore := Area(DolRegion_Names.shopping_centre_toystore))
    world_regions.append(
            shopping_centre := Area(DolRegion_Names.shopping_centre, [
                shopping_centre_clothingshop, shopping_centre_furnitureshop, shopping_centre_cosmeticsshop, 
                shopping_centre_hairdressers, shopping_centre_petshop, shopping_centre_rooftop, 
                shopping_centre_supermarket, shopping_centre_tailor, shopping_centre_tattooparlour, 
                shopping_centre_toystore
            ]))

    world_regions.append(office_building := Area(DolRegion_Names.office_building))
    world_regions.append(
            high_street := Area(DolRegion_Names.high_street, [
                office_building, shopping_centre, park, 
                commercial_drain, commercial_alleyways
            ]))

        # Nightingale Street
    world_regions.append(hospital := Area(DolRegion_Names.hospital))
    world_regions.append(photography_studio := Area(DolRegion_Names.photography_studio))
    world_regions.append(
            nightingale_street := Area(DolRegion_Names.nightingale_street, [
                hospital, photography_studio, forest, 
                park, commercial_drain, commercial_alleyways
            ], extra_rules = [
                [photography_studio],
                ["TODO: photgraphy studio discovery"]
            ]))

        # Wolf Street
    world_regions.append(temple := Area(DolRegion_Names.temple))
    world_regions.append(soup_kitchen := Area(DolRegion_Names.soup_kitchen))
    world_regions.append(
            wolf_street := Area(DolRegion_Names.wolf_street, [
                temple, soup_kitchen, forest, 
                commercial_drain, commercial_alleyways
            ], extra_rules = [
                [soup_kitchen],
                ["TODO: soup kitchen discovery"]
            ]))

        # Oxford Street
    world_regions.append(school := Area(DolRegion_Names.school, [park, industrial_alleyways, commercial_drain], 
            extra_rules = [
                [commercial_drain],
                ["TODO: history ? grade"]
            ]))
    world_regions.append(museum := Area(DolRegion_Names.museum))
    world_regions.append(
            oxford_street := Area(DolRegion_Names.oxford_street, [
                school, museum, commercial_alleyways,
                commercial_drain, industrial_alleyways, park
            ]))
    
    # Industrial
        # Harvest Street
    world_regions.append(brothel := Area(DolRegion_Names.brothel))
    world_regions.append(pub := Area(DolRegion_Names.pub))
    world_regions.append(bus_station := Area(DolRegion_Names.bus_station))
    world_regions.append(factory := Area(DolRegion_Names.factory))
    world_regions.append(
            harvest_street := Area(DolRegion_Names.harvest_street, [
                brothel, pub, bus_station, 
                factory, industrial_drain, industrial_alleyways,
                farmlands_road
            ], extra_rules = [
                [brothel],
                ["TODO: $brothelknown >= 1"]
            ]))

        # Mer Street
    world_regions.append(docks := Area(DolRegion_Names.docks, sub_regions_oneway_outgoing=[ocean],
            extra_rules=[
                [ocean], # night docks connects to ocean
                ["TODO: skul c grade"]
            ]))
    world_regions.append(coastal_path := Area(DolRegion_Names.coastal_path, [meadow], 
            extra_rules=[
                [meadow],
                ["TODO: $historytrait >= 3"]
            ]))
    world_regions.append(
            mer_street := Area(DolRegion_Names.mer_street, [
                docks, coastal_path, industrial_alleyways, industrial_drain
            ], extra_rules=[
                [coastal_path],
                ["TODO: $historytrait >= 3"]
            ]))

        # Elk Street
    # landfill requires discovery 
    world_regions.append(landfill := Area(DolRegion_Names.landfill))
    # adult shop requires building it
    world_regions.append(adult_shop := Area(DolRegion_Names.adult_shop))
    world_regions.append(compound := Area(DolRegion_Names.compound))
    world_regions.append(
            elk_street := Area(DolRegion_Names.elk_street, [
                landfill, adult_shop, compound,
                industrial_alleyways, industrial_drain
            ]))


    in_town = [danube_street, barb_street, domus_street, 
            starfish_street, cliff_street, high_street,
            nightingale_street, wolf_street, connudatus_street,
            oxford_street, harvest_street, mer_street,
            elk_street]

    # "town" isn't a real place, however this makes it easier for me to connect every single walkable point
    # since if you're in town, you have access to the bus, therefore have access to every stop in town
    town = Area(DolRegion_Names.town, in_town)

    badends = [prison, island, underground_brothel, asylum, dog_pound_ending, mines, eden_cabin, kylar_manor]

    # Running through world options
    def badend_connections():
        badend_connect_list_entrances = [
            [], #prison: 1 (:: Police Prison Intro)
            [], #island: 2 (:: Pirate Passout Wake)
            [orphanage, hospital].extend(in_town), #underground_brothel: 3 (:: Underground Intro), briar hack can be included but can become impossible
            in_town, #asylum: 4 (:: Asylum Intro)
            [dog_pound], #dog_pound_ending: 5 () (:: Pound Assault Caught AND :: Pound Abudction), require wolf TF for Pound Abduction 
            [], #mines: 6
            [], #eden_cabin: 7
            [], #kylar_manor: 8
        ]
        badend_connect_list_exits = [
            [], #prison: 1
            [], #island: 2
            [], #underground_brothel: 3
            [], #asylum: 4
            [], #dog_pound_ending: 5
            [], #mines: 6
            [forest], #eden_cabin: 7
            [], #kylar_manor: 8
        ]
        if world.options.randomize_badends:
            world.random.shuffle(badend_connect_list_entrances)
            world.random.shuffle(badend_connect_list_exits)
        for x, end in enumerate(badends):
            end.add_connection([badend_connect_list_entrances[x]], "entrance")
            end.add_connection([badend_connect_list_exits[x]], "exit")


    if world.options.randomize_entrances:
        if world.options.randomize_entrances_badends:
            badend_connections()
        
        if not world.options.walkable_town:
            domus_street.add_connection([barb_street, danube_street]) # column 1
            barb_street.add_connection([cliff_street, connudatus_street]) # column 2
            danube_street.add_connection([wolf_street, connudatus_street]) 
            connudatus_street.add_connection([cliff_street, wolf_street]) # column 4
            cliff_street.add_connection([starfish_street, high_street]) # column 5
            wolf_street.add_connection([nightingale_street, high_street])
            high_street.add_connection([starfish_street, nightingale_street]) # column 6
            starfish_street.add_connection([oxford_street, mer_street]) # column 8
            nightingale_street.add_connection([oxford_street, elk_street])
            oxford_street.add_connection([mer_street, elk_street]) # column 9
            mer_street.add_connection([harvest_street]) # column 10
            elk_street.add_connection([harvest_street])
            # harvest_street.add_connection() # column 11
        
        print("TODO: randomization")

    
   
    if not world.options.randomize_entrances_badends:
        badend_connections()

    # TODO: import and add rules and items here
    
    for reg in world_regions:
        reg.add_to_multiworld()