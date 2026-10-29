from dataclasses import dataclass

from Options import Choice, OptionGroup, OptionSet, PerGameCommonOptions, Range, Toggle

from .en import TPT2OptionsLocalization

class RandomizationTargets(OptionSet):
    """
    Choose what you want to randomize

    Full List:
    ['modules', ]

    1: 'modules'
    """
    display_name = TPT2OptionsLocalization.display_target.value

    valid_keys = [
        TPT2OptionsLocalization.target_modules.value,
        # continue
    ]
    default = list(valid_keys)


@dataclass
class TPT2Options(PerGameCommonOptions):
    randomization_targets: RandomizationTargets

# takes option names for use later
# retrieved by using getattr(world.options, TPT2_OPTION_NAME[option])
TPT2_OPTION_NAME = {option: optionname for optionname, option in TPT2Options.type_hints.items()}


# option_groups = [
#     OptionGroup(
#     ),
#     OptionGroup(
#     ),
# ]

# option_presets = {
#     "1": {
#     },
#     "2": {
#     },
# }
