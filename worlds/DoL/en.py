from dataclasses import dataclass
from enum import StrEnum, Enum

# HOW TO LOCALIZE
#
# You do NOT need to change the values inside """ """ (docstrings)
# You do NOT need to change anything after a # (comment)
#
# You do need to change every value between " " (quotes)
#
# You will also need to copy the .yaml template
# and create a translated copy


class DoLRegionNames(StrEnum):
    """
    The exact name of every Region
    """
    # -- Residential
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

    # -- Commercial
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

    # -- Industrial
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

    # -- Outside Town
    # Forest
    forest = "Forest"
    forest_shop = "Forest Shop"
    forest_lake = "Forest Lake"
    wolf_cave = "Black Wolf's Cave"
    eden_cabin = "Eden's Cabin"

    # Ocean
    ocean = "Ocean"

    # -- Outskirts
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
    remy_estate = "Remy's Estate"
    maze = "Maze"

    # Other Regions
    bog = "The Bog"
    tentacle_plains = "Tentacle Plains"
    old_sewers = "Old Sewers"

    # -- Soft Bad Ends
    prison = "Prison"
    island = "Island"
    underground_brothel = "Underground Brothel"
    asylum = "Asylum"
    dog_pound_ending = "Dog Pound Soft Bad End"
    mines = "The Mines"
    pirate_ship = "Pirate Ship"

    # -- Debug Regions
    jail = "Arrested"
    ambluance = "Ambluance"
    in_town = "Any Place in Town"
    in_global = "Any Place"
    events_street = "Street Event"


class DoLItemNames(StrEnum):
    """
    The exact name for every item
    
    ### Coding:
    Easiest to have the variable name identical 
    to the location name if they are 1:1
    """
    # -- Filler
    money_100 = "100 Pounds"

    # -- Antiques
    # Churchyard (forest)
    antique_ivorystatuette = "Antique: Ivory Statuette"
    antique_silvercoin     = "Antique: Silver Coin"
    antique_silvercrown    = "Antique: Silver Crown"
    antique_crystal        = "Antique: Crystal"
    antique_silverblade    = "Antique: Silver Blade"
    antique_coppercoin     = "Antique: Copper Coin"
    antique_silvergoblet   = "Antique: Silver Goblet"
    antique_fetish         = "Antique: Fetish"
    antique_goldcoin       = "Antique: Gold Coin"

    # Forest
    antique_forestdagger = "Antique: Dagger"
    antique_forestgem    = "Antique: Forest Gem"
    antique_arrow        = "Antique: Arrow"

    # Forest Lake
    antique_ivorynecklace = "Antique: Ivory Necklace"
    antique_ivorybox      = "Antique: Ivory Box"
    antique_silverring    = "Antique: Silver Ring"
    antique_goldnecklace  = "Antique: Gold Necklace"
    antique_chastitybelt  = "Antique: Chastity Belt"

    # Meadow
    antique_stonetalisman = "Antique: Stone Talisman"

    # Maze
    antique_horn            = "Antique: Horn"
    antique_snuffer         = "Antique: Snuffer"
    antique_bucket          = "Antique: Bucket"
    antique_silvermanacle   = "Antique: Silver Manacle"
    antique_whip            = "Antique: Whip"
    antique_serpentpainting = "Antique: Serpent Painting"

    # Moor
    antique_goldring       = "Antique: Gold Ring"
    antique_bell           = "Antique: Bell"
    antique_bullet         = "Antique: Bullet"
    antique_artilleryshell = "Antique: Artillery Shell"

    # Riding School
    antique_grenade = "Antique: Grenade"

    # Dance School
    antique_goldbrooch = "Antique: Gold Brooch"

    # Orphanage
    antique_silverbrooch = "Antique: Silver Brooch"

    # Island
    antique_islanderarrow   = "Antique: Islander Arrow"
    antique_islandermask    = "Antique: Islander Mask"
    antique_obsidiandisc    = "Antique: Obsidian Disc"
    antique_trilobitefossil = "Antique: Trilobite Fossil"

    # Landfill
    antique_baileyminesign = "Antique: Bailey Mine Sign"
    antique_incenseburner  = "Antique: Incense Burner"
    antique_cup            = "Antique: Cup"

    # Museum
    antique_silvermask = "Antique: Silver Mask"

    # Bird Tower
    # antique_bullet = "" also found in moor

    # Manors
    antique_silveramulet = "Antique: Silver Amulet"

    # Compound
    antique_hourglass = "Antique: Hourglass"

    # Pirate Ship
    antique_swordcane      = "Antique: Sword Cane"
    antique_chocolate      = "Antique: Chocolate"
    antique_teacaddy       = "Antique: Tea Caddy"
    antique_woodenfigurine = "Antique: Wooden Figurine"
    antique_copperring     = "Antique: Copper Ring"
    antique_goldcompass    = "Antique: Gold Compass"

    # Ocean
    antique_coppercompass = "Antique: Copper Compass"
    antique_coralring     = "Antique: Coral Ring"
    antique_diamond       = "Antique: Diamond"

    # Temple
    antique_brassstatuette = "Antique: Brass Statuette"

    # Avery Mansion
    antique_golddagger = "Antique: Gold Dagger"
    antique_goldamulet = "Antique: Gold Amulet"
    antique_goldmask   = "Antique: Gold Mask"

    # Beach Cave
    antique_silvercompass = "Antique: Silver Compass"
    antique_leathermap    = "Antique: Leather Map"
    antique_cutlass       = "Antique: Cutlass"
    antique_silverdagger  = "Antique: Silver Dagger"
    antique_rustedcutlass = "Antique: Rusted Cutlass"

    # Sewers
    antique_pinkcrystal = "Antique: Pink Crystal"
    antique_candlestick = "Antique: Candlestick"
    antique_dildo       = "Antique: Dildo"
    # antique_horn = "" also found in maze
    antique_watch = "Antique: Watch"


    # -- Skills
    progressive_skulduggery_rank   = "Progressive Skulduggery Rank"
    progressive_dancing_rank       = "Progressive Dancing Rank"
    progressive_swimming_rank      = "Progressive Swimming Rank"
    progressive_athletics_rank     = "Progressive Athletics Rank"
    progressive_tending_rank       = "Progressive Tending Rank"
    progressive_housekeeping_rank  = "Progressive Housekeeping Rank"
    progressive_seduction_rank     = "Progressive Seduction Rank"
    progressive_oral_rank          = "Progressive Oral Rank"
    progressive_chest_rank         = "Progressive Chest Rank"
    progressive_hands_rank         = "Progressive Hands Rank"
    progressive_buttocks_rank      = "Progressive Buttocks Rank"
    progressive_privates_rank      = "Progressive Privates Rank"
    progressive_anal_rank          = "Progressive Anal Rank"
    progressive_thighs_rank        = "Progressive Thighs Rank"
    progressive_feet_rank          = "Progressive Feet Rank"
    progressive_science_rank       = "Progressive Science Rank"
    progressive_math_rank          = "Progressive Math Rank"
    progressive_english_rank       = "Progressive English Rank"
    progressive_history_rank       = "Progressive History Rank"
    progressive_willpower_rank     = "Progressive Willpower Rank"
    progressive_physique_rank      = "Progressive Physique Rank"
    progressive_promiscuity_rank   = "Progressive Promiscuity Rank"
    progressive_exhibitionism_rank = "Progressive Exhibitionism Rank"
    progressive_deviancy_rank      = "Progressive Deviancy Rank"


    # -- Upgrades
    upgrade_flatsbridge        = "Flats Bridge"                   # ascend
    upgrade_forestroad         = "Forest Road"                    # ascend
    upgrade_fieldoffice        = "Winter's Field Office"          # ascend
    upgrade_residentialthicket = "Residential Alleyways Thicket"  # decend
    upgrade_schoolgreen        = "School Green"                   # decend
    upgrade_hookahparlour      = "Hookah Parlour Ownership"
    
    upgrade_adultshop          = "Built Adult Shop"
    upgrade_cafe               = "Cafe Re-Opened"

    # TODO: CODE make farm upgrades instant
    upgrade_farm_wall          = "Farm: Progressive Wall" # 4
    upgrade_farm_security      = "Farm: Progressive Security" # 2
    upgrade_farm_kennel        = "Farm: Kennel"
    upgrade_farm_woodland      = "Farm: Progressive Woodlands" # 3
    upgrade_farm_barn          = "Farm: Progressive Barn" # 2
    upgrade_farm_coop          = "Farm: Progressive Coop" # 2
    upgrade_farm_irrigation    = "Farm: Irrigation"
    upgrade_farm_stable        = "Farm: Stable"
    upgrade_farm_parasite      = "Farm: Progressive Parasite Barn" # 2
    upgrade_farm_greenhouse    = "Farm: Greenhouse"

    upgrade_loft_pepperspraylab = "Loft: Pepper Spray Lab" # kylar
    upgrade_loft_kitchen = "Loft: Secret Kitchen" # river
    upgrade_loft_window = "Loft: Bay Window" # great hawk
    upgrade_loft_nook = "Loft: Reading Nook" # doren
    upgrade_loft_coffee = "Loft: Coffee Pot" # sam
    upgrade_loft_whitney = "Loft: An Apparatus" # whitney



    # -- Transformations - Locations done via Feats

    # Example:
    # Example TF Full (only be added to pool if transformation full selected)
    # Example TF Appearance (special trait + appearance selection)
    # Example TF Trait (species specific trait)
    # Example TF Shared Trait (trait shared with another, add to shared category)

    # Wolf:
    transformation_wolffull   = "Wolf TF: Full"
    transformation_wolfappear = "Wolf TF: Appearance"
    # Fangs (tf shared trait)

    # Cat:
    transformation_catfull       = "Cat TF: Full"
    transformation_catappear     = "Cat TF: Appearance"
    transformation_heterochromia = "TF Trait: Heterochromia"  # effectively filler
    # Fangs (tf shared trait)
    # Sharp Eyes (tf shared trait)

    # Cow:
    transformation_cowfull    = "Cow TF: Full"
    transformation_cowappear  = "Cow TF: Appearance"
    transformation_sturyhorns = "TF Trait: Sturdy Horns"

    # Harpy:
    transformation_harpyfull   = "Harpy TF: Full"
    transformation_harpyappear = "Harpy TF: Appearance"
    transformation_strongwings = "TF Trait: Strong Wings"
    # Sharp Eyes (tf shared trait)
    # Mate For Life (tf shared trait)
    # Wings (tf shared trait)

    # Fox:
    transformation_foxfull          = "Fox TF: Full"
    transformation_foxappear        = "Fox TF: Appearance"
    transformation_thrillofthechase = "TF Trait: Thrill of the Chase"
    # Fangs (tf shared trait)
    # Sharp Eyes (tf shared trait)
    # Mate For Life (tf shared trait)

    # Angel:
    transformation_angelfull   = "Angel TF: Full"
    transformation_angelappear = "Angel TF: Appearance"
    transformation_radiant     = "TF Trait: Radiant"
    # Wings (tf shared trait)

    # Fallen Angel:
    transformation_fallenangelfull   = "Fallen Angel TF: Full"
    transformation_fallenangelappear = "Fallen Angel TF: Appearance"
    # Wings (tf shared trait)

    # Demon:
    transformation_demonfull   = "Demon TF: Full"
    transformation_demonappear = "Demon TF: Appearance"
    transformation_darkhorns   = "TF Trait: Dark Horns"
    # Wings (tf shared trait)

    # Transformation Shared Traits
    transformation_fangs       = "TF Trait: Fangs"          # (wolf, cat, fox)
    transformation_sharpeyes   = "TF Trait: Sharp Eyes"     # (cat, harpy, fox)
    transformation_wings       = "TF Trait: Wings"          # (harpy, angel, fallen angel, demon)
    transformation_mateforlife = "TF Trait: Mate for Life"  # (harpy, fox)

    # Basic Traits Combined:
    # transformation_heterochromia
    # transformation_sturyhorns
    # transformation_strongwings
    # transformation_thrillofthechase
    # transformation_radiant
    # transformation_darkhorns

    # Other:
    # NOTE: normally flight is restricted to having harpy TF
    # but I wish to extend it to having wings
    # TODO: CODE flight ^
    transformation_flight = "TF Upgrade: Flight"


    # -- Access Items
    accessitem_adoptionpapers = "Access Item: Avery's Adoption Papers"
    accessitem_fakeid         = "Access Item: Fake ID"
    accessitem_mazekey        = "Access Item: Maze Key"

    # when adding a new item make sure to give it a class and id in items.py
    # also if it belongs to a group, add it to item_groups in world.py
    # then add it to nonlocation items in the very bottom


