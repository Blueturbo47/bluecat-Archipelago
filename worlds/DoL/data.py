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
    feat = "Feat",

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

    # Feats
    feat_pocketchange = "Pocket Change Feat"
    feat_moneymaker = "Money Maker Feat"
    feat_tycoon = "Tycoon Feat"
    feat_millionaire = "Millionaire Feat"
    feat_itbelongsinamuseum = "It Belongs in a Museum Feat"
    feat_fullycovered = "Fully Covered Feat"
    feat_beingaboy = "Being a Boy Feat"
    feat_beingagirl = "Being a Girl Feat"
    feat_beingahermaphrodite = "Being a Hermaphrodite Feat"
    feat_beinganorphan = "Being an Orphan Feat"
    feat_stressfulchallenge = "Stressful Challenge Feat"
    feat_longstressfulchallenge = "Long Stressful Challenge Feat"
    feat_billboard = "Billboard Feat"
    feat_alivingcanvas = "A Living Canvas Feat"
    feat_farmhand = "Farmhand Feat"
    feat_farmer = "Farmer Feat"
    feat_cultivator = "Cultivator Feat"
    feat_therivalfarm = "The Rival Farm Feat"
    feat_therivalestate = "The Rival Estate Feat"
    feat_heroicvictory = "Heroic Victory Feat"
    feat_fiveinarow = "Five in a Row Feat"
    feat_distinction = "Distinction Feat"
    feat_distinctive = "Distinctive Feat"
    feat_distinguished = "Distinguished Feat"
    feat_chefdetournant = "Chef de Tournant Feat"
    feat_chefdepartie = "Chef de Partie Feat"
    feat_souschef = "Sous Chef Feat"
    feat_sciencefairwinner = "Science Fair Winner Feat"
    feat_thesisoffence = "Thesis Offence Feat"
    feat_mathscompetitionwinner = "Maths Competition Winner Feat"
    feat_richhearts = "Rich Hearts Feat"
    feat_mostaware = "Most Aware Feat"
    feat_mostinnocent = "Most Innocent Feat"
    feat_nomorecontrol = "No More Control Feat"
    feat_thief = "Thief Feat"
    feat_mayihavethisdance = "May I Have This Dance? Feat"
    feat_aquanaut = "Aquanaut Feat"
    feat_seductress = "Seductress Feat"
    feat_greenfingered = "Green Fingered Feat"
    feat_majordomo = "Majordomo Feat"
    feat_swift = "Swift Feat"
    feat_alluring = "Alluring Feat"
    feat_sexspecialist = "Sex Specialist Feat"
    feat_perfectrecord = "Perfect Record Feat"
    feat_perfectsub = "Perfect Sub Feat"
    feat_defyingtheodds = "Defying the Odds Feat"
    feat_hawker = "Hawker Feat"
    feat_vendor = "Vendor Feat"
    feat_merchant = "Merchant Feat"
    feat_twisteddesire = "Twisted Desire Feat"
    feat_servedhot = "Served Hot Feat"
    feat_sadomasochist = "Sadomasochist Feat"
    feat_shiningreputation = "Shining Reputation Feat"
    feat_socialbutterfly = "Social Butterfly Feat"
    feat_unsocialmoth = "Unsocial Moth Feat"
    feat_teacherspet = "Teacher's Pet Feat"
    feat_teachersnightmare = "Teacher's Nightmare Feat"
    feat_robinthelover = "Robin the Lover Feat"
    feat_hungryorphan = "Hungry Orphan Feat"
    feat_robinssong = "Robin's Song Feat"
    feat_whitneythebully = "Whitney the Bully Feat"
    feat_thebullystithe = "The Bully's Tithe Feat"
    feat_delinquentantics = "Delinquent Antics Feat"
    feat_giddyup = "Giddy Up Feat"
    feat_whitneyssecret = "Whitney's Secret Feat"
    feat_kylartheobsessed = "Kylar the Obsessed Feat"
    feat_notforrats = "Not for Rats Feat"
    feat_edenthelonely = "Eden the Lonely Feat"
    feat_sweetandtender = "Sweet and Tender Feat"
    feat_averythemoneybags = "Avery the Moneybags Feat"
    feat_kept = "Kept Feat"
    feat_whatgoesaround = "What Goes Around Feat"
    feat_mostexclusive = "Most Exclusive Feat"
    feat_pridecometh = "Pride Cometh Feat"
    feat_hautecuisine = "Haute Cuisine Feat"
    feat_leightontheshady = "Leighton the Shady Feat"
    feat_alextherobust = "Alex the Robust Feat"
    feat_homecooking = "Home Cooking Feat"
    feat_greathawktheterror = "Great Hawk the Terror Feat"
    feat_returnthefavour = "Return the Favour Feat"
    feat_feathertrick = "Feather Trick Feat"
    feat_wrenthesly = "Wren the Sly Feat"
    feat_blackwolfthealpha = "Black Wolf the Alpha Feat"
    feat_encroachingcivilisation = "Encroaching Civilisation Feat"
    feat_sydneythepurehearted = "Sydney the Pure-Hearted Feat"
    feat_communion = "Communion Feat"
    feat_harperthehypnotist = "Harper the Hypnotist Feat"
    feat_morganthelost = "Morgan the Lost Feat"
    feat_gwylanthebewitching = "Gwylan the Bewitching Feat"
    feat_covencomforts = "Coven Comforts Feat"
    feat_lovetriangles = "Love Triangles Feat"
    feat_lovetrapezoids = "Love Trapezoids Feat"
    feat_bemyvalentine = "Be My Valentine Feat"
    feat_ballroomshowoff = "Ballroom Show-off Feat"
    feat_underthetable = "Under the Table Feat"
    feat_pubcrawlvictors = "Pub Crawl Victors Feat"
    feat_masonssecret = "Mason's Secret Feat"
    feat_masonsshame = "Mason's Shame Feat"
    feat_animaltender = "Animal Tender Feat"
    feat_ispy = "I Spy Feat"
    feat_firstkiss = "First Kiss Feat"
    feat_acrimemostfoul = "A Crime Most Foul Feat"
    feat_longing = "Longing Feat"
    feat_paganrite = "Pagan Rite Feat"
    feat_warmestwinter = "Warmest Winter Feat"
    feat_trialsoffaith = "Trials of Faith Feat"
    feat_firstverse = "First Verse Feat"
    feat_wildsong = "Wildsong Feat"
    feat_foxbane = "Foxbane Feat"
    feat_purrfect = "Purrfect Feat"
    feat_howlatthemoon = "Howl at the Moon Feat"
    feat_messwiththebull = "Mess With the Bull... Feat"
    feat_flylikeaneagle = "Fly Like an Eagle Feat"
    feat_youslyfox = "You Sly Fox Feat"
    feat_walklikeanangel = "Walk Like an Angel Feat"
    feat_fallingfallingfalling = "Falling, Falling, Falling... Feat"
    feat_devilishlooks = "Devilish Looks Feat"
    feat_headchef = "Head Chef Feat"
    feat_laughingstock = "Laughingstock Feat"
    feat_yourethelaughingstock = "You're the Laughingstock Feat"
    feat_illicitscience = "Illicit Science Feat"
    feat_mouthsealedshut = "Mouth Sealed Shut Feat"
    feat_neckdeep = "Neck Deep Feat"
    feat_seedy = "Seedy Feat"
    feat_breedy = "Breedy Feat"
    feat_athunderousresponse = "A Thunderous Response Feat"
    feat_alewdadventure = "A Lewd Adventure Feat"
    feat_sourdealing = "Sour Dealing Feat"
    feat_painrider = "Pain Rider Feat"
    feat_submerged = "Submerged Feat"
    feat_wrongsize = "Wrong Size Feat"
    feat_idlehands = "Idle Hands Feat"
    feat_stolentechnology = "Stolen Technology Feat"
    feat_spelunking = "Spelunking Feat"
    feat_xmarksthespot = "X Marks the Spot Feat"
    feat_buriedtreasure = "Buried Treasure Feat"
    feat_flurry = "Flurry Feat"
    feat_afestivehome = "A Festive Home Feat"
    feat_employeebenefits = "Employee Benefits Feat"
    feat_dealing = "Dealing Feat"
    feat_bentcopper = "Bent Copper Feat"
    feat_socialcontract = "Social Contract Feat"
    feat_slipthroughthebackdoor = "Slip Through the Backdoor Feat"
    feat_lifeoftheparty = "Life of the Party Feat"
    feat_belleoftheball = "Belle of the Ball Feat"
    feat_breakingthestone = "Breaking the Stone Feat"
    feat_poundalpha = "Pound Alpha Feat"
    feat_poundrunt = "Pound Runt Feat"
    feat_poundedpound = "Pounded Pound Feat"
    feat_poundliberator = "Pound Liberator Feat"
    feat_thevalueofpain = "The Value of Pain Feat"
    feat_bewitchingechoes = "Bewitching Echoes Feat"
    feat_bridgingthepast = "Bridging the Past Feat"
    feat_safetrail = "Safe Trail Feat"
    feat_fieldwork = "Field Work Feat"
    feat_concretewoodland = "Concrete Woodland Feat"
    feat_schoolgreen = "School Green Feat"
    feat_hookahmaster = "Hookah Master Feat"
    feat_sinsofthepast = "Sins of the Past Feat"
    feat_panicroom = "Panic Room Feat"
    feat_defythenight = "Defy the Night Feat"
    feat_witheringtruth = "Withering Truth Feat"
    feat_backroomdeals = "Backroom Deals Feat"
    feat_stompingdownthestreet = "Stomping Down The Street Feat"
    feat_hearmeroar = "Hear Me Roar Feat"
    feat_maxthoseshots = "Max Those Shots Feat"
    feat_openedpandorasbox = "Opened Pandora's Box Feat"
    feat_openedpandorascocks = "Opened Pandora's Cocks Feat"
    feat_brothelprovider = "Brothel Provider Feat"
    feat_playerofthematch = "Player of the Match Feat"
    feat_lockedingold = "Locked in Gold Feat"
    feat_theendlessdeep = "The Endless Deep Feat"
    feat_wetandruined = "Wet and Ruined Feat"
    feat_terrorsequal = "Terror's Equal Feat"
    feat_birdsofafeather = "Birds of a Feather... Feat"
    feat_runawaycattle = "Runaway Cattle Feat"
    feat_equinerescue = "Equine Rescue Feat"
    feat_rearpassenger = "Rear Passenger Feat"
    feat_corneredrogue = "Cornered Rogue Feat"
    feat_farmprotector = "Farm Protector Feat"
    feat_aknottoremember = "A Knot to Remember Feat"
    feat_abnormalmollusc = "Abnormal Mollusc Feat"
    feat_leverage = "Leverage Feat"
    feat_undertheice = "Under the Ice Feat"
    feat_inredlight = "In Red Light Feat"
    feat_ohbother = "Oh Bother Feat"
    feat_notlikethemovies = "Not Like the Movies Feat"
    feat_slippery = "Slippery Feat"
    feat_highreflection = "High Reflection Feat"
    feat_schism = "Schism Feat"
    feat_catchthewind = "Catch The Wind Feat"
    feat_tradingdignity = "Trading Dignity Feat"
    feat_playingwithfire = "Playing with Fire Feat"
    feat_firestarter = "Firestarter Feat"
    feat_towatchthefields = "To Watch the Fields Feat"
    feat_reliableemployer = "Reliable Employer Feat"
    feat_intothesunset = "Into the Sunset Feat"
    feat_institutionalised = "Institutionalised Feat"
    feat_breaker = "Breaker Feat"
    feat_timeandpressure = "Time and Pressure Feat"
    feat_morethananumber = "More than a Number Feat"
    feat_friendsinthesky = "Friends in the Sky Feat"
    feat_notmeanttobecaged = "Not Meant to be Caged Feat"
    feat_freebooze = "Free Booze Feat"
    feat_darkdelvings = "Dark Delvings Feat"
    feat_lurkerbeyond = "Lurker Beyond Feat"
    feat_downbelow = "Down Below Feat"
    feat_lostworld = "Lost World Feat"
    feat_prehistoriclandscape = "Prehistoric Landscape Feat"
    feat_faceofaguardian = "Face of a Guardian Feat"
    feat_wildmonarch = "Wild Monarch Feat"
    feat_naturalised = "Naturalised Feat"
    feat_gildedspear = "Gilded Spear Feat"
    feat_lostheirloom = "Lost Heirloom Feat"
    feat_50shadesoftan = "50 Shades of Tan Feat"
    feat_aspecialtrait = "A Special Trait Feat"
    feat_aspecialtraitcollector = "A Special Trait Collector Feat"
    feat_produceroflewdfluids = "Producer of Lewd Fluids Feat"
    feat_literallybuckets = "Literally Buckets Feat"
    feat_feelingfull = "Feeling Full Feat"
    feat_baileystroublemaker = "Bailey's Trouble Maker Feat"
    feat_leightonsnightmare = "Leighton's Nightmare Feat"
    feat_alexspartner = "Alex's Partner Feat"
    feat_harpersbane = "Harper's Bane Feat"
    feat_headofthepack = "Head of the Pack Feat"
    feat_topofthefoodchain = "Top of the Food Chain Feat"
    feat_prideofthefarm = "Pride of the Farm Feat"
    feat_dawntodusk = "Dawn to Dusk Feat"
    feat_earslimelover = "Ear Slime Lover Feat"
    feat_earslimeamalgam = "Ear Slime Amalgam Feat"
    feat_thepathtoredemption = "The Path to Redemption Feat"
    feat_anewlife = "A New Life Feat"
    feat_negotiator = "Negotiator Feat"
    feat_curiousattire = "Curious Attire Feat"
    feat_wickedwardrobe = "Wicked Wardrobe Feat"
    feat_mycollectionoffeats = "My Collection of Feats Feat"
    feat_mytimelesscollectionoffeats = "My Timeless Collection of Feats Feat"
    feat_broodmotherhost = "Broodmother Host Feat"
    feat_topbroodmotherhost = "Top Broodmother Host Feat"
    feat_broodmotherzoologist = "Broodmother Zoologist Feat"
    feat_miracleoflife = "Miracle of Life Feat"
    feat_firstfatherhood = "First Fatherhood Feat"
    feat_hailmary = "Hail Mary Feat"
    feat_bicyclemother = "Bicycle Mother Feat"
    feat_lifecomesinthrees = "Life Comes in Threes Feat"
    feat_lifebeginswhenyouleastexpect = "Life begins when you least expect Feat"
    feat_diversityoflife = "Diversity of Life Feat"

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

    # Area Access General
    access_orphanage = CanReachRegion(DoLRegionNames.orphanage)
    access_school = CanReachRegion(DoLRegionNames.school)
    access_remyfarm = CanReachRegion(DoLRegionNames.remy_farm)
    access_averymansion = CanReachRegion(DoLRegionNames.avery_mansion)
    access_park = CanReachRegion(DoLRegionNames.park)
    access_temple = CanReachRegion(DoLRegionNames.temple)
    access_industrialdrain = CanReachRegion(DoLRegionNames.industrial_drain)
    access_forest = CanReachRegion(DoLRegionNames.forest)
    access_beach = CanReachRegion(DoLRegionNames.beach)
    access_cliffstreet = CanReachRegion(DoLRegionNames.cliff_street)
    access_oxfordstreet = CanReachRegion(DoLRegionNames.oxford_street)
    access_moor = CanReachRegion(DoLRegionNames.moor)
    # TODO: check ^this for access maze
    access_pub = CanReachRegion(DoLRegionNames.pub)
    access_landfill = CanReachRegion(DoLRegionNames.landfill)
    access_photography = CanReachRegion(DoLRegionNames.photography_studio)
    access_adultshop = CanReachRegion(DoLRegionNames.adult_shop)
    access_brothel = CanReachRegion(DoLRegionNames.brothel)
    access_birdtower = CanReachRegion(DoLRegionNames.bird_tower)

    # Game Options:
    multipleruns_toggle = OptionFilter(MultipleRuns, MultipleRuns.option_true)
    rng_toggle = OptionFilter(DontRestrictRNG, DontRestrictRNG.option_true)

    # World Options:
    anal_toggle = OptionFilter(Anal, Anal.option_true)
    tentacles_toggle = OptionFilter(Tentacles, Tentacles.option_true)
    lactation_toggle = OptionFilter(Lactation, Lactation.option_true)
    softvore_toggle = OptionFilter(SoftVore, SoftVore.option_true)
    bestiality_toggle = OptionFilter(Bestiality, Bestiality.option_true)
    parasites_toggle = OptionFilter(Parasites, Parasites.option_true)
    # swarms_toggle = OptionFilter(Swarms)
    bodywriting_toggle = OptionFilter(Bodywriting, Bodywriting.option_true)

    pregnancy_toggle = OptionFilter(Pregnancy, Pregnancy.option_true)
    parasiticpregnancy_toggle = OptionFilter(ParasiticPregnancy, ParasiticPregnancy.option_true)

    animal_transformation_toggle = OptionFilter(AnimalTransformations, AnimalTransformations.option_true)
    divine_transformation_toggle = OptionFilter(DivineTransformations, DivineTransformations.option_true)

    tentacles_or_beastiality = Rule(tentacles_toggle) | bestiality_toggle

    # Transformations:
    randomize_tf_parts = OptionFilter(RandomizeTransformations, RandomizeTransformations.option_tfparts)
    randomize_tf_full = OptionFilter(RandomizeTransformations, RandomizeTransformations.option_transformations)

    # TODO: redo these rules
    # wolf_tf = Has("Wolf Transformation") & randomize_tf_parts | randomize_tf_full  # TODO: update with actual part 
    # harpy_tf = Has("Harpy Transformation")
    # flight = Has("Flight")
    # animal_transformation = animal_transformation_toggle # all feats that require an animal tf
    # angel = divine_transformation_toggle & multipleruns_toggle
    # fallenangel = divine_transformation_toggle & multipleruns_toggle
    # demon = divine_transformation_toggle


    # Area Access Complex:
    access_tentacleplains = tentacles_toggle & deviancy_5
    access_tentacleforest = tentacles_toggle

    # avery_mansion_score = Rule(housekeeping_4) # replace with adoption papers check

    # Science Fair
    science_lichen = access_park & access_temple & access_industrialdrain & access_forest
    science_mushroom = access_forest
    science_phalli = access_beach & promiscuity_3
    # cliff street is the location set of the fair so does not be in rule
    sciencefairwinner = (science_lichen | science_mushroom | science_phalli) & access_school
    sciencefairoffence = science_phalli & access_school

    # Math Fair
    # just need oxford street for stims, and orphanage for studying
    mathcomp = access_school & access_orphanage & access_oxfordstreet

    # Recipes (able to learn any)
    access_recipe = access_school | access_averymansion

    # TODO: cur at pound liberator
    # Specific Feats
    ballroomshowoff = dancing_8 | promiscuity_2
    



