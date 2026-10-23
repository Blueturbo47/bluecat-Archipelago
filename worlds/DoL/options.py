from dataclasses import dataclass
from enum import StrEnum

from Options import Choice, OptionGroup, OptionSet, PerGameCommonOptions, Range, Toggle
from .localization.en import OptionsLocalization

# -------------- Basic Options

class TrapChance(Range):
    """
    Percentage of filler items that are Traps
    """

    display_name = OptionsLocalization.display_trap.value

    range_start = 0
    range_end = 100
    default = 0


class RandomizationTargets(OptionSet):
    """
    Choose what you want to randomize defined in a list.
    I highly recommend keeping 'feats' on, as that is the bulk
    of checks.

    Full List: 
    ['feats', 'antiques', 'skills', 'transformations', 'area_upgrades', 'area_unlocks']


    1: 'feats'
        Your toggles and other options remove feats you cannot get, 
        so don't worry if you might make an impossible check with your settings!
    2: 'antiques'
        Note: Obtaining the item is what gives the check,
        you don't have to turn them in to the museum
    3: 'skills'
        Examples: Exhibitionism, Math, or Thigh Skill
        (Purity, Beauty, and Awareness excluded)
    4: 'transformations'
        Details explained in Randomize Transformation Type option
        If you want to disable animal/divine specifically, use World Options
    5: 'area_upgrades'
        Locations like Tentacle Forest mayor upgrades, or Alex's Farm upgrades
        May be further modified 'Randomize Upgrade Types'
    6: 'area_unlocks'
        Locations like the Strip Club which needs the Fake ID to access will
        have their item in the item pool, otherwise you can find it normally
    """

    display_name = OptionsLocalization.display_target.value
    valid_keys = [
        OptionsLocalization.target_feats.value,
        OptionsLocalization.target_antiques.value,
        OptionsLocalization.target_skills.value,
        OptionsLocalization.target_transformations.value,
        OptionsLocalization.target_areaupgrades.value,
        OptionsLocalization.target_areaunlocks.value,
    ]
    default = list(valid_keys)


class RandomizeTransformationsType(Choice):
    """
    Determines how transformatins are randomized. 
    Must be added to Randomization Targets for them to get randomized.
    
    Note: If its detected there's not enough checks in the pool, tfparts will default
    to be transformations instead

    - transformations (0): 
        Randomize whole transformations, so you get every part of a transformation at once
    - tfparts (1): 
        Randomize individual parts of transformations like Wings or Horns
        Includes an 'Appearance' part, which will give you the race specific trait
    """
    disply_name = OptionsLocalization.display_transformationtype.value
    option_transformations = 0
    option_tfparts = 1
    default = option_transformations


class RandomizationTargetRequirements(OptionSet):
    """
    Determines what type of locations you need to check

    Full List: 
    ['feat_copper', 'feat_silver', 'feat_gold', 'feat_platinum', 'feat_jeweled', 
    'transformation', 'love_interest', 'bad_end', 'seasonal', 'difficult',
    'multiple_runs']

    1: 'feat_copper'
    2: 'feat_silver'
    3: 'feat_gold'
    4: 'feat_platinum'
    5: 'feat_jeweled'
        Note: There is only 1 Jeweled Feat
    6: 'transformation'
        Anything that require a transformation to obtain
        Note: This does not disable transformations as Check
        Locations, so you still need to get transformations
    7: 'love_interest'
        Anything that require progressing with a love interest
        in order to obtain
    8: 'bad_end'
        Anything that require access to or going to a badend.
        Note: badends (as wiki states) are: Asylum, Remy's Farm, Prison,
        Underground Brothel, Dog Pound, Mines, Island, Pirate Ship,
        Kylar Abduction, Eden's Cabin, Hawk Tower, and Wolf Cave
    9: 'seasonal'
        Locations or Access to Areas requiring a season or time of year
    10: 'difficult'
        Anything that requires a large amount of time, just generally difficult, or rare RNG checks
        Examples: Millionaire, Sadomasochist, Stressful Challenge, 
            Collection of Feats, Thesis Offence, Harper the Hypnotist
    11: 'multiple_runs'
        Anything that requires making a new savefile to get
        Examples: Being a Boy, Being a Herm, Angel TF
        Note: this can make Angel TF not required to be checked if transformations are check,
        however if feats are disabled will become a check (to prevent more items than locations)
    """
    display_name = OptionsLocalization.display_req.value
    valid_keys = [
        OptionsLocalization.req_featcopper.value,
        OptionsLocalization.req_featsilver.value,
        OptionsLocalization.req_featgold.value,
        OptionsLocalization.req_featplatinum.value,
        OptionsLocalization.req_featjeweled.value,
        OptionsLocalization.req_transformation.value,
        OptionsLocalization.req_loveinterest.value,
        OptionsLocalization.req_badend.value,
        OptionsLocalization.req_seasonal.value,
        OptionsLocalization.req_difficult.value,
        OptionsLocalization.req_multipleruns.value,
    ]
    default = list(valid_keys)