class DoLLocationTypes(StrEnum):
    """
    The Type for a Location or Item
    
    ### Coding:
    Used for item_groups grouping
    """
    antique = "Antique Item",
    skill = "Skill Rank",

    transformation = "Transformation Item"
    transformation_divine = "Divine Transformation Item"
    transformation_animal = "Animal Transformation Item"

    feat = "Feat",
    feat_copper = "Copper Feat",
    feat_silver = "Silver Feat",
    feat_gold = "Gold Feat",
    feat_platinum = "Platinum Feat",
    feat_jeweled = "Jeweled Feat"
    feat_transformation = "Transformation Feat"
    feat_loveinterest = "Love Interest Feat"

    upgrade = "Area Upgrade"
    upgrade_alex = "Alex's Farm Upgrade"
    upgrade_tentacleforest = "Tentacle Forest/Mayor Upgrade"
    upgrade_town = "General Town Upgrade"


class DoLLocationNames(StrEnum):
    """
    List of locations for checks

    ### Coding:
    MUST keep these variable names the same as 
    locations varaible names

    antique_ = ``Antique 'Antique Name' : 'Location'``\n
    skill_ = ``'Skill' Rank 'X'``\n
    feat_ = ``'Feat' Feat``\n
    upgrade_ = ``'Type': 'Name'``\n
    """

    # -- Antiques
    # Churchyard Catacombs
    antique_ivorystatuette = f"{DoLItemNames.antique_ivorystatuette.value} : Churchyard"
    antique_silvercoin = f"{DoLItemNames.antique_silvercoin.value} : Churchyard"
    antique_silvercrown = f"{DoLItemNames.antique_silvercrown.value} : Churchyard"
    antique_crystal = f"{DoLItemNames.antique_crystal.value} : Churchyard"
    antique_silverblade = f"{DoLItemNames.antique_silverblade.value} : Churchyard"
    antique_coppercoin = f"{DoLItemNames.antique_coppercoin.value} : Churchyard"
    antique_silvergoblet = f"{DoLItemNames.antique_silvergoblet.value} : Churchyard"
    antique_fetish = f"{DoLItemNames.antique_fetish.value} : Churchyard"
    antique_goldcoin = f"{DoLItemNames.antique_goldcoin.value} : Churchyard"

    # Forest
    antique_forestdagger = f"{DoLItemNames.antique_forestdagger.value} : Forest"
    antique_forestgem = f"{DoLItemNames.antique_forestgem.value} : Forest"
    antique_arrow = f"{DoLItemNames.antique_arrow.value} : Forest"

    # Lake
    antique_ivorynecklace = f"{DoLItemNames.antique_ivorynecklace.value} : Lake"
    antique_ivorybox = f"{DoLItemNames.antique_ivorybox.value} : Lake"
    antique_silverring = f"{DoLItemNames.antique_silverring.value} : Lake"
    antique_goldnecklace = f"{DoLItemNames.antique_goldnecklace.value} : Lake"
    antique_chastitybelt = f"{DoLItemNames.antique_chastitybelt.value} : Lake"

    # Meadow
    antique_stonetalisman = f"{DoLItemNames.antique_stonetalisman.value} : Meadow"

    # Maze
    antique_horn = f"{DoLItemNames.antique_horn.value} : Maze or Sewers"
    antique_snuffer = f"{DoLItemNames.antique_snuffer.value} : Maze"
    antique_bucket = f"{DoLItemNames.antique_bucket.value} : Maze"
    antique_silvermanacle = f"{DoLItemNames.antique_silvermanacle.value} : Maze"
    antique_whip = f"{DoLItemNames.antique_whip.value} : Maze"
    antique_serpentpainting = f"{DoLItemNames.antique_serpentpainting.value} : Maze"

    # Moor
    antique_goldring = f"{DoLItemNames.antique_goldring.value} : Moor"
    antique_bell = f"{DoLItemNames.antique_bell.value} : Moor"
    antique_bullet = f"{DoLItemNames.antique_bullet.value} : Moor or Great Hawk"
    antique_artilleryshell = f"{DoLItemNames.antique_artilleryshell.value} : Moor"

    # Riding School
    antique_grenade = f"{DoLItemNames.antique_grenade.value} : Riding School"

    # Dance School
    antique_goldbrooch = f"{DoLItemNames.antique_goldbrooch.value} : Dance School"

    # Orphanage
    antique_silverbrooch = f"{DoLItemNames.antique_silverbrooch.value} : Orphange"

    # Island
    antique_islanderarrow = f"{DoLItemNames.antique_islanderarrow.value} : Island"
    antique_islandermask = f"{DoLItemNames.antique_islandermask.value} : Island"
    antique_obsidiandisc = f"{DoLItemNames.antique_obsidiandisc.value} : Island"
    antique_trilobitefossil = f"{DoLItemNames.antique_trilobitefossil.value} : Island"

    # Landfill
    antique_baileyminesign = f"{DoLItemNames.antique_baileyminesign.value} : Landfill"
    antique_incenseburner = f"{DoLItemNames.antique_incenseburner.value} : Landfill"
    antique_cup = f"{DoLItemNames.antique_cup.value} : Landfill"

    # Museum
    antique_silvermask = f"{DoLItemNames.antique_silvermask.value} : Museum"

    # Bird Tower
    # antique_bullet = also found in moor

    # Manors
    antique_silveramulet = f"{DoLItemNames.antique_silveramulet.value} : Manors"

    # Compound
    antique_hourglass = f"{DoLItemNames.antique_hourglass.value} : Compound"

    # Pirate Ship
    antique_swordcane = f"{DoLItemNames.antique_swordcane.value} : Pirate Ship"
    antique_chocolate = f"{DoLItemNames.antique_chocolate.value} : Pirate Ship"
    antique_teacaddy = f"{DoLItemNames.antique_teacaddy.value} : Pirate Ship"
    antique_woodenfigurine = f"{DoLItemNames.antique_woodenfigurine.value} : Pirate Ship"
    antique_copperring = f"{DoLItemNames.antique_copperring.value} : Pirate Ship"
    antique_goldcompass = f"{DoLItemNames.antique_goldcompass.value} : Pirate Ship"

    # Ocean
    antique_coppercompass = f"{DoLItemNames.antique_coppercompass.value} : Ocean"
    antique_coralring = f"{DoLItemNames.antique_coralring.value} : Ocean"
    antique_diamond = f"{DoLItemNames.antique_diamond.value} : Ocean"

    # Temple
    antique_brassstatuette = f"{DoLItemNames.antique_brassstatuette.value} : Temple"

    # Avery Mansion
    antique_golddagger = f"{DoLItemNames.antique_golddagger.value} : Avery's Mansion"
    antique_goldamulet = f"{DoLItemNames.antique_goldamulet.value} : Avery's Mansion"
    antique_goldmask = f"{DoLItemNames.antique_goldmask.value} : Avery's Mansion"

    # Beach Cave
    antique_silvercompass = f"{DoLItemNames.antique_silvercompass.value} : Beach Cave"
    antique_leathermap = f"{DoLItemNames.antique_leathermap.value} : Beach Cave"
    antique_cutlass = f"{DoLItemNames.antique_cutlass.value} : Beach Cave"
    antique_silverdagger = f"{DoLItemNames.antique_silverdagger.value} : Beach Cave"
    antique_rustedcutlass = f"{DoLItemNames.antique_rustedcutlass.value} : Beach Cave"

    # Sewers
    antique_pinkcrystal = f"{DoLItemNames.antique_pinkcrystal.value} : Sewers"
    antique_candlestick = f"{DoLItemNames.antique_candlestick.value} : Sewers"
    antique_dildo = f"{DoLItemNames.antique_dildo.value} : Sewers"
    # antique_horn = also found in maze
    antique_watch = f"{DoLItemNames.antique_watch.value} : Sewers"


    # -- Skill Levels
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

    # despite being 6 ranks of text,
    # these skills are divided into 7 segments (0 - 6)
    # ingame, meaning to reach max rank would be an 8th segment
    # NOTE: willpower and phyisque are divded into 7 segments
    # while the others are not, just requires 95% or above
    # meaning willpower 1-6 will be 142, 285, 428, 571, 875, 1000
    # the others are above 95%, so last rank will just be a 5% increase
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


    # -- Feats
    feat_pocketchange                 = "Feat: Pocket Change"
    feat_moneymaker                   = "Feat: Money Maker"
    feat_tycoon                       = "Feat: Tycoon"
    feat_millionaire                  = "Feat: Millionaire"
    feat_itbelongsinamuseum           = "Feat: It Belongs in a Museum"
    feat_fullycovered                 = "Feat: Fully Covered"
    feat_beingaboy                    = "Feat: Being a Boy"
    feat_beingagirl                   = "Feat: Being a Girl"
    feat_beingahermaphrodite          = "Feat: Being a Hermaphrodite"
    feat_beinganorphan                = "Feat: Being an Orphan"
    feat_stressfulchallenge           = "Feat: Stressful Challenge"
    feat_longstressfulchallenge       = "Feat: Long Stressful Challenge"
    feat_billboard                    = "Feat: Billboard"
    feat_alivingcanvas                = "Feat: A Living Canvas"
    feat_farmhand                     = "Feat: Farmhand"
    feat_farmer                       = "Feat: Farmer"
    feat_cultivator                   = "Feat: Cultivator"
    feat_therivalfarm                 = "Feat: The Rival Farm"
    feat_therivalestate               = "Feat: The Rival Estate"
    feat_heroicvictory                = "Feat: Heroic Victory"
    feat_fiveinarow                   = "Feat: Five in a Row"
    feat_distinction                  = "Feat: Distinction"
    feat_distinctive                  = "Feat: Distinctive"
    feat_distinguished                = "Feat: Distinguished"
    feat_chefdetournant               = "Feat: Chef de Tournant"
    feat_chefdepartie                 = "Feat: Chef de Partie"
    feat_souschef                     = "Feat: Sous Chef"
    feat_sciencefairwinner            = "Feat: Science Fair Winner"
    feat_thesisoffence                = "Feat: Thesis Offence"
    feat_mathscompetitionwinner       = "Feat: Maths Competition Winner"
    feat_richhearts                   = "Feat: Rich Hearts"
    feat_mostaware                    = "Feat: Most Aware"
    feat_mostinnocent                 = "Feat: Most Innocent"
    feat_nomorecontrol                = "Feat: No More Control"
    feat_thief                        = "Feat: Thief"
    feat_mayihavethisdance            = "Feat: May I Have This Dance?"
    feat_aquanaut                     = "Feat: Aquanaut"
    feat_seductress                   = "Feat: Seductress"
    feat_greenfingered                = "Feat: Green Fingered"
    feat_majordomo                    = "Feat: Majordomo"
    feat_swift                        = "Feat: Swift"
    feat_alluring                     = "Feat: Alluring"
    feat_sexspecialist                = "Feat: Sex Specialist"
    feat_perfectrecord                = "Feat: Perfect Record"
    feat_perfectsub                   = "Feat: Perfect Sub"
    feat_defyingtheodds               = "Feat: Defying the Odds"
    feat_hawker                       = "Feat: Hawker"
    feat_vendor                       = "Feat: Vendor"
    feat_merchant                     = "Feat: Merchant"
    feat_twisteddesire                = "Feat: Twisted Desire"
    feat_servedhot                    = "Feat: Served Hot"
    feat_sadomasochist                = "Feat: Sadomasochist"
    feat_shiningreputation            = "Feat: Shining Reputation"
    feat_socialbutterfly              = "Feat: Social Butterfly"
    feat_unsocialmoth                 = "Feat: Unsocial Moth"
    feat_teacherspet                  = "Feat: Teacher's Pet"
    feat_teachersnightmare            = "Feat: Teacher's Nightmare"
    feat_robinthelover                = "Feat: Robin the Lover"
    feat_hungryorphan                 = "Feat: Hungry Orphan"
    feat_robinssong                   = "Feat: Robin's Song"
    feat_whitneythebully              = "Feat: Whitney the Bully"
    feat_thebullystithe               = "Feat: The Bully's Tithe"
    feat_delinquentantics             = "Feat: Delinquent Antics"
    feat_giddyup                      = "Feat: Giddy Up"
    feat_whitneyssecret               = "Feat: Whitney's Secret"
    feat_kylartheobsessed             = "Feat: Kylar the Obsessed"
    feat_notforrats                   = "Feat: Not for Rats"
    feat_edenthelonely                = "Feat: Eden the Lonely"
    feat_sweetandtender               = "Feat: Sweet and Tender"
    feat_averythemoneybags            = "Feat: Avery the Moneybags"
    feat_kept                         = "Feat: Kept"
    feat_whatgoesaround               = "Feat: What Goes Around"
    feat_mostexclusive                = "Feat: Most Exclusive"
    feat_pridecometh                  = "Feat: Pride Cometh"
    feat_hautecuisine                 = "Feat: Haute Cuisine"
    feat_leightontheshady             = "Feat: Leighton the Shady"
    feat_alextherobust                = "Feat: Alex the Robust"
    feat_homecooking                  = "Feat: Home Cooking"
    feat_greathawktheterror           = "Feat: Great Hawk the Terror"
    feat_returnthefavour              = "Feat: Return the Favour"
    feat_feathertrick                 = "Feat: Feather Trick"
    feat_wrenthesly                   = "Feat: Wren the Sly"
    feat_blackwolfthealpha            = "Feat: Black Wolf the Alpha"
    feat_encroachingcivilisation      = "Feat: Encroaching Civilisation"
    feat_sydneythepurehearted         = "Feat: Sydney the Pure-Hearted"
    feat_communion                    = "Feat: Communion"
    feat_harperthehypnotist           = "Feat: Harper the Hypnotist"
    feat_morganthelost                = "Feat: Morgan the Lost"
    feat_gwylanthebewitching          = "Feat: Gwylan the Bewitching"
    feat_covencomforts                = "Feat: Coven Comforts"
    feat_lovetriangles                = "Feat: Love Triangles"
    feat_lovetrapezoids               = "Feat: Love Trapezoids"
    feat_bemyvalentine                = "Feat: Be My Valentine"
    feat_ballroomshowoff              = "Feat: Ballroom Show-off"
    feat_underthetable                = "Feat: Under the Table"
    feat_pubcrawlvictors              = "Feat: Pub Crawl Victors"
    feat_masonssecret                 = "Feat: Mason's Secret"
    feat_masonsshame                  = "Feat: Mason's Shame"
    feat_animaltender                 = "Feat: Animal Tender"
    feat_ispy                         = "Feat: I Spy"
    feat_firstkiss                    = "Feat: First Kiss"
    feat_acrimemostfoul               = "Feat: A Crime Most Foul"
    feat_longing                      = "Feat: Longing"
    feat_paganrite                    = "Feat: Pagan Rite"
    feat_warmestwinter                = "Feat: Warmest Winter"
    feat_trialsoffaith                = "Feat: Trials of Faith"
    feat_firstverse                   = "Feat: First Verse"
    feat_wildsong                     = "Feat: Wildsong"
    feat_foxbane                      = "Feat: Foxbane"
    feat_purrfect                     = "Feat: Purrfect"
    feat_howlatthemoon                = "Feat: Howl at the Moon"
    feat_messwiththebull              = "Feat: Mess With the Bull..."
    feat_flylikeaneagle               = "Feat: Fly Like an Eagle"
    feat_youslyfox                    = "Feat: You Sly Fox"
    feat_walklikeanangel              = "Feat: Walk Like an Angel"
    feat_fallingfallingfalling        = "Feat: Falling, Falling, Falling..."
    feat_devilishlooks                = "Feat: Devilish Looks"
    feat_headchef                     = "Feat: Head Chef"
    feat_laughingstock                = "Feat: Laughingstock"
    feat_yourethelaughingstock        = "Feat: You're the Laughingstock"
    feat_illicitscience               = "Feat: Illicit Science"
    feat_mouthsealedshut              = "Feat: Mouth Sealed Shut"
    feat_neckdeep                     = "Feat: Neck Deep"
    feat_seedy                        = "Feat: Seedy"
    feat_breedy                       = "Feat: Breedy"
    feat_athunderousresponse          = "Feat: A Thunderous Response"
    feat_alewdadventure               = "Feat: A Lewd Adventure"
    feat_sourdealing                  = "Feat: Sour Dealing"
    feat_painrider                    = "Feat: Pain Rider"
    feat_submerged                    = "Feat: Submerged"
    feat_wrongsize                    = "Feat: Wrong Size"
    feat_idlehands                    = "Feat: Idle Hands"
    feat_stolentechnology             = "Feat: Stolen Technology"
    feat_spelunking                   = "Feat: Spelunking"
    feat_xmarksthespot                = "Feat: X Marks the Spot"
    feat_buriedtreasure               = "Feat: Buried Treasure"
    feat_flurry                       = "Feat: Flurry"
    feat_afestivehome                 = "Feat: A Festive Home"
    feat_employeebenefits             = "Feat: Employee Benefits"
    feat_dealing                      = "Feat: Dealing"
    feat_bentcopper                   = "Feat: Bent Copper"
    feat_socialcontract               = "Feat: Social Contract"
    feat_slipthroughthebackdoor       = "Feat: Slip Through the Backdoor"
    feat_lifeoftheparty               = "Feat: Life of the Party"
    feat_belleoftheball               = "Feat: Belle of the Ball"
    feat_breakingthestone             = "Feat: Breaking the Stone"
    feat_poundalpha                   = "Feat: Pound Alpha"
    feat_poundrunt                    = "Feat: Pound Runt"
    feat_poundedpound                 = "Feat: Pounded Pound"
    feat_poundliberator               = "Feat: Pound Liberator"
    feat_thevalueofpain               = "Feat: The Value of Pain"
    feat_bewitchingechoes             = "Feat: Bewitching Echoes"
    feat_bridgingthepast              = "Feat: Bridging the Past"
    feat_safetrail                    = "Feat: Safe Trail"
    feat_fieldwork                    = "Feat: Field Work"
    feat_concretewoodland             = "Feat: Concrete Woodland"
    feat_schoolgreen                  = "Feat: School Green"
    feat_hookahmaster                 = "Feat: Hookah Master"
    feat_sinsofthepast                = "Feat: Sins of the Past"
    feat_panicroom                    = "Feat: Panic Room"
    feat_defythenight                 = "Feat: Defy the Night"
    feat_witheringtruth               = "Feat: Withering Truth"
    feat_backroomdeals                = "Feat: Backroom Deals"
    feat_stompingdownthestreet        = "Feat: Stomping Down The Street"
    feat_hearmeroar                   = "Feat: Hear Me Roar"
    feat_maxthoseshots                = "Feat: Max Those Shots"
    feat_openedpandorasbox            = "Feat: Opened Pandora's Box"
    feat_openedpandorascocks          = "Feat: Opened Pandora's Cocks"
    feat_brothelprovider              = "Feat: Brothel Provider"
    feat_playerofthematch             = "Feat: Player of the Match"
    feat_lockedingold                 = "Feat: Locked in Gold"
    feat_theendlessdeep               = "Feat: The Endless Deep"
    feat_wetandruined                 = "Feat: Wet and Ruined"
    feat_terrorsequal                 = "Feat: Terror's Equal"
    feat_birdsofafeather              = "Feat: Birds of a Feather..."
    feat_runawaycattle                = "Feat: Runaway Cattle"
    feat_equinerescue                 = "Feat: Equine Rescue"
    feat_rearpassenger                = "Feat: Rear Passenger"
    feat_corneredrogue                = "Feat: Cornered Rogue"
    feat_farmprotector                = "Feat: Farm Protector"
    feat_aknottoremember              = "Feat: A Knot to Remember"
    feat_abnormalmollusc              = "Feat: Abnormal Mollusc"
    feat_leverage                     = "Feat: Leverage"
    feat_undertheice                  = "Feat: Under the Ice"
    feat_inredlight                   = "Feat: In Red Light"
    feat_ohbother                     = "Feat: Oh Bother"
    feat_notlikethemovies             = "Feat: Not Like the Movies"
    feat_slippery                     = "Feat: Slippery"
    feat_highreflection               = "Feat: High Reflection"
    feat_schism                       = "Feat: Schism"
    feat_catchthewind                 = "Feat: Catch The Wind"
    feat_tradingdignity               = "Feat: Trading Dignity"
    feat_playingwithfire              = "Feat: Playing with Fire"
    feat_firestarter                  = "Feat: Firestarter"
    feat_towatchthefields             = "Feat: To Watch the Fields"
    feat_reliableemployer             = "Feat: Reliable Employer"
    feat_intothesunset                = "Feat: Into the Sunset"
    feat_institutionalised            = "Feat: Institutionalised"
    feat_breaker                      = "Feat: Breaker"
    feat_timeandpressure              = "Feat: Time and Pressure"
    feat_morethananumber              = "Feat: More than a Number"
    feat_friendsinthesky              = "Feat: Friends in the Sky"
    feat_notmeanttobecaged            = "Feat: Not Meant to be Caged"
    feat_freebooze                    = "Feat: Free Booze"
    feat_darkdelvings                 = "Feat: Dark Delvings"
    feat_lurkerbeyond                 = "Feat: Lurker Beyond"
    feat_downbelow                    = "Feat: Down Below"
    feat_lostworld                    = "Feat: Lost World"
    feat_prehistoriclandscape         = "Feat: Prehistoric Landscape"
    feat_faceofaguardian              = "Feat: Face of a Guardian"
    feat_wildmonarch                  = "Feat: Wild Monarch"
    feat_naturalised                  = "Feat: Naturalised"
    feat_gildedspear                  = "Feat: Gilded Spear"
    feat_lostheirloom                 = "Feat: Lost Heirloom"
    feat_50shadesoftan                = "Feat: 50 Shades of Tan"
    feat_aspecialtrait                = "Feat: A Special Trait"
    feat_aspecialtraitcollector       = "Feat: A Special Trait Collector"
    feat_produceroflewdfluids         = "Feat: Producer of Lewd Fluids"
    feat_literallybuckets             = "Feat: Literally Buckets"
    feat_feelingfull                  = "Feat: Feeling Full"
    feat_baileystroublemaker          = "Feat: Bailey's Trouble Maker"
    feat_leightonsnightmare           = "Feat: Leighton's Nightmare"
    feat_alexspartner                 = "Feat: Alex's Partner"
    feat_harpersbane                  = "Feat: Harper's Bane"
    feat_headofthepack                = "Feat: Head of the Pack"
    feat_topofthefoodchain            = "Feat: Top of the Food Chain"
    feat_prideofthefarm               = "Feat: Pride of the Farm"
    feat_dawntodusk                   = "Feat: Dawn to Dusk"
    feat_earslimelover                = "Feat: Ear Slime Lover"
    feat_earslimeamalgam              = "Feat: Ear Slime Amalgam"
    feat_thepathtoredemption          = "Feat: The Path to Redemption"
    feat_anewlife                     = "Feat: A New Life"
    feat_negotiator                   = "Feat: Negotiator"
    feat_curiousattire                = "Feat: Curious Attire"
    feat_wickedwardrobe               = "Feat: Wicked Wardrobe"
    feat_mycollectionoffeats          = "Feat: My Collection of Feats"
    feat_mytimelesscollectionoffeats  = "Feat: My Timeless Collection of Feats"
    feat_broodmotherhost              = "Feat: Broodmother Host"
    feat_topbroodmotherhost           = "Feat: Top Broodmother Host"
    feat_broodmotherzoologist         = "Feat: Broodmother Zoologist"
    feat_miracleoflife                = "Feat: Miracle of Life"
    feat_firstfatherhood              = "Feat: First Fatherhood"
    feat_hailmary                     = "Feat: Hail Mary"
    feat_bicyclemother                = "Feat: Bicycle Mother"
    feat_lifecomesinthrees            = "Feat: Life Comes in Threes"
    feat_lifebeginswhenyouleastexpect = "Feat: Life begins when you least expect"
    feat_diversityoflife              = "Feat: Diversity of Life"


    # -- Upgrades
    upgrade_flatsbridge        = "Bought: Flats Bridge"                   # ascend
    upgrade_forestroad         = "Bought: Forest Road"                    # ascend
    upgrade_fieldoffice        = "Bought: Winter's Field Office"          # ascend
    upgrade_residentialthicket = "Bought: Residential Alleyways Thicket"  # decend
    upgrade_schoolgreen        = "Bought: School Green"                   # decend
    upgrade_hookahparlour      = "Hookah Parlour Ownership"

    upgrade_adultshop          = "Built Adult Shop"
    upgrade_cafe               = "Cafe Re-Opened"

    upgrade_farm_wall_1      = "Farm: Wall Fully Repaired"
    upgrade_farm_wall_2      = "Farm: Wall Reinforced"
    upgrade_farm_wall_3      = "Farm: Wall Metal Fence"
    upgrade_farm_wall_4      = "Farm: Wall Barbed Wire"
    upgrade_farm_security_1  = "Farm: Security Watchtower"
    upgrade_farm_security_2  = "Farm: Security Searchlights"
    upgrade_farm_kennel      = "Farm: Kennel"
    upgrade_farm_woodland_1  = "Farm: Woodlands Purchased"
    upgrade_farm_woodland_2  = "Farm: Woodlands More Purchased"
    upgrade_farm_woodland_3  = "Farm: Woodlands Even More Purchased"
    upgrade_farm_barn_1      = "Farm: Barn New Equipment"
    upgrade_farm_barn_2      = "Farm: Barn Expanded"
    upgrade_farm_coop_1      = "Farm: Coop Expanded"
    upgrade_farm_coop_2      = "Farm: Coop Expanded Again"
    upgrade_farm_irrigation  = "Farm: Irrigation"
    upgrade_farm_stable      = "Farm: Stable"
    upgrade_farm_parasite_1  = "Farm: Parasite Barn Built"
    upgrade_farm_parasite_2  = "Farm: Parasite Barn Expanded"
    upgrade_farm_greenhouse  = "Farm: Greenhouse"

    upgrade_loft_pepperspraylab = "Loft: Pepper Spray Lab"  # kylar
    upgrade_loft_kitchen        = "Loft: Secret Kitchen"    # river
    upgrade_loft_window         = "Loft: Bay Window"        # great hawk
    upgrade_loft_nook           = "Loft: Reading Nook"      # doren
    upgrade_loft_coffee         = "Loft: Coffee Pot"        # sam
    upgrade_loft_whitney        = "Loft: An Apparatus"      # whitney


    # -- Overrides
    override_transformation_cat         = "Transformation: Cat"
    override_transformation_wolf        = "Transformation: Wolf"
    override_transformation_cow         = "Transformation: Cow"
    override_transformation_harpy       = "Transformation: Harpy"
    override_transformation_fox         = "Transformation: Fox"
    override_transformation_angel       = "Transformation: Angel"
    override_transformation_fallenangel = "Transformation: Fallen Angel"
    override_transformation_demon       = "Transformation: Demon"

    override_upgrade_flatsbridge        = "Upgrade: Flats Bridge"
    override_upgrade_forestroad         = "Upgrade: Forest Road"
    override_upgrade_fieldoffice        = "Upgrade: Field Office"
    override_upgrade_residentialthicket = "Upgrade: Residential Thicket"
    override_upgrade_schoolgreen        = "Upgrade: School Green"
    override_upgrade_hookahparlour      = "Upgrade: Hookah Parlour"
    override_upgrade_adultshop          = "Upgrade: Adult Shop"
    override_upgrade_cafeopening        = "Upgrade: Cafe Opening"

    # -- Access Items
    accessitem_adoptionpapers = "Avery Adoption"
    accessitem_fakeid         = "Item: Fake ID"
    accessitem_mazekey        = "Item: Maze Key"