# Definition: [Location Name, [Location ID, [Locations this is from], [Rules to generate the location], [Rules to get to the location]]]
# note: [Locations this is from] is ANY location not ALL locations needed
# create a rule for all locations needed

# Notes:

# Skills
    # the rules here determine when leveling is out of logic
    # due to you being able to still have a chance to level
    # from high difficulty encounters, I've set them to all
    # require around challenging difficulty encounters

    # most skills uses a difficulty graph, which maths to
    # challenging requiring a check of skilllevel + 300
    # so just skilllevel - 300 or 3 levels lower for rules

    # dancing, swimming, athletics, and tending all use their same training places

# Sex Skills
    # The difficulty of them changes based on the arousal and trust in encounters
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

# School skills
    # school skill is ran by the schoolskillgeneral widget
    # it just adds to the base exam chance each time you increase
    # your skill via studying, set to a multiplier based on trait [2.4, 1.2, 0.6, 0.3]
    # TODO: need to recode this to make sure this isn't based
    # on the trait, instead based on the value that eats ur skill

    # the notable thing is, school skills do not base off you having earlier skills
    # therefore logic dictates that you can get level 5 in all of them whenever


# Reminder that a rule does not need to be set
# for the region that it needs to go to, that's already implied

# TODO:
# currently working on adding rules to getting to feats
# and their generation rules generation rules

# might make a condition to remove seasonal stuff
# I have a todo below for where to start


LOCATION_DATA:dict[DoLLocationNames, tuple[int, list[DoLRegionNames], list[StrEnum], list[DoLRules]]] = {

    # ---------------- Antiques ----------------
    
    DoLLocationNames.antique_ivorystatuette: (100, [
                    DoLRegionNames.temple
                ], [
                    DoLLocationTypes.antique
                ], []), # antiqueivorystatuette
                
    DoLLocationNames.antique_silvercoin: (101, [
                    DoLRegionNames.temple,
                    DoLRegionNames.moor
                ], [
                    DoLLocationTypes.antique
                ], []), # antiquesilvercoin
                
    DoLLocationNames.antique_crystal: (102, [
                    DoLRegionNames.temple
                ], [
                    DoLLocationTypes.antique
                ], []), # antiquewhitecrystal
                
    DoLLocationNames.antique_silverblade: (103, [
                    DoLRegionNames.temple
                ], [
                    DoLLocationTypes.antique
                ], []), # antiquesilverblade
                
    DoLLocationNames.antique_coppercoin: (104, [
                    DoLRegionNames.temple
                ], [
                    DoLLocationTypes.antique
                ], []), # antiquecoppercoin
                
    DoLLocationNames.antique_silvergoblet: (105, [
                    DoLRegionNames.temple
                ], [
                    DoLLocationTypes.antique
                ], []), # antiquesilvergoblet
                
    DoLLocationNames.antique_fetish: (106, [
                    DoLRegionNames.temple
                ], [
                    DoLLocationTypes.antique
                ], []), # antiquestrangefetish
                
    DoLLocationNames.antique_goldcoin: (107, [
                    DoLRegionNames.temple
                ], [
                    DoLLocationTypes.antique
                ], []), # antiquegoldcoin
                
    DoLLocationNames.antique_forestdagger: (108, [
                    DoLRegionNames.forest
                ], [
                    DoLLocationTypes.antique
                ], []), # antiqueforestdagger
                
    DoLLocationNames.antique_forestgem: (109, [
                    DoLRegionNames.forest
                ], [
                    DoLLocationTypes.antique
                ], []), # antiqueforestgem
                
    DoLLocationNames.antique_arrow: (110, [
                    DoLRegionNames.forest
                ], [
                    DoLLocationTypes.antique
                ], []), # antiqueforestarrow
                
    DoLLocationNames.antique_ivorynecklace: (111, [
                    DoLRegionNames.forest_lake
                ], [
                    DoLLocationTypes.antique
                ], []), # antiqueivorynecklace
                
    DoLLocationNames.antique_ivorybox: (112, [
                    DoLRegionNames.forest_lake
                ], [
                    DoLLocationTypes.antique
                ], []), # antiquebox
                
    DoLLocationNames.antique_silverring: (113, [
                    DoLRegionNames.forest_lake
                ], [
                    DoLLocationTypes.antique
                ], []), # antiquesilverring
                
    DoLLocationNames.antique_goldnecklace: (114, [
                    DoLRegionNames.forest_lake
                ], [
                    DoLLocationTypes.antique
                ], []), # antiquegoldnecklace
                
    DoLLocationNames.antique_chastitybelt: (115, [
                    DoLRegionNames.forest_lake
                ], [
                    DoLLocationTypes.antique
                ], []), # antiquegoldchastitybelt
                
    DoLLocationNames.antique_stonetalisman: (116, [
                    DoLRegionNames.meadow
                ], [
                    DoLLocationTypes.antique
                ], []), # antiquestonetalisman
                
    DoLLocationNames.antique_horn: (117, [
                    DoLRegionNames.moor, # maze
                    DoLRegionNames.residential_drain, # lower sewers 
                    DoLRegionNames.commercial_drain, # TODO: replace with deep sewers location?
                    DoLRegionNames.industrial_drain
                ], [
                    DoLLocationTypes.antique
                ], []), # antiquehorn
                
    DoLLocationNames.antique_snuffer: (118, [
                    DoLRegionNames.moor, # maze
                ], [
                    DoLLocationTypes.antique
                ], []), # antiquesnuffer
                
    DoLLocationNames.antique_bucket: (119, [
                    DoLRegionNames.moor, # maze
                ], [
                    DoLLocationTypes.antique
                ], []), # antiquebucket
                
    DoLLocationNames.antique_silvermanacle: (120, [
                    DoLRegionNames.moor, # maze
                ], [
                    DoLLocationTypes.antique
                ], []), # antiquesilvermanacle
                
    DoLLocationNames.antique_whip: (121, [
                    DoLRegionNames.moor, # maze
                ], [
                    DoLLocationTypes.antique
                ], []), # antiquewhip
                
    DoLLocationNames.antique_goldring: (122, [
                    DoLRegionNames.moor
                ], [
                    DoLLocationTypes.antique
                ], []), # antiquegoldring
                
    DoLLocationNames.antique_bell: (123, [
                    DoLRegionNames.moor
                ], [
                    DoLLocationTypes.antique
                ], []), # antiquebell
                
    DoLLocationNames.antique_bullet: (124, [
                    DoLRegionNames.moor,
                    DoLRegionNames.bird_tower
                ], [
                    DoLLocationTypes.antique
                ], []), # antiquebullet
                
    DoLLocationNames.antique_artilleryshell: (125, [
                    DoLRegionNames.moor
                ], [
                    DoLLocationTypes.antique
                ], []), # antiqueshell
                
    DoLLocationNames.antique_grenade: (126, [
                    DoLRegionNames.riding_school
                ], [
                    DoLLocationTypes.antique
                ], []), # antiquegrenade
                
    DoLLocationNames.antique_goldbrooch: (127, [
                    DoLRegionNames.dance_studio
                ], [
                    DoLLocationTypes.antique
                ], []), # antiquegoldbrooch
                
    DoLLocationNames.antique_silverbrooch: (128, [
                    DoLRegionNames.orphanage
                ], [
                    DoLLocationTypes.antique
                ], []), # antiquesilverbrooch
                
    DoLLocationNames.antique_islanderarrow: (129, [
                    DoLRegionNames.island
                ], [
                    DoLLocationTypes.antique
                ], []), # antiqueislandarrow
                
    DoLLocationNames.antique_islandermask: (130, [
                    DoLRegionNames.island
                ], [
                    DoLLocationTypes.antique
                ], []), # antiquewoodenmask
                
    DoLLocationNames.antique_obsidiandisc: (131, [
                    DoLRegionNames.island
                ], [
                    DoLLocationTypes.antique
                ], []), # antiqueobsidiandisc
                
    DoLLocationNames.antique_trilobitefossil: (132, [
                    DoLRegionNames.island
                ], [
                    DoLLocationTypes.antique
                ], []), # antiquetrilobitefossil
                
    DoLLocationNames.antique_baileyminesign: (133, [
                    DoLRegionNames.landfill
                ], [
                    DoLLocationTypes.antique
                ], []), # antiqueminesign
                
    DoLLocationNames.antique_incenseburner: (134, [
                    DoLRegionNames.landfill
                ], [
                    DoLLocationTypes.antique
                ], []), # antiquetrashburner
                
    DoLLocationNames.antique_cup: (135, [
                    DoLRegionNames.landfill
                ], [
                    DoLLocationTypes.antique
                ], []), # antiquetrashcup 
                
    DoLLocationNames.antique_silvermask: (136, [
                    DoLRegionNames.manors
                ], [
                    DoLLocationTypes.antique
                ], [
                    DoLRules.silvermask
                ]), # antiquesilvermask
                
    DoLLocationNames.antique_silveramulet: (137, [
                    DoLRegionNames.compound
                ], [
                    DoLLocationTypes.antique
                ], []), # antiquesilveramulet
                
    DoLLocationNames.antique_hourglass: (138, [
                    DoLRegionNames.pirate_ship
                ], [
                    DoLLocationTypes.antique
                ], []), # antiquehourglass
                
    DoLLocationNames.antique_swordcane: (139, [
                    DoLRegionNames.pirate_ship
                ], [
                    DoLLocationTypes.antique
                ], []), # antiqueswordcane
                
    DoLLocationNames.antique_chocolate: (140, [
                    DoLRegionNames.pirate_ship
                ], [
                    DoLLocationTypes.antique
                ], []), # antiquechocolate
                
    DoLLocationNames.antique_teacaddy: (141, [
                    DoLRegionNames.pirate_ship
                ], [
                    DoLLocationTypes.antique
                ], []), # antiqueteacaddy
                
    DoLLocationNames.antique_woodenfigurine: (142, [
                    DoLRegionNames.pirate_ship
                ], [
                    DoLLocationTypes.antique
                ], []), # antiquewoodenfigurine
                
    DoLLocationNames.antique_copperring: (143, [
                    DoLRegionNames.pirate_ship
                ], [
                    DoLLocationTypes.antique
                ], []), # antiquecopperring
                
    DoLLocationNames.antique_goldcompass: (144, [
                    DoLRegionNames.pirate_ship
                ], [
                    DoLLocationTypes.antique
                ], []), # antiquegoldcompass
                
    DoLLocationNames.antique_coppercompass: (145, [
                    DoLRegionNames.ocean
                ], [
                    DoLLocationTypes.antique
                ], []), # antiquecoppercompass
                
    DoLLocationNames.antique_coralring: (146, [
                    DoLRegionNames.ocean
                ], [
                    DoLLocationTypes.antique
                ], []), # antiquecoralring
                
    DoLLocationNames.antique_diamond: (147, [
                    DoLRegionNames.ocean
                ], [
                    DoLLocationTypes.antique
                ], []), # antiquediamond
                
    DoLLocationNames.antique_brassstatuette: (148, [
                    DoLRegionNames.temple
                ], [
                    DoLLocationTypes.antique
                ], []), # antiquebrassstatuette
                
    DoLLocationNames.antique_golddagger: (149, [
                    DoLRegionNames.avery_mansion
                ], [
                    DoLLocationTypes.antique
                ], []), # antiquegolddagger
                
    DoLLocationNames.antique_goldamulet: (150, [
                    DoLRegionNames.avery_mansion
                ], [
                    DoLLocationTypes.antique
                ], []), # antiquegoldamulet
                
    DoLLocationNames.antique_goldmask: (151, [
                    DoLRegionNames.avery_mansion
                ], [
                    DoLLocationTypes.antique
                ], []), # antiquegoldmask
                
    DoLLocationNames.antique_silvercompass: (152, [
                    DoLRegionNames.beach
                ], [
                    DoLLocationTypes.antique
                ], []), # antiquesilvercompass
                
    DoLLocationNames.antique_leathermap: (153, [
                    DoLRegionNames.beach
                ], [
                    DoLLocationTypes.antique
                ], []), # antiqueleathermap
                
    DoLLocationNames.antique_cutlass: (154, [
                    DoLRegionNames.beach
                ], [
                    DoLLocationTypes.antique
                ], []), # antiquecutlass
                
    DoLLocationNames.antique_silverdagger: (155, [
                    DoLRegionNames.beach
                ], [
                    DoLLocationTypes.antique
                ], []), # antiquesilverdagger
                
    DoLLocationNames.antique_rustedcutlass: (156, [
                    DoLRegionNames.beach
                ], [
                    DoLLocationTypes.antique
                ], []), # antiquerustedcutlass
                
    DoLLocationNames.antique_pinkcrystal: (157, [
                    DoLRegionNames.commercial_drain,
                    DoLRegionNames.industrial_drain, # TODO: replace with deep sewers location?
                    DoLRegionNames.residential_drain,
                ], [
                    DoLLocationTypes.antique
                ], []), # antiquecrystal
                
    DoLLocationNames.antique_candlestick: (158, [
                    DoLRegionNames.commercial_drain,
                    DoLRegionNames.industrial_drain, # TODO: replace with deep sewers location?
                    DoLRegionNames.residential_drain,
                ], [
                    DoLLocationTypes.antique
                ], []), # antiquecandlestick
                
    DoLLocationNames.antique_dildo: (159, [
                    DoLRegionNames.commercial_drain,
                    DoLRegionNames.industrial_drain, # TODO: replace with deep sewers location?
                    DoLRegionNames.residential_drain,
                ], [
                    DoLLocationTypes.antique
                ], []), # antiquedildo
                
    DoLLocationNames.antique_watch: (160, [
                    DoLRegionNames.commercial_drain,
                    DoLRegionNames.industrial_drain, # TODO: replace with deep sewers location?
                    DoLRegionNames.residential_drain,
                ], [
                    DoLLocationTypes.antique
                ], []), # antiquewatch
                    
    DoLLocationNames.antique_silvercrown: (161, [
                    DoLRegionNames.temple
                ], [
                    DoLLocationTypes.antique
                ], []), # antiquesilvercrown
                



    # ---------------- Skills ----------------
    
    DoLLocationNames.skill_skulduggery_1: (162, [
                        DoLRegionNames.school, 
                    ], [
                        DoLLocationTypes.skill,
                    ], []),
    
    DoLLocationNames.skill_skulduggery_2: (163, [
                        DoLRegionNames.domus_houses, 
                    ], [
                        DoLLocationTypes.skill,
                    ], []),
    
    DoLLocationNames.skill_skulduggery_3: (164, [
                        DoLRegionNames.barb_street, 
                        DoLRegionNames.connudatus_street,
                    ], [
                        DoLLocationTypes.skill,
                    ], []),
    
    DoLLocationNames.skill_skulduggery_4: (165, [
                        DoLRegionNames.danube_houses, 
                    ], [
                        DoLLocationTypes.skill,
                    ], [
                        DoLRules.skulduggery_1,
                    ]),
    
    DoLLocationNames.skill_skulduggery_5: (166, [
                        DoLRegionNames.docks, 
                    ], [
                        DoLLocationTypes.skill,
                    ], [
                        DoLRules.skulduggery_2,
                    ]),
    
    DoLLocationNames.skill_skulduggery_6: (167, [
                        DoLRegionNames.temple,
                    ], [
                        DoLLocationTypes.skill,
                    ], [
                        DoLRules.skulduggery_3,
                    ]),
    
    DoLLocationNames.skill_skulduggery_7: (168, [
                        DoLRegionNames.manors,
                    ], [
                        DoLLocationTypes.skill,
                    ], [
                        DoLRules.skulduggery_4,
                    ]),
    
    DoLLocationNames.skill_skulduggery_8: (169, [
                        DoLRegionNames.in_town, 
                    ], [
                        DoLLocationTypes.skill,
                    ], [
                        DoLRules.skulduggery_5,
                    ]),
    
    DoLLocationNames.skill_skulduggery_9: (170, [
                        DoLRegionNames.in_town, 
                    ], [
                        DoLLocationTypes.skill,
                    ], [
                        DoLRules.skulduggery_6,
                    ]),
    
    DoLLocationNames.skill_skulduggery_10: (171, [
                        DoLRegionNames.in_town, 
                    ], [
                        DoLLocationTypes.skill,
                    ], [
                        DoLRules.skulduggery_7,
                    ]),



    # Dancing just wants dance studio, but can be leveled in strip club and brothel
    DoLLocationNames.skill_dancing_1: (172, [
                        DoLRegionNames.dance_studio,
                    ], [
                        DoLLocationTypes.skill,
                    ], []),
    
    DoLLocationNames.skill_dancing_2: (173, [
                        DoLRegionNames.dance_studio,
                    ], [
                        DoLLocationTypes.skill,
                    ], []),
    
    DoLLocationNames.skill_dancing_3: (174, [
                        DoLRegionNames.dance_studio,
                    ], [
                        DoLLocationTypes.skill,
                    ], []),
    
    DoLLocationNames.skill_dancing_4: (175, [
                        DoLRegionNames.dance_studio,
                    ], [
                        DoLLocationTypes.skill,
                    ], []),
    
    DoLLocationNames.skill_dancing_5: (176, [
                        DoLRegionNames.dance_studio,
                    ], [
                        DoLLocationTypes.skill,
                    ], []),
    
    DoLLocationNames.skill_dancing_6: (177, [
                        DoLRegionNames.dance_studio,
                    ], [
                        DoLLocationTypes.skill,
                    ], []),
    
    DoLLocationNames.skill_dancing_7: (178, [
                        DoLRegionNames.dance_studio,
                    ], [
                        DoLLocationTypes.skill,
                    ], []),
    
    DoLLocationNames.skill_dancing_8: (179, [
                        DoLRegionNames.dance_studio,
                    ], [
                        DoLLocationTypes.skill,
                    ], []),
    
    DoLLocationNames.skill_dancing_9: (180, [
                        DoLRegionNames.dance_studio,
                    ], [
                        DoLLocationTypes.skill,
                    ], []),
    
    DoLLocationNames.skill_dancing_10: (181, [
                        DoLRegionNames.dance_studio,
                    ], [
                        DoLLocationTypes.skill,
                    ], []),



    # School for at least level 1
    DoLLocationNames.skill_swimming_1: (182, [
                        DoLRegionNames.school, 
                    ], [
                        DoLLocationTypes.skill,
                    ], []),
    
    DoLLocationNames.skill_swimming_2: (183, [
                        DoLRegionNames.school, 
                    ], [
                        DoLLocationTypes.skill,
                    ], []),
    
    DoLLocationNames.skill_swimming_3: (184, [
                        DoLRegionNames.school, 
                    ], [
                        DoLLocationTypes.skill,
                    ], []),
    
    DoLLocationNames.skill_swimming_4: (185, [
                        DoLRegionNames.school,
                    ], [
                        DoLLocationTypes.skill,
                    ], []),
    
    DoLLocationNames.skill_swimming_5: (186, [
                        DoLRegionNames.school, 
                    ], [
                        DoLLocationTypes.skill,
                    ], []),
    
    DoLLocationNames.skill_swimming_6: (187, [
                        DoLRegionNames.school, 
                    ], [
                        DoLLocationTypes.skill,
                    ], []),
    
    DoLLocationNames.skill_swimming_7: (188, [
                        DoLRegionNames.school, 
                    ], [
                        DoLLocationTypes.skill,
                    ], []),
    
    DoLLocationNames.skill_swimming_8: (189, [
                        DoLRegionNames.school, 
                    ], [
                        DoLLocationTypes.skill,
                    ], []),
    
    DoLLocationNames.skill_swimming_9: (190, [
                        DoLRegionNames.school, 
                    ], [
                        DoLLocationTypes.skill,
                    ], []),
    
    DoLLocationNames.skill_swimming_10: (191, [
                        DoLRegionNames.school, 
                    ], [
                        DoLLocationTypes.skill,
                    ], []),



    # Starting levels anywhere, rest park good place to train
    DoLLocationNames.skill_athletics_1: (192, [
                        DoLRegionNames.in_town, 
                    ], [
                        DoLLocationTypes.skill,
                    ], []),
    
    DoLLocationNames.skill_athletics_2: (193, [
                        DoLRegionNames.in_town, 
                    ], [
                        DoLLocationTypes.skill,
                    ], []),
    
    DoLLocationNames.skill_athletics_3: (194, [
                        DoLRegionNames.park, 
                    ], [
                        DoLLocationTypes.skill,
                    ], []),
    
    DoLLocationNames.skill_athletics_4: (195, [
                        DoLRegionNames.park, 
                    ], [
                        DoLLocationTypes.skill,
                    ], []),
    
    DoLLocationNames.skill_athletics_5: (196, [
                        DoLRegionNames.park, 
                    ], [
                        DoLLocationTypes.skill,
                    ], []),
    
    DoLLocationNames.skill_athletics_6: (197, [
                        DoLRegionNames.park, 
                    ], [
                        DoLLocationTypes.skill,
                    ], []),
    
    DoLLocationNames.skill_athletics_7: (198, [
                        DoLRegionNames.park,
                    ], [
                        DoLLocationTypes.skill,
                    ], []),
    
    DoLLocationNames.skill_athletics_8: (199, [
                        DoLRegionNames.park, 
                    ], [
                        DoLLocationTypes.skill,
                    ], []),
    
    DoLLocationNames.skill_athletics_9: (200, [
                        DoLRegionNames.park, 
                    ], [
                        DoLLocationTypes.skill,
                    ], []),
    
    DoLLocationNames.skill_athletics_10: (201, [
                        DoLRegionNames.park, 
                    ], [
                        DoLLocationTypes.skill,
                    ], []),



    DoLLocationNames.skill_tending_1: (202, [
                        DoLRegionNames.in_town,
                    ], [
                        DoLLocationTypes.skill,
                    ], []),
    
    DoLLocationNames.skill_tending_2: (203, [
                        DoLRegionNames.in_town,  
                    ], [
                        DoLLocationTypes.skill,
                    ], []),

    # Farm good place to train further levels
    DoLLocationNames.skill_tending_3: (204, [
                        DoLRegionNames.alex_farm, 
                    ], [
                        DoLLocationTypes.skill,
                    ], []),
    
    DoLLocationNames.skill_tending_4: (205, [
                        DoLRegionNames.alex_farm,
                    ], [
                        DoLLocationTypes.skill,
                    ], []),
    
    DoLLocationNames.skill_tending_5: (206, [
                        DoLRegionNames.alex_farm,
                    ], [
                        DoLLocationTypes.skill,
                    ], []),
    
    DoLLocationNames.skill_tending_6: (207, [
                        DoLRegionNames.alex_farm,
                    ], [
                        DoLLocationTypes.skill,
                    ], []),
    
    DoLLocationNames.skill_tending_7: (208, [
                        DoLRegionNames.alex_farm,
                    ], [
                        DoLLocationTypes.skill,
                    ], []),
    
    DoLLocationNames.skill_tending_8: (209, [
                        DoLRegionNames.alex_farm,
                    ], [
                        DoLLocationTypes.skill,
                    ], []),
    
    DoLLocationNames.skill_tending_9: (210, [
                        DoLRegionNames.alex_farm,
                    ], [
                        DoLLocationTypes.skill,
                    ], []),
    
    DoLLocationNames.skill_tending_10: (211, [
                        DoLRegionNames.alex_farm,
                    ], [
                        DoLLocationTypes.skill,
                    ], []),

    

    DoLLocationNames.skill_housekeeping_1: (212, [
                        DoLRegionNames.domus_houses,
                    ], [
                        DoLLocationTypes.skill,
                    ], []),
    
    DoLLocationNames.skill_housekeeping_2: (213, [
                        DoLRegionNames.flats,
                    ], [
                        DoLLocationTypes.skill,
                    ], []),
    
    DoLLocationNames.skill_housekeeping_3: (214, [
                        DoLRegionNames.starfish_street,
                    ], [
                        DoLLocationTypes.skill,
                    ], []),
    
    DoLLocationNames.skill_housekeeping_4: (215, [
                        DoLRegionNames.danube_street,
                    ], [
                        DoLLocationTypes.skill,
                    ], []),
    
    DoLLocationNames.skill_housekeeping_5: (216, [
                        DoLRegionNames.temple,
                    ], [
                        DoLLocationTypes.skill,
                    ], []),
    
    DoLLocationNames.skill_housekeeping_6: (217, [
                        DoLRegionNames.temple,
                    ], [
                        DoLLocationTypes.skill,
                    ], []),
    
    DoLLocationNames.skill_housekeeping_7: (218, [
                        DoLRegionNames.temple,
                    ], [
                        DoLLocationTypes.skill,
                    ], []),
    
    DoLLocationNames.skill_housekeeping_8: (219, [
                        DoLRegionNames.temple,
                    ], [
                        DoLLocationTypes.skill,
                    ], []),
    
    DoLLocationNames.skill_housekeeping_9: (220, [
                        DoLRegionNames.temple,
                    ], [
                        DoLLocationTypes.skill,
                    ], []),
    
    DoLLocationNames.skill_housekeeping_10: (221, [
                        DoLRegionNames.temple,
                    ], [
                        DoLLocationTypes.skill,
                    ], []),


    # ---------------- Sex Skills ----------------
    # sex skills just require encounters

    DoLLocationNames.skill_seduction_1: (222, [
                        DoLRegionNames.in_town,
                    ], [
                        DoLLocationTypes.skill,
                    ], []),
    
    DoLLocationNames.skill_seduction_2: (223, [
                        DoLRegionNames.in_town,
                    ], [
                        DoLLocationTypes.skill,
                    ], []),
    
    DoLLocationNames.skill_seduction_3: (224, [
                        DoLRegionNames.in_town,
                    ], [
                        DoLLocationTypes.skill,
                    ], []),
    
    DoLLocationNames.skill_seduction_4: (225, [
                        DoLRegionNames.in_town,
                    ], [
                        DoLLocationTypes.skill,
                    ], []),
    
    DoLLocationNames.skill_seduction_5: (226, [
                        DoLRegionNames.in_town,
                    ], [
                        DoLLocationTypes.skill,
                    ], []),




    DoLLocationNames.skill_oral_1: (227, [
                        DoLRegionNames.in_town,
                    ], [
                        DoLLocationTypes.skill,
                    ], []),
    
    DoLLocationNames.skill_oral_2: (228, [
                        DoLRegionNames.in_town,
                    ], [
                        DoLLocationTypes.skill,
                    ], []),
    
    DoLLocationNames.skill_oral_3: (229, [
                        DoLRegionNames.in_town,
                    ], [
                        DoLLocationTypes.skill,
                    ], [
                        DoLRules.oral_1
                    ]),
    
    DoLLocationNames.skill_oral_4: (230, [
                        DoLRegionNames.in_town,
                    ], [
                        DoLLocationTypes.skill,
                    ], [
                        DoLRules.oral_2
                    ]),
    
    DoLLocationNames.skill_oral_5: (231, [
                        DoLRegionNames.in_town,
                    ], [
                        DoLLocationTypes.skill,
                    ], [
                        DoLRules.oral_3
                    ]),



    DoLLocationNames.skill_chest_1: (232, [
                        DoLRegionNames.in_town,
                    ], [
                        DoLLocationTypes.skill,
                    ], []),
    
    DoLLocationNames.skill_chest_2: (233, [
                        DoLRegionNames.in_town,
                    ], [
                        DoLLocationTypes.skill,
                    ], []),
    
    DoLLocationNames.skill_chest_3: (234, [
                        DoLRegionNames.in_town,
                    ], [
                        DoLLocationTypes.skill,
                    ], [
                        DoLRules.chest_1,
                    ]),
    
    DoLLocationNames.skill_chest_4: (235, [
                        DoLRegionNames.in_town,
                    ], [
                        DoLLocationTypes.skill,
                    ], [
                        DoLRules.chest_2,
                    ]),
    
    DoLLocationNames.skill_chest_5: (236, [
                        DoLRegionNames.in_town,
                    ], [
                        DoLLocationTypes.skill,
                    ], [
                        DoLRules.chest_3,
                    ]),



    DoLLocationNames.skill_hands_1: (237, [
                        DoLRegionNames.in_town,
                    ], [
                        DoLLocationTypes.skill,
                    ], []),
    
    DoLLocationNames.skill_hands_2: (238, [
                        DoLRegionNames.in_town,
                    ], [
                        DoLLocationTypes.skill,
                    ], []),
    
    DoLLocationNames.skill_hands_3: (239, [
                        DoLRegionNames.in_town,
                    ], [
                        DoLLocationTypes.skill,
                    ], [
                        DoLRules.hands_1,
                    ]),
    
    DoLLocationNames.skill_hands_4: (240, [
                        DoLRegionNames.in_town,
                    ], [
                        DoLLocationTypes.skill,
                    ], [
                        DoLRules.hands_2
                    ]),
    
    DoLLocationNames.skill_hands_5: (241, [
                        DoLRegionNames.in_town,
                    ], [
                        DoLLocationTypes.skill,
                    ], [
                        DoLRules.hands_3
                    ]),



    DoLLocationNames.skill_buttocks_1: (242, [
                        DoLRegionNames.in_town,
                    ], [
                        DoLLocationTypes.skill,
                    ], []),
    
    DoLLocationNames.skill_buttocks_2: (243, [
                        DoLRegionNames.in_town,
                    ], [
                        DoLLocationTypes.skill,
                    ], []),
    
    DoLLocationNames.skill_buttocks_3: (244, [
                        DoLRegionNames.in_town,
                    ], [
                        DoLLocationTypes.skill,
                    ], [
                        DoLRules.buttocks_1,
                    ]),
    
    DoLLocationNames.skill_buttocks_4: (245, [
                        DoLRegionNames.in_town,
                    ], [
                        DoLLocationTypes.skill,
                    ], [
                        DoLRules.buttocks_2,
                    ]),
    
    DoLLocationNames.skill_buttocks_5: (246, [
                        DoLRegionNames.in_town,
                    ], [
                        DoLLocationTypes.skill,
                    ], [
                        DoLRules.buttocks_3,
                    ]),


                        
    DoLLocationNames.skill_privates_1: (247, [
                        DoLRegionNames.in_town,
                    ], [
                        DoLLocationTypes.skill,
                    ], []),
    
    DoLLocationNames.skill_privates_2: (248, [
                        DoLRegionNames.in_town,
                    ], [
                        DoLLocationTypes.skill,
                    ], []),
    
    DoLLocationNames.skill_privates_3: (249, [
                        DoLRegionNames.in_town,
                    ], [
                        DoLLocationTypes.skill,
                    ], [
                        DoLRules.privates_1,
                    ]),
    
    DoLLocationNames.skill_privates_4: (250, [
                        DoLRegionNames.in_town,
                    ], [
                        DoLLocationTypes.skill,
                    ], [
                         DoLRules.privates_2,
                    ]),
    
    DoLLocationNames.skill_privates_5: (251, [
                        DoLRegionNames.in_town,
                    ], [
                        DoLLocationTypes.skill,
                    ], [
                        DoLRules.privates_3,
                    ]),



    DoLLocationNames.skill_anal_1: (252, [
                        DoLRegionNames.in_town,
                    ], [
                        DoLLocationTypes.skill,
                    ], []),
    
    DoLLocationNames.skill_anal_2: (253, [
                        DoLRegionNames.in_town,
                    ], [
                        DoLLocationTypes.skill,
                    ], []),
    
    DoLLocationNames.skill_anal_3: (254, [
                        DoLRegionNames.in_town,
                    ], [
                        DoLLocationTypes.skill,
                    ], [
                        DoLRules.anal_1,
                    ]),
    
    DoLLocationNames.skill_anal_4: (255, [
                        DoLRegionNames.in_town,
                    ], [
                        DoLLocationTypes.skill,
                    ], [
                        DoLRules.anal_2,
                    ]),
    
    DoLLocationNames.skill_anal_5: (256, [
                        DoLRegionNames.in_town,
                    ], [
                        DoLLocationTypes.skill,
                    ], [
                        DoLRules.anal_3,
                    ]),



    # note: can use riding school for higher levels
    DoLLocationNames.skill_thighs_1: (257, [
                        DoLRegionNames.in_town,
                    ], [
                        DoLLocationTypes.skill,
                    ], []),
    
    DoLLocationNames.skill_thighs_2: (258, [
                        DoLRegionNames.in_town,
                    ], [
                        DoLLocationTypes.skill,
                    ], []),
    
    DoLLocationNames.skill_thighs_3: (259, [
                        DoLRegionNames.in_town,
                    ], [
                        DoLLocationTypes.skill,
                    ], [
                        DoLRules.thighs_1,
                    ]),
    
    DoLLocationNames.skill_thighs_4: (260, [
                        DoLRegionNames.in_town,
                    ], [
                        DoLLocationTypes.skill,
                    ], [
                        DoLRules.thighs_2,
                    ]),
    
    DoLLocationNames.skill_thighs_5: (261, [
                        DoLRegionNames.in_town,
                    ], [
                        DoLLocationTypes.skill,
                    ], [
                        DoLRules.thighs_3,
                    ]),


             
    # note: can use dance studio for higher levels
    DoLLocationNames.skill_feet_1: (262, [
                        DoLRegionNames.in_town,
                    ], [
                        DoLLocationTypes.skill,
                    ], []),
    
    DoLLocationNames.skill_feet_2: (263, [
                        DoLRegionNames.in_town,
                    ], [
                        DoLLocationTypes.skill,
                    ], []),
    
    DoLLocationNames.skill_feet_3: (264, [
                        DoLRegionNames.in_town,
                    ], [
                        DoLLocationTypes.skill,
                    ], [
                        DoLRules.feet_1,
                    ]),
    
    DoLLocationNames.skill_feet_4: (265, [
                        DoLRegionNames.in_town,
                    ], [
                        DoLLocationTypes.skill,
                    ], [
                        DoLRules.feet_2,
                    ]),
    
    DoLLocationNames.skill_feet_5: (266, [
                        DoLRegionNames.in_town,
                    ], [
                        DoLLocationTypes.skill,
                    ], [
                        DoLRules.feet_3,
                    ]),



    # ---------------- School Skills ----------------
    # pretty much need school for all school skills

    DoLLocationNames.skill_science_1: (267, [
                        DoLRegionNames.school,
                    ], [
                        DoLLocationTypes.skill,
                    ], []),
    
    DoLLocationNames.skill_science_2: (268, [
                        DoLRegionNames.school,
                    ], [
                        DoLLocationTypes.skill,
                    ], []),
    
    DoLLocationNames.skill_science_3: (269, [
                        DoLRegionNames.school,
                    ], [
                        DoLLocationTypes.skill,
                    ], []),
    
    DoLLocationNames.skill_science_4: (270, [
                        DoLRegionNames.school,
                    ], [
                        DoLLocationTypes.skill,
                    ], []),
    
    DoLLocationNames.skill_science_5: (271, [
                        DoLRegionNames.school,
                    ], [
                        DoLLocationTypes.skill,
                    ], []),


                        
    DoLLocationNames.skill_math_1: (272, [
                        DoLRegionNames.school,
                    ], [
                        DoLLocationTypes.skill,
                    ], []),
    
    DoLLocationNames.skill_math_2: (273, [
                        DoLRegionNames.school,
                    ], [
                        DoLLocationTypes.skill,
                    ], []),
    
    DoLLocationNames.skill_math_3: (274, [
                        DoLRegionNames.school,
                    ], [
                        DoLLocationTypes.skill,
                    ], []),
    
    DoLLocationNames.skill_math_4: (275, [
                        DoLRegionNames.school,
                    ], [
                        DoLLocationTypes.skill,
                    ], []),
    
    DoLLocationNames.skill_math_5: (276, [
                        DoLRegionNames.school,
                    ], [
                        DoLLocationTypes.skill,
                    ], []),


    
    DoLLocationNames.skill_english_1: (277, [
                        DoLRegionNames.school,
                    ], [
                        DoLLocationTypes.skill,
                    ], []),
    
    DoLLocationNames.skill_english_2: (278, [
                        DoLRegionNames.school,
                    ], [
                        DoLLocationTypes.skill,
                    ], []),
    
    DoLLocationNames.skill_english_3: (279, [
                        DoLRegionNames.school,
                    ], [
                        DoLLocationTypes.skill,
                    ], []),
    
    DoLLocationNames.skill_english_4: (280, [
                        DoLRegionNames.school,
                    ], [
                        DoLLocationTypes.skill,
                    ], []),
    
    DoLLocationNames.skill_english_5: (281, [
                        DoLRegionNames.school,
                    ], [
                        DoLLocationTypes.skill,
                    ], []),


    
    DoLLocationNames.skill_history_1: (282, [
                        DoLRegionNames.school,
                    ], [
                        DoLLocationTypes.skill,
                    ], []),
    
    DoLLocationNames.skill_history_2: (283, [
                        DoLRegionNames.school,
                    ], [
                        DoLLocationTypes.skill,
                    ], []),
    
    DoLLocationNames.skill_history_3: (284, [
                        DoLRegionNames.school,
                    ], [
                        DoLLocationTypes.skill,
                    ], []),
    
    DoLLocationNames.skill_history_4: (285, [
                        DoLRegionNames.school,
                    ], [
                        DoLLocationTypes.skill,
                    ], []),
    
    DoLLocationNames.skill_history_5: (286, [
                        DoLRegionNames.school,
                    ], [
                        DoLLocationTypes.skill,
                    ], []),



    # ---------------- Core Skills ----------------
    # no strict requirements for any of these stats, outside of doing encounters that grow them
    # willpower: grows via any encounters
    # physique: grows via exercise
    # promiscuity: grows by doing things with this stat
    # exhibitionism: grows by doing things with this stat
    # deviancy: grows via animal encounters

    DoLLocationNames.skill_willpower_1: (287, [
                        DoLRegionNames.in_town, 
                    ], [
                        DoLLocationTypes.skill,
                    ], []),
    
    DoLLocationNames.skill_willpower_2: (288, [
                        DoLRegionNames.in_town, 
                    ], [
                        DoLLocationTypes.skill,
                    ], []),
    
    DoLLocationNames.skill_willpower_3: (289, [
                        DoLRegionNames.in_town, 
                    ], [
                        DoLLocationTypes.skill,
                    ], []),
    
    DoLLocationNames.skill_willpower_4: (290, [
                        DoLRegionNames.in_town, 
                    ], [
                        DoLLocationTypes.skill,
                    ], []),
    
    DoLLocationNames.skill_willpower_5: (291, [
                        DoLRegionNames.in_town, 
                    ], [
                        DoLLocationTypes.skill,
                    ], []),
    
    DoLLocationNames.skill_willpower_6: (292, [
                        DoLRegionNames.in_town, 
                    ], [
                        DoLLocationTypes.skill,
                    ], []),



    # park good place to train
    DoLLocationNames.skill_physique_1: (293, [
                        DoLRegionNames.park, 
                    ], [
                        DoLLocationTypes.skill,
                    ], []),
    
    DoLLocationNames.skill_physique_2: (294, [
                        DoLRegionNames.park, 
                    ], [
                        DoLLocationTypes.skill,
                    ], []),
    
    DoLLocationNames.skill_physique_3: (295, [
                        DoLRegionNames.park,
                    ], [
                        DoLLocationTypes.skill,
                    ], []),
    
    DoLLocationNames.skill_physique_4: (296, [
                        DoLRegionNames.park,
                    ], [
                        DoLLocationTypes.skill,
                    ], []),
    
    DoLLocationNames.skill_physique_5: (297, [
                        DoLRegionNames.park,
                    ], [
                        DoLLocationTypes.skill,
                    ], []),
    
    DoLLocationNames.skill_physique_6: (298, [
                        DoLRegionNames.park,
                    ], [
                        DoLLocationTypes.skill,
                    ], []),



    DoLLocationNames.skill_promiscuity_1: (299, [
                        DoLRegionNames.in_town,
                    ], [
                        DoLLocationTypes.skill,
                    ], []),
    
    DoLLocationNames.skill_promiscuity_2: (300, [
                        DoLRegionNames.in_town,
                    ], [
                        DoLLocationTypes.skill,
                    ], []),
    
    DoLLocationNames.skill_promiscuity_3: (301, [
                        DoLRegionNames.in_town,
                    ], [
                        DoLLocationTypes.skill,
                    ], []),
    
    DoLLocationNames.skill_promiscuity_4: (302, [
                        DoLRegionNames.in_town,
                    ], [
                        DoLLocationTypes.skill,
                    ], []),
    
    DoLLocationNames.skill_promiscuity_5: (303, [
                        DoLRegionNames.in_town,
                    ], [
                        DoLLocationTypes.skill,
                    ], []),
    
    DoLLocationNames.skill_promiscuity_6: (304, [
                        DoLRegionNames.in_town,
                    ], [
                        DoLLocationTypes.skill,
                    ], []),



    # orph for minimum level + need wardrobe
    DoLLocationNames.skill_exhibitionism_1: (305, [
                        DoLRegionNames.orphanage, 
                    ], [
                        DoLLocationTypes.skill,
                    ], []),
    
    DoLLocationNames.skill_exhibitionism_2: (306, [
                        DoLRegionNames.orphanage,
                    ], [
                        DoLLocationTypes.skill,
                    ], []),
    
    DoLLocationNames.skill_exhibitionism_3: (307, [
                        DoLRegionNames.orphanage,
                    ], [
                        DoLLocationTypes.skill,
                    ], []),
    
    DoLLocationNames.skill_exhibitionism_4: (308, [
                        DoLRegionNames.orphanage,
                    ], [
                        DoLLocationTypes.skill,
                    ], []),
    
    DoLLocationNames.skill_exhibitionism_5: (309, [
                        DoLRegionNames.orphanage,
                    ], [
                        DoLLocationTypes.skill,
                    ], []),
    
    DoLLocationNames.skill_exhibitionism_6: (310, [
                        DoLRegionNames.orphanage,
                    ], [
                        DoLLocationTypes.skill,
                    ], []),



    # wiki recommends farm, but can level from anywhere
    DoLLocationNames.skill_deviancy_1: (311, [
                        DoLRegionNames.in_town, 
                    ], [
                        DoLLocationTypes.skill,
                    ], []),
    
    DoLLocationNames.skill_deviancy_2: (312, [
                        DoLRegionNames.in_town,
                    ], [
                        DoLLocationTypes.skill,
                    ], []),
    
    DoLLocationNames.skill_deviancy_3: (313, [
                        DoLRegionNames.in_town,
                    ], [
                        DoLLocationTypes.skill,
                    ], []),
    
    DoLLocationNames.skill_deviancy_4: (314, [
                        DoLRegionNames.in_town,
                    ], [
                        DoLLocationTypes.skill,
                    ], []),
    
    DoLLocationNames.skill_deviancy_5: (315, [
                        DoLRegionNames.in_town,
                    ], [
                        DoLLocationTypes.skill,
                    ], []),
    
    DoLLocationNames.skill_deviancy_6: (316, [
                        DoLRegionNames.in_town,
                    ], [
                        DoLLocationTypes.skill,
                    ], []),



    # ---------------- Feats  ----------------

    DoLLocationNames.feat_pocketchange: (317, [
                        DoLRegionNames.X,
                    ], [
                        DoLLocationTypes.feat,
                    ], []),

    DoLLocationNames.feat_moneymaker: (318, [
                        DoLRegionNames.X,
                    ], [
                        DoLLocationTypes.feat,
                    ], []),

    DoLLocationNames.feat_tycoon: (319, [
                        DoLRegionNames.X,
                    ], [
                        DoLLocationTypes.feat,
                    ], []),

    DoLLocationNames.feat_millionaire: (320, [
                        DoLRegionNames.X,
                    ], [
                        DoLLocationTypes.feat,
                    ], []),

    DoLLocationNames.feat_itbelongsinamuseum: (321, [
                        DoLRegionNames.X,
                    ], [
                        DoLLocationTypes.feat,
                    ], []),

    DoLLocationNames.feat_fullycovered: (322, [
                        DoLRegionNames.X,
                    ], [
                        DoLLocationTypes.feat,
                    ], []),

    DoLLocationNames.feat_beingaboy: (323, [
                        DoLRegionNames.X,
                    ], [
                        DoLLocationTypes.feat,
                        DoLRules.multipleruns_toggle,
                    ], []),

    DoLLocationNames.feat_beingagirl: (324, [
                        DoLRegionNames.X,
                    ], [
                        DoLLocationTypes.feat,
                        DoLRules.multipleruns_toggle,
                    ], []),

    DoLLocationNames.feat_beingahermaphrodite: (325, [
                        DoLRegionNames.X,
                    ], [
                        DoLLocationTypes.feat,
                        DoLRules.multipleruns_toggle,
                    ], []),

    DoLLocationNames.feat_beinganorphan: (326, [
                        DoLRegionNames.X,
                    ], [
                        DoLLocationTypes.feat
                        # TODO: long time toggle?
                    ], []),

    DoLLocationNames.feat_stressfulchallenge: (327, [
                        DoLRegionNames.X,
                    ], [
                        DoLLocationTypes.feat,
                        DoLRules.multipleruns_toggle,
                    ], []),

    DoLLocationNames.feat_longstressfulchallenge: (328, [
                        DoLRegionNames.X,
                    ], [
                        DoLLocationTypes.feat,
                        DoLRules.multipleruns_toggle,
                    ], []),

    DoLLocationNames.feat_billboard: (329, [
                        DoLRegionNames.X,
                    ], [
                        DoLLocationTypes.feat,
                        DoLRules.bodywriting_toggle,
                    ], []),

    DoLLocationNames.feat_alivingcanvas: (330, [
                        DoLRegionNames.X,
                    ], [
                        DoLLocationTypes.feat,
                        DoLRules.bodywriting_toggle,
                    ], []),

    DoLLocationNames.feat_farmhand: (331, [
                        DoLRegionNames.X,
                    ], [
                        DoLLocationTypes.feat,
                    ], []),

    DoLLocationNames.feat_farmer: (332, [
                        DoLRegionNames.X,
                    ], [
                        DoLLocationTypes.feat,
                    ], []),

    DoLLocationNames.feat_cultivator: (333, [
                        DoLRegionNames.X,
                    ], [
                        DoLLocationTypes.feat,
                    ], []),

    DoLLocationNames.feat_therivalfarm: (334, [
                        DoLRegionNames.X,
                    ], [
                        DoLLocationTypes.feat,
                    ], []),

    DoLLocationNames.feat_therivalestate: (335, [
                        DoLRegionNames.X,
                    ], [
                        DoLLocationTypes.feat,
                    ], []),

    DoLLocationNames.feat_heroicvictory: (336, [
                        DoLRegionNames.X,
                    ], [
                        DoLLocationTypes.feat,
                    ], []),

    DoLLocationNames.feat_fiveinarow: (337, [
                        DoLRegionNames.X,
                    ], [
                        DoLLocationTypes.feat,
                    ], []),

    DoLLocationNames.feat_distinction: (338, [
                        DoLRegionNames.X,
                    ], [
                        DoLLocationTypes.feat,
                    ], []),

    DoLLocationNames.feat_distinctive: (339, [
                        DoLRegionNames.X,
                    ], [
                        DoLLocationTypes.feat,
                        # TODO: difficult rule
                    ], []),

    DoLLocationNames.feat_distinguished: (340, [
                        DoLRegionNames.X,
                    ], [
                        DoLLocationTypes.feat,
                        # TODO: difficult rule
                    ], []),

    DoLLocationNames.feat_chefdetournant: (341, [
                        DoLRegionNames.school,
                        DoLRegionNames.avery_mansion,
                    ], [
                        DoLLocationTypes.feat,
                    ], []),

    DoLLocationNames.feat_chefdepartie: (342, [
                        DoLRegionNames.school,
                        DoLRegionNames.avery_mansion,
                    ], [
                        DoLLocationTypes.feat,
                    ], []),

    DoLLocationNames.feat_souschef: (343, [
                        DoLRegionNames.school,
                        DoLRegionNames.avery_mansion,
                    ], [
                        DoLLocationTypes.feat,
                    ], []),

    DoLLocationNames.feat_sciencefairwinner: (344, [
                        DoLRegionNames.cliff_street,
                    ], [
                        DoLLocationTypes.feat,
                    ], [
                        DoLRules.sciencefairwinner,
                    ]),

    DoLLocationNames.feat_thesisoffence: (345, [
                        DoLRegionNames.cliff_street,
                    ], [
                        DoLLocationTypes.feat,
                        # TODO: difficult rule
                    ], [
                        DoLRules.sciencefairoffence,
                    ]),

    DoLLocationNames.feat_mathscompetitionwinner: (346, [
                        DoLRegionNames.school,
                    ], [
                        DoLLocationTypes.feat,
                    ], [
                        DoLRules.mathcomp
                    ]),

    DoLLocationNames.feat_richhearts: (347, [
                        DoLRegionNames.school,
                    ], [
                        DoLLocationTypes.feat,
                    ], []),

    DoLLocationNames.feat_mostaware: (348, [
                        DoLRegionNames.X,
                    ], [
                        DoLLocationTypes.feat,
                        # TODO: difficult rule
                    ], []),

    DoLLocationNames.feat_mostinnocent: (349, [
                        DoLRegionNames.X,
                    ], [
                        DoLLocationTypes.feat,
                    ], []),

    DoLLocationNames.feat_nomorecontrol: (350, [
                        DoLRegionNames.X,
                    ], [
                        DoLLocationTypes.feat,
                        DoLRules.bestiality_toggle, # beastiality or monster chance
                    ], []),

    # most stats feats just require their minimum training
    DoLLocationNames.feat_thief: (351, [
                        DoLRegionNames.X,
                    ], [
                        DoLLocationTypes.feat,
                    ], [
                        DoLRules.skulduggery_7,
                    ]),

    DoLLocationNames.feat_mayihavethisdance: (352, [
                        DoLRegionNames.X,
                    ], [
                        DoLLocationTypes.feat,
                    ], []),

    DoLLocationNames.feat_aquanaut: (353, [
                        DoLRegionNames.X,
                    ], [
                        DoLLocationTypes.feat,
                    ], []),

    DoLLocationNames.feat_seductress: (354, [
                        DoLRegionNames.X,
                    ], [
                        DoLLocationTypes.feat,
                    ], [
                        DoLRules.seduction_3,
                    ]),

    DoLLocationNames.feat_greenfingered: (355, [
                        DoLRegionNames.X,
                    ], [
                        DoLLocationTypes.feat,
                    ], []),

    DoLLocationNames.feat_majordomo: (356, [
                        DoLRegionNames.X,
                    ], [
                        DoLLocationTypes.feat,
                    ], [
                        DoLRules.housekeeping_7,
                    ]),

    DoLLocationNames.feat_swift: (357, [
                        DoLRegionNames.X,
                    ], [
                        DoLLocationTypes.feat,
                    ], []),

    DoLLocationNames.feat_alluring: (358, [
                        DoLRegionNames.X,
                    ], [
                        DoLLocationTypes.feat,
                    ], []),

    DoLLocationNames.feat_sexspecialist: (359, [
                        DoLRegionNames.X,
                    ], [
                        DoLLocationTypes.feat,
                    ], [
                        DoLRules.sexspecialist
                    ]),

    DoLLocationNames.feat_perfectrecord: (360, [
                        DoLRegionNames.X,
                    ], [
                        DoLLocationTypes.feat
                        # TODO: difficult rule
                    ], []),

    DoLLocationNames.feat_perfectsub: (361, [
                        DoLRegionNames.X,
                    ], [
                        DoLLocationTypes.feat,
                        # TODO: difficult rule
                    ], []),

    DoLLocationNames.feat_defyingtheodds: (362, [
                        DoLRegionNames.X,
                    ], [
                        DoLLocationTypes.feat,
                        # TODO: difficult rule
                    ], []),

    DoLLocationNames.feat_hawker: (363, [
                        DoLRegionNames.X,
                    ], [
                        DoLLocationTypes.feat,
                        # TODO: difficult rule
                    ], []),

    DoLLocationNames.feat_vendor: (364, [
                        DoLRegionNames.X,
                    ], [
                        DoLLocationTypes.feat,
                    ], []),

    DoLLocationNames.feat_merchant: (365, [
                        DoLRegionNames.X,
                    ], [
                        DoLLocationTypes.feat,
                    ], []),

    DoLLocationNames.feat_twisteddesire: (366, [
                        DoLRegionNames.X,
                    ], [
                        DoLLocationTypes.feat,
                    ], []),

    DoLLocationNames.feat_servedhot: (367, [
                        DoLRegionNames.X,
                    ], [
                        DoLLocationTypes.feat,
                    ], []),

    DoLLocationNames.feat_sadomasochist: (368, [
                        DoLRegionNames.X,
                    ], [
                        DoLLocationTypes.feat
                        # TODO: difficult rule
                    ], []),

    DoLLocationNames.feat_shiningreputation: (369, [
                        DoLRegionNames.X,
                    ], [
                        DoLLocationTypes.feat,
                        # TODO: difficult rule
                    ], []),

    DoLLocationNames.feat_socialbutterfly: (370, [
                        DoLRegionNames.X,
                    ], [
                        DoLLocationTypes.feat,
                    ], []),

    DoLLocationNames.feat_unsocialmoth: (371, [
                        DoLRegionNames.X,
                    ], [
                        DoLLocationTypes.feat,
                    ], []),

    DoLLocationNames.feat_teacherspet: (372, [
                        DoLRegionNames.X,
                    ], [
                        DoLLocationTypes.feat,
                    ], []),

    DoLLocationNames.feat_teachersnightmare: (373, [
                        DoLRegionNames.X,
                    ], [
                        DoLLocationTypes.feat,
                    ], []),

    DoLLocationNames.feat_robinthelover: (374, [
                        DoLRegionNames.X,
                    ], [
                        DoLLocationTypes.feat,
                        DoLRules.multipleruns_toggle,
                    ], []),

    DoLLocationNames.feat_hungryorphan: (375, [
                        DoLRegionNames.school,
                        DoLRegionNames.avery_mansion,
                    ], [
                        DoLLocationTypes.feat,
                    ], []),

    DoLLocationNames.feat_robinssong: (376, [
                        DoLRegionNames.X,
                    ], [
                        DoLLocationTypes.feat,
                    ], []),

    DoLLocationNames.feat_whitneythebully: (377, [
                        DoLRegionNames.X,
                    ], [
                        DoLLocationTypes.feat,
                        DoLRules.multipleruns_toggle,
                    ], []),

    DoLLocationNames.feat_thebullystithe: (378, [
                        DoLRegionNames.school,
                        DoLRegionNames.avery_mansion,
                    ], [
                        DoLLocationTypes.feat,
                    ], []),

    DoLLocationNames.feat_delinquentantics: (379, [
                        DoLRegionNames.X,
                    ], [
                        DoLLocationTypes.feat,
                    ], []),

    DoLLocationNames.feat_giddyup: (380, [
                        DoLRegionNames.X,
                    ], [
                        DoLLocationTypes.feat,
                    ], []),

    DoLLocationNames.feat_whitneyssecret: (381, [
                        DoLRegionNames.X,
                    ], [
                        DoLLocationTypes.feat,
                    ], []),

    DoLLocationNames.feat_kylartheobsessed: (382, [
                        DoLRegionNames.X,
                    ], [
                        DoLLocationTypes.feat,
                        DoLRules.multipleruns_toggle,
                    ], []),

    DoLLocationNames.feat_notforrats: (383, [
                        DoLRegionNames.school,
                        DoLRegionNames.avery_mansion,
                    ], [
                        DoLLocationTypes.feat,
                    ], []),

    DoLLocationNames.feat_edenthelonely: (384, [
                        DoLRegionNames.X,
                    ], [
                        DoLLocationTypes.feat,
                        DoLRules.multipleruns_toggle,
                    ], []),

    DoLLocationNames.feat_sweetandtender: (385, [
                        DoLRegionNames.school,
                        DoLRegionNames.avery_mansion,
                    ], [
                        DoLLocationTypes.feat,
                    ], []),

    DoLLocationNames.feat_averythemoneybags: (386, [
                        DoLRegionNames.X,
                    ], [
                        DoLLocationTypes.feat,
                        DoLRules.multipleruns_toggle,
                    ], []),

    DoLLocationNames.feat_kept: (387, [
                        DoLRegionNames.X,
                    ], [
                        DoLLocationTypes.feat,
                    ], []),

    DoLLocationNames.feat_whatgoesaround: (388, [
                        DoLRegionNames.X,
                    ], [
                        DoLLocationTypes.feat,
                    ], []),

    DoLLocationNames.feat_mostexclusive: (389, [
                        DoLRegionNames.X,
                    ], [
                        DoLLocationTypes.feat,
                    ], []),

    DoLLocationNames.feat_pridecometh: (390, [
                        DoLRegionNames.X,
                    ], [
                        DoLLocationTypes.feat,
                    ], []),

    DoLLocationNames.feat_hautecuisine: (391, [
                        DoLRegionNames.school,
                        DoLRegionNames.avery_mansion,
                    ], [
                        DoLLocationTypes.feat,
                    ], []),

    DoLLocationNames.feat_leightontheshady: (392, [
                        DoLRegionNames.X,
                    ], [
                        DoLLocationTypes.feat,
                        DoLRules.multipleruns_toggle,
                    ], []),

    DoLLocationNames.feat_alextherobust: (393, [
                        DoLRegionNames.X,
                    ], [
                        DoLLocationTypes.feat,
                        DoLRules.multipleruns_toggle,
                    ], []),

    DoLLocationNames.feat_homecooking: (394, [
                        DoLRegionNames.school,
                        DoLRegionNames.avery_mansion,
                    ], [
                        DoLLocationTypes.feat,
                    ], []),

    DoLLocationNames.feat_greathawktheterror: (395, [
                        DoLRegionNames.X,
                    ], [
                        DoLLocationTypes.feat,
                        DoLRules.multipleruns_toggle,
                    ], []),

    DoLLocationNames.feat_returnthefavour: (396, [
                        DoLRegionNames.school,
                        DoLRegionNames.avery_mansion,
                    ], [
                        DoLLocationTypes.feat,
                    ], []),

    DoLLocationNames.feat_feathertrick: (397, [
                        DoLRegionNames.X,
                    ], [
                        DoLLocationTypes.feat,
                    ], []),

    DoLLocationNames.feat_wrenthesly: (398, [
                        DoLRegionNames.X,
                    ], [
                        DoLLocationTypes.feat,
                        DoLRules.multipleruns_toggle,
                    ], []),

    DoLLocationNames.feat_blackwolfthealpha: (399, [
                        DoLRegionNames.X,
                    ], [
                        DoLLocationTypes.feat,
                        DoLRules.multipleruns_toggle,
                    ], []),

    DoLLocationNames.feat_encroachingcivilisation: (400, [
                        DoLRegionNames.school,
                        DoLRegionNames.avery_mansion,
                    ], [
                        DoLLocationTypes.feat,
                    ], []),

    DoLLocationNames.feat_sydneythepurehearted: (401, [
                        DoLRegionNames.X,
                    ], [
                        DoLLocationTypes.feat,
                    ], []),

    DoLLocationNames.feat_communion: (402, [
                        DoLRegionNames.school,
                        DoLRegionNames.avery_mansion,
                    ], [
                        DoLLocationTypes.feat,
                    ], []),

    DoLLocationNames.feat_harperthehypnotist: (403, [
                        DoLRegionNames.X,
                    ], [
                        DoLLocationTypes.feat,
                        DoLRules.multipleruns_toggle,
                    ], []),

    DoLLocationNames.feat_morganthelost: (404, [
                        DoLRegionNames.X,
                    ], [
                        DoLLocationTypes.feat,
                        DoLRules.multipleruns_toggle,
                    ], []),

    DoLLocationNames.feat_gwylanthebewitching: (405, [
                        DoLRegionNames.X,
                    ], [
                        DoLLocationTypes.feat,
                        DoLRules.multipleruns_toggle,
                    ], []),

    DoLLocationNames.feat_covencomforts: (406, [
                        DoLRegionNames.school,
                        DoLRegionNames.avery_mansion,
                    ], [
                        DoLLocationTypes.feat,
                    ], []),

    DoLLocationNames.feat_lovetriangles: (407, [
                        DoLRegionNames.X,
                    ], [
                        DoLLocationTypes.feat,
                    ], []),

    DoLLocationNames.feat_lovetrapezoids: (408, [
                        DoLRegionNames.X,
                    ], [
                        DoLLocationTypes.feat,
                    ], []),

    DoLLocationNames.feat_bemyvalentine: (409, [
                        DoLRegionNames.X,
                    ], [
                        DoLLocationTypes.feat,
                    ], []),

    DoLLocationNames.feat_ballroomshowoff: (410, [
                        DoLRegionNames.X,
                    ], [
                        DoLLocationTypes.feat,
                    ], [
                        DoLRules.ballroomshowoff
                    ]),

    DoLLocationNames.feat_underthetable: (411, [
                        DoLRegionNames.X,
                    ], [
                        DoLLocationTypes.feat,
                    ], []),

    DoLLocationNames.feat_pubcrawlvictors: (412, [
                        DoLRegionNames.X,
                    ], [
                        DoLLocationTypes.feat,
                    ], []),

    DoLLocationNames.feat_masonssecret: (413, [
                        DoLRegionNames.X,
                    ], [
                        DoLLocationTypes.feat,
                    ], []),

    DoLLocationNames.feat_masonsshame: (414, [
                        DoLRegionNames.X,
                    ], [
                        DoLLocationTypes.feat,
                    ], []),

    DoLLocationNames.feat_animaltender: (415, [
                        DoLRegionNames.X,
                    ], [
                        DoLLocationTypes.feat,
                    ], []),

    DoLLocationNames.feat_ispy: (416, [
                        DoLRegionNames.X,
                    ], [
                        DoLLocationTypes.feat,
                    ], []),

    DoLLocationNames.feat_firstkiss: (417, [
                        DoLRegionNames.X,
                    ], [
                        DoLLocationTypes.feat,
                        DoLRules.multipleruns_toggle,
                    ], []),

    DoLLocationNames.feat_acrimemostfoul: (418, [
                        DoLRegionNames.X,
                    ], [
                        DoLLocationTypes.feat,
                    ], [
                        DoLRules.bodywriting_toggle # sydney will write on you unless you have bodywriting **off**
                    ]),

    DoLLocationNames.feat_longing: (419, [
                        DoLRegionNames.X,
                    ], [
                        DoLLocationTypes.feat,
                    ], []),

    DoLLocationNames.feat_paganrite: (420, [
                        DoLRegionNames.X,
                    ], [
                        DoLLocationTypes.feat,
                    ], []),

    DoLLocationNames.feat_warmestwinter: (421, [
                        DoLRegionNames.X,
                    ], [
                        DoLLocationTypes.feat,
                    ], [
                        DoLRules.access_moor
                    ]),

    DoLLocationNames.feat_trialsoffaith: (422, [
                        DoLRegionNames.X,
                    ], [
                        DoLLocationTypes.feat,
                    ], []), # TODO: rules for this (gwylan)

    DoLLocationNames.feat_firstverse: (423, [
                        DoLRegionNames.X,
                    ], [
                        DoLLocationTypes.feat,
                    ], []), # TODO: rules for this (gwylan)

    DoLLocationNames.feat_wildsong: (424, [
                        DoLRegionNames.X,
                    ], [
                        DoLLocationTypes.feat,
                    ], []), # TODO: rules for this (gwylan)

    DoLLocationNames.feat_foxbane: (425, [
                        DoLRegionNames.X,
                    ], [
                        DoLLocationTypes.feat,
                    ], []), # TODO: rules for this (gwylan/eden)

    DoLLocationNames.feat_purrfect: (426, [
                        DoLRegionNames.X,
                    ], [
                        DoLLocationTypes.feat,
                        DoLRules.animal_transformation_toggle,
                    ], []),

    DoLLocationNames.feat_howlatthemoon: (427, [
                        DoLRegionNames.X,
                    ], [
                        DoLLocationTypes.feat,
                        DoLRules.animal_transformation_toggle,
                    ], []),

    DoLLocationNames.feat_messwiththebull: (428, [
                        DoLRegionNames.X,
                    ], [
                        DoLLocationTypes.feat,
                        DoLRules.animal_transformation_toggle,
                    ], []),

    DoLLocationNames.feat_flylikeaneagle: (429, [
                        DoLRegionNames.X,
                    ], [
                        DoLLocationTypes.feat,
                        DoLRules.animal_transformation_toggle,
                    ], []),

    DoLLocationNames.feat_youslyfox: (430, [
                        DoLRegionNames.X,
                    ], [
                        DoLLocationTypes.feat,
                        DoLRules.animal_transformation_toggle,
                    ], []),

    DoLLocationNames.feat_walklikeanangel: (431, [
                        DoLRegionNames.X,
                    ], [
                        DoLLocationTypes.feat,
                        DoLRules.divine_transformation_toggle,
                        DoLRules.multipleruns_toggle,
                    ], []),

    DoLLocationNames.feat_fallingfallingfalling: (432, [
                        DoLRegionNames.X,
                    ], [
                        DoLLocationTypes.feat,
                        DoLRules.divine_transformation_toggle,
                        DoLRules.multipleruns_toggle,
                    ], []),

    DoLLocationNames.feat_devilishlooks: (433, [
                        DoLRegionNames.X,
                    ], [
                        DoLLocationTypes.feat,
                        DoLRules.divine_transformation_toggle,
                    ], []),

    DoLLocationNames.feat_headchef: (434, [
                        DoLRegionNames.X,
                    ], [
                        DoLLocationTypes.feat,
                    ], []),

    DoLLocationNames.feat_laughingstock: (435, [
                        DoLRegionNames.X,
                    ], [
                        DoLLocationTypes.feat,
                    ], [
                        DoLRules.access_pub,
                    ]),

    DoLLocationNames.feat_yourethelaughingstock: (436, [
                        DoLRegionNames.X,
                    ], [
                        DoLLocationTypes.feat,
                    ], []),

    DoLLocationNames.feat_illicitscience: (437, [
                        DoLRegionNames.X,
                    ], [
                        DoLLocationTypes.feat,
                    ], []), # TODO: rules for this

    DoLLocationNames.feat_mouthsealedshut: (438, [
                        DoLRegionNames.X,
                    ], [
                        DoLLocationTypes.feat,
                    ], []),

    DoLLocationNames.feat_neckdeep: (439, [
                        DoLRegionNames.X,
                    ], [
                        DoLLocationTypes.feat,
                    ], []),

    DoLLocationNames.feat_seedy: (440, [
                        DoLRegionNames.X,
                    ], [
                        DoLLocationTypes.feat,
                    ], []), # TODO: rules for this

    DoLLocationNames.feat_breedy: (441, [
                        DoLRegionNames.X,
                    ], [
                        DoLLocationTypes.feat,
                    ], []), # TODO: rules for this

    DoLLocationNames.feat_athunderousresponse: (442, [
                        DoLRegionNames.X,
                    ], [
                        DoLLocationTypes.feat,
                    ], [
                        DoLRules.exhibitionism_5,
                    ]),

    DoLLocationNames.feat_alewdadventure: (443, [
                        DoLRegionNames.X,
                    ], [
                        DoLLocationTypes.feat,
                    ], [
                        DoLRules.exhibitionism_5,
                    ]),

    DoLLocationNames.feat_sourdealing: (444, [
                        DoLRegionNames.X,
                    ], [
                        DoLLocationTypes.feat,
                    ], []),

    DoLLocationNames.feat_painrider: (445, [
                        DoLRegionNames.X,
                    ], [
                        DoLLocationTypes.feat,
                    ], [
                        DoLRules.antiques_10,
                        # TODO: willpower requirement
                    ]),

    DoLLocationNames.feat_submerged: (446, [
                        DoLRegionNames.X,
                    ], [
                        DoLLocationTypes.feat,
                    ], [
                        DoLRules.antiques_20,
                        # TODO: willpower requirement
                    ]),

    DoLLocationNames.feat_wrongsize: (447, [
                        DoLRegionNames.X,
                    ], [
                        DoLLocationTypes.feat,
                        DoLRules.multipleruns_toggle,
                    ], [
                        DoLRules.skulduggery_4,
                    ]),

    DoLLocationNames.feat_idlehands: (448, [
                        DoLRegionNames.X,
                    ], [
                        DoLLocationTypes.feat,
                    ], [
                        # skuldug requirement of f+
                    ]),

    DoLLocationNames.feat_stolentechnology: (449, [
                        DoLRegionNames.X,
                    ], [
                        DoLLocationTypes.feat,
                    ], [
                        DoLRules.access_landfill,
                    ]),

    DoLLocationNames.feat_spelunking: (450, [
                        DoLRegionNames.X,
                    ], [
                        DoLLocationTypes.feat,
                    ], []),

    DoLLocationNames.feat_xmarksthespot: (451, [
                        DoLRegionNames.X,
                    ], [
                        DoLLocationTypes.feat,
                    ], [
                        DoLRules.skulduggery_7,
                    ]),

    DoLLocationNames.feat_buriedtreasure: (452, [
                        DoLRegionNames.X,
                    ], [
                        DoLLocationTypes.feat,
                    ], []), 

    DoLLocationNames.feat_flurry: (453, [
                        DoLRegionNames.X,
                    ], [
                        DoLLocationTypes.feat,
                    ], []),

    DoLLocationNames.feat_afestivehome: (454, [
                        DoLRegionNames.X,
                    ], [
                        DoLLocationTypes.feat,
                    ], []),

    DoLLocationNames.feat_employeebenefits: (455, [
                        DoLRegionNames.X,
                    ], [
                        DoLLocationTypes.feat,
                    ], []),

    DoLLocationNames.feat_dealing: (456, [
                        DoLRegionNames.X,
                    ], [
                        DoLLocationTypes.feat,
                    ], []), # TODO: farm construction rules

    DoLLocationNames.feat_bentcopper: (457, [
                        DoLRegionNames.X,
                    ], [
                        DoLLocationTypes.feat,
                    ], [
                        DoLRules.skulduggery_4,
                    ]),

    DoLLocationNames.feat_socialcontract: (458, [
                        DoLRegionNames.X,
                    ], [
                        DoLLocationTypes.feat,
                    ], []),

    DoLLocationNames.feat_slipthroughthebackdoor: (459, [
                        DoLRegionNames.X,
                    ], [
                        DoLLocationTypes.feat,
                    ], [
                        DoLRules.access_orphanage,
                    ]),

    DoLLocationNames.feat_lifeoftheparty: (460, [
                        DoLRegionNames.X,
                    ], [
                        DoLLocationTypes.feat,
                    ], []),

    # TODO: dancing requirements for dance job
    DoLLocationNames.feat_belleoftheball: (461, [
                        DoLRegionNames.X,
                    ], [
                        DoLLocationTypes.feat,
                    ], [
                        DoLRules.exhibitionism_5
                    ]),

    DoLLocationNames.feat_breakingthestone: (462, [
                        DoLRegionNames.X,
                    ], [
                        DoLLocationTypes.feat,
                    ], [
                        DoLRules.skulduggery_10
                    ]),

    DoLLocationNames.feat_poundalpha: (463, [
                        DoLRegionNames.X,
                    ], [
                        DoLLocationTypes.feat,
                    ], []),

    DoLLocationNames.feat_poundrunt: (464, [
                        DoLRegionNames.X,
                    ], [
                        DoLLocationTypes.feat,
                    ], []),

    DoLLocationNames.feat_poundedpound: (465, [
                        DoLRegionNames.X,
                    ], [
                        DoLLocationTypes.feat,
                    ], []),

    DoLLocationNames.feat_poundliberator: (466, [
                        DoLRegionNames.X,
                    ], [
                        DoLLocationTypes.feat,
                    ], [
                        # TODO: tending requirement
                        DoLRules.skulduggery_2
                    ]),

    DoLLocationNames.feat_thevalueofpain: (467, [
                        DoLRegionNames.X,
                    ], [
                        DoLLocationTypes.feat,
                    ], []),

    # TODO: whatever this thing is
    DoLLocationNames.feat_bewitchingechoes: (468, [
                        DoLRegionNames.X,
                    ], [
                        DoLLocationTypes.feat,
                    ], []),

    DoLLocationNames.feat_bridgingthepast: (469, [
                        DoLRegionNames.X,
                    ], [
                        DoLLocationTypes.feat,
                    ], []), # Tentacle Forest Money Check

    DoLLocationNames.feat_safetrail: (470, [
                        DoLRegionNames.X,
                    ], [
                        DoLLocationTypes.feat,
                    ], []), # Tentacle Forest Money Check

    DoLLocationNames.feat_fieldwork: (471, [
                        DoLRegionNames.X,
                    ], [
                        DoLLocationTypes.feat,
                    ], []), # Tentacle Forest Money Check

    DoLLocationNames.feat_concretewoodland: (472, [
                        DoLRegionNames.X,
                    ], [
                        DoLLocationTypes.feat,
                    ], []), # Tentacle Forest Money Check

    DoLLocationNames.feat_schoolgreen: (473, [
                        DoLRegionNames.X,
                    ], [
                        DoLLocationTypes.feat,
                    ], []), # Tentacle Forest Money Check

    DoLLocationNames.feat_hookahmaster: (474, [
                        DoLRegionNames.X,
                    ], [
                        DoLLocationTypes.feat,
                    ], []), # Tentacle Forest Money Check

    DoLLocationNames.feat_sinsofthepast: (475, [
                        DoLRegionNames.X,
                    ], [
                        DoLLocationTypes.feat,
                    ], []),

    DoLLocationNames.feat_panicroom: (476, [
                        DoLRegionNames.X,
                    ], [
                        DoLLocationTypes.feat,
                    ], [
                        # TODO: flats min skul
                    ]),

    DoLLocationNames.feat_defythenight: (477, [
                        DoLRegionNames.X,
                    ], [
                        DoLLocationTypes.feat,
                    ], [
                        DoLRules.willpower_5,
                        DoLRules.science_4,
                    ]),

    DoLLocationNames.feat_witheringtruth: (478, [
                        DoLRegionNames.X,
                    ], [
                        DoLLocationTypes.feat,
                    ], [
                        # TODO: check min willpower
                    ]),

    # TODO: check if the dates have a min req to get here
    DoLLocationNames.feat_backroomdeals: (479, [
                        DoLRegionNames.X,
                    ], [
                        DoLLocationTypes.feat,
                    ], []),
    
    DoLLocationNames.feat_stompingdownthestreet: (480, [
                        DoLRegionNames.X,
                    ], [
                        DoLLocationTypes.feat,
                    ], [
                        DoLRules.access_photography,
                        # TODO: check if there's a min stat requirement
                    ]),

    DoLLocationNames.feat_hearmeroar: (481, [
                        DoLRegionNames.X,
                    ], [
                        DoLLocationTypes.feat,
                    ], [
                        DoLRules.access_photography,
                        # TODO: check if there's a min stat requirement
                    ]),

    DoLLocationNames.feat_maxthoseshots: (482, [
                        DoLRegionNames.X,
                    ], [
                        DoLLocationTypes.feat,
                        DoLRules.tentacles_toggle,
                    ], [
                        # TODO: location rules for pepper spray
                    ]),

    DoLLocationNames.feat_openedpandorasbox: (483, [
                        DoLRegionNames.X,
                    ], [
                        DoLLocationTypes.feat,
                    ], [
                        DoLRules.access_adultshop,
                    ]),

    DoLLocationNames.feat_openedpandorascocks: (484, [
                        DoLRegionNames.X,
                    ], [
                        DoLLocationTypes.feat,
                    ], []),

    DoLLocationNames.feat_brothelprovider: (485, [
                        DoLRegionNames.X,
                    ], [
                        DoLLocationTypes.feat,
                    ], [
                        DoLRules.access_brothel,
                        DoLRules.access_adultshop, # TODO: replace with finish adultshop
                    ]),

    DoLLocationNames.feat_playerofthematch: (486, [
                        DoLRegionNames.X,
                    ], [
                        DoLLocationTypes.feat,
                    ], [
                        # TODO: check min skul
                    ]),

    DoLLocationNames.feat_lockedingold: (487, [
                        DoLRegionNames.X,
                    ], [
                        DoLLocationTypes.feat,
                    ], [
                        DoLRules.access_forest,
                    ]),

    DoLLocationNames.feat_theendlessdeep: (488, [
                        DoLRegionNames.X,
                    ], [
                        DoLLocationTypes.feat,
                    ], [
                        # TODO: check min swimming
                    ]),

    DoLLocationNames.feat_wetandruined: (489, [
                        DoLRegionNames.X,
                    ], [
                        DoLLocationTypes.feat,
                    ], [
                        DoLRules.access_moor,
                    ]),

    DoLLocationNames.feat_terrorsequal: (490, [
                        DoLRegionNames.X,
                    ], [
                        DoLLocationTypes.feat,
                    ], []),

    DoLLocationNames.feat_birdsofafeather: (491, [
                        DoLRegionNames.X,
                    ], [
                        DoLLocationTypes.feat,
                    ], [
                        DoLRules.access_birdtower,
                        # TODO: harpy tf, flight
                    ]),

    DoLLocationNames.feat_runawaycattle: (492, [
                        DoLRegionNames.X,
                    ], [
                        DoLLocationTypes.feat,
                    ], [
                        DoLRules.access_remyfarm,
                    ]),

    DoLLocationNames.feat_equinerescue: (493, [
                        DoLRegionNames.X,
                    ], [
                        DoLLocationTypes.feat,
                        # does not require bestiality
                    ], [
                        DoLRules.access_remyfarm,
                    ]),

    # TODO: START FROM THIS LINE

    DoLLocationNames.feat_rearpassenger: (494, [
                        DoLRegionNames.X,
                    ], [
                        DoLLocationTypes.feat,
                    ], []), 

    DoLLocationNames.feat_corneredrogue: (495, [
                        DoLRegionNames.X,
                    ], [
                        DoLLocationTypes.feat,
                    ], []),

    DoLLocationNames.feat_farmprotector: (496, [
                        DoLRegionNames.X,
                    ], [
                        DoLLocationTypes.feat,
                    ], []),

    DoLLocationNames.feat_aknottoremember: (497, [
                        DoLRegionNames.X,
                    ], [
                        DoLLocationTypes.feat,
                    ], [
                        DoLRules.bestiality_toggle
                    ]),

    DoLLocationNames.feat_abnormalmollusc: (498, [
                        DoLRegionNames.X,
                    ], [
                        DoLLocationTypes.feat,
                    ], []),

    DoLLocationNames.feat_leverage: (499, [
                        DoLRegionNames.X,
                    ], [
                        DoLLocationTypes.feat,
                    ], []),

    DoLLocationNames.feat_undertheice: (500, [
                        DoLRegionNames.X,
                    ], [
                        DoLLocationTypes.feat,
                    ], []),

    DoLLocationNames.feat_inredlight: (501, [
                        DoLRegionNames.X,
                    ], [
                        DoLLocationTypes.feat,
                    ], []),

    DoLLocationNames.feat_ohbother: (502, [
                        DoLRegionNames.X,
                    ], [
                        DoLLocationTypes.feat,
                    ], []),

    DoLLocationNames.feat_notlikethemovies: (503, [
                        DoLRegionNames.X,
                    ], [
                        DoLLocationTypes.feat,
                    ], []),

    DoLLocationNames.feat_slippery: (504, [
                        DoLRegionNames.X,
                    ], [
                        DoLLocationTypes.feat,
                    ], []),

    DoLLocationNames.feat_highreflection: (505, [
                        DoLRegionNames.X,
                    ], [
                        DoLLocationTypes.feat,
                    ], []),

    DoLLocationNames.feat_schism: (506, [
                        DoLRegionNames.X,
                    ], [
                        DoLLocationTypes.feat,
                    ], []),

    DoLLocationNames.feat_catchthewind: (507, [
                        DoLRegionNames.X,
                    ], [
                        DoLLocationTypes.feat,
                    ], []),

    DoLLocationNames.feat_tradingdignity: (508, [
                        DoLRegionNames.X,
                    ], [
                        DoLLocationTypes.feat,
                    ], []),

    DoLLocationNames.feat_playingwithfire: (509, [
                        DoLRegionNames.X,
                    ], [
                        DoLLocationTypes.feat,
                    ], []),

    DoLLocationNames.feat_firestarter: (510, [
                        DoLRegionNames.X,
                    ], [
                        DoLLocationTypes.feat,
                    ], []),

    DoLLocationNames.feat_towatchthefields: (511, [
                        DoLRegionNames.X,
                    ], [
                        DoLLocationTypes.feat,
                    ], []),

    DoLLocationNames.feat_reliableemployer: (512, [
                        DoLRegionNames.X,
                    ], [
                        DoLLocationTypes.feat,
                    ], []),

    DoLLocationNames.feat_intothesunset: (513, [
                        DoLRegionNames.X,
                    ], [
                        DoLLocationTypes.feat,
                    ], []),

    DoLLocationNames.feat_institutionalised: (514, [
                        DoLRegionNames.X,
                    ], [
                        DoLLocationTypes.feat,
                    ], []),

    DoLLocationNames.feat_breaker: (515, [
                        DoLRegionNames.X,
                    ], [
                        DoLLocationTypes.feat,
                    ], []),

    DoLLocationNames.feat_timeandpressure: (516, [
                        DoLRegionNames.X,
                    ], [
                        DoLLocationTypes.feat,
                    ], []),

    DoLLocationNames.feat_morethananumber: (517, [
                        DoLRegionNames.X,
                    ], [
                        DoLLocationTypes.feat,
                    ], []),

    DoLLocationNames.feat_friendsinthesky: (518, [
                        DoLRegionNames.X,
                    ], [
                        DoLLocationTypes.feat,
                    ], []),

    DoLLocationNames.feat_notmeanttobecaged: (519, [
                        DoLRegionNames.X,
                    ], [
                        DoLLocationTypes.feat,
                    ], []),

    DoLLocationNames.feat_freebooze: (520, [
                        DoLRegionNames.X,
                    ], [
                        DoLLocationTypes.feat,
                    ], []),

    DoLLocationNames.feat_darkdelvings: (521, [
                        DoLRegionNames.X,
                    ], [
                        DoLLocationTypes.feat,
                    ], []),

    DoLLocationNames.feat_lurkerbeyond: (522, [
                        DoLRegionNames.X,
                    ], [
                        DoLLocationTypes.feat,
                    ], []),

    DoLLocationNames.feat_downbelow: (523, [
                        DoLRegionNames.X,
                    ], [
                        DoLLocationTypes.feat,
                    ], []),

    DoLLocationNames.feat_lostworld: (524, [
                        DoLRegionNames.X,
                    ], [
                        DoLLocationTypes.feat,
                    ], []),

    DoLLocationNames.feat_prehistoriclandscape: (525, [
                        DoLRegionNames.X,
                    ], [
                        DoLLocationTypes.feat,
                    ], []),

    DoLLocationNames.feat_faceofaguardian: (526, [
                        DoLRegionNames.X,
                    ], [
                        DoLLocationTypes.feat,
                    ], []),

    DoLLocationNames.feat_wildmonarch: (527, [
                        DoLRegionNames.X,
                    ], [
                        DoLLocationTypes.feat,
                    ], []),

    DoLLocationNames.feat_naturalised: (528, [
                        DoLRegionNames.X,
                    ], [
                        DoLLocationTypes.feat,
                    ], []),

    DoLLocationNames.feat_gildedspear: (529, [
                        DoLRegionNames.X,
                    ], [
                        DoLLocationTypes.feat,
                    ], []),

    DoLLocationNames.feat_lostheirloom: (530, [
                        DoLRegionNames.X,
                    ], [
                        DoLLocationTypes.feat,
                    ], []),

    DoLLocationNames.feat_50shadesoftan: (531, [
                        DoLRegionNames.X,
                    ], [
                        DoLLocationTypes.feat,
                    ], []),

    DoLLocationNames.feat_aspecialtrait: (532, [
                        DoLRegionNames.X,
                    ], [
                        DoLLocationTypes.feat,
                    ], []),

    DoLLocationNames.feat_aspecialtraitcollector: (533, [
                        DoLRegionNames.X,
                    ], [
                        DoLLocationTypes.feat,
                        # TODO: conditions for this
                    ], []),

    DoLLocationNames.feat_produceroflewdfluids: (534, [
                        DoLRegionNames.X,
                    ], [
                        DoLLocationTypes.feat,
                    ], []),

    DoLLocationNames.feat_literallybuckets: (535, [
                        DoLRegionNames.X,
                    ], [
                        DoLLocationTypes.feat,
                    ], []),

    DoLLocationNames.feat_feelingfull: (536, [
                        DoLRegionNames.X,
                    ], [
                        DoLLocationTypes.feat,
                    ], []),

    DoLLocationNames.feat_baileystroublemaker: (537, [
                        DoLRegionNames.X,
                    ], [
                        DoLLocationTypes.feat,
                    ], []),

    DoLLocationNames.feat_leightonsnightmare: (538, [
                        DoLRegionNames.X,
                    ], [
                        DoLLocationTypes.feat,
                    ], []),

    DoLLocationNames.feat_alexspartner: (539, [
                        DoLRegionNames.X,
                    ], [
                        DoLLocationTypes.feat,
                    ], []),

    DoLLocationNames.feat_harpersbane: (540, [
                        DoLRegionNames.X,
                    ], [
                        DoLLocationTypes.feat,
                    ], []),

    DoLLocationNames.feat_headofthepack: (541, [
                        DoLRegionNames.X,
                    ], [
                        DoLLocationTypes.feat,
                        DoLRules.bestiality_toggle,
                    ], []),

    DoLLocationNames.feat_topofthefoodchain: (542, [
                        DoLRegionNames.X,
                    ], [
                        DoLLocationTypes.feat,
                        DoLRules.bestiality_toggle,
                    ], []),

    DoLLocationNames.feat_prideofthefarm: (543, [
                        DoLRegionNames.X,
                    ], [
                        DoLLocationTypes.feat,
                        DoLRules.lactation_toggle,
                    ], []),

    DoLLocationNames.feat_dawntodusk: (544, [
                        DoLRegionNames.X,
                    ], [
                        DoLLocationTypes.feat,
                    ], []),

    DoLLocationNames.feat_earslimelover: (545, [
                        DoLRegionNames.X,
                    ], [
                        DoLLocationTypes.feat,
                        DoLRules.parasites_toggle,
                        DoLRules.parasiticpregnancy_toggle, # change if I ever change ppreg
                    ], []),

    DoLLocationNames.feat_earslimeamalgam: (546, [
                        DoLRegionNames.X,
                    ], [
                        DoLLocationTypes.feat,
                        DoLRules.parasites_toggle,
                        DoLRules.parasiticpregnancy_toggle, # change if I ever change ppreg
                    ], []),

    DoLLocationNames.feat_thepathtoredemption: (547, [
                        DoLRegionNames.X,
                    ], [
                        DoLLocationTypes.feat,
                        DoLRules.divine_transformation_toggle,
                    ], []),

    DoLLocationNames.feat_anewlife: (548, [
                        DoLRegionNames.X,
                    ], [
                        DoLLocationTypes.feat,
                        DoLRules.multipleruns_toggle,
                    ], []),

    # TODO: spa rules (or check how possible anywhere is)
    DoLLocationNames.feat_negotiator: (549, [
                        DoLRegionNames.X,
                    ], [
                        DoLLocationTypes.feat,
                    ], []),

    # TODO: gwlyan rules
    DoLLocationNames.feat_curiousattire: (550, [
                        DoLRegionNames.X,
                    ], [
                        DoLLocationTypes.feat,
                    ], []),

    # TODO: gwlyan rules
    DoLLocationNames.feat_wickedwardrobe: (551, [
                        DoLRegionNames.X,
                    ], [
                        DoLLocationTypes.feat,
                    ], []),

    DoLLocationNames.feat_mycollectionoffeats: (552, [
                        DoLRegionNames.X,
                    ], [
                        DoLLocationTypes.feat,
                        DoLRules.multipleruns_toggle,
                        # TODO: difficult feat
                    ], []),

    DoLLocationNames.feat_mytimelesscollectionoffeats: (553, [
                        DoLRegionNames.X,
                    ], [
                        DoLLocationTypes.feat,
                        DoLRules.multipleruns_toggle,
                        # TODO: difficult feat
                    ], []),

    DoLLocationNames.feat_broodmotherhost: (554, [
                        DoLRegionNames.X,
                    ], [
                        DoLLocationTypes.feat,
                        DoLRules.parasiticpregnancy_toggle,
                        DoLRules.tentacles_or_beastiality,
                    ], []),

    DoLLocationNames.feat_topbroodmotherhost: (555, [
                        DoLRegionNames.X,
                    ], [
                        DoLLocationTypes.feat,
                        DoLRules.parasiticpregnancy_toggle,
                        DoLRules.tentacles_or_beastiality,
                    ], []),

    DoLLocationNames.feat_broodmotherzoologist: (556, [
                        DoLRegionNames.X,
                    ], [
                        DoLLocationTypes.feat,
                        DoLRules.parasiticpregnancy_toggle,
                        DoLRules.tentacles_toggle,
                        DoLRules.bestiality_toggle,
                    ], []),

    DoLLocationNames.feat_miracleoflife: (557, [
                        DoLRegionNames.X,
                    ], [
                        DoLLocationTypes.feat,
                        DoLRules.pregnancy_toggle,
                        # TODO: mpreg rules
                    ], []),

    DoLLocationNames.feat_firstfatherhood: (558, [
                        DoLRegionNames.X,
                    ], [
                        DoLLocationTypes.feat,
                        DoLRules.pregnancy_toggle,
                    ], []),

    DoLLocationNames.feat_hailmary: (559, [
                        DoLRegionNames.X,
                    ], [
                        DoLLocationTypes.feat,
                        DoLRules.multipleruns_toggle,
                        # TODO: difficult rule
                    ], []),

    DoLLocationNames.feat_bicyclemother: (560, [
                        DoLRegionNames.X,
                    ], [
                        DoLLocationTypes.feat,
                        DoLRules.pregnancy_toggle,
                    ], []),

    DoLLocationNames.feat_lifecomesinthrees: (561, [
                        DoLRegionNames.X,
                    ], [
                        DoLLocationTypes.feat,
                        DoLRules.pregnancy_toggle,
                    ], []),

    DoLLocationNames.feat_lifebeginswhenyouleastexpect: (562, [
                        DoLRegionNames.X,
                    ], [
                        DoLLocationTypes.feat,
                        DoLRules.pregnancy_toggle,
                        DoLRules.multipleruns_toggle,
                    ], []),

    DoLLocationNames.feat_diversityoflife: (563, [
                        DoLRegionNames.X,
                    ], [
                        DoLLocationTypes.feat,
                        DoLRules.pregnancy_toggle,
                    ], []),
}