class RandomizeUpgradesType(OptionSet):
    """
    Determines what type of upgrades will be randomized

    Full List:
    ['alex_farm', 'tentacle_forest', 'orphanage_loft', 'general']

    1: 'alex_farm'
        Cleared fields are not upgrades, and are not randomized
    2: 'tentacle_forest'
        Upgrades bought via the Mayor's Office
    3: 'orphanage_loft'
        Any upgrade to the loft, respects Target Requirements
    4: 'general'
        Any world upgrades that are not the above
    """
    display_name = OptionsLocalization.display_upgradetype.value
    valid_keys = [
        OptionsLocalization.upgrade_alexfarm.value,
        OptionsLocalization.upgrade_tentacleforest.value,
        OptionsLocalization.upgrade_orphanageloft.value,
        OptionsLocalization.upgrade_general.value,
    ]
    default = list(valid_keys)


# -------------- Goal Options

class CompletionGoal(Choice):
    """
    Which Goal you wish to set for finishing
    Default: Antiques

    - Antiques: Number of antiques collected, set in 'Completion Goal: Antiques'
    - Money: Total Money, set in 'Complete Goal: Money'
    """
    display_name = OptionsLocalization.display_goal.value
    option_antiques = 0
    option_money = 1
    default = option_antiques

class CompletionGoal_Antiques(Range):
    """
    Number of antiques required for Completion Goal of Antiques
    Range of 1 to 63
    Default: 40
    """
    display_name = OptionsLocalization.display_goal_antiques.value
    range_start = 1
    range_end = 63
    default = 40

class CompletionGoal_Money(Range):
    """
    Amount of money required for Completion Goal of Money
    Range of 10,000 to 10,000,000
    Default: 100,000
    """
    display_name = OptionsLocalization.display_goal_money.value
    range_start = 10000  # 1e4
    range_end = 10000000 # 1e6
    default = 100000     # 1e5

# -------------- Region Randomizer Options

class RandomizeStart(Choice):
    """
    Lets you change your starting location. Don't randomize means starting at the orphanage
    """
    display_name = OptionsLocalization.display_randomizestart.value

    option_disabled = 0
    option_randomLocation = 1
    option_danube_street = 2
    option_barb_street = 3
    option_domus_street = 4
    option_starfish_street = 5
    option_cliff_street = 6
    option_high_street = 7
    option_nightingale_street = 8
    option_wolf_street = 9
    option_connudatus_street = 10
    option_oxford_street = 11
    option_harvest_street = 12
    option_mer_street = 13
    option_elk_street = 14

    default = option_disabled


class RandomizeEntrances(Toggle):
    """
    Randomizes where each exit leads to
    
    Areas Not Randomized:
        Very Minor Areas    (ex: Churchyard Catacombs)
        Bad-Ends*           (ex: Underground Brothel)
        Tentacle Areas*     (Tentacle Forest, Tentacle Plains)
    
    * = However can be enabled below

    Fainting to the hospital is not randomized and
    getting arrested can still takes you to Jail

    This disables the bus by default, to re-enable enable WalkableTown
    """
    display_name = OptionsLocalization.display_erand.value