@dataclass(frozen=True)
class _NoteDetail():
    """
    A creator for making a localized note for
    a connection between 2 regions

    Usage of this contained in ConnectionNotes

    ### English Example:
    variables:
    ```
        prefix: "via "
        flip: " from "
        location1: "Alex's Farm"
        location2: "Farmlands"
    ```
    Defintion:  ``{prefix}{location1}{flip}{location2}``\n
    Output:     ``via Alex's Farm from Farmlands``\n
    Definition Flipped: ``{prefix}{location2}{flip}{location1}``\n
    Output Flipped:     ``via Farmlands from Alex's Farm``\n

    ### Addendum:
    I've created it this way because I noticed a significant Chinese modding
    community following for this game, and wished to create an easy to
    localize system, if anyone wished to create a localization

    If you wish to change the formatting of the string, check out the 
    resolve() function below, and swap around the placements of the variables there

    You aren't required to use same variables as shown via the
    ConnectionNotes class below using {prefix} and {flip_from}.
    You may add new ones inside the Enum, to your convineince.
    You may also override any variables included in the notes.
    They just exit there to help localization, to be changed as needed

    If the connection is one-way (no way back) then the code to flip
    will just not run.
    """
    prefix: str
    flip: str = ""
    location1: str = ""
    location2: str = ""
    override_flipstr: str = None

    def resolve(self, flip:bool = False):
        """
        Change ordering of values in returns here
        """
        if flip == False: 
            return f"{self.prefix}{self.location1}{self.flip}{self.location2}"
        elif self.override_flipstr is None:
            return f"{self.prefix}{self.location2}{self.flip}{self.location1}"
        else:
            return self.override_flipstr


