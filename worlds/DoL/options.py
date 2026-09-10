from dataclasses import dataclass

from Options import Choice, OptionGroup, PerGameCommonOptions, Range, Toggle

# -------------- Basic Options

class TrapChance(Range):
    """
    Percentage of filler items that are Traps
    """

    display_name = "Trap Chance"

    range_start = 0
    range_end = 100
    default = 0

class RandomizeTransformations(Toggle):
    """
    Add transformations into the pool?

    If disabled you will be able to get a transformation normally, and will disable checks and connections that require transformations
    """

    disply_name = "Randomize Transformations"

class MultipleRuns(Toggle):
    """
    Enable checks that may require multiple runs. Ex: "Falling, Falling, Falling..." feat
    """
    display_name = "Multiple Runs Toggle"
    default = False

class DontRestrictRNG(Toggle):
    """
    Enables checks/paths that may require a higher RNG roll. Ex: getting caught in a van to go to Remy's Farm
    """

    display_name = "Don't Restrict RNG"
    
# -------------- Entrance Randomizer Options

class RandomizeEntrances(Toggle):
    """
    Randomizes where each exit leads to. 
    
    Badends and very minor areas are not randomized. \
        Ex: The Lake in forest and the Underground Brothel

    This disables the bus by default, to re-enable enable WalkableTown
    """

    display_name = "Entrance Randomizer"

class RandomizeBadends(Toggle):
    """
    Randomizes where bad ends leave and the location you enter them within themselves. 
    
    Ex: going to the Underground Brothel now takes you to the Prison, and leaving the Prison takes you to the Flats

    If Bad End Entrance Randomizer is enabled this does nothing, otherwise works as expected
    """

    display_name = "Bad End Randomizer"

class RandomizeEntrancesBadends(Toggle):
    """
    If entrance randomizer is enabled, this causes it to add badends to the pool instead. Don't accidently walk into one!
    """

    display_name = "Bad End Entrance Randomizer"

class WalkableTown(Toggle):
    """
    If Entrance Randomizer is enabled, enables the bus, and prevents street to street randomization.
    
    Ex: Domus street -> Danube Street always leads to Danube Street
    """

    display_name = "Walkable Town"

class RandomizeStart(Choice):
    """
    Lets you change your starting location. Don't randomize means starting at the orphanage
    """
    display_name = "Change Starting Location"

    option_dontRandomize = 0
    random = 1
    danube_street = 2
    barb_street = 3
    domus_street = 4
    starfish_street = 5
    cliff_street = 6
    high_street = 7
    nightingale_street = 8
    wolf_street = 9
    connudatus_street = 10
    oxford_street = 11
    harvest_street = 12
    mer_street = 13
    elk_street = 14

    default = option_dontRandomize

class RandomizeTentacleAreas:
    """
    Randomize where Tentacle Plains and Tentacle Forest entrances are? Note: this makes Asylum much easier to leave, \
        but makes it a requirement to check there

    This will do nothing if tentacles are not enabled
    """
    display_name = "Randomized Tentacle Area Entrances"

class ShopLocations(Choice):
    """
    Randomize the location of shops

    Between themselves means that all shopping centre shops, the pharmacy, and forest shop \
        will be added to a pool and then redistributed between them
    """

    dont_randomize = 0
    between_themselves = 1
    anywhere = 2

    default = anywhere

# -------------- Game World Options

class Tentacles(Toggle):
    """
    Are tentacles enabled in your world?

    Restricts some areas if disabled (TODO: maybe feats?)
    """

    display_name = "Tentacle Toggle"

class Pregnancy(Toggle):
    """
    Is (non-parasitic) pregnancy enabled in your world?

    Restricts some feats if disabled (TODO: double check)
    """

    display_name = "Pregnancy Toggle"
    

class ParasiticPregnancy(Toggle):
    """
    Is parasitic pregnancy enabled in your world? 
    
    This toggle also assumes: \
        Swarms, Spiders, Bees, Wasps, Lurkers, Slimes, Slugs, and plantpeople are enabled. \
        If you have one off please disable this

    Restricts some checks if disabled
    """

    display_name = "Parasitic Pregnancy Toggle"

class AnimalTransformations(Toggle):
    """
    Are animal transformations enabled in your world? Does nothing if transformations are not randomized

    Restricts some checks if disabled
    """

    display_name = "Animal Transformations Toggle"

class DivineTransformations(Toggle):
    """
    Are divine transformations enabled in your world? Does nothing if transformations are not randomized

    Restricts some checks if disabled
    """

    display_name = "Divine Transformations Toggle"

class Beastiality(Toggle):
    """
    Is beastiality enabled in your world?

    Restricts some checks if disabled 
    """ # TODO: check if this also disables farm

    display_name = "Beastiality Toggle"

class Lactation(Toggle):
    """
    Is lactation enabled in your world?

    Restricts some checks if disabled
    """

    display_name = "Lactation Toggle"

class SoftVore(Toggle):
    """
    Is Soft Vore enabled in your world?

    Restricts some checks if disabled
    """

    display_name = "Soft Vore Toggle"

class Parasites(Toggle):
    """
    Are parasites enabled in your world? Note: Parasites are Earslimes and urchins, slimes, and maggots that stick to you.

    The type of monsters that impregnate are included part of the Parasitic Pregnancy toggle

    Restricts some checks if disabled
    """

    display_name = "Parasites Toggle"

class Anal(Toggle):
    """
    Is Anal enabled in your world?

    Restricts some checks if disabled
    """

    display_name = "Anal Toggle"

class Bodywriting(Toggle):
    """
    Is bodywriting (anything above npcs will not write) enabled in your world?

    Restricts some checks if disabled
    """

    display_name = "Bodywriting Toggle"

# TODO: add more options


@dataclass
class DoLOptions(PerGameCommonOptions):
    trap_chance: TrapChance
    randomize_transformations: RandomizeTransformations
    
    randomize_entrances: RandomizeEntrances
    randomize_badends: RandomizeBadends
    randomize_entrances_badends: RandomizeEntrancesBadends
    randomize_start: RandomizeStart
    walkable_town: WalkableTown
    randomize_tentacleareas: RandomizeTentacleAreas
    shop_locations: ShopLocations
    
    tentacles: Tentacles
    pregnancy: Pregnancy
    parasitic_pregnancy: ParasiticPregnancy
    animal_transformations: AnimalTransformations
    divine_transformations: DivineTransformations
    beastiality: Beastiality
    lactation: Lactation
    softvore: SoftVore
    parasites: Parasites
    anal: Anal
    bodywriting: Bodywriting


option_groups = [
    OptionGroup("Basic Options",
        [TrapChance, RandomizeTransformations],
    ),
    OptionGroup("Entrance Randomizer Options",
        [RandomizeEntrances, RandomizeBadends, RandomizeEntrancesBadends, RandomizeStart, 
        WalkableTown, RandomizeTentacleAreas],
    ),
    OptionGroup("Game World Options", 
        [Tentacles, Pregnancy, ParasiticPregnancy, AnimalTransformations, 
        DivineTransformations, Beastiality, Lactation, SoftVore, 
        Parasites, Anal, Bodywriting],
    ),
]

option_presets = {
    "standard": {
        # TODO
    },
    "long": {
        # TODO
    },
}