class RandomizeBadends(Choice):
    """
    Randomizes where bad ends leave and the location you enter them.

    - disabled (0):
        No Change
    - between_themselves (1):
        Pool the badends, so they only randomize between themselves
        Ex: going to the Underground Brothel instead takes you to the Prison
        and leaving the Prison takes you to the Flats
    - anywhere (2):
        Adds to the global pool, so anywhere can lead to a badend
        Don't accidently walk into one!
    """
    display_name = OptionsLocalization.display_erand_badend.value
    
    option_disabled = 0
    option_between_themelves = 1
    option_anywhere = 2
    default = option_anywhere


class RandomizeTentacleAreas(Toggle):
    """
    If Entrance Randomizer is enabled, Randomizes where the 
    Tentacle Plains and Tentacle Forest entrances are, provided
    you have Tentacles enabled to enter them

    Note: this makes Asylum much easier to leave, but makes it a requirement to check there
    if you have bad_end in Randomization Target Requirements
    """
    display_name = OptionsLocalization.display_erand_tentacleareas.value


class ShopLocations(Choice):
    """
    Randomize the location of Shops
    (Shopping Centre Shops, Pharmacy, and Forest Shop)

    - disabled (0):
        No Change
    - between_themselves (1):
        All shops will be redistributed between themselves,
        instead of being added to the global pool
    - anywhere (2):
        Adds to the global pool, so anywhere can lead to a shop
    """
    display_name = OptionsLocalization.display_erand_shops.value

    option_disabled = 0
    option_between_themselves = 1
    option_anywhere = 2
    default = option_disabled


class PoolOneWayRandomization(Toggle):
    """
    If enabled, this causes paths that are one-way (Prison -> Beach) to only be randomized within themselves,
    instead of being in a global pool where they can come up randomly anywhere.

    Example if enabled:
    'Oxford Street' -> 'Forest Lake' (via students)
    Forest Lake can swap with Beach from 'Prison' -> 'Beach' to become 'Prison' -> 'Forest Lake'
    Forest Lake cannot swap with Cafe from 'Cliff Street' <-> 'Cafe' to become 'Cliff Street' -> 'Forest Lake'

    This mostly only effects bad-ends
    """
    display_name = OptionsLocalization.display_erand_pooloneway.value

    default = False


class WalkableTown(Toggle):
    """
    If Entrance Randomizer is enabled, enables the bus, and prevents street to street randomization.
    Ex: 'Domus Street' <-> 'Danube Street' will not be randomized
    """
    display_name = OptionsLocalization.display_erand_walkabletown.value

    default = False


# -------------- Game World Options

class GameWorldOptions(OptionSet):
    """
    List that says which options are enabled in your world.
    If you disable one of these for your playthrough, remove it here
    first then any paths or checks will not exist in your world that 
    require one of these. Not strictly required to 1:1 this with
    your save if you just want to disable some content for checks.

    Full List: 
    ['pregnancy', 'parasitic_pregnancy', 'animal_transformations', 
    'divine_transformations', 'bestiality', 'monster_people', 
    'lactation', 'soft_vore', 'anal', 
    'bodywriting', 'hypnosis']

    Options:
    1:  'pregnancy'
    2:  'parasitic_pregnancy'
    3:  'animal_transformations'
    4:  'divine_transformations'
    5:  'bestiality'
    6:  'monster_people'
        Any chance to have monster people via hallucinations
        or in general counts
    7:  'lactation'
    8:  'soft_vore'
    9:  'anal'
    10: 'bodywriting'
        Anything above 'NPCs may not write on you'
    11: 'hypnosis'
    """
    display_name = OptionsLocalization.display_worldoptions.value

    valid_keys = [
        OptionsLocalization.toggle_pregnancy.value,
        OptionsLocalization.toggle_parapregnancy.value,
        OptionsLocalization.toggle_animaltransformations.value,
        OptionsLocalization.toggle_divinetransformations.value,
        OptionsLocalization.toggle_bestiality.value,
        OptionsLocalization.toggle_monsterpeople.value,
        OptionsLocalization.toggle_lactation.value,
        OptionsLocalization.toggle_softvore.value,
        OptionsLocalization.toggle_anal.value,
        OptionsLocalization.toggle_bodywriting.value,
        OptionsLocalization.toggle_hypnosis.value,
    ]
    default = list(valid_keys)


class GameAnimalOptions(OptionSet):
    """
    What type of animals/beasts are enabled in your world
    Full List:
    ['swarms', 'parasites', 'tentacles',
    'slimes', 'spiders', 'slugs',
    'wasps', 'bees', 'lurkers',
    'horses', 'plantpeople']

    1:  'swarms'
    2:  'parasites'
        Note: Parasites are Earslimes and urchins, slimes, 
        and maggots that stick to you.
    3:  'tentacles'
    4:  'slimes'
    5:  'spiders'
    6:  'slugs'
    7:  'wasps'
    8:  'bees'
    9:  'lurkers'
    10: 'horses'
    11: 'plantpeople'
    """
    display_name = OptionsLocalization.display_animaloptions.value

    valid_keys = [
        OptionsLocalization.animal_swarms.value,
        OptionsLocalization.animal_parasites.value,
        OptionsLocalization.animal_tentacles.value,
        OptionsLocalization.animal_slimes.value,
        OptionsLocalization.animal_spiders.value,
        OptionsLocalization.animal_slugs.value,
        OptionsLocalization.animal_wasps.value,
        OptionsLocalization.animal_bees.value,
        OptionsLocalization.animal_lurkers.value,
        OptionsLocalization.animal_horses.value,
        OptionsLocalization.animal_plantpeople.value,
    ]
    default = list(valid_keys)


@dataclass
class DoLOptions(PerGameCommonOptions):
    # trap_chance: TrapChance
    randomization_targets: RandomizationTargets
    randomize_transformations_type: RandomizeTransformationsType
    randomization_target_requirements: RandomizationTargetRequirements
    randomize_upgrades_type: RandomizeUpgradesType

    completiongoal: CompletionGoal
    completiongoal_antiques: CompletionGoal_Antiques
    completiongoal_money: CompletionGoal_Money
    
    randomize_entrances: RandomizeEntrances
    pool_onewayrandomization: PoolOneWayRandomization
    randomize_badends: RandomizeBadends
    randomize_start: RandomizeStart
    walkable_town: WalkableTown
    randomize_tentacleareas: RandomizeTentacleAreas
    shop_locations: ShopLocations
    
    gameworld_options: GameWorldOptions
    gameanimal_options: GameAnimalOptions

# takes option names for use later
# retrieved by using getattr(world.options, DOL_OPTION_NAME[option])
DOL_OPTION_NAME = {option: optionname for optionname, option in DoLOptions.type_hints.items()}


option_groups = [
    OptionGroup(OptionsLocalization.group_randomization.value, [
        TrapChance, RandomizationTargets, RandomizeTransformationsType, 
        RandomizationTargetRequirements, RandomizeUpgradesType
    ]),
    OptionGroup(OptionsLocalization.group_goal.value, [
        CompletionGoal, CompletionGoal_Antiques, CompletionGoal_Money
    ]),
    OptionGroup(OptionsLocalization.group_entrancerandomizer.value, [
        # Locations
        RandomizeEntrances, RandomizeBadends, RandomizeTentacleAreas, 
        ShopLocations, 
        # Settings
        PoolOneWayRandomization, RandomizeStart, WalkableTown
    ]),
    OptionGroup(OptionsLocalization.group_gameworld.value, [
        GameWorldOptions, GameAnimalOptions
    ]),
]



# option_presets = { # TODO: presets
#     "standard": {},
#     "long": {},
# }