class ConnectionNotes(Enum):
    """
    The notes used for connections between two regions

    How to modify is explained inside _NoteDetail()
    """
    # this is used to allow a creation of "1 -> 2"
    # and a creation of "2 -> 1"
    prefix = "via "
    flip_from = " from "

    forest_forestlake = _NoteDetail(
        prefix, flip_from, DoLRegionNames.forest_lake, DoLRegionNames.forest)
    forest_forestshop = _NoteDetail(
        prefix, flip_from, DoLRegionNames.forest_shop, DoLRegionNames.forest)

    farmlands_manors = _NoteDetail(
        prefix, flip_from, DoLRegionNames.manors, DoLRegionNames.farmlands)
    farmlands_meadow = _NoteDetail(
        prefix, flip_from, DoLRegionNames.meadow, DoLRegionNames.farmlands)
    farmlands_ridingschool = _NoteDetail(
        prefix, flip_from, DoLRegionNames.riding_school, DoLRegionNames.farmlands)
    farmlands_alexfarm = _NoteDetail(
        prefix, flip_from, DoLRegionNames.alex_farm, DoLRegionNames.farmlands)
    farmlands_farmlandsroad = _NoteDetail(
        prefix, flip_from, DoLRegionNames.farmlands_road, DoLRegionNames.farmlands)
    farmlands_maze = _NoteDetail(
        prefix, flip_from, DoLRegionNames.maze, DoLRegionNames.farmlands)

    moor_remyestate = _NoteDetail(
        prefix, flip_from, "Remys Estate", DoLRegionNames.moor)

    bog_moor = _NoteDetail(
        prefix, flip_from, DoLRegionNames.moor, DoLRegionNames.bog)
    bog_forest = _NoteDetail( # oneway entrance
        prefix, flip_from, DoLRegionNames.bog, DoLRegionNames.forest)

    oldsewers_beach = _NoteDetail(
        prefix, flip_from, "Diving to the bottom", "Beach Rocks to Pool")
    oldsewers_residentialdrain = _NoteDetail(
        prefix, flip_from, DoLRegionNames.old_sewers, "Climbing down inside the Residential Drain")
    residentialdrain_commercialdrain = _NoteDetail(
        prefix, flip_from, DoLRegionNames.residential_drain, DoLRegionNames.commercial_drain)
    oldsewers_commercialdrain = _NoteDetail(
        prefix, flip_from, DoLRegionNames.old_sewers, "Climbing down inside the Residential Drain")
    commercialdrain_industrialdrain = _NoteDetail(
        prefix, flip_from, DoLRegionNames.commercial_drain, DoLRegionNames.industrial_drain)
    oldsewers_industrialdrain = _NoteDetail(
        prefix, flip_from, DoLRegionNames.old_sewers, "Climbing down inside the Residential Drain")

    residentialdrain_residentialalleyways = _NoteDetail(
        prefix, flip_from, DoLRegionNames.residential_drain, DoLRegionNames.residential_alleyways)
    commercialdrain_commercialalleyways = _NoteDetail(
        prefix, flip_from, DoLRegionNames.commercial_drain, DoLRegionNames.commercial_alleyways)
    industrialdrain_industrialalleyways = _NoteDetail(
        prefix, flip_from, DoLRegionNames.industrial_alleyways, DoLRegionNames.industrial_alleyways)

    residentialalleyways_commercialalleyways = _NoteDetail(
        prefix, flip_from, DoLRegionNames.residential_alleyways, DoLRegionNames.commercial_alleyways)
    commercialalleyways_industrialalleyways = _NoteDetail(
        prefix, flip_from, DoLRegionNames.commercial_alleyways, DoLRegionNames.industrial_alleyways)

    park_commercialalleyways = _NoteDetail(
        prefix, flip_from, DoLRegionNames.park, DoLRegionNames.commercial_alleyways)
    park_industrialalleyways = _NoteDetail(
        prefix, flip_from, DoLRegionNames.park, DoLRegionNames.industrial_alleyways)

    danubestreet_spa = _NoteDetail(
        prefix, flip_from, DoLRegionNames.spa, DoLRegionNames.danube_street)
    danubestreet_averymansion = _NoteDetail(
        prefix, flip_from, DoLRegionNames.avery_mansion, DoLRegionNames.danube_street)
    danubestreet_danubehouses = _NoteDetail(
        prefix, flip_from, DoLRegionNames.danube_houses, DoLRegionNames.danube_street)
    danubestreet_forest = _NoteDetail(
        prefix, flip_from, DoLRegionNames.forest, DoLRegionNames.danube_street)
    danubestreet_residentialalleyways = _NoteDetail(
        prefix, flip_from, DoLRegionNames.residential_alleyways, DoLRegionNames.danube_street)
    danubestreet_residentialdrain = _NoteDetail(
        prefix, flip_from, DoLRegionNames.residential_drain, DoLRegionNames.danube_street)
    
    flats_hookahparlour = _NoteDetail(
        prefix, flip_from, DoLRegionNames.hookah_parlour, DoLRegionNames.flats)
    
    barbstreet_dancestudio = _NoteDetail(
        prefix, flip_from, DoLRegionNames.dance_studio, DoLRegionNames.barb_street)
    barbstreet_policestation = _NoteDetail(
        prefix, flip_from, DoLRegionNames.police_station, DoLRegionNames.barb_street)
    barbstreet_flats = _NoteDetail(
        prefix, flip_from, DoLRegionNames.flats, DoLRegionNames.barb_street)
    barbstreet_residentialalleyway = _NoteDetail(
        prefix, flip_from, DoLRegionNames.residential_alleyways, DoLRegionNames.barb_street)
    barbstreet_residentialdrain = _NoteDetail(
        prefix, flip_from, DoLRegionNames.residential_drain, DoLRegionNames.barb_street)
    
    orphanage_residentialalleyways = _NoteDetail(
        prefix, flip_from, "Climb the Fence", DoLRegionNames.orphanage)
    
    domusstreet_orphanage = _NoteDetail(
        prefix, flip_from, DoLRegionNames.orphanage, DoLRegionNames.domus_street)
    domusstreet_domushouses = _NoteDetail(
        prefix, flip_from, DoLRegionNames.domus_houses, DoLRegionNames.domus_street)
    domusstreet_residentialalleyways = _NoteDetail(
        prefix, flip_from, DoLRegionNames.residential_alleyways, DoLRegionNames.domus_street)
    domusstreet_residentialdrain = _NoteDetail(
        prefix, flip_from, DoLRegionNames.residential_drain, DoLRegionNames.domus_street)
    
    connudatusstreet_stripclub = _NoteDetail(
        prefix, flip_from, DoLRegionNames.strip_club, DoLRegionNames.connudatus_street)
    connudatusstreet_commercialdrain = _NoteDetail(
        prefix, flip_from, DoLRegionNames.commercial_drain, DoLRegionNames.connudatus_street)
    connudatusstreet_residentialalleyways = _NoteDetail(
        prefix, flip_from, DoLRegionNames.residential_alleyways, DoLRegionNames.connudatus_street)
    connudatusstreet_commercialalleyways = _NoteDetail(
        prefix, flip_from, DoLRegionNames.commercial_alleyways, DoLRegionNames.connudatus_street)
    
    starfishstreet_arcade = _NoteDetail(
        prefix, flip_from, DoLRegionNames.arcade, DoLRegionNames.starfish_street)
    starfishstreet_chalets = _NoteDetail(
        prefix, flip_from, DoLRegionNames.chalets, DoLRegionNames.starfish_street)
    starfishstreet_dogpound = _NoteDetail(
        prefix, flip_from, DoLRegionNames.dog_pound, DoLRegionNames.starfish_street)
    starfishstreet_beach = _NoteDetail(
        prefix, flip_from, DoLRegionNames.beach, DoLRegionNames.starfish_street)
    starfishstreet_park = _NoteDetail(
        prefix, flip_from, DoLRegionNames.park, DoLRegionNames.starfish_street)
    starfishstreet_commercialdrain = _NoteDetail(
        prefix, flip_from, DoLRegionNames.commercial_drain, DoLRegionNames.starfish_street)
    
    cliffstreet_mayoroffice = _NoteDetail(
        prefix, flip_from, DoLRegionNames.mayors_office, DoLRegionNames.cliff_street)
    cliffstreet_cafe = _NoteDetail(
        prefix, flip_from, DoLRegionNames.cafe, DoLRegionNames.cliff_street)
    cliffstreet_beach = _NoteDetail(
        prefix, flip_from, DoLRegionNames.beach, DoLRegionNames.cliff_street)
    cliffstreet_commercialdrain = _NoteDetail(
        prefix, flip_from, DoLRegionNames.commercial_drain, DoLRegionNames.cliff_street)
    cliffstreet_commercialalleyways = _NoteDetail(
        prefix, flip_from, DoLRegionNames.commercial_alleyways, DoLRegionNames.cliff_street)
    
    shoppingcentrerooftop_ladder = _NoteDetail(
        prefix, flip_from, DoLRegionNames.commercial_alleyways, "The Ladder on The Shopping Centre Rooftop")
    shoppingcentre_rooftop = _NoteDetail( # Shopping Centre areas do not use region names to make slightly smaller
        prefix, flip_from, "Rooftop", DoLRegionNames.shopping_centre)
    shoppingcentre_hairdressers = _NoteDetail(
        prefix, flip_from, "Hairdressers", DoLRegionNames.shopping_centre)
    shoppingcentre_petshop = _NoteDetail(
        prefix, flip_from, "Pet Shop", DoLRegionNames.shopping_centre)
    shoppingcentre_tattooparlour = _NoteDetail(
        prefix, flip_from, "Tattoo Parlour", DoLRegionNames.shopping_centre)
    shoppingcentre_furnitureshop = _NoteDetail(
        prefix, flip_from, "Furniture Shop", DoLRegionNames.shopping_centre)
    shoppingcentre_supermarket = _NoteDetail(
        prefix, flip_from, "Supermarket", DoLRegionNames.shopping_centre)
    shoppingcentre_clothingshop = _NoteDetail(
        prefix, flip_from, "Clothing Shop", DoLRegionNames.shopping_centre)
    shoppingcentre_tailor = _NoteDetail(
        prefix, flip_from, "Tailor", DoLRegionNames.shopping_centre)
    shoppingcentre_cosmeticsshop = _NoteDetail(
        prefix, flip_from, "Cosmetics Shop", DoLRegionNames.shopping_centre)
    shoppingcentre_toystore = _NoteDetail(
        prefix, flip_from, "Toy Store", DoLRegionNames.shopping_centre)
    
    highstreet_officebuilding = _NoteDetail(
        prefix, flip_from, DoLRegionNames.office_building, DoLRegionNames.high_street)
    highstreet_shoppingcentre = _NoteDetail(
        prefix, flip_from, DoLRegionNames.shopping_centre, DoLRegionNames.high_street)
    highstreet_park = _NoteDetail(
        prefix, flip_from, DoLRegionNames.park, DoLRegionNames.high_street)
    highstreet_commercialdrain = _NoteDetail(
        prefix, flip_from, DoLRegionNames.commercial_drain, DoLRegionNames.high_street)
    highstreet_commercialalleyways = _NoteDetail(
        prefix, flip_from, DoLRegionNames.commercial_alleyways, DoLRegionNames.high_street)
    
    nightingalestreet_hospital = _NoteDetail(
        prefix, flip_from, DoLRegionNames.hospital, DoLRegionNames.nightingale_street)
    nightingalestreet_photographystudio = _NoteDetail(
        prefix, flip_from, DoLRegionNames.photography_studio, DoLRegionNames.nightingale_street)
    nightingalestreet_forest = _NoteDetail(
        prefix, flip_from, DoLRegionNames.forest, DoLRegionNames.nightingale_street)
    nightingalestreet_park = _NoteDetail(
        prefix, flip_from, DoLRegionNames.park, DoLRegionNames.nightingale_street)
    nightingalestreet_commercialdrain = _NoteDetail(
        prefix, flip_from, DoLRegionNames.commercial_drain, DoLRegionNames.nightingale_street)
    nightingalestreet_commercialalleyways = _NoteDetail(
        prefix, flip_from, DoLRegionNames.commercial_alleyways, DoLRegionNames.nightingale_street)
    
    hospital_pharmacy = _NoteDetail(
        prefix, flip_from, DoLRegionNames.pharmacy, DoLRegionNames.hospital)
    
    wolfstreet_temple = _NoteDetail(
        prefix, flip_from, DoLRegionNames.temple, DoLRegionNames.wolf_street)
    wolfstreet_soupkitchen = _NoteDetail(
        prefix, flip_from, DoLRegionNames.soup_kitchen, DoLRegionNames.wolf_street)
    wolfstreet_forest = _NoteDetail(
        prefix, flip_from, DoLRegionNames.forest, DoLRegionNames.wolf_street)
    wolfstreet_commercialdrain = _NoteDetail(
        prefix, flip_from, DoLRegionNames.commercial_drain, DoLRegionNames.wolf_street)
    wolfstreet_commercialalleyways = _NoteDetail(
        prefix, flip_from, DoLRegionNames.commercial_alleyways, DoLRegionNames.wolf_street)
    
    school_park = _NoteDetail(
        prefix, flip_from, DoLRegionNames.park, DoLRegionNames.school)
    school_industrialalleyways = _NoteDetail(
        prefix, flip_from, DoLRegionNames.industrial_alleyways, DoLRegionNames.school)
    school_commercialdrain = _NoteDetail(
        prefix, flip_from, DoLRegionNames.commercial_drain, "School Toilets")
    
    oxfordstreet_school = _NoteDetail(
        prefix, flip_from, DoLRegionNames.school, DoLRegionNames.oxford_street)
    oxfordstreet_museum = _NoteDetail(
        prefix, flip_from, DoLRegionNames.museum, DoLRegionNames.oxford_street)
    oxfordstreet_commercialalleyways = _NoteDetail(
        prefix, flip_from, DoLRegionNames.commercial_alleyways, DoLRegionNames.oxford_street)
    oxfordstreet_commercialdrain = _NoteDetail(
        prefix, flip_from, DoLRegionNames.commercial_drain, DoLRegionNames.oxford_street)
    oxfordstreet_industrialalleyways = _NoteDetail(
        prefix, flip_from, DoLRegionNames.industrial_alleyways, DoLRegionNames.oxford_street)
    oxfordstreet_park = _NoteDetail(
        prefix, flip_from, DoLRegionNames.park, DoLRegionNames.oxford_street)
    oxfordstreet_forestlake = _NoteDetail( # oneway entrance
        prefix, flip_from, DoLRegionNames.forest_lake, "Oxford Street Afterschool Students")
    oxfordstreet_orphanage = _NoteDetail( # oneway entrance
        prefix, flip_from, DoLRegionNames.orphanage, "Oxford Street Afterschool Robin")
    
    pub_forest = _NoteDetail(
        prefix, flip_from, DoLRegionNames.forest, "Flirting in the Pub")
    
    harveststreet_brothel = _NoteDetail(
        prefix, flip_from, DoLRegionNames.brothel, DoLRegionNames.harvest_street)
    harveststreet_pub = _NoteDetail(
        prefix, flip_from, DoLRegionNames.pub, DoLRegionNames.harvest_street)
    harveststreet_bustation = _NoteDetail(
        prefix, flip_from, DoLRegionNames.bus_station, DoLRegionNames.harvest_street)
    harveststreet_factory = _NoteDetail(
        prefix, flip_from, DoLRegionNames.factory, DoLRegionNames.harvest_street)
    harveststreet_industrialdrain = _NoteDetail(
        prefix, flip_from, DoLRegionNames.industrial_alleyways, DoLRegionNames.harvest_street)
    harveststreet_industrialalleyways = _NoteDetail(
        prefix, flip_from, DoLRegionNames.industrial_alleyways, DoLRegionNames.harvest_street)
    harveststreet_farmlandsroad = _NoteDetail(
        prefix, flip_from, DoLRegionNames.farmlands_road, DoLRegionNames.harvest_street)
    
    docks_beach = _NoteDetail(
        prefix, flip_from, DoLRegionNames.beach, "diving off Nighttime Docks")
    
    costalpath_meadow = _NoteDetail( # oneway exit
        prefix, flip_from, DoLRegionNames.meadow, DoLRegionNames.coastal_path)

    merstreet_beach = _NoteDetail(
        prefix, flip_from, "Beach (Docks Area)", DoLRegionNames.mer_street)
    merstreet_docks = _NoteDetail(
        prefix, flip_from, DoLRegionNames.docks, DoLRegionNames.mer_street)
    merstreet_costalpath = _NoteDetail(
        prefix, flip_from, DoLRegionNames.coastal_path, DoLRegionNames.mer_street)
    merstreet_industrialalleyways = _NoteDetail(
        prefix, flip_from, DoLRegionNames.industrial_alleyways, DoLRegionNames.mer_street)
    merstreet_industrialdrain = _NoteDetail(
        prefix, flip_from, DoLRegionNames.industrial_alleyways, DoLRegionNames.mer_street)
    
    elkstreet_landfill = _NoteDetail(
        prefix, flip_from, DoLRegionNames.landfill, DoLRegionNames.elk_street)
    elkstreet_adultshop = _NoteDetail(
        prefix, flip_from, DoLRegionNames.adult_shop, DoLRegionNames.elk_street)
    elkstreet_compound = _NoteDetail(
        prefix, flip_from, DoLRegionNames.compound, DoLRegionNames.elk_street)
    elkstreet_industrialalleyways = _NoteDetail(
        prefix, flip_from, DoLRegionNames.industrial_alleyways, DoLRegionNames.elk_street)
    elkstreet_industrialdrain = _NoteDetail(
        prefix, flip_from, DoLRegionNames.industrial_alleyways, DoLRegionNames.elk_street)
    
    police_prison = _NoteDetail( # oneway entrance
        prefix, flip_from, DoLRegionNames.prison, "Being caught by Police or Turning yourself into the Police with >=5000 Crime Score")
    
    pirateship_island = _NoteDetail( # oneway entrance
        prefix, flip_from, DoLRegionNames.island, "On the Pirate Ship, passout or become a mate and asking Zephyr")
    
    bailey_undergroundbrothel = _NoteDetail( # oneway entrance
        prefix, flip_from, DoLRegionNames.underground_brothel, "Failing to pay Bailey")
    police_undergroundbrothel = _NoteDetail( # oneway entrance
        prefix, flip_from, DoLRegionNames.underground_brothel, "A Vent from running from the Police after being taken in")
    
    harper_asylum = _NoteDetail( # oneway entrance
        prefix, flip_from, DoLRegionNames.asylum, "Harper Abduction")
    
    dogpound_dogpoundbadend = _NoteDetail( # oneway entrance
        prefix, flip_from, DoLRegionNames.dog_pound_ending, "Having 'fun' with the Dog Pound Dogs, often close to closing time")
    wolfabudction_dogpoundbadend = _NoteDetail( # oneway entrance
        prefix, flip_from, DoLRegionNames.dog_pound_ending, "Town Abduction with Wolf Appearance")
    
    flats_mines = _NoteDetail( # oneway entrance
        prefix, flip_from, DoLRegionNames.mines, "the Flats Abduction")
    
    eden_edencabin = _NoteDetail( # oneway entrance
        prefix, flip_from, DoLRegionNames.eden_cabin, "Meeting Eden inside the Forest")
    bailey_edencabin = _NoteDetail( # oneway entrance
        prefix, flip_from, DoLRegionNames.eden_cabin, "Failing to pay Bailey")
    
    kylar_kylarmanor = _NoteDetail( # oneway entrance
        prefix, flip_from, DoLRegionNames.kylar_manor, "Kylar Abduction")
    
    ocean_pirateship = _NoteDetail( # oneway entrance
        prefix, flip_from, DoLRegionNames.pirate_ship, "Passing out inside the ocean")
    oldsewers_pirateship = _NoteDetail( # oneway entrance
        prefix, flip_from, DoLRegionNames.pirate_ship, "Meeting Zephyr inside the Smugglers Pub, knowing about the Spear")
    
    greathawk_birdtower = _NoteDetail( # oneway entrance
        prefix, flip_from, DoLRegionNames.bird_tower, "Abduction by the Great Hawk")
    
    bailey_remyfarm = _NoteDetail( # oneway entrance
        prefix, flip_from, DoLRegionNames.remy_farm, "Failing to pay Bailey")  # :: Street Van Bailey
    moor_remyfarm = _NoteDetail( # oneway entrance
        prefix, flip_from, DoLRegionNames.remy_farm, "Abduction inside the Moor")
    remyestate_remyfarm = _NoteDetail( # oneway entrance
        prefix, flip_from, DoLRegionNames.remy_farm, "Passing out or losing blackjack inside Remy's Estate")
    cliffstreet_remyfarm = _NoteDetail( # oneway entrance
        prefix, flip_from, DoLRegionNames.remy_farm, "Making Sam mad and being on Cliff Street and Arrested")
    pub_remyfarm = _NoteDetail( # oneway entrance
        prefix, flip_from, DoLRegionNames.remy_farm, "Getting drunk at the pub, someone taking you to the Forest, then taking their White Pill")
    intown_remyfarm = _NoteDetail( # oneway entrance
        prefix, flip_from, DoLRegionNames.remy_farm, "Abduction while helping someone unload their Van")
    
    forest_wolfcave = _NoteDetail( # oneway entrance
        prefix, flip_from, DoLRegionNames.wolf_cave, "Wolves inside the Forest")
    
    prison_orphanage = _NoteDetail( # oneway exit
        prefix, flip_from, DoLRegionNames.orphanage, "Leaving the Prison normally")
    prison_docks = _NoteDetail( # oneway exit
        prefix, flip_from, DoLRegionNames.docks, "Leaving the Prion with the Boat")
    prison_oceanswim = _NoteDetail( # oneway exit
        prefix, flip_from, DoLRegionNames.ocean, "Swimming away the Prison")
    prison_oceanpassout = _NoteDetail( # oneway exit
        prefix, flip_from, DoLRegionNames.ocean, "Passing out in the Prison's rut")
    prison_beach = _NoteDetail( # oneway exit
        prefix, flip_from, DoLRegionNames.beach, "Flying away from the Prison")
    
    island_pirateship = _NoteDetail( # oneway exit
        prefix, flip_from, DoLRegionNames.pirate_ship, "Handing over the spear to Zephyr on the Island")
    island_merstreet = _NoteDetail( # oneway exit
        prefix, flip_from, DoLRegionNames.mer_street, "Sailing away in a Raft from the Island")
    island_ocean = _NoteDetail( # oneway exit
        prefix, flip_from, DoLRegionNames.ocean, "Successfully running with the Island Spear")
    island_hospital = _NoteDetail( # oneway exit
        prefix, flip_from, DoLRegionNames.hospital, "Leaving the Island due to Pregnancy")
     
    undergroundbrothel_ocean = _NoteDetail( # oneway exit
        prefix, flip_from, DoLRegionNames.ocean, "Digging out from the Underground Brothel")
    undergroundbrothel_forest = _NoteDetail( # oneway exit
        prefix, flip_from, DoLRegionNames.forest, "Running away from an Underground Brothel Event")
    
    asylum_forest = _NoteDetail( # oneway exit
        prefix, flip_from, DoLRegionNames.forest, "Running from The Asylum")
    asylum_orphanage = _NoteDetail( # oneway exit
        prefix, flip_from, DoLRegionNames.orphanage, "Leaving The Asylum Normally")
    
    dogpoundbadend_starfishstreet = _NoteDetail( # oneway exit
        prefix, flip_from, DoLRegionNames.starfish_street, "Escaping the Dog Pound Bad-End")
    
    mines_residentialdrain = _NoteDetail( # oneway exit
        prefix, flip_from, DoLRegionNames.residential_drain, "Escaping the Guards or Passing out in the Mines")
    mines_flats = _NoteDetail( # oneway exit
        prefix, flip_from, DoLRegionNames.flats, "Escaping the Mines")
    
    edencabin_forest = _NoteDetail( # oneway exit
        prefix, flip_from, DoLRegionNames.forest, "Running from Eden's Cabin")
    
    kylarmanor_danubestreet = _NoteDetail( # oneway exit
        prefix, flip_from, DoLRegionNames.danube_street, "Running or Leaving Kylar's Manor") 
    
    pirateship_ocean = _NoteDetail( # oneway exit
        prefix, flip_from, DoLRegionNames.ocean, "Diving from the Pirate Ship")
    pirateship_merstreet = _NoteDetail( # oneway exit
        prefix, flip_from, DoLRegionNames.mer_street, "Having Zephyr return you to town")
    
    birdtower_farmlands = _NoteDetail( # oneway exit
        prefix, flip_from, DoLRegionNames.farmlands, "Flying from the Great Hawk's Tower")
    birdtower_moor = _NoteDetail( # oneway exit
        prefix, flip_from, DoLRegionNames.moor, "Leaving the Great Hawk's Tower")
    
    remyfarm_forest = _NoteDetail( # oneway exit
        prefix, flip_from, DoLRegionNames.forest, "Escaping Remy's Farm")
    
    wolfcave_forest = _NoteDetail( # oneway exit
        prefix, flip_from, DoLRegionNames.forest, "Running from the Wolves Cave")
    wolfcave_ocean = _NoteDetail( # oneway exit
        prefix, flip_from, DoLRegionNames.ocean, "Digging out from the Wolves Cave")
    
    asylum_tentacleplains = _NoteDetail(
        prefix, flip_from, DoLRegionNames.tentacle_plains, DoLRegionNames.asylum)
    hookahparlour_tentacleforest = _NoteDetail(
        prefix, flip_from, DoLRegionNames.tentacle_forest, DoLRegionNames.hookah_parlour)
    orphanage_tentacleplains = _NoteDetail(
        prefix, flip_from, DoLRegionNames.tentacle_plains, DoLRegionNames.orphanage)
    
    domusstreet_barbstreet = _NoteDetail(
        prefix, flip_from, DoLRegionNames.barb_street, DoLRegionNames.domus_street)
    domusstreet_danubestreet = _NoteDetail(
        prefix, flip_from, DoLRegionNames.danube_street, DoLRegionNames.domus_street)
    barbstreet_cliffstreet = _NoteDetail(
        prefix, flip_from, DoLRegionNames.cliff_street, DoLRegionNames.barb_street)
    barbstreet_connudatusstreet = _NoteDetail(
        prefix, flip_from, DoLRegionNames.connudatus_street, DoLRegionNames.barb_street)
    danubestreet_wolfstreet = _NoteDetail(
        prefix, flip_from, DoLRegionNames.wolf_street, DoLRegionNames.danube_street)
    danubestreet_connudatusstreet = _NoteDetail(
        prefix, flip_from, DoLRegionNames.connudatus_street, DoLRegionNames.danube_street)
    connudatusstreet_cliffstreet = _NoteDetail(
        prefix, flip_from, DoLRegionNames.cliff_street, DoLRegionNames.connudatus_street)
    connudatusstreet_wolfstreet = _NoteDetail(
        prefix, flip_from, DoLRegionNames.wolf_street, DoLRegionNames.connudatus_street)
    cliffstreet_starfishstreet = _NoteDetail(
        prefix, flip_from, DoLRegionNames.starfish_street, DoLRegionNames.cliff_street)
    cliffstreet_highstreet = _NoteDetail(
        prefix, flip_from, DoLRegionNames.high_street, DoLRegionNames.cliff_street)
    wolfstreet_nightingalestreet = _NoteDetail(
        prefix, flip_from, DoLRegionNames.nightingale_street, DoLRegionNames.wolf_street)
    wolfstreet_highstreet = _NoteDetail(
        prefix, flip_from, DoLRegionNames.high_street, DoLRegionNames.wolf_street)
    highstreet_starfishstreet = _NoteDetail(
        prefix, flip_from, DoLRegionNames.starfish_street, DoLRegionNames.high_street)
    highstreet_nightingalestreet = _NoteDetail(
        prefix, flip_from, DoLRegionNames.nightingale_street, DoLRegionNames.high_street)
    starfishstreet_oxfordstreet = _NoteDetail(
        prefix, flip_from, DoLRegionNames.oxford_street, DoLRegionNames.starfish_street)
    starfishstreet_merstreet = _NoteDetail(
        prefix, flip_from, DoLRegionNames.mer_street, DoLRegionNames.starfish_street)
    nightingalestreet_oxfordstreet = _NoteDetail(
        prefix, flip_from, DoLRegionNames.oxford_street, DoLRegionNames.nightingale_street)
    nightingalestreet_elkstreet = _NoteDetail(
        prefix, flip_from, DoLRegionNames.elk_street, DoLRegionNames.nightingale_street)
    oxfordstreet_merstreet = _NoteDetail(
        prefix, flip_from, DoLRegionNames.mer_street, DoLRegionNames.oxford_street)
    oxfordstreet_elkstreet = _NoteDetail(
        prefix, flip_from, DoLRegionNames.elk_street, DoLRegionNames.oxford_street)
    merstreet_harvestreet = _NoteDetail(
        prefix, flip_from, DoLRegionNames.harvest_street, DoLRegionNames.mer_street)
    elkstreet_harvestreet = _NoteDetail(
        prefix, flip_from, DoLRegionNames.harvest_street, DoLRegionNames.elk_street)

    arrested_kylarambluance = _NoteDetail(
        prefix, flip_from, DoLRegionNames.jail, "Being taken while fainting at School or in Town by Kylar, and protecting him")

    hospital_fainting = _NoteDetail( # oneway entrance
        prefix, flip_from, DoLRegionNames.hospital, "Fainting")

    note_town = _NoteDetail("Exists in Town")
    note_world = _NoteDetail("Exists in The World")
    note_eventsstreet = _NoteDetail("In Town Street Event")


class OptionsLocalization(StrEnum):
    """
    The option text for names, groups, and whatever
    needs to be put inside an option
    """
    display_trap = "Trap Chance"
    display_target = "Randomization Targets"
    display_transformationtype = "Randomize Transformation Type"
    display_req = "Randomization Target Requirements"
    display_upgradetype = "Randomize Upgrade Type"
    display_goal = "Completion Goal"
    display_goal_antiques = "Completion Goal: Antiques"
    display_goal_money = "Completion Goal: Money"
    display_randomizestart = "Change Starting Location"

    display_erand = "Entrance Randomizer"
    display_erand_badend = "Bad End Entrance Randomization"
    display_erand_tentacleareas = "Tentacle Area Entrance Randomization"
    display_erand_shops = "Shop Entrance Randomiation"
    display_erand_pooloneway = "Pool One Way Randomization"
    display_erand_walkabletown = "Walkable Town"

    display_worldoptions = "World Options"
    display_animaloptions = "Animal Options"

    group_randomization = "Randomization Options"
    group_goal = "Goal Options"
    group_entrancerandomizer = "Region Randomizer Options"
    group_gameworld = "Game World Options"

    target_feats = "feats"
    target_antiques = "antiques"
    target_skills = "skills"
    target_transformations = "transformations"
    target_areaupgrades = "area_upgrades"
    target_areaunlocks = "area_unlocks"

    req_featcopper = "feat_copper"
    req_featsilver = "feat_silver"
    req_featgold = "feat_gold"
    req_featplatinum = "feat_platinum"
    req_featjeweled = "feat_jeweled"
    req_transformation = "transformation"
    req_loveinterest = "love_interest"
    req_badend = "bad_end"
    req_seasonal = "seasonal"
    req_difficult = "difficult"
    req_multipleruns = "multiple_runs"

    upgrade_alexfarm = "alex_farm"
    upgrade_tentacleforest = "tentacle_forest"
    upgrade_orphanageloft = "orphanage_loft"
    upgrade_general = "general"

    toggle_pregnancy = "pregnancy"
    toggle_parapregnancy = "parasitic_pregnancy"
    toggle_animaltransformations = "animal_transformation"
    toggle_divinetransformations = "divine_transformations"
    toggle_bestiality = "bestiality"
    toggle_monsterpeople = "monster_people"
    toggle_lactation = "lactation"
    toggle_softvore = "soft_vore"
    toggle_anal = "anal"
    toggle_bodywriting = "bodywriting"
    toggle_hypnosis = "hypnosis"

    animal_swarms = "swarms"
    animal_parasites = "parasites"
    animal_tentacles = "tentacles"
    animal_slimes = "slimes"
    animal_spiders = "spiders"
    animal_slugs = "slugs"
    animal_wasps = "wasps"
    animal_bees = "bees"
    animal_lurkers = "lurkers"
    animal_horses = "horses"
    animal_plantpeople = "plantpeople"
