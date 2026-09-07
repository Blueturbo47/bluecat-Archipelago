from dataclasses import dataclass

from Options import Choice, OptionGroup, PerGameCommonOptions, Range, Toggle

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

class RandomizeStart(Toggle):
    """
    Lets you change your starting location
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
    orphanage = 15

    default = option_dontRandomize


class TrapChance(Range):
    """
    Percentage of filler items that are Traps
    """

    display_name = "Trap Chance"

    range_start = 0
    range_end = 100
    default = 0

# TODO: add more options


@dataclass
class DoLOptions(PerGameCommonOptions):
    randomize_entrances: RandomizeEntrances
    randomize_badends: RandomizeBadends
    randomize_entrances_badends:RandomizeEntrancesBadends
    walkable_town: WalkableTown
    trap_chance: TrapChance
    randomize_start: RandomizeStart


option_groups = [
    OptionGroup("Randomizer Options",
        [],
    ),
    OptionGroup("Shop Options",
        [],
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
