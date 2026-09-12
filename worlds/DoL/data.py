from enum import StrEnum


class DoLRegion_Names(StrEnum):
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