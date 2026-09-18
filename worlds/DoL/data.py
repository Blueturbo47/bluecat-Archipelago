from enum import StrEnum, Enum
from rule_builder.rules import Has, HasAll, HasGroupUnique, Rule, CanReachRegion, HasGroup
from rule_builder.options import OptionFilter
from .options import *

class DoLRegionNames(StrEnum):
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

    in_town = "Any Place in town" # debug region used for some location

class DoLItemNames(StrEnum):
        # Money
    money_100 = "100 Pounds"
    antique_ivorystatuette = "Antique Ivory Statuette"
    antique_silvercoin = "Antique Silver Crown"
    antique_silvercrown = "Antique Silver Crown"
    antique_crystal = "Antique Crystal"
    antique_silverblade = "Antique Silver Blade"
    antique_coppercoin = "Antique Copper Coin"
    antique_silvergoblet = "Antique Silver Goblet"
    antique_fetish = "Antique Fetish"
    antique_goldcoin = "Antique Gold Coin"

        # Forest
    antique_forestdagger = "Antique Dagger"
    antique_forestgem = "Antique Forest Gem"
    antique_arrow = "Antique Arrow"

        # Lake
    antique_ivorynecklace = "Antique Ivory Necklace"
    antique_ivorybox = "Antique Ivory Box"
    antique_silverring = "Antique Silver Ring"
    antique_goldnecklace = "Antique Gold Necklace"
    antique_chastitybelt = "Antique Chastity Belt"

        # Meadow
    antique_stonetalisman = "Antique Stone Talisman"

        # Maze
    antique_horn = "Antique Horn"
    antique_snuffer = "Antique Snuffer"
    antique_bucket = "Antique Bucket"
    antique_silvermanacle = "Antique Silver Manacle"
    antique_whip = "Antique Whip"

        # Moor
    antique_goldring = "Antique Gold Ring"
    antique_bell = "Antique Bell"
    antique_bullet = "Antique Bullet"
    antique_artilleryshell = "Antique Artillery Shell"

        # Riding School
    antique_grenade = "Antique Grenade Riding"

        # Dance School
    antique_goldbrooch = "Antique Gold Brooch Dance"

        # Orphanage
    antique_silverbrooch = "Antique Silver Brooch"

        # Island
    antique_islanderarrow = "Antique Islander Arrow"
    antique_islandermask = "Antique Islander Mask"
    antique_obsidiandisc = "Antique Obsidian Disc"
    antique_trilobitefossil = "Antique Trilobite Fossil"

        # Landfill
    antique_baileyminesign = "Antique Bailey Mine Sign"
    antique_incenseburner = "Antique Incense Burner"
    antique_cup = "Antique Cup"

        # Museum
    antique_silvermask = "Antique Silver Mask"

        # Bird Tower
    # antique_bullet = "" also found in moor

        # Manors
    antique_silveramulet = "Antique Silver Amulet"

        # Compound
    antique_hourglass = "Antique Hourglass"

        # Pirate Ship
    antique_swordcane = "Antique Sword Cane"
    antique_chocolate = "Antique Chocolate"
    antique_teacaddy = "Antique Tea Caddy"
    antique_woodenfigurine = "Antique Wooden Figurine"
    antique_copperring = "Antique Copper Ring"
    antique_goldcompass = "Antique Gold Compass"

        # Ocean
    antique_coppercompass = "Antique Copper Compass"
    antique_coralring = "Antique Coral Ring"
    antique_diamond = "Antique Diamond"

        # Temple
    antique_brassstatuette = "Antique Brass Statuette"

        # Avery Mansion
    antique_golddagger = "Antique Gold Dagger"
    antique_goldamulet = "Antique Gold Amulet"
    antique_goldmask = "Antique Gold Mask"

        # Beach Cave
    antique_silvercompass = "Antique Silver Compass"
    antique_leathermap = "Antique Leather Map"
    antique_cutlass = "Antique Cutlass"
    antique_silverdagger = "Antique Silver Dagger"
    antique_rustedcutlass = "Antique Rusted Cutlass"

        # Sewers
    antique_pinkcrystal = "Antique Pink Crystal"
    antique_candlestick = "Antique Candlestick"
    antique_dildo = "Antique Dildo"
    # antique_horn = "" also found in maze
    antique_watch = "Antique Watch"


    # Skills
    progressive_skulduggery_rank = "Progressive Skulduggery Rank"
    progressive_dancing_rank = "Progressive Dancing Rank"
    progressive_swimming_rank = "Progressive Swimming Rank"
    progressive_athletics_rank = "Progressive Athletics Rank"
    progressive_tending_rank = "Progressive Tending Rank"
    progressive_housekeeping_rank = "Progressive Housekeeping Rank"
    progressive_seduction_rank = "Progressive Seduction Rank"
    progressive_oral_rank = "Progressive Oral Rank"
    progressive_chest_rank = "Progressive Chest Rank"
    progressive_hands_rank = "Progressive Hands Rank"
    progressive_buttocks_rank = "Progressive Buttocks Rank"
    progressive_privates_rank = "Progressive Privates Rank"
    progressive_anal_rank = "Progressive Anal Rank"
    progressive_thighs_rank = "Progressive Thighs Rank"
    progressive_feet_rank = "Progressive Feet Rank"
    progressive_science_rank = "Progressive Science Rank"
    progressive_math_rank = "Progressive Math Rank"
    progressive_english_rank = "Progressive English Rank"
    progressive_history_rank = "Progressive History Rank"
    progressive_willpower_rank = "Progressive Willpower Rank"
    progressive_physique_rank = "Progressive Physique Rank"
    progressive_promiscuity_rank = "Progressive Promiscuity Rank"
    progressive_exhibitionism_rank = "Progressive Exhibitionism Rank"
    progressive_deviancy_rank = "Progressive Deviancy Rank"

class DoLLocationTypes(StrEnum):
    antique = "Antique",
    skill = "Skill Rank",

class DoLLocationNames(StrEnum):
    """
    List of locations for checks

    antique_ = ``'Antique Name' : 'Location'``\n
    skill_ = ``'Skill' Rank 'X'``
    
    """
    # Antiques
        # Churchyard Catacombs
    antique_ivorystatuette = f"{DoLItemNames.antique_ivorystatuette} : Churchyard"
    antique_silvercoin = f"{DoLItemNames.antique_silvercoin} : Churchyard"
    antique_silvercrown = f"{DoLItemNames.antique_silvercrown} : Churchyard"
    antique_crystal = f"{DoLItemNames.antique_crystal} : Churchyard"
    antique_silverblade = f"{DoLItemNames.antique_silverblade} : Churchyard"
    antique_coppercoin = f"{DoLItemNames.antique_coppercoin} : Churchyard"
    antique_silvergoblet = f"{DoLItemNames.antique_silvergoblet} : Churchyard"
    antique_fetish = f"{DoLItemNames.antique_fetish} : Churchyard"
    antique_goldcoin = f"{DoLItemNames.antique_goldcoin} : Churchyard"

        # Forest
    antique_forestdagger = f"{DoLItemNames.antique_forestdagger} : Forest"
    antique_forestgem = f"{DoLItemNames.antique_forestgem} : Forest"
    antique_arrow = f"{DoLItemNames.antique_arrow} : Forest"

        # Lake
    antique_ivorynecklace = f"{DoLItemNames.antique_ivorynecklace} : Lake"
    antique_ivorybox = f"{DoLItemNames.antique_ivorybox} : Lake"
    antique_silverring = f"{DoLItemNames.antique_silverring} : Lake"
    antique_goldnecklace = f"{DoLItemNames.antique_goldnecklace} : Lake"
    antique_chastitybelt = f"{DoLItemNames.antique_chastitybelt} : Lake"

        # Meadow
    antique_stonetalisman = f"{DoLItemNames.antique_stonetalisman} : Meadow"

        # Maze
    antique_horn = f"{DoLItemNames.antique_horn} : Maze or Sewers"
    antique_snuffer = f"{DoLItemNames.antique_snuffer} : Maze"
    antique_bucket = f"{DoLItemNames.antique_bucket} : Maze"
    antique_silvermanacle = f"{DoLItemNames.antique_silvermanacle} : Maze"
    antique_whip = f"{DoLItemNames.antique_whip} : Maze"

        # Moor
    antique_goldring = f"{DoLItemNames.antique_goldring} : Moor"
    antique_bell = f"{DoLItemNames.antique_bell} : Moor"
    antique_bullet = f"{DoLItemNames.antique_bullet} : Moor or Great Hawk"
    antique_artilleryshell = f"{DoLItemNames.antique_artilleryshell} : Moor"

        # Riding School
    antique_grenade = f"{DoLItemNames.antique_grenade} : Riding School"

        # Dance School
    antique_goldbrooch = f"{DoLItemNames.antique_goldbrooch} : Dance School"

        # Orphanage
    antique_silverbrooch = f"{DoLItemNames.antique_silverbrooch} : Orphange"

        # Island
    antique_islanderarrow = f"{DoLItemNames.antique_islanderarrow} : Island"
    antique_islandermask = f"{DoLItemNames.antique_islandermask} : Island"
    antique_obsidiandisc = f"{DoLItemNames.antique_obsidiandisc} : Island"
    antique_trilobitefossil = f"{DoLItemNames.antique_trilobitefossil} : Island"

        # Landfill
    antique_baileyminesign = f"{DoLItemNames.antique_baileyminesign} : Landfill"
    antique_incenseburner = f"{DoLItemNames.antique_incenseburner} : Landfill"
    antique_cup = f"{DoLItemNames.antique_cup} : Landfill"

        # Museum
    antique_silvermask = f"{DoLItemNames.antique_silvermask} : Museum"

        # Bird Tower
    # antique_bullet = also found in moor

        # Manors
    antique_silveramulet = f"{DoLItemNames.antique_silveramulet} : Manors"

        # Compound
    antique_hourglass = f"{DoLItemNames.antique_hourglass} : Compound"

        # Pirate Ship
    antique_swordcane = f"{DoLItemNames.antique_swordcane} : Pirate Ship"
    antique_chocolate = f"{DoLItemNames.antique_chocolate} : Pirate Ship"
    antique_teacaddy = f"{DoLItemNames.antique_teacaddy} : Pirate Ship"
    antique_woodenfigurine = f"{DoLItemNames.antique_woodenfigurine} : Pirate Ship"
    antique_copperring = f"{DoLItemNames.antique_copperring} : Pirate Ship"
    antique_goldcompass = f"{DoLItemNames.antique_goldcompass} : Pirate Ship"

        # Ocean
    antique_coppercompass = f"{DoLItemNames.antique_coppercompass} : Ocean"
    antique_coralring = f"{DoLItemNames.antique_coralring} : Ocean"
    antique_diamond = f"{DoLItemNames.antique_diamond} : Ocean"

        # Temple
    antique_brassstatuette = f"{DoLItemNames.antique_brassstatuette} : Temple"

        # Avery Mansion
    antique_golddagger = f"{DoLItemNames.antique_golddagger} : Avery's Mansion"
    antique_goldamulet = f"{DoLItemNames.antique_goldamulet} : Avery's Mansion"
    antique_goldmask = f"{DoLItemNames.antique_goldmask} : Avery's Mansion"

        # Beach Cave
    antique_silvercompass = f"{DoLItemNames.antique_silvercompass} : Beach Cave"
    antique_leathermap = f"{DoLItemNames.antique_leathermap} : Beach Cave"
    antique_cutlass = f"{DoLItemNames.antique_cutlass} : Beach Cave"
    antique_silverdagger = f"{DoLItemNames.antique_silverdagger} : Beach Cave"
    antique_rustedcutlass = f"{DoLItemNames.antique_rustedcutlass} : Beach Cave"

        # Sewers
    antique_pinkcrystal = f"{DoLItemNames.antique_pinkcrystal} : Sewers"
    antique_candlestick = f"{DoLItemNames.antique_candlestick} : Sewers"
    antique_dildo = f"{DoLItemNames.antique_dildo} : Sewers"
    # antique_horn = also found in maze
    antique_watch = f"{DoLItemNames.antique_watch} : Sewers"


    # Skill Levels
    skill_skulduggery_1 = "Skulduggery Rank F+" # F+ 
    skill_skulduggery_2 = "Skulduggery Rank D" # D
    skill_skulduggery_3 = "Skulduggery Rank D+" # D+
    skill_skulduggery_4 = "Skulduggery Rank C" # C
    skill_skulduggery_5 = "Skulduggery Rank C+" # C+
    skill_skulduggery_6 = "Skulduggery Rank B" # B
    skill_skulduggery_7 = "Skulduggery Rank B+" # B+
    skill_skulduggery_8 = "Skulduggery Rank A" # A
    skill_skulduggery_9 = "Skulduggery Rank A+" # A+
    skill_skulduggery_10 = "Skulduggery Rank S"  # S

    skill_dancing_1 = "Dancing Rank F+" # F+
    skill_dancing_2 = "Dancing Rank D" # D
    skill_dancing_3 = "Dancing Rank D+" # D+
    skill_dancing_4 = "Dancing Rank C" # C
    skill_dancing_5 = "Dancing Rank C+" # C+
    skill_dancing_6 = "Dancing Rank B" # B
    skill_dancing_7 = "Dancing Rank B+" # B+
    skill_dancing_8 = "Dancing Rank A" # A
    skill_dancing_9 = "Dancing Rank A+" # A+
    skill_dancing_10 = "Dancing Rank S"  # S

    skill_swimming_1 = "Swimming Rank F+" # F+
    skill_swimming_2 = "Swimming Rank D" # D
    skill_swimming_3 = "Swimming Rank D+" # D+
    skill_swimming_4 = "Swimming Rank C" # C
    skill_swimming_5 = "Swimming Rank C+" # C+
    skill_swimming_6 = "Swimming Rank B" # B
    skill_swimming_7 = "Swimming Rank B+" # B+
    skill_swimming_8 = "Swimming Rank A" # A
    skill_swimming_9 = "Swimming Rank A+" # A+
    skill_swimming_10 = "Swimming Rank S"  # S

    skill_athletics_1 = "Athletics Rank F+" # F+
    skill_athletics_2 = "Athletics Rank D" # D
    skill_athletics_3 = "Athletics Rank D+" # D+
    skill_athletics_4 = "Athletics Rank C" # C
    skill_athletics_5 = "Athletics Rank C+" # C+
    skill_athletics_6 = "Athletics Rank B" # B
    skill_athletics_7 = "Athletics Rank B+" # B+
    skill_athletics_8 = "Athletics Rank A" # A
    skill_athletics_9 = "Athletics Rank A+" # A+
    skill_athletics_10 = "Athletics Rank S"  # S

    skill_tending_1 = "Tending Rank F+" # F+
    skill_tending_2 = "Tending Rank D" # D
    skill_tending_3 = "Tending Rank D+" # D+
    skill_tending_4 = "Tending Rank C" # C
    skill_tending_5 = "Tending Rank C+" # C+
    skill_tending_6 = "Tending Rank B" # B
    skill_tending_7 = "Tending Rank B+" # B+
    skill_tending_8 = "Tending Rank A" # A
    skill_tending_9 = "Tending Rank A+" # A+
    skill_tending_10 = "Tending Rank S"  # S

    skill_housekeeping_1 = "Housekeeping Rank F+" # F+
    skill_housekeeping_2 = "Housekeeping Rank D" # D
    skill_housekeeping_3 = "Housekeeping Rank D+" # D+
    skill_housekeeping_4 = "Housekeeping Rank C" # C
    skill_housekeeping_5 = "Housekeeping Rank C+" # C+
    skill_housekeeping_6 = "Housekeeping Rank B" # B
    skill_housekeeping_7 = "Housekeeping Rank B+" # B+
    skill_housekeeping_8 = "Housekeeping Rank A" # A
    skill_housekeeping_9 = "Housekeeping Rank A+" # A+
    skill_housekeeping_10 = "Housekeeping Rank S"  # S

    skill_seduction_1 = "Seduction Rank D" # D
    skill_seduction_2 = "Seduction Rank C" # C
    skill_seduction_3 = "Seduction Rank B" # B
    skill_seduction_4 = "Seduction Rank A" # A
    skill_seduction_5 = "Seduction Rank S" # S

    skill_oral_1 = "Oral Rank D" # D
    skill_oral_2 = "Oral Rank C" # C
    skill_oral_3 = "Oral Rank B" # B
    skill_oral_4 = "Oral Rank A" # A
    skill_oral_5 = "Oral Rank S" # S

    skill_chest_1 = "Chest Rank D" # D
    skill_chest_2 = "Chest Rank C" # C
    skill_chest_3 = "Chest Rank B" # B
    skill_chest_4 = "Chest Rank A" # A
    skill_chest_5 = "Chest Rank S" # S

    skill_hands_1 = "Hands Rank D" # D
    skill_hands_2 = "Hands Rank C" # C
    skill_hands_3 = "Hands Rank B" # B
    skill_hands_4 = "Hands Rank A" # A
    skill_hands_5 = "Hands Rank S" # S

    skill_buttocks_1 = "Buttocks Rank D" # D
    skill_buttocks_2 = "Buttocks Rank C" # C
    skill_buttocks_3 = "Buttocks Rank B" # B
    skill_buttocks_4 = "Buttocks Rank A" # A
    skill_buttocks_5 = "Buttocks Rank S" # S

    skill_privates_1 = "Privates Rank D" # D
    skill_privates_2 = "Privates Rank C" # C
    skill_privates_3 = "Privates Rank B" # B
    skill_privates_4 = "Privates Rank A" # A
    skill_privates_5 = "Privates Rank S" # S

    skill_anal_1 = "Anal Rank D" # D
    skill_anal_2 = "Anal Rank C" # C
    skill_anal_3 = "Anal Rank B" # B
    skill_anal_4 = "Anal Rank A" # A
    skill_anal_5 = "Anal Rank S" # S

    skill_thighs_1 = "Thighs Rank D" # D
    skill_thighs_2 = "Thighs Rank C" # C
    skill_thighs_3 = "Thighs Rank B" # B
    skill_thighs_4 = "Thighs Rank A" # A
    skill_thighs_5 = "Thighs Rank S" # S

    skill_feet_1 = "Feet Rank D" # D
    skill_feet_2 = "Feet Rank C" # C
    skill_feet_3 = "Feet Rank B" # B
    skill_feet_4 = "Feet Rank A" # A
    skill_feet_5 = "Feet Rank S" # S

    skill_science_1 = "Science Rank D" # D : 0
    skill_science_2 = "Science Rank C" # C : 1
    skill_science_3 = "Science Rank B" # B : 2
    skill_science_4 = "Science Rank A" # A : 3
    skill_science_5 = "Science Rank A*" # A* : 4

    skill_math_1 = "Math Rank D" # D : 0
    skill_math_2 = "Math Rank C" # C : 1
    skill_math_3 = "Math Rank B" # B : 2
    skill_math_4 = "Math Rank A" # A : 3
    skill_math_5 = "Math Rank A*" # A* : 4

    skill_english_1 = "English Rank D" # D : 0
    skill_english_2 = "English Rank C" # C : 1
    skill_english_3 = "English Rank B" # B : 2
    skill_english_4 = "English Rank A" # A : 3
    skill_english_5 = "English Rank A*" # A* : 4

    skill_history_1 = "History Rank D" # D : 0
    skill_history_2 = "History Rank C" # C : 1
    skill_history_3 = "History Rank B" # B : 2
    skill_history_4 = "History Rank A" # A : 3
    skill_history_5 = "History Rank A*" # A* : 4

    skill_willpower_1 = "Willpower Rank 1" # fainthearted
    skill_willpower_2 = "Willpower Rank 2" # mindful
    skill_willpower_3 = "Willpower Rank 3" # resolved
    skill_willpower_4 = "Willpower Rank 4" # determined
    skill_willpower_5 = "Willpower Rank 5" # tenacious
    skill_willpower_6 = "Willpower Rank 6" # iron

    skill_physique_1 = "Physique Rank 1" # skinny
    skill_physique_2 = "Physique Rank 2" # slender
    skill_physique_3 = "Physique Rank 3" # slim
    skill_physique_4 = "Physique Rank 4" # athletic
    skill_physique_5 = "Physique Rank 5" # firm
    skill_physique_6 = "Physique Rank 6" # powerful

    skill_promiscuity_1 = "Promiscuity Rank 1" # prudish
    skill_promiscuity_2 = "Promiscuity Rank 2" # curious
    skill_promiscuity_3 = "Promiscuity Rank 3" # excited
    skill_promiscuity_4 = "Promiscuity Rank 4" # crave
    skill_promiscuity_5 = "Promiscuity Rank 5" # slut
    skill_promiscuity_6 = "Promiscuity Rank 6" # insatiable

    skill_exhibitionism_1 = "Exhibitionism Rank 1" # shy
    skill_exhibitionism_2 = "Exhibitionism Rank 2" # like
    skill_exhibitionism_3 = "Exhibitionism Rank 3" # enjoy
    skill_exhibitionism_4 = "Exhibitionism Rank 4" # excites
    skill_exhibitionism_5 = "Exhibitionism Rank 5" # shameless
    skill_exhibitionism_6 = "Exhibitionism Rank 6" # wild

    skill_deviancy_1 = "Deviancy Rank 1" # conventional
    skill_deviancy_2 = "Deviancy Rank 2" # strange
    skill_deviancy_3 = "Deviancy Rank 3" # shocking
    skill_deviancy_4 = "Deviancy Rank 4" # scandalous
    skill_deviancy_5 = "Deviancy Rank 5" # crave
    skill_deviancy_6 = "Deviancy Rank 6" # lust

class DoLRules(Enum):
    # optionfilter...
    # if option X equals (or whatever is set as condition) 
    # option_true or option_false
    # return true or false


    # if skills are not randomized don't include having required levels as a rule
    skulduggery_1 = Has("Progressive Skulduggery Rank", 1) | OptionFilter(RandomizeSkills, RandomizeSkills.option_false) # F+ 
    skulduggery_2 = Has("Progressive Skulduggery Rank", 2) | OptionFilter(RandomizeSkills, RandomizeSkills.option_false) # D
    skulduggery_3 = Has("Progressive Skulduggery Rank", 3) | OptionFilter(RandomizeSkills, RandomizeSkills.option_false) # D+
    skulduggery_4 = Has("Progressive Skulduggery Rank", 4) | OptionFilter(RandomizeSkills, RandomizeSkills.option_false) # C
    skulduggery_5 = Has("Progressive Skulduggery Rank", 5) | OptionFilter(RandomizeSkills, RandomizeSkills.option_false) # C+
    skulduggery_6 = Has("Progressive Skulduggery Rank", 6) | OptionFilter(RandomizeSkills, RandomizeSkills.option_false) # B
    skulduggery_7 = Has("Progressive Skulduggery Rank", 7) | OptionFilter(RandomizeSkills, RandomizeSkills.option_false) # B+
    skulduggery_8 = Has("Progressive Skulduggery Rank", 8) | OptionFilter(RandomizeSkills, RandomizeSkills.option_false) # A
    skulduggery_9 = Has("Progressive Skulduggery Rank", 9) | OptionFilter(RandomizeSkills, RandomizeSkills.option_false) # A+
    skulduggery_10 = Has("Progressive Skulduggery Rank", 10) | OptionFilter(RandomizeSkills, RandomizeSkills.option_false) # S

    dancing_1 = Has("Progressive Dancing Rank", 1) | OptionFilter(RandomizeSkills, RandomizeSkills.option_false) # F+
    dancing_2 = Has("Progressive Dancing Rank", 2) | OptionFilter(RandomizeSkills, RandomizeSkills.option_false) # D
    dancing_3 = Has("Progressive Dancing Rank", 3) | OptionFilter(RandomizeSkills, RandomizeSkills.option_false) # D+
    dancing_4 = Has("Progressive Dancing Rank", 4) | OptionFilter(RandomizeSkills, RandomizeSkills.option_false) # C
    dancing_5 = Has("Progressive Dancing Rank", 5) | OptionFilter(RandomizeSkills, RandomizeSkills.option_false) # C+
    dancing_6 = Has("Progressive Dancing Rank", 6) | OptionFilter(RandomizeSkills, RandomizeSkills.option_false) # B
    dancing_7 = Has("Progressive Dancing Rank", 7) | OptionFilter(RandomizeSkills, RandomizeSkills.option_false) # B+
    dancing_8 = Has("Progressive Dancing Rank", 8) | OptionFilter(RandomizeSkills, RandomizeSkills.option_false) # A
    dancing_9 = Has("Progressive Dancing Rank", 9) | OptionFilter(RandomizeSkills, RandomizeSkills.option_false) # A+
    dancing_10 = Has("Progressive Dancing Rank", 10) | OptionFilter(RandomizeSkills, RandomizeSkills.option_false) # S

    swimming_1 = Has("Progressive Swimming Rank", 1) | OptionFilter(RandomizeSkills, RandomizeSkills.option_false) # F+
    swimming_2 = Has("Progressive Swimming Rank", 2) | OptionFilter(RandomizeSkills, RandomizeSkills.option_false) # D
    swimming_3 = Has("Progressive Swimming Rank", 3) | OptionFilter(RandomizeSkills, RandomizeSkills.option_false) # D+
    swimming_4 = Has("Progressive Swimming Rank", 4) | OptionFilter(RandomizeSkills, RandomizeSkills.option_false) # C
    swimming_5 = Has("Progressive Swimming Rank", 5) | OptionFilter(RandomizeSkills, RandomizeSkills.option_false) # C+
    swimming_6 = Has("Progressive Swimming Rank", 6) | OptionFilter(RandomizeSkills, RandomizeSkills.option_false) # B
    swimming_7 = Has("Progressive Swimming Rank", 7) | OptionFilter(RandomizeSkills, RandomizeSkills.option_false) # B+
    swimming_8 = Has("Progressive Swimming Rank", 8) | OptionFilter(RandomizeSkills, RandomizeSkills.option_false) # A
    swimming_9 = Has("Progressive Swimming Rank", 9) | OptionFilter(RandomizeSkills, RandomizeSkills.option_false) # A+
    swimming_10 = Has("Progressive Swimming Rank", 10) | OptionFilter(RandomizeSkills, RandomizeSkills.option_false) # S

    athletics_1 = Has("Progressive Athletics Rank", 1) | OptionFilter(RandomizeSkills, RandomizeSkills.option_false) # F+
    athletics_2 = Has("Progressive Athletics Rank", 2) | OptionFilter(RandomizeSkills, RandomizeSkills.option_false) # D
    athletics_3 = Has("Progressive Athletics Rank", 3) | OptionFilter(RandomizeSkills, RandomizeSkills.option_false) # D+
    athletics_4 = Has("Progressive Athletics Rank", 4) | OptionFilter(RandomizeSkills, RandomizeSkills.option_false) # C
    athletics_5 = Has("Progressive Athletics Rank", 5) | OptionFilter(RandomizeSkills, RandomizeSkills.option_false) # C+
    athletics_6 = Has("Progressive Athletics Rank", 6) | OptionFilter(RandomizeSkills, RandomizeSkills.option_false) # B
    athletics_7 = Has("Progressive Athletics Rank", 7) | OptionFilter(RandomizeSkills, RandomizeSkills.option_false) # B+
    athletics_8 = Has("Progressive Athletics Rank", 8) | OptionFilter(RandomizeSkills, RandomizeSkills.option_false) # A
    athletics_9 = Has("Progressive Athletics Rank", 9) | OptionFilter(RandomizeSkills, RandomizeSkills.option_false) # A+
    athletics_10 = Has("Progressive Athletics Rank", 10) | OptionFilter(RandomizeSkills, RandomizeSkills.option_false) # S

    tending_1 = Has("Progressive Tending Rank", 1) | OptionFilter(RandomizeSkills, RandomizeSkills.option_false) # F+
    tending_2 = Has("Progressive Tending Rank", 2) | OptionFilter(RandomizeSkills, RandomizeSkills.option_false) # D
    tending_3 = Has("Progressive Tending Rank", 3) | OptionFilter(RandomizeSkills, RandomizeSkills.option_false) # D+
    tending_4 = Has("Progressive Tending Rank", 4) | OptionFilter(RandomizeSkills, RandomizeSkills.option_false) # C
    tending_5 = Has("Progressive Tending Rank", 5) | OptionFilter(RandomizeSkills, RandomizeSkills.option_false) # C+
    tending_6 = Has("Progressive Tending Rank", 6) | OptionFilter(RandomizeSkills, RandomizeSkills.option_false) # B
    tending_7 = Has("Progressive Tending Rank", 7) | OptionFilter(RandomizeSkills, RandomizeSkills.option_false) # B+
    tending_8 = Has("Progressive Tending Rank", 8) | OptionFilter(RandomizeSkills, RandomizeSkills.option_false) # A
    tending_9 = Has("Progressive Tending Rank", 9) | OptionFilter(RandomizeSkills, RandomizeSkills.option_false) # A+
    tending_10 = Has("Progressive Tending Rank", 10) | OptionFilter(RandomizeSkills, RandomizeSkills.option_false) # S

    housekeeping_1 = Has("Progressive Housekeeping Rank", 1) | OptionFilter(RandomizeSkills, RandomizeSkills.option_false) # F+
    housekeeping_2 = Has("Progressive Housekeeping Rank", 2) | OptionFilter(RandomizeSkills, RandomizeSkills.option_false) # D
    housekeeping_3 = Has("Progressive Housekeeping Rank", 3) | OptionFilter(RandomizeSkills, RandomizeSkills.option_false) # D+
    housekeeping_4 = Has("Progressive Housekeeping Rank", 4) | OptionFilter(RandomizeSkills, RandomizeSkills.option_false) # C
    housekeeping_5 = Has("Progressive Housekeeping Rank", 5) | OptionFilter(RandomizeSkills, RandomizeSkills.option_false) # C+
    housekeeping_6 = Has("Progressive Housekeeping Rank", 6) | OptionFilter(RandomizeSkills, RandomizeSkills.option_false) # B
    housekeeping_7 = Has("Progressive Housekeeping Rank", 7) | OptionFilter(RandomizeSkills, RandomizeSkills.option_false) # B+
    housekeeping_8 = Has("Progressive Housekeeping Rank", 8) | OptionFilter(RandomizeSkills, RandomizeSkills.option_false) # A
    housekeeping_9 = Has("Progressive Housekeeping Rank", 9) | OptionFilter(RandomizeSkills, RandomizeSkills.option_false) # A+
    housekeeping_10 = Has("Progressive Housekeeping Rank", 10) | OptionFilter(RandomizeSkills, RandomizeSkills.option_false) # S

    seduction_1 = Has("Progressive Seduction Rank", 1) | OptionFilter(RandomizeSkills, RandomizeSkills.option_false) # D
    seduction_2 = Has("Progressive Seduction Rank", 2) | OptionFilter(RandomizeSkills, RandomizeSkills.option_false) # C
    seduction_3 = Has("Progressive Seduction Rank", 3) | OptionFilter(RandomizeSkills, RandomizeSkills.option_false) # B
    seduction_4 = Has("Progressive Seduction Rank", 4) | OptionFilter(RandomizeSkills, RandomizeSkills.option_false) # A
    seduction_5 = Has("Progressive Seduction Rank", 5) | OptionFilter(RandomizeSkills, RandomizeSkills.option_false) # S

    oral_1 = Has("Progressive Oral Rank", 1) | OptionFilter(RandomizeSkills, RandomizeSkills.option_false) # D
    oral_2 = Has("Progressive Oral Rank", 2) | OptionFilter(RandomizeSkills, RandomizeSkills.option_false) # C
    oral_3 = Has("Progressive Oral Rank", 3) | OptionFilter(RandomizeSkills, RandomizeSkills.option_false) # B
    oral_4 = Has("Progressive Oral Rank", 4) | OptionFilter(RandomizeSkills, RandomizeSkills.option_false) # A
    oral_5 = Has("Progressive Oral Rank", 5) | OptionFilter(RandomizeSkills, RandomizeSkills.option_false) # S

    chest_1 = Has("Progressive Chest Rank", 1) | OptionFilter(RandomizeSkills, RandomizeSkills.option_false) # D
    chest_2 = Has("Progressive Chest Rank", 2) | OptionFilter(RandomizeSkills, RandomizeSkills.option_false) # C
    chest_3 = Has("Progressive Chest Rank", 3) | OptionFilter(RandomizeSkills, RandomizeSkills.option_false) # B
    chest_4 = Has("Progressive Chest Rank", 4) | OptionFilter(RandomizeSkills, RandomizeSkills.option_false) # A
    chest_5 = Has("Progressive Chest Rank", 5) | OptionFilter(RandomizeSkills, RandomizeSkills.option_false) # S

    hands_1 = Has("Progressive Hands Rank", 1) | OptionFilter(RandomizeSkills, RandomizeSkills.option_false) # D
    hands_2 = Has("Progressive Hands Rank", 2) | OptionFilter(RandomizeSkills, RandomizeSkills.option_false) # C
    hands_3 = Has("Progressive Hands Rank", 3) | OptionFilter(RandomizeSkills, RandomizeSkills.option_false) # B
    hands_4 = Has("Progressive Hands Rank", 4) | OptionFilter(RandomizeSkills, RandomizeSkills.option_false) # A
    hands_5 = Has("Progressive Hands Rank", 5) | OptionFilter(RandomizeSkills, RandomizeSkills.option_false) # S

    buttocks_1 = Has("Progressive Buttocks Rank", 1) | OptionFilter(RandomizeSkills, RandomizeSkills.option_false) # D
    buttocks_2 = Has("Progressive Buttocks Rank", 2) | OptionFilter(RandomizeSkills, RandomizeSkills.option_false) # C
    buttocks_3 = Has("Progressive Buttocks Rank", 3) | OptionFilter(RandomizeSkills, RandomizeSkills.option_false) # B
    buttocks_4 = Has("Progressive Buttocks Rank", 4) | OptionFilter(RandomizeSkills, RandomizeSkills.option_false) # A
    buttocks_5 = Has("Progressive Buttocks Rank", 5) | OptionFilter(RandomizeSkills, RandomizeSkills.option_false) # S

    privates_1 = Has("Progressive Privates Rank", 1) | OptionFilter(RandomizeSkills, RandomizeSkills.option_false) # D
    privates_2 = Has("Progressive Privates Rank", 2) | OptionFilter(RandomizeSkills, RandomizeSkills.option_false) # C
    privates_3 = Has("Progressive Privates Rank", 3) | OptionFilter(RandomizeSkills, RandomizeSkills.option_false) # B
    privates_4 = Has("Progressive Privates Rank", 4) | OptionFilter(RandomizeSkills, RandomizeSkills.option_false) # A
    privates_5 = Has("Progressive Privates Rank", 5) | OptionFilter(RandomizeSkills, RandomizeSkills.option_false) # S

    anal_1 = Has("Progressive Anal Rank", 1) | OptionFilter(RandomizeSkills, RandomizeSkills.option_false) # D
    anal_2 = Has("Progressive Anal Rank", 2) | OptionFilter(RandomizeSkills, RandomizeSkills.option_false) # C
    anal_3 = Has("Progressive Anal Rank", 3) | OptionFilter(RandomizeSkills, RandomizeSkills.option_false) # B
    anal_4 = Has("Progressive Anal Rank", 4) | OptionFilter(RandomizeSkills, RandomizeSkills.option_false) # A
    anal_5 = Has("Progressive Anal Rank", 5) | OptionFilter(RandomizeSkills, RandomizeSkills.option_false) # S

    thighs_1 = Has("Progressive Thighs Rank", 1) | OptionFilter(RandomizeSkills, RandomizeSkills.option_false) # D
    thighs_2 = Has("Progressive Thighs Rank", 2) | OptionFilter(RandomizeSkills, RandomizeSkills.option_false) # C
    thighs_3 = Has("Progressive Thighs Rank", 3) | OptionFilter(RandomizeSkills, RandomizeSkills.option_false) # B
    thighs_4 = Has("Progressive Thighs Rank", 4) | OptionFilter(RandomizeSkills, RandomizeSkills.option_false) # A
    thighs_5 = Has("Progressive Thighs Rank", 5) | OptionFilter(RandomizeSkills, RandomizeSkills.option_false) # S

    feet_1 = Has("Progressive Feet Rank", 1) | OptionFilter(RandomizeSkills, RandomizeSkills.option_false) # D
    feet_2 = Has("Progressive Feet Rank", 2) | OptionFilter(RandomizeSkills, RandomizeSkills.option_false) # C
    feet_3 = Has("Progressive Feet Rank", 3) | OptionFilter(RandomizeSkills, RandomizeSkills.option_false) # B
    feet_4 = Has("Progressive Feet Rank", 4) | OptionFilter(RandomizeSkills, RandomizeSkills.option_false) # A
    feet_5 = Has("Progressive Feet Rank", 5) | OptionFilter(RandomizeSkills, RandomizeSkills.option_false) # S

    science_1 = Has("Progressive Science Rank", 1) | OptionFilter(RandomizeSkills, RandomizeSkills.option_false) # D : 0
    science_2 = Has("Progressive Science Rank", 2) | OptionFilter(RandomizeSkills, RandomizeSkills.option_false) # C : 1
    science_3 = Has("Progressive Science Rank", 3) | OptionFilter(RandomizeSkills, RandomizeSkills.option_false) # B : 2
    science_4 = Has("Progressive Science Rank", 4) | OptionFilter(RandomizeSkills, RandomizeSkills.option_false) # A : 3
    science_5 = Has("Progressive Science Rank", 5) | OptionFilter(RandomizeSkills, RandomizeSkills.option_false) # A* : 4

    math_1 = Has("Progressive Math Rank", 1) | OptionFilter(RandomizeSkills, RandomizeSkills.option_false) # D : 0
    math_2 = Has("Progressive Math Rank", 2) | OptionFilter(RandomizeSkills, RandomizeSkills.option_false) # C : 1
    math_3 = Has("Progressive Math Rank", 3) | OptionFilter(RandomizeSkills, RandomizeSkills.option_false) # B : 2
    math_4 = Has("Progressive Math Rank", 4) | OptionFilter(RandomizeSkills, RandomizeSkills.option_false) # A : 3
    math_5 = Has("Progressive Math Rank", 5) | OptionFilter(RandomizeSkills, RandomizeSkills.option_false) # A* : 4

    english_1 = Has("Progressive English Rank", 1) | OptionFilter(RandomizeSkills, RandomizeSkills.option_false) # D : 0
    english_2 = Has("Progressive English Rank", 2) | OptionFilter(RandomizeSkills, RandomizeSkills.option_false) # C : 1
    english_3 = Has("Progressive English Rank", 3) | OptionFilter(RandomizeSkills, RandomizeSkills.option_false) # B : 2
    english_4 = Has("Progressive English Rank", 4) | OptionFilter(RandomizeSkills, RandomizeSkills.option_false) # A : 3
    english_5 = Has("Progressive English Rank", 5) | OptionFilter(RandomizeSkills, RandomizeSkills.option_false) # A* : 4

    history_1 = Has("Progressive History Rank", 1) | OptionFilter(RandomizeSkills, RandomizeSkills.option_false) # D : 0
    history_2 = Has("Progressive History Rank", 2) | OptionFilter(RandomizeSkills, RandomizeSkills.option_false) # C : 1
    history_3 = Has("Progressive History Rank", 3) | OptionFilter(RandomizeSkills, RandomizeSkills.option_false) # B : 2
    history_4 = Has("Progressive History Rank", 4) | OptionFilter(RandomizeSkills, RandomizeSkills.option_false) # A : 3
    history_5 = Has("Progressive History Rank", 5) | OptionFilter(RandomizeSkills, RandomizeSkills.option_false) # A* : 4

    willpower_1 = Has("Progressive Willpower Rank", 1) | OptionFilter(RandomizeSkills, RandomizeSkills.option_false) # fainthearted
    willpower_2 = Has("Progressive Willpower Rank", 2) | OptionFilter(RandomizeSkills, RandomizeSkills.option_false) # mindful
    willpower_3 = Has("Progressive Willpower Rank", 3) | OptionFilter(RandomizeSkills, RandomizeSkills.option_false) # resolved
    willpower_4 = Has("Progressive Willpower Rank", 4) | OptionFilter(RandomizeSkills, RandomizeSkills.option_false) # determined
    willpower_5 = Has("Progressive Willpower Rank", 5) | OptionFilter(RandomizeSkills, RandomizeSkills.option_false) # tenacious
    willpower_6 = Has("Progressive Willpower Rank", 6) | OptionFilter(RandomizeSkills, RandomizeSkills.option_false) # iron

    physique_1 = Has("Progressive Physique Rank", 1) | OptionFilter(RandomizeSkills, RandomizeSkills.option_false) # skinny
    physique_2 = Has("Progressive Physique Rank", 2) | OptionFilter(RandomizeSkills, RandomizeSkills.option_false) # slender
    physique_3 = Has("Progressive Physique Rank", 3) | OptionFilter(RandomizeSkills, RandomizeSkills.option_false) # slim
    physique_4 = Has("Progressive Physique Rank", 4) | OptionFilter(RandomizeSkills, RandomizeSkills.option_false) # athletic
    physique_5 = Has("Progressive Physique Rank", 5) | OptionFilter(RandomizeSkills, RandomizeSkills.option_false) # firm
    physique_6 = Has("Progressive Physique Rank", 6) | OptionFilter(RandomizeSkills, RandomizeSkills.option_false) # powerful

    promiscuity_1 = Has("Progressive Promiscuity Rank", 1) | OptionFilter(RandomizeSkills, RandomizeSkills.option_false) # prudish
    promiscuity_2 = Has("Progressive Promiscuity Rank", 2) | OptionFilter(RandomizeSkills, RandomizeSkills.option_false) # curious
    promiscuity_3 = Has("Progressive Promiscuity Rank", 3) | OptionFilter(RandomizeSkills, RandomizeSkills.option_false) # excited
    promiscuity_4 = Has("Progressive Promiscuity Rank", 4) | OptionFilter(RandomizeSkills, RandomizeSkills.option_false) # crave
    promiscuity_5 = Has("Progressive Promiscuity Rank", 5) | OptionFilter(RandomizeSkills, RandomizeSkills.option_false) # slut
    promiscuity_6 = Has("Progressive Promiscuity Rank", 6) | OptionFilter(RandomizeSkills, RandomizeSkills.option_false) # insatiable

    exhibitionism_1 = Has("Progressive Exhibitionism Rank", 1) | OptionFilter(RandomizeSkills, RandomizeSkills.option_false) # shy
    exhibitionism_2 = Has("Progressive Exhibitionism Rank", 2) | OptionFilter(RandomizeSkills, RandomizeSkills.option_false) # like
    exhibitionism_3 = Has("Progressive Exhibitionism Rank", 3) | OptionFilter(RandomizeSkills, RandomizeSkills.option_false) # enjoy
    exhibitionism_4 = Has("Progressive Exhibitionism Rank", 4) | OptionFilter(RandomizeSkills, RandomizeSkills.option_false) # excites
    exhibitionism_5 = Has("Progressive Exhibitionism Rank", 5) | OptionFilter(RandomizeSkills, RandomizeSkills.option_false) # shameless
    exhibitionism_6 = Has("Progressive Exhibitionism Rank", 6) | OptionFilter(RandomizeSkills, RandomizeSkills.option_false) # wild

    deviancy_1 = Has("Progressive Deviancy Rank", 1) | OptionFilter(RandomizeSkills, RandomizeSkills.option_false) # conventional
    deviancy_2 = Has("Progressive Deviancy Rank", 2) | OptionFilter(RandomizeSkills, RandomizeSkills.option_false) # strange
    deviancy_3 = Has("Progressive Deviancy Rank", 3) | OptionFilter(RandomizeSkills, RandomizeSkills.option_false) # shocking
    deviancy_4 = Has("Progressive Deviancy Rank", 4) | OptionFilter(RandomizeSkills, RandomizeSkills.option_false) # scandalous
    deviancy_5 = Has("Progressive Deviancy Rank", 5) | OptionFilter(RandomizeSkills, RandomizeSkills.option_false) # crave
    deviancy_6 = Has("Progressive Deviancy Rank", 6) | OptionFilter(RandomizeSkills, RandomizeSkills.option_false) # lust
    # if needed later add weapon skills here too
    
    # Museum Check
    antiques_10 = HasGroupUnique(DoLLocationTypes.antique.value, 10)
    antiques_20 = HasGroupUnique(DoLLocationTypes.antique.value, 20)
    silvermask = antiques_20


    # Item Checks
    fakeid = Has("Fake ID")

    # Area Checks
    access_orphanage = CanReachRegion(DoLRegionNames.orphanage)
    access_school = CanReachRegion(DoLRegionNames.school)

    # Game Options:

    multipleruns_toggle = OptionFilter(MultipleRuns, MultipleRuns.option_true)
    rng_toggle = OptionFilter(DontRestrictRNG, DontRestrictRNG.option_true)

    # World Options:
    anal_toggle = OptionFilter(Anal, Anal.option_true)
    tentacles_toggle = OptionFilter(Tentacles, Tentacles.option_true)
    lactation_toggle = OptionFilter(Lactation, Lactation.option_true)
    softvore_toggle = OptionFilter(SoftVore, SoftVore.option_true)
    beastiality_toggle = OptionFilter(Beastiality, Beastiality.option_true)
    parasites_toggle = OptionFilter(Parasites, Parasites.option_true)
    # swarms_toggle = OptionFilter(Swarms)
    bodywriting_toggle = OptionFilter(Bodywriting, Bodywriting.option_true)

    pregnancy_toggle = OptionFilter(Pregnancy, Pregnancy.option_true)
    parasiticpregnancy_toggle = OptionFilter(ParasiticPregnancy, ParasiticPregnancy.option_true)

    animal_transformation_toggle = OptionFilter(AnimalTransformations, AnimalTransformations.option_true)
    divine_transformation_toggle = OptionFilter(DivineTransformations, DivineTransformations.option_true)


    # Transformations:
    randomize_tf_parts = OptionFilter(RandomizeTransformations, RandomizeTransformations.option_tfparts)
    randomize_tf_full = OptionFilter(RandomizeTransformations, RandomizeTransformations.option_transformations)
    
    wolf_tf = Has("Wolf Transformation") & randomize_tf_parts | randomize_tf_full  # TODO: update with actual part 
    harpy_tf = Has("Harpy Transformation")

    flight = Has("Flight")

    # Sexual Traits
    bitch_trait = beastiality_toggle
    prey_trait = tentacles_toggle
    tasty_trait = softvore_toggle
    milkaddict_trait = lactation_toggle

    # Area Rulings:
    tentacle_plains = tentacles_toggle & deviancy_5
    tentacle_forest = tentacles_toggle

    # avery_mansion_score = Rule(housekeeping_4) # replace with adoption papers check

    # # Feat Rulings:
    # # no_control = Rule(beastiality_toggle) # "beastiality or monster people"? so doesn't require any toggle?
    # # equinerescue_feat = Rule(beastiality_toggle) # TODO: double check that this requires beastiality, I dobut it
    # # headpack_feat = Rule(beastiality_toggle) # TODO: double check that this requires beastiality, I dobut it
    # # foodchain_feat = Rule(beastiality_toggle) # TODO: double check that this requires beastiality, I dobut it
    # knot_feat = beastiality_toggle

    # sexspecialist_feat = anal_toggle
    # pridefarm_feat = lactation_toggle
    # crimmostfowl_feat = bodywriting_toggle # sydney will write on you unless you have bodywriting **off**

    # animal_transformation_feat = animal_transformation_toggle # all feats that require an animal tf
    # angel_feat = divine_transformation_toggle & multipleruns_toggle
    # fallenangel_feat = divine_transformation_toggle & multipleruns_toggle
    # demon_feat = divine_transformation_toggle
    
    # specialtraitcollector_feat = bitch_trait & prey_trait & tasty_trait & milkaddict_trait
    
    # broodmother_feat = parasiticpregnancy_toggle & tentacles_toggle & beastiality_toggle
    # # zoologist also here ^
    # earslime_feat = parasites_toggle & parasiticpregnancy_toggle # change if I ever swap parasitic preg toggle
    # # ear slime amalgam also here ^
    # giantslug_feat = parasiticpregnancy_toggle # change if I ever swap parasitic preg toggle
    # redemption_feat = divine_transformation_toggle
    
    # getpregnant_feat = pregnancy_toggle
    # fatherhood_feat = pregnancy_toggle
    # mpreg_feat = pregnancy_toggle & parasites_toggle
    # hailmary_feat = pregnancy_toggle & multipleruns_toggle

LOCATION_DATA:dict[DoLLocationNames, tuple[int, DoLLocationTypes, list[DoLRegionNames]]] = {

    # -------- Antiques --------
    
    DoLLocationNames.antique_ivorystatuette: (100, DoLLocationTypes.antique, [
                    DoLRegionNames.temple
                ]), # antiqueivorystatuette

    DoLLocationNames.antique_silvercoin: (101, DoLLocationTypes.antique, [
                    DoLRegionNames.temple,
                    DoLRegionNames.moor
                ]), # antiquesilvercoin

    DoLLocationNames.antique_crystal: (102, DoLLocationTypes.antique, [
                    DoLRegionNames.temple
                ]), # antiquewhitecrystal

    DoLLocationNames.antique_silverblade: (103, DoLLocationTypes.antique, [
                    DoLRegionNames.temple
                ]), # antiquesilverblade

    DoLLocationNames.antique_coppercoin: (104, DoLLocationTypes.antique, [
                    DoLRegionNames.temple
                ]), # antiquecoppercoin

    DoLLocationNames.antique_silvergoblet: (105, DoLLocationTypes.antique, [
                    DoLRegionNames.temple
                ]), # antiquesilvergoblet

    DoLLocationNames.antique_fetish: (106, DoLLocationTypes.antique, [
                    DoLRegionNames.temple
                ]), # antiquestrangefetish

    DoLLocationNames.antique_goldcoin: (107, DoLLocationTypes.antique, [
                    DoLRegionNames.temple
                ]), # antiquegoldcoin

    DoLLocationNames.antique_forestdagger: (108, DoLLocationTypes.antique, [
                    DoLRegionNames.forest
                ]), # antiqueforestdagger

    DoLLocationNames.antique_forestgem: (109, DoLLocationTypes.antique, [
                    DoLRegionNames.forest
                ]), # antiqueforestgem

    DoLLocationNames.antique_arrow: (110, DoLLocationTypes.antique, [
                    DoLRegionNames.forest
                ]), # antiqueforestarrow

    DoLLocationNames.antique_ivorynecklace: (111, DoLLocationTypes.antique, [
                    DoLRegionNames.forest_lake
                ]), # antiqueivorynecklace

    DoLLocationNames.antique_ivorybox: (112, DoLLocationTypes.antique, [
                    DoLRegionNames.forest_lake
                ]), # antiquebox

    DoLLocationNames.antique_silverring: (113, DoLLocationTypes.antique, [
                    DoLRegionNames.forest_lake
                ]), # antiquesilverring

    DoLLocationNames.antique_goldnecklace: (114, DoLLocationTypes.antique, [
                    DoLRegionNames.forest_lake
                ]), # antiquegoldnecklace

    DoLLocationNames.antique_chastitybelt: (115, DoLLocationTypes.antique, [
                    DoLRegionNames.forest_lake
                ]), # antiquegoldchastitybelt

    DoLLocationNames.antique_stonetalisman: (116, DoLLocationTypes.antique, [
                    DoLRegionNames.meadow
                ]), # antiquestonetalisman

    DoLLocationNames.antique_horn: (117, DoLLocationTypes.antique, [
                    DoLRegionNames.moor, # maze
                    DoLRegionNames.residential_drain, # lower sewers 
                    DoLRegionNames.commercial_drain, # TODO: replace with deep sewers location?
                    DoLRegionNames.industrial_drain
                ]), # antiquehorn

    DoLLocationNames.antique_snuffer: (118, DoLLocationTypes.antique, [
                    DoLRegionNames.moor, # maze
                ]), # antiquesnuffer

    DoLLocationNames.antique_bucket: (119, DoLLocationTypes.antique, [
                    DoLRegionNames.moor, # maze
                ]), # antiquebucket

    DoLLocationNames.antique_silvermanacle: (120, DoLLocationTypes.antique, [
                    DoLRegionNames.moor, # maze
                ]), # antiquesilvermanacle

    DoLLocationNames.antique_whip: (121, DoLLocationTypes.antique, [
                    DoLRegionNames.moor, # maze
                ]), # antiquewhip

    DoLLocationNames.antique_goldring: (122, DoLLocationTypes.antique, [
                    DoLRegionNames.moor
                ]), # antiquegoldring

    DoLLocationNames.antique_bell: (123, DoLLocationTypes.antique, [
                    DoLRegionNames.moor
                ]), # antiquebell

    DoLLocationNames.antique_bullet: (124, DoLLocationTypes.antique, [
                    DoLRegionNames.moor,
                    DoLRegionNames.bird_tower
                ]), # antiquebullet

    DoLLocationNames.antique_artilleryshell: (125, DoLLocationTypes.antique, [
                    DoLRegionNames.moor
                ]), # antiqueshell

    DoLLocationNames.antique_grenade: (126, DoLLocationTypes.antique, [
                    DoLRegionNames.riding_school
                ]), # antiquegrenade

    DoLLocationNames.antique_goldbrooch: (127, DoLLocationTypes.antique, [
                    DoLRegionNames.dance_studio
                ]), # antiquegoldbrooch

    DoLLocationNames.antique_silverbrooch: (128, DoLLocationTypes.antique, [
                    DoLRegionNames.orphanage
                ]), # antiquesilverbrooch

    DoLLocationNames.antique_islanderarrow: (129, DoLLocationTypes.antique, [
                    DoLRegionNames.island
                ]), # antiqueislandarrow

    DoLLocationNames.antique_islandermask: (130, DoLLocationTypes.antique, [
                    DoLRegionNames.island
                ]), # antiquewoodenmask

    DoLLocationNames.antique_obsidiandisc: (131, DoLLocationTypes.antique, [
                    DoLRegionNames.island
                ]), # antiqueobsidiandisc

    DoLLocationNames.antique_trilobitefossil: (132, DoLLocationTypes.antique, [
                    DoLRegionNames.island
                ]), # antiquetrilobitefossil

    DoLLocationNames.antique_baileyminesign: (133, DoLLocationTypes.antique, [
                    DoLRegionNames.landfill
                ]), # antiqueminesign

    DoLLocationNames.antique_incenseburner: (134, DoLLocationTypes.antique, [
                    DoLRegionNames.landfill
                ]), # antiquetrashburner

    DoLLocationNames.antique_cup: (135, DoLLocationTypes.antique, [
                    DoLRegionNames.landfill
                ]), # antiquetrashcup 

    DoLLocationNames.antique_silvermask: (136, DoLLocationTypes.antique, [
                    DoLRegionNames.manors
                ]), # antiquesilvermask

    DoLLocationNames.antique_silveramulet: (137, DoLLocationTypes.antique, [
                    DoLRegionNames.compound
                ]), # antiquesilveramulet

    DoLLocationNames.antique_hourglass: (138, DoLLocationTypes.antique, [
                    DoLRegionNames.pirate_ship
                ]), # antiquehourglass

    DoLLocationNames.antique_swordcane: (139, DoLLocationTypes.antique, [
                    DoLRegionNames.pirate_ship
                ]), # antiqueswordcane

    DoLLocationNames.antique_chocolate: (140, DoLLocationTypes.antique, [
                    DoLRegionNames.pirate_ship
                ]), # antiquechocolate

    DoLLocationNames.antique_teacaddy: (141, DoLLocationTypes.antique, [
                    DoLRegionNames.pirate_ship
                ]), # antiqueteacaddy

    DoLLocationNames.antique_woodenfigurine: (142, DoLLocationTypes.antique, [
                    DoLRegionNames.pirate_ship
                ]), # antiquewoodenfigurine

    DoLLocationNames.antique_copperring: (143, DoLLocationTypes.antique, [
                    DoLRegionNames.pirate_ship
                ]), # antiquecopperring

    DoLLocationNames.antique_goldcompass: (144, DoLLocationTypes.antique, [
                    DoLRegionNames.pirate_ship
                ]), # antiquegoldcompass

    DoLLocationNames.antique_coppercompass: (145, DoLLocationTypes.antique, [
                    DoLRegionNames.ocean
                ]), # antiquecoppercompass

    DoLLocationNames.antique_coralring: (146, DoLLocationTypes.antique, [
                    DoLRegionNames.ocean
                ]), # antiquecoralring

    DoLLocationNames.antique_diamond: (147, DoLLocationTypes.antique, [
                    DoLRegionNames.ocean
                ]), # antiquediamond

    DoLLocationNames.antique_brassstatuette: (148, DoLLocationTypes.antique, [
                    DoLRegionNames.temple
                ]), # antiquebrassstatuette

    DoLLocationNames.antique_golddagger: (149, DoLLocationTypes.antique, [
                    DoLRegionNames.avery_mansion
                ]), # antiquegolddagger

    DoLLocationNames.antique_goldamulet: (150, DoLLocationTypes.antique, [
                    DoLRegionNames.avery_mansion
                ]), # antiquegoldamulet

    DoLLocationNames.antique_goldmask: (151, DoLLocationTypes.antique, [
                    DoLRegionNames.avery_mansion
                ]), # antiquegoldmask

    DoLLocationNames.antique_silvercompass: (152, DoLLocationTypes.antique, [
                    DoLRegionNames.beach
                ]), # antiquesilvercompass

    DoLLocationNames.antique_leathermap: (153, DoLLocationTypes.antique, [
                    DoLRegionNames.beach
                ]), # antiqueleathermap

    DoLLocationNames.antique_cutlass: (154, DoLLocationTypes.antique, [
                    DoLRegionNames.beach
                ]), # antiquecutlass

    DoLLocationNames.antique_silverdagger: (155, DoLLocationTypes.antique, [
                    DoLRegionNames.beach
                ]), # antiquesilverdagger

    DoLLocationNames.antique_rustedcutlass: (156, DoLLocationTypes.antique, [
                    DoLRegionNames.beach
                ]), # antiquerustedcutlass

    DoLLocationNames.antique_pinkcrystal: (157, DoLLocationTypes.antique, [
                    DoLRegionNames.commercial_drain,
                    DoLRegionNames.industrial_drain, # TODO: replace with deep sewers location?
                    DoLRegionNames.residential_drain,
                ]), # antiquecrystal

    DoLLocationNames.antique_candlestick: (158, DoLLocationTypes.antique, [
                    DoLRegionNames.commercial_drain,
                    DoLRegionNames.industrial_drain, # TODO: replace with deep sewers location?
                    DoLRegionNames.residential_drain,
                ]), # antiquecandlestick

    DoLLocationNames.antique_dildo: (159, DoLLocationTypes.antique, [
                    DoLRegionNames.commercial_drain,
                    DoLRegionNames.industrial_drain, # TODO: replace with deep sewers location?
                    DoLRegionNames.residential_drain,
                ]), # antiquedildo

    DoLLocationNames.antique_watch: (160, DoLLocationTypes.antique, [
                    DoLRegionNames.commercial_drain,
                    DoLRegionNames.industrial_drain, # TODO: replace with deep sewers location?
                    DoLRegionNames.residential_drain,
                ]), # antiquewatch
    
    DoLLocationNames.antique_silvercrown: (161, DoLLocationTypes.antique, [
                    DoLRegionNames.temple
                ]), # antiquesilvercrown

    # -------- skills --------

    DoLLocationNames.skill_skulduggery_1 : (162, DoLLocationTypes.skill, [
                        DoLRegionNames.school, 
                    ]),
    DoLLocationNames.skill_skulduggery_2 : (163, DoLLocationTypes.skill, [
                        DoLRegionNames.domus_houses, 
                    ]),
    DoLLocationNames.skill_skulduggery_3 : (164, DoLLocationTypes.skill, [
                        DoLRegionNames.barb_street, 
                        DoLRegionNames.connudatus_street,
                    ]),
    DoLLocationNames.skill_skulduggery_4 : (165, DoLLocationTypes.skill, [
                        DoLRegionNames.danube_houses, 
                    ]),
    DoLLocationNames.skill_skulduggery_5 : (166, DoLLocationTypes.skill, [
                        DoLRegionNames.docks, 
                    ]),
    DoLLocationNames.skill_skulduggery_6 : (167, DoLLocationTypes.skill, [
                        DoLRegionNames.temple,
                    ]),
    DoLLocationNames.skill_skulduggery_7 : (168, DoLLocationTypes.skill, [
                        DoLRegionNames.manors,
                    ]),
    DoLLocationNames.skill_skulduggery_8 : (169, DoLLocationTypes.skill, [
                        DoLRegionNames.in_town, 
                    ]),
    DoLLocationNames.skill_skulduggery_9 : (170, DoLLocationTypes.skill, [
                        DoLRegionNames.in_town, 
                    ]),
    DoLLocationNames.skill_skulduggery_10 : (171, DoLLocationTypes.skill, [
                        DoLRegionNames.in_town, 
                    ]),

    # dancing just wants dance studio, but can be leveled in strip club and brothel
    DoLLocationNames.skill_dancing_1 : (172, DoLLocationTypes.skill, [
                        DoLRegionNames.dance_studio,
                    ]),
    DoLLocationNames.skill_dancing_2 : (173, DoLLocationTypes.skill, [
                        DoLRegionNames.dance_studio,
                    ]),
    DoLLocationNames.skill_dancing_3 : (174, DoLLocationTypes.skill, [
                        DoLRegionNames.dance_studio,
                    ]),
    DoLLocationNames.skill_dancing_4 : (175, DoLLocationTypes.skill, [
                        DoLRegionNames.dance_studio,
                    ]),
    DoLLocationNames.skill_dancing_5 : (176, DoLLocationTypes.skill, [
                        DoLRegionNames.dance_studio,
                    ]),
    DoLLocationNames.skill_dancing_6 : (177, DoLLocationTypes.skill, [
                        DoLRegionNames.dance_studio,
                    ]),
    DoLLocationNames.skill_dancing_7 : (178, DoLLocationTypes.skill, [
                        DoLRegionNames.dance_studio,
                    ]),
    DoLLocationNames.skill_dancing_8 : (179, DoLLocationTypes.skill, [
                        DoLRegionNames.dance_studio,
                    ]),
    DoLLocationNames.skill_dancing_9 : (180, DoLLocationTypes.skill, [
                        DoLRegionNames.dance_studio,
                    ]),
    DoLLocationNames.skill_dancing_10 : (181, DoLLocationTypes.skill, [
                        DoLRegionNames.dance_studio,
                    ]),

    # school for at least level 1
    DoLLocationNames.skill_swimming_1 : (182, DoLLocationTypes.skill, [
                        DoLRegionNames.school, 
                    ]),
    DoLLocationNames.skill_swimming_2 : (183, DoLLocationTypes.skill, [
                        DoLRegionNames.school, 
                    ]),
    DoLLocationNames.skill_swimming_3 : (184, DoLLocationTypes.skill, [
                        DoLRegionNames.school, 
                    ]),
    DoLLocationNames.skill_swimming_4 : (185, DoLLocationTypes.skill, [
                        DoLRegionNames.school,
                    ]),
    DoLLocationNames.skill_swimming_5 : (186, DoLLocationTypes.skill, [
                        DoLRegionNames.school, 
                    ]),
    DoLLocationNames.skill_swimming_6 : (187, DoLLocationTypes.skill, [
                        DoLRegionNames.school, 
                    ]),
    DoLLocationNames.skill_swimming_7 : (188, DoLLocationTypes.skill, [
                        DoLRegionNames.school, 
                    ]),
    DoLLocationNames.skill_swimming_8 : (189, DoLLocationTypes.skill, [
                        DoLRegionNames.school, 
                    ]),
    DoLLocationNames.skill_swimming_9 : (190, DoLLocationTypes.skill, [
                        DoLRegionNames.school, 
                    ]),
    DoLLocationNames.skill_swimming_10 : (191, DoLLocationTypes.skill, [
                        DoLRegionNames.school, 
                    ]),

    # starting levels anywhere, rest park good place to train
    DoLLocationNames.skill_athletics_1 : (192, DoLLocationTypes.skill, [
                        DoLRegionNames.in_town, 
                    ]),
    DoLLocationNames.skill_athletics_2 : (193, DoLLocationTypes.skill, [
                        DoLRegionNames.in_town, 
                    ]),
    DoLLocationNames.skill_athletics_3 : (194, DoLLocationTypes.skill, [
                        DoLRegionNames.park, 
                    ]),
    DoLLocationNames.skill_athletics_4 : (195, DoLLocationTypes.skill, [
                        DoLRegionNames.park, 
                    ]),
    DoLLocationNames.skill_athletics_5 : (196, DoLLocationTypes.skill, [
                        DoLRegionNames.park, 
                    ]),
    DoLLocationNames.skill_athletics_6 : (197, DoLLocationTypes.skill, [
                        DoLRegionNames.park, 
                    ]),
    DoLLocationNames.skill_athletics_7 : (198, DoLLocationTypes.skill, [
                        DoLRegionNames.park,
                    ]),
    DoLLocationNames.skill_athletics_8 : (199, DoLLocationTypes.skill, [
                        DoLRegionNames.park, 
                    ]),
    DoLLocationNames.skill_athletics_9 : (200, DoLLocationTypes.skill, [
                        DoLRegionNames.park, 
                    ]),
    DoLLocationNames.skill_athletics_10 : (201, DoLLocationTypes.skill, [
                        DoLRegionNames.park, 
                    ]),

    DoLLocationNames.skill_tending_1 : (202, DoLLocationTypes.skill, [
                        DoLRegionNames.in_town,
                    ]),
    DoLLocationNames.skill_tending_2 : (203, DoLLocationTypes.skill, [
                        DoLRegionNames.in_town,  
                    ]),
    DoLLocationNames.skill_tending_3 : (204, DoLLocationTypes.skill, [
                        DoLRegionNames.alex_farm, # farm good place to train
                    ]),
    DoLLocationNames.skill_tending_4 : (205, DoLLocationTypes.skill, [
                        DoLRegionNames.alex_farm,
                    ]),
    DoLLocationNames.skill_tending_5 : (206, DoLLocationTypes.skill, [
                        DoLRegionNames.alex_farm,
                    ]),
    DoLLocationNames.skill_tending_6 : (207, DoLLocationTypes.skill, [
                        DoLRegionNames.alex_farm,
                    ]),
    DoLLocationNames.skill_tending_7 : (208, DoLLocationTypes.skill, [
                        DoLRegionNames.alex_farm,
                    ]),
    DoLLocationNames.skill_tending_8 : (209, DoLLocationTypes.skill, [
                        DoLRegionNames.alex_farm,
                    ]),
    DoLLocationNames.skill_tending_9 : (210, DoLLocationTypes.skill, [
                        DoLRegionNames.alex_farm,
                    ]),
    DoLLocationNames.skill_tending_10 : (211, DoLLocationTypes.skill, [
                        DoLRegionNames.alex_farm,
                    ]),

    # using wiki recommended leveling order
    DoLLocationNames.skill_housekeeping_1 : (212, DoLLocationTypes.skill, [
                        DoLRegionNames.domus_houses,
                    ]),
    DoLLocationNames.skill_housekeeping_2 : (213, DoLLocationTypes.skill, [
                        DoLRegionNames.flats,
                    ]),
    DoLLocationNames.skill_housekeeping_3 : (214, DoLLocationTypes.skill, [
                        DoLRegionNames.starfish_street,
                    ]),
    DoLLocationNames.skill_housekeeping_4 : (215, DoLLocationTypes.skill, [
                        DoLRegionNames.danube_street,
                    ]),
    DoLLocationNames.skill_housekeeping_5 : (216, DoLLocationTypes.skill, [
                        DoLRegionNames.temple,
                    ]),
    DoLLocationNames.skill_housekeeping_6 : (217, DoLLocationTypes.skill, [
                        DoLRegionNames.temple,
                    ]),
    DoLLocationNames.skill_housekeeping_7 : (218, DoLLocationTypes.skill, [
                        DoLRegionNames.temple,
                    ]),
    DoLLocationNames.skill_housekeeping_8 : (219, DoLLocationTypes.skill, [
                        DoLRegionNames.temple,
                    ]),
    DoLLocationNames.skill_housekeeping_9 : (220, DoLLocationTypes.skill, [
                        DoLRegionNames.temple,
                    ]),
    DoLLocationNames.skill_housekeeping_10 : (221, DoLLocationTypes.skill, [
                        DoLRegionNames.temple,
                    ]),

    # sex skills just require encounters
    DoLLocationNames.skill_seduction_1 : (222, DoLLocationTypes.skill, [
                        DoLRegionNames.in_town,
                    ]),
    DoLLocationNames.skill_seduction_2 : (223, DoLLocationTypes.skill, [
                        DoLRegionNames.in_town,
                    ]),
    DoLLocationNames.skill_seduction_3 : (224, DoLLocationTypes.skill, [
                        DoLRegionNames.in_town,
                    ]),
    DoLLocationNames.skill_seduction_4 : (225, DoLLocationTypes.skill, [
                        DoLRegionNames.in_town,
                    ]),
    DoLLocationNames.skill_seduction_5 : (226, DoLLocationTypes.skill, [
                        DoLRegionNames.in_town,
                    ]),

    DoLLocationNames.skill_oral_1 : (227, DoLLocationTypes.skill, [
                        DoLRegionNames.in_town,
                    ]),
    DoLLocationNames.skill_oral_2 : (228, DoLLocationTypes.skill, [
                        DoLRegionNames.in_town,
                    ]),
    DoLLocationNames.skill_oral_3 : (229, DoLLocationTypes.skill, [
                        DoLRegionNames.in_town,
                    ]),
    DoLLocationNames.skill_oral_4 : (230, DoLLocationTypes.skill, [
                        DoLRegionNames.in_town,
                    ]),
    DoLLocationNames.skill_oral_5 : (231, DoLLocationTypes.skill, [
                        DoLRegionNames.in_town,
                    ]),

    DoLLocationNames.skill_chest_1 : (232, DoLLocationTypes.skill, [
                        DoLRegionNames.in_town,
                    ]),
    DoLLocationNames.skill_chest_2 : (233, DoLLocationTypes.skill, [
                        DoLRegionNames.in_town,
                    ]),
    DoLLocationNames.skill_chest_3 : (234, DoLLocationTypes.skill, [
                        DoLRegionNames.in_town,
                    ]),
    DoLLocationNames.skill_chest_4 : (235, DoLLocationTypes.skill, [
                        DoLRegionNames.in_town,
                    ]),
    DoLLocationNames.skill_chest_5 : (236, DoLLocationTypes.skill, [
                        DoLRegionNames.in_town,
                    ]),

    DoLLocationNames.skill_hands_1 : (237, DoLLocationTypes.skill, [
                        DoLRegionNames.in_town,
                    ]),
    DoLLocationNames.skill_hands_2 : (238, DoLLocationTypes.skill, [
                        DoLRegionNames.in_town,
                    ]),
    DoLLocationNames.skill_hands_3 : (239, DoLLocationTypes.skill, [
                        DoLRegionNames.in_town,
                    ]),
    DoLLocationNames.skill_hands_4 : (240, DoLLocationTypes.skill, [
                        DoLRegionNames.in_town,
                    ]),
    DoLLocationNames.skill_hands_5 : (241, DoLLocationTypes.skill, [
                        DoLRegionNames.in_town,
                    ]),

    DoLLocationNames.skill_buttocks_1 : (242, DoLLocationTypes.skill, [
                        DoLRegionNames.in_town,
                    ]),
    DoLLocationNames.skill_buttocks_2 : (243, DoLLocationTypes.skill, [
                        DoLRegionNames.in_town,
                    ]),
    DoLLocationNames.skill_buttocks_3 : (244, DoLLocationTypes.skill, [
                        DoLRegionNames.in_town,
                    ]),
    DoLLocationNames.skill_buttocks_4 : (245, DoLLocationTypes.skill, [
                        DoLRegionNames.in_town,
                    ]),
    DoLLocationNames.skill_buttocks_5 : (246, DoLLocationTypes.skill, [
                        DoLRegionNames.in_town,
                    ]),

    DoLLocationNames.skill_privates_1 : (247, DoLLocationTypes.skill, [
                        DoLRegionNames.in_town,
                    ]),
    DoLLocationNames.skill_privates_2 : (248, DoLLocationTypes.skill, [
                        DoLRegionNames.in_town,
                    ]),
    DoLLocationNames.skill_privates_3 : (249, DoLLocationTypes.skill, [
                        DoLRegionNames.in_town,
                    ]),
    DoLLocationNames.skill_privates_4 : (250, DoLLocationTypes.skill, [
                        DoLRegionNames.in_town,
                    ]),
    DoLLocationNames.skill_privates_5 : (251, DoLLocationTypes.skill, [
                        DoLRegionNames.in_town,
                    ]),

    DoLLocationNames.skill_anal_1 : (252, DoLLocationTypes.skill, [
                        DoLRegionNames.in_town,
                    ]),
    DoLLocationNames.skill_anal_2 : (253, DoLLocationTypes.skill, [
                        DoLRegionNames.in_town,
                    ]),
    DoLLocationNames.skill_anal_3 : (254, DoLLocationTypes.skill, [
                        DoLRegionNames.in_town,
                    ]),
    DoLLocationNames.skill_anal_4 : (255, DoLLocationTypes.skill, [
                        DoLRegionNames.in_town,
                    ]),
    DoLLocationNames.skill_anal_5 : (256, DoLLocationTypes.skill, [
                        DoLRegionNames.in_town,
                    ]),

    # can use riding school for higher levels
    DoLLocationNames.skill_thighs_1 : (257, DoLLocationTypes.skill, [
                        DoLRegionNames.in_town,
                    ]),
    DoLLocationNames.skill_thighs_2 : (258, DoLLocationTypes.skill, [
                        DoLRegionNames.in_town,
                    ]),
    DoLLocationNames.skill_thighs_3 : (259, DoLLocationTypes.skill, [
                        DoLRegionNames.in_town,
                    ]),
    DoLLocationNames.skill_thighs_4 : (260, DoLLocationTypes.skill, [
                        DoLRegionNames.in_town,
                    ]),
    DoLLocationNames.skill_thighs_5 : (261, DoLLocationTypes.skill, [
                        DoLRegionNames.in_town,
                    ]),

    # can use dance studio for higher levels
    DoLLocationNames.skill_feet_1 : (262, DoLLocationTypes.skill, [
                        DoLRegionNames.in_town,
                    ]),
    DoLLocationNames.skill_feet_2 : (263, DoLLocationTypes.skill, [
                        DoLRegionNames.in_town,
                    ]),
    DoLLocationNames.skill_feet_3 : (264, DoLLocationTypes.skill, [
                        DoLRegionNames.in_town,
                    ]),
    DoLLocationNames.skill_feet_4 : (265, DoLLocationTypes.skill, [
                        DoLRegionNames.in_town,
                    ]),
    DoLLocationNames.skill_feet_5 : (266, DoLLocationTypes.skill, [
                        DoLRegionNames.in_town,
                    ]),

    # pretty much need school for all school skills
    DoLLocationNames.skill_science_1 : (267, DoLLocationTypes.skill, [
                        DoLRegionNames.school,
                    ]),
    DoLLocationNames.skill_science_2 : (268, DoLLocationTypes.skill, [
                        DoLRegionNames.school,
                    ]),
    DoLLocationNames.skill_science_3 : (269, DoLLocationTypes.skill, [
                        DoLRegionNames.school,
                    ]),
    DoLLocationNames.skill_science_4 : (270, DoLLocationTypes.skill, [
                        DoLRegionNames.school,
                    ]),
    DoLLocationNames.skill_science_5 : (271, DoLLocationTypes.skill, [
                        DoLRegionNames.school,
                    ]),

    DoLLocationNames.skill_math_1 : (272, DoLLocationTypes.skill, [
                        DoLRegionNames.school,
                    ]),
    DoLLocationNames.skill_math_2 : (273, DoLLocationTypes.skill, [
                        DoLRegionNames.school,
                    ]),
    DoLLocationNames.skill_math_3 : (274, DoLLocationTypes.skill, [
                        DoLRegionNames.school,
                    ]),
    DoLLocationNames.skill_math_4 : (275, DoLLocationTypes.skill, [
                        DoLRegionNames.school,
                    ]),
    DoLLocationNames.skill_math_5 : (276, DoLLocationTypes.skill, [
                        DoLRegionNames.school,
                    ]),

    DoLLocationNames.skill_english_1 : (277, DoLLocationTypes.skill, [
                        DoLRegionNames.school,
                    ]),
    DoLLocationNames.skill_english_2 : (278, DoLLocationTypes.skill, [
                        DoLRegionNames.school,
                    ]),
    DoLLocationNames.skill_english_3 : (279, DoLLocationTypes.skill, [
                        DoLRegionNames.school,
                    ]),
    DoLLocationNames.skill_english_4 : (280, DoLLocationTypes.skill, [
                        DoLRegionNames.school,
                    ]),
    DoLLocationNames.skill_english_5 : (281, DoLLocationTypes.skill, [
                        DoLRegionNames.school,
                    ]),

    DoLLocationNames.skill_history_1 : (282, DoLLocationTypes.skill, [
                        DoLRegionNames.school,
                    ]),
    DoLLocationNames.skill_history_2 : (283, DoLLocationTypes.skill, [
                        DoLRegionNames.school,
                    ]),
    DoLLocationNames.skill_history_3 : (284, DoLLocationTypes.skill, [
                        DoLRegionNames.school,
                    ]),
    DoLLocationNames.skill_history_4 : (285, DoLLocationTypes.skill, [
                        DoLRegionNames.school,
                    ]),
    DoLLocationNames.skill_history_5 : (286, DoLLocationTypes.skill, [
                        DoLRegionNames.school,
                    ]),

    DoLLocationNames.skill_willpower_1 : (287, DoLLocationTypes.skill, [
                        DoLRegionNames.in_town, 
                    ]),
    DoLLocationNames.skill_willpower_2 : (288, DoLLocationTypes.skill, [
                        DoLRegionNames.in_town, 
                    ]),
    DoLLocationNames.skill_willpower_3 : (289, DoLLocationTypes.skill, [
                        DoLRegionNames.in_town, 
                    ]),
    DoLLocationNames.skill_willpower_4 : (290, DoLLocationTypes.skill, [
                        DoLRegionNames.in_town, 
                    ]),
    DoLLocationNames.skill_willpower_5 : (291, DoLLocationTypes.skill, [
                        DoLRegionNames.in_town, 
                    ]),
    DoLLocationNames.skill_willpower_6 : (292, DoLLocationTypes.skill, [
                        DoLRegionNames.in_town, 
                    ]),

    # park good place to train
    DoLLocationNames.skill_physique_1 : (293, DoLLocationTypes.skill, [
                        DoLRegionNames.park, 
                    ]),
    DoLLocationNames.skill_physique_2 : (294, DoLLocationTypes.skill, [
                        DoLRegionNames.park, 
                    ]),
    DoLLocationNames.skill_physique_3 : (295, DoLLocationTypes.skill, [
                        DoLRegionNames.park,
                    ]),
    DoLLocationNames.skill_physique_4 : (296, DoLLocationTypes.skill, [
                        DoLRegionNames.park,
                    ]),
    DoLLocationNames.skill_physique_5 : (297, DoLLocationTypes.skill, [
                        DoLRegionNames.park,
                    ]),
    DoLLocationNames.skill_physique_6 : (298, DoLLocationTypes.skill, [
                        DoLRegionNames.park,
                    ]),

    DoLLocationNames.skill_promiscuity_1 : (299, DoLLocationTypes.skill, [
                        DoLRegionNames.in_town,
                    ]),
    DoLLocationNames.skill_promiscuity_2 : (300, DoLLocationTypes.skill, [
                        DoLRegionNames.in_town,
                    ]),
    DoLLocationNames.skill_promiscuity_3 : (301, DoLLocationTypes.skill, [
                        DoLRegionNames.in_town,
                    ]),
    DoLLocationNames.skill_promiscuity_4 : (302, DoLLocationTypes.skill, [
                        DoLRegionNames.in_town,
                    ]),
    DoLLocationNames.skill_promiscuity_5 : (303, DoLLocationTypes.skill, [
                        DoLRegionNames.in_town,
                    ]),
    DoLLocationNames.skill_promiscuity_6 : (304, DoLLocationTypes.skill, [
                        DoLRegionNames.in_town,
                    ]),

    # orph for minimum level + need wardrobe
    DoLLocationNames.skill_exhibitionism_1 : (305, DoLLocationTypes.skill, [
                        DoLRegionNames.orphanage, 
                    ]),
    DoLLocationNames.skill_exhibitionism_2 : (306, DoLLocationTypes.skill, [
                        DoLRegionNames.orphanage,
                    ]),
    DoLLocationNames.skill_exhibitionism_3 : (307, DoLLocationTypes.skill, [
                        DoLRegionNames.orphanage,
                    ]),
    DoLLocationNames.skill_exhibitionism_4 : (308, DoLLocationTypes.skill, [
                        DoLRegionNames.orphanage,
                    ]),
    DoLLocationNames.skill_exhibitionism_5 : (309, DoLLocationTypes.skill, [
                        DoLRegionNames.orphanage,
                    ]),
    DoLLocationNames.skill_exhibitionism_6 : (310, DoLLocationTypes.skill, [
                        DoLRegionNames.orphanage,
                    ]),

    # wiki recommends farm, but can level from anywhere
    DoLLocationNames.skill_deviancy_1 : (311, DoLLocationTypes.skill, [
                        DoLRegionNames.in_town, 
                    ]),
    DoLLocationNames.skill_deviancy_2 : (312, DoLLocationTypes.skill, [
                        DoLRegionNames.in_town,
                    ]),
    DoLLocationNames.skill_deviancy_3 : (313, DoLLocationTypes.skill, [
                        DoLRegionNames.in_town,
                    ]),
    DoLLocationNames.skill_deviancy_4 : (314, DoLLocationTypes.skill, [
                        DoLRegionNames.in_town,
                    ]),
    DoLLocationNames.skill_deviancy_5 : (315, DoLLocationTypes.skill, [
                        DoLRegionNames.in_town,
                    ]),
    DoLLocationNames.skill_deviancy_6 : (316, DoLLocationTypes.skill, [
                        DoLRegionNames.in_town,
                    ]),
}

LOCATION_RULES:dict[DoLLocationNames, DoLRules] = {
    # Antiques
    DoLLocationNames.antique_silvermask: DoLRules.silvermask,

    # Skills
    # the rules here determine when leveling is out of logic
    # due to you being able to still have a chance to level
    # from high difficulty encounters, I've set them to all
    # require around challenging difficulty encounters

    # most skills uses a difficulty graph, which maths to
    # challenging requiring a check of skilllevel + 300
    # so just skilllevel - 300 or 3 levels lower for rules

    # DoLLocationNames.skill_skulduggery_2: DoLRules.skulduggery_,
    # DoLLocationNames.skill_skulduggery_3: DoLRules.skulduggery_,
    DoLLocationNames.skill_skulduggery_4: DoLRules.skulduggery_1,
    DoLLocationNames.skill_skulduggery_5: DoLRules.skulduggery_2,
    DoLLocationNames.skill_skulduggery_6: DoLRules.skulduggery_3,
    DoLLocationNames.skill_skulduggery_7: DoLRules.skulduggery_4,
    DoLLocationNames.skill_skulduggery_8: DoLRules.skulduggery_5,
    DoLLocationNames.skill_skulduggery_9: DoLRules.skulduggery_6,
    DoLLocationNames.skill_skulduggery_10: DoLRules.skulduggery_7,

    # DoLLocationNames.skill_dancing_2: DoLRules.dancing_,
    # DoLLocationNames.skill_dancing_3: DoLRules.dancing_,
    DoLLocationNames.skill_dancing_4: DoLRules.dancing_1,
    DoLLocationNames.skill_dancing_5: DoLRules.dancing_2,
    DoLLocationNames.skill_dancing_6: DoLRules.dancing_3,
    DoLLocationNames.skill_dancing_7: DoLRules.dancing_4,
    DoLLocationNames.skill_dancing_8: DoLRules.dancing_5,
    DoLLocationNames.skill_dancing_9: DoLRules.dancing_6,
    DoLLocationNames.skill_dancing_10: DoLRules.dancing_7,

    # DoLLocationNames.skill_swimming_2: DoLRules.swimming_,
    # DoLLocationNames.skill_swimming_3: DoLRules.swimming_,
    DoLLocationNames.skill_swimming_4: DoLRules.swimming_1,
    DoLLocationNames.skill_swimming_5: DoLRules.swimming_2,
    DoLLocationNames.skill_swimming_6: DoLRules.swimming_3,
    DoLLocationNames.skill_swimming_7: DoLRules.swimming_4,
    DoLLocationNames.skill_swimming_8: DoLRules.swimming_5,
    DoLLocationNames.skill_swimming_9: DoLRules.swimming_6,
    DoLLocationNames.skill_swimming_10: DoLRules.swimming_7,

    # DoLLocationNames.skill_athletics_2: DoLRules.athletics_,
    # DoLLocationNames.skill_athletics_3: DoLRules.athletics_,
    DoLLocationNames.skill_athletics_4: DoLRules.athletics_1,
    DoLLocationNames.skill_athletics_5: DoLRules.athletics_2,
    DoLLocationNames.skill_athletics_6: DoLRules.athletics_3,
    DoLLocationNames.skill_athletics_7: DoLRules.athletics_4,
    DoLLocationNames.skill_athletics_8: DoLRules.athletics_5,
    DoLLocationNames.skill_athletics_9: DoLRules.athletics_6,
    DoLLocationNames.skill_athletics_10: DoLRules.athletics_7,

    # DoLLocationNames.skill_tending_2: DoLRules.tending_,
    # DoLLocationNames.skill_tending_3: DoLRules.tending_,
    DoLLocationNames.skill_tending_4: DoLRules.tending_1,
    DoLLocationNames.skill_tending_5: DoLRules.tending_2,
    DoLLocationNames.skill_tending_6: DoLRules.tending_3,
    DoLLocationNames.skill_tending_7: DoLRules.tending_4,
    DoLLocationNames.skill_tending_8: DoLRules.tending_5,
    DoLLocationNames.skill_tending_9: DoLRules.tending_6,
    DoLLocationNames.skill_tending_10: DoLRules.tending_7,

    # DoLLocationNames.skill_housekeeping_2: DoLRules.housekeeping_,
    # DoLLocationNames.skill_housekeeping_3: DoLRules.housekeeping_,
    DoLLocationNames.skill_housekeeping_4: DoLRules.housekeeping_1,
    DoLLocationNames.skill_housekeeping_5: DoLRules.housekeeping_2,
    DoLLocationNames.skill_housekeeping_6: DoLRules.housekeeping_3,
    DoLLocationNames.skill_housekeeping_7: DoLRules.housekeeping_4,
    DoLLocationNames.skill_housekeeping_8: DoLRules.housekeeping_5,
    DoLLocationNames.skill_housekeeping_9: DoLRules.housekeeping_6,
    DoLLocationNames.skill_housekeeping_10: DoLRules.housekeeping_7,


    # sex skills are a bit more complicatied
    # because the difficulty of them changes based
    # on the arousal and trust in encounters
    # (trust * 10) - skillvalue + anger) <= ((maxarousal / (arousal + 1)) * 100)
    # this still however balances out to about req of skilllevel + 300 
    # is around challenging in an early encounter with low anger and low trust
    # so I will make most sex skills require 2 levels lower


    # seduction is very complicated because it bases off
    # attractiveness value, which gets modified by many systems:
    # transformations, clothing, nakedness, hair length, beauty, and makeup
    # also increased by similar modifiers that every other stat has

    # if you have no modifiers, challenging requirement is your seduction level
    # however you should have at least a few modifiers no matter what.
    # I might be able to create a rule that bases off a math formula,
    # however since its only 5 levels, just leaving it at 1 level behind for 2 and 3
    # and 2 levels behind for 4 and 5
    DoLLocationNames.skill_seduction_2: DoLRules.seduction_1,
    DoLLocationNames.skill_seduction_3: DoLRules.seduction_2,
    DoLLocationNames.skill_seduction_4: DoLRules.seduction_2,
    DoLLocationNames.skill_seduction_5: DoLRules.seduction_3,

    # DoLLocationNames.skill_oral_2: DoLRules.oral_,
    DoLLocationNames.skill_oral_3: DoLRules.oral_1,
    DoLLocationNames.skill_oral_4: DoLRules.oral_2,
    DoLLocationNames.skill_oral_5: DoLRules.oral_3,

    # DoLLocationNames.skill_chest_2: DoLRules.chest_,
    DoLLocationNames.skill_chest_3: DoLRules.chest_1,
    DoLLocationNames.skill_chest_4: DoLRules.chest_2,
    DoLLocationNames.skill_chest_5: DoLRules.chest_3,

    # DoLLocationNames.skill_hands_2: DoLRules.hands_,
    DoLLocationNames.skill_hands_3: DoLRules.hands_1,
    DoLLocationNames.skill_hands_4: DoLRules.hands_2,
    DoLLocationNames.skill_hands_5: DoLRules.hands_3,

    # DoLLocationNames.skill_buttocks_2: DoLRules.buttocks_,
    DoLLocationNames.skill_buttocks_3: DoLRules.buttocks_1,
    DoLLocationNames.skill_buttocks_4: DoLRules.buttocks_2,
    DoLLocationNames.skill_buttocks_5: DoLRules.buttocks_3,

    # DoLLocationNames.skill_privates_2: DoLRules.privates_,
    DoLLocationNames.skill_privates_3: DoLRules.privates_1,
    DoLLocationNames.skill_privates_4: DoLRules.privates_2,
    DoLLocationNames.skill_privates_5: DoLRules.privates_3,

    # DoLLocationNames.skill_anal_2: DoLRules.anal_,
    DoLLocationNames.skill_anal_3: DoLRules.anal_1,
    DoLLocationNames.skill_anal_4: DoLRules.anal_2,
    DoLLocationNames.skill_anal_5: DoLRules.anal_3,

    # DoLLocationNames.skill_thighs_2: DoLRules.thighs_,
    DoLLocationNames.skill_thighs_3: DoLRules.thighs_1,
    DoLLocationNames.skill_thighs_4: DoLRules.thighs_2,
    DoLLocationNames.skill_thighs_5: DoLRules.thighs_3,

    # DoLLocationNames.skill_feet_2: DoLRules.feet_,
    DoLLocationNames.skill_feet_3: DoLRules.feet_1,
    DoLLocationNames.skill_feet_4: DoLRules.feet_2,
    DoLLocationNames.skill_feet_5: DoLRules.feet_3,


    # school skills
    # school skill is ran by the schoolskillgeneral widget
    # it just adds to the base exam chance each time you increase
    # your skill via studying, set to a multiplier based on trait [2.4, 1.2, 0.6, 0.3]
    # TODO: need to recode this to make sure this isn't based
    # on the trait, instead based on the value that eats ur skill

    # the notable thing is, school skills do not base off you having earlier skills
    # therefore logic dictates that you can get level 5 in all of them whenever
    # however, still need rules for having access to school for studying

    DoLLocationNames.skill_science_1: DoLRules.access_school,
    DoLLocationNames.skill_science_2: DoLRules.access_school,
    DoLLocationNames.skill_science_3: DoLRules.access_school,
    DoLLocationNames.skill_science_4: DoLRules.access_school,
    DoLLocationNames.skill_science_5: DoLRules.access_school,

    DoLLocationNames.skill_math_1: DoLRules.access_school,
    DoLLocationNames.skill_math_2: DoLRules.access_school,
    DoLLocationNames.skill_math_3: DoLRules.access_school,
    DoLLocationNames.skill_math_4: DoLRules.access_school,
    DoLLocationNames.skill_math_5: DoLRules.access_school,

    DoLLocationNames.skill_english_1: DoLRules.access_school,
    DoLLocationNames.skill_english_2: DoLRules.access_school,
    DoLLocationNames.skill_english_3: DoLRules.access_school,
    DoLLocationNames.skill_english_4: DoLRules.access_school,
    DoLLocationNames.skill_english_5: DoLRules.access_school,

    DoLLocationNames.skill_history_1: DoLRules.access_school,
    DoLLocationNames.skill_history_2: DoLRules.access_school,
    DoLLocationNames.skill_history_3: DoLRules.access_school,
    DoLLocationNames.skill_history_4: DoLRules.access_school,
    DoLLocationNames.skill_history_5: DoLRules.access_school,


    # core stats
    # no strict requirements for any of these stats, outside of doing
    # encounters that grow them
    # willpower: grows via any encounters
    # physique: grows via exercise
    # promiscuity: grows by doing things with this stat
    # exhibitionism: grows by doing things with this stat
    # deviancy: grows via animal encounters

    # DoLLocationNames.skill_willpower_2: DoLRules.willpower_1,
    # DoLLocationNames.skill_willpower_3: DoLRules.willpower_2,
    # DoLLocationNames.skill_willpower_4: DoLRules.willpower_3,
    # DoLLocationNames.skill_willpower_5: DoLRules.willpower_4,
    # DoLLocationNames.skill_willpower_6: DoLRules.willpower_5,

    # DoLLocationNames.skill_physique_2: DoLRules.physique_1,
    # DoLLocationNames.skill_physique_3: DoLRules.physique_2,
    # DoLLocationNames.skill_physique_4: DoLRules.physique_3,
    # DoLLocationNames.skill_physique_5: DoLRules.physique_4,
    # DoLLocationNames.skill_physique_6: DoLRules.physique_5,

    # DoLLocationNames.skill_promiscuity_2: DoLRules.promiscuity_1,
    # DoLLocationNames.skill_promiscuity_3: DoLRules.promiscuity_2,
    # DoLLocationNames.skill_promiscuity_4: DoLRules.promiscuity_3,
    # DoLLocationNames.skill_promiscuity_5: DoLRules.promiscuity_4,
    # DoLLocationNames.skill_promiscuity_6: DoLRules.promiscuity_5,

    # DoLLocationNames.skill_exhibitionism_2: DoLRules.exhibitionism_1,
    # DoLLocationNames.skill_exhibitionism_3: DoLRules.exhibitionism_2,
    # DoLLocationNames.skill_exhibitionism_4: DoLRules.exhibitionism_3,
    # DoLLocationNames.skill_exhibitionism_5: DoLRules.exhibitionism_4,
    # DoLLocationNames.skill_exhibitionism_6: DoLRules.exhibitionism_5,

    # DoLLocationNames.skill_deviancy_2: DoLRules.deviancy_1,
    # DoLLocationNames.skill_deviancy_3: DoLRules.deviancy_2,
    # DoLLocationNames.skill_deviancy_4: DoLRules.deviancy_3,
    # DoLLocationNames.skill_deviancy_5: DoLRules.deviancy_4,
    # DoLLocationNames.skill_deviancy_6: DoLRules.deviancy_5,
}
