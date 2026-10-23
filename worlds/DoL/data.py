from __future__ import annotations
from enum import StrEnum, Enum
from dataclasses import dataclass
import math

from BaseClasses import ItemClassification
from rule_builder.rules import And, AtLeast, Filtered, Has, HasGroupUnique, Or, CanReachRegion, Rule, True_, False_
from rule_builder.options import OptionFilter
from .options import DOL_OPTION_NAME, DoLOptions, GameAnimalOptions, GameWorldOptions, RandomizationTargets, RandomizationTargetRequirements, TrapChance

from .en import DoLItemNames, DoLLocationNames, DoLLocationTypes, DoLRegionNames, OptionsLocalization

from typing import TYPE_CHECKING
if TYPE_CHECKING: from .world import DoLWorld


# TODO: ITEM missing items below
# pepper spray max
# player traits
# Elk-scarred trait # will have to document Avery for just this
# small body size (as an extra trait)
# recipes


# World Helpers
class DoLRegionGroups(Enum):
    """
    Useful for putting many regions into a location, and 
    unpacking/using them for a locations regions
    """
    parasitedelivery = [DoLRegionNames.orphanage.value, DoLRegionNames.alex_farm.value, DoLRegionNames.forest_lake.value]
    loveinterest = [
        DoLRegionNames.school.value, # robin, kylar, sydney, whitney
        DoLRegionNames.temple.value, # sydney
        DoLRegionNames.orphanage.value, # robin
        DoLRegionNames.domus_street.value, # avery
        DoLRegionNames.eden_cabin.value, # eden
        DoLRegionNames.alex_farm.value, # alex
        DoLRegionNames.wolf_cave.value, # black wolf
        DoLRegionNames.bird_tower.value, # great hawk
        DoLRegionNames.forest_shop.value, # gwylan
    ]

# World Rules

# Rule Optionfilter combination class
@dataclass(frozen=True)
class ROptionFilter:
    """
    ### Description:
    In order to combat not being able to resolve AP rules as bools,
    this exists to construct bools from optionfilters

    Built off a normal optionfilter, option is a normal world option,
    value is a bool, str, or int, and operator is a string.
    
    However, you may include ROptionFilter's inside Option and Value,
    to create a bigger rule

    ### Details:
    Operators include the normal operators for OptionFilter and
    'not-contains', 'not-in', 'and', and 'or'

    To chain rules, you may use '|', '&', and '~' 
    instead of 'and' and 'or' operators and 'invert' 

    Once ready in a world avaiable function, use .resolve(world)

    If you wish to convert back to OptionFilter for rules, use .convert()
    """
    option: DoLOptions | ROptionFilter
    value: bool | str | int | ROptionFilter
    operator: str = "eq"

    def resolve(self, world:DoLWorld):
        """
        Pass the current world and resolve the rule once you're running
        inside the world functions
        """
        # print(f"Running {self.option} '{self.operator}', '{self.value}'")

        if type(self.option).__name__ == ROptionFilter.__name__: option = self.option.resolve(world)
        else: option = getattr(world.options, DOL_OPTION_NAME[self.option])

        if type(self.value).__name__ == ROptionFilter.__name__: value = self.value.resolve(world)
        else: value = self.value

        match self.operator:
            case "eq": final = option == value
            case "ne": final = option != value
            case "gt": final = option > value
            case "lt": final = option < value
            case "ge": final = option >= value
            case "le": final = option <= value
            case "contains": final = value in option
            case "not-contains": final = not (value in option)
            case "in": final = option in value
            case "not-in": final = not (option in value)
            case "and": final = option and value
            case "or": final = option or value
            case _: raise ValueError("Invalid ROptionFilter Operator")
        # print(f"Resolution for {self.option}: '{option}', '{self.operator}', '{value}' IS {final}")
        return final

    def convert(self):
        """
        Returns an OptionFilter of the current data
        Current data must follow OptionFilter construction requirements 
        (normal operators, no ROptionFilter in option or value)
        """
        return OptionFilter(self.option, self.value, self.operator)

    def __and__(self, other:'ROptionFilter' | bool | str | int):
        return ROptionFilter(ROptionFilter(self.option, self.value, self.operator), other, "and")
    
    def __rand__(self, other:'ROptionFilter' | bool | str | int):
        return self.__and__(self.option, other, "and")
    
    def __or__(self, other:'ROptionFilter' | bool | str | int):
        return ROptionFilter(ROptionFilter(self.option, self.value, self.operator), other, "or")

    def __ror__(self, other:'ROptionFilter' | bool | str | int):
        return self.__or__(self.option, other, "or")

    def __invert__(self):
        # Reminder:
        # (True == False) = False
        # (False == False) = True
        return ROptionFilter(self.option, False)

    def __bool__(self):
        raise TypeError("Use '|', '&', and '~' to handle rules")


class DoLOptionFilters(Enum):
    # -- Convience Rules
    f = ROptionFilter(RandomizationTargets, "false", operator="contains")

    # -- World Options:
    toggle_anal                  = ROptionFilter(GameWorldOptions, OptionsLocalization.toggle_anal.value,                    operator="contains")
    toggle_lactation             = ROptionFilter(GameWorldOptions, OptionsLocalization.toggle_lactation.value,               operator="contains")
    toggle_softvore              = ROptionFilter(GameWorldOptions, OptionsLocalization.toggle_softvore.value,                operator="contains")
    toggle_bodywriting           = ROptionFilter(GameWorldOptions, OptionsLocalization.toggle_bodywriting.value,             operator="contains")
    toggle_bestiality            = ROptionFilter(GameWorldOptions, OptionsLocalization.toggle_bestiality.value,              operator="contains")
    toggle_monsterpeople         = ROptionFilter(GameWorldOptions, OptionsLocalization.toggle_monsterpeople.value,           operator="contains")
    toggle_pregnancy             = ROptionFilter(GameWorldOptions, OptionsLocalization.toggle_pregnancy.value,               operator="contains")
    toggle_parasiticpregnancy    = ROptionFilter(GameWorldOptions, OptionsLocalization.toggle_parapregnancy.value,           operator="contains")
    toggle_transformation_animal = ROptionFilter(GameWorldOptions, OptionsLocalization.toggle_animaltransformations.value,   operator="contains")
    toggle_transformation_divine = ROptionFilter(GameWorldOptions, OptionsLocalization.toggle_divinetransformations.value,   operator="contains")


    toggle_tentacles   = ROptionFilter(GameAnimalOptions, OptionsLocalization.animal_tentacles.value,   operator="contains")
    toggle_parasites   = ROptionFilter(GameAnimalOptions, OptionsLocalization.animal_parasites.value,   operator="contains")
    toggle_swarms      = ROptionFilter(GameAnimalOptions, OptionsLocalization.animal_swarms.value,      operator="contains")
    toggle_bees        = ROptionFilter(GameAnimalOptions, OptionsLocalization.animal_bees.value,        operator="contains")
    toggle_slugs       = ROptionFilter(GameAnimalOptions, OptionsLocalization.animal_slugs.value,       operator="contains")
    toggle_slimes      = ROptionFilter(GameAnimalOptions, OptionsLocalization.animal_slimes.value,      operator="contains")


    # -- World Location Enable/Disables:
    type_antiques       = ROptionFilter(RandomizationTargets, OptionsLocalization.target_antiques.value,          operator="contains")
    type_skills         = ROptionFilter(RandomizationTargets, OptionsLocalization.target_skills.value,            operator="contains")
    type_feat           = ROptionFilter(RandomizationTargets, OptionsLocalization.target_feats.value,             operator="contains")
    type_transformation = ROptionFilter(RandomizationTargets, OptionsLocalization.target_transformations.value,   operator="contains")
    type_upgrade        = ROptionFilter(RandomizationTargets, OptionsLocalization.target_areaupgrades.value,      operator="contains")
    type_accessitem     = ROptionFilter(RandomizationTargets, OptionsLocalization.target_areaunlocks.value,       operator="contains")
    

    req_feat_copper    = ROptionFilter(RandomizationTargetRequirements, OptionsLocalization.req_featcopper.value,       operator="contains")
    req_feat_silver    = ROptionFilter(RandomizationTargetRequirements, OptionsLocalization.req_featsilver.value,       operator="contains")
    req_feat_gold      = ROptionFilter(RandomizationTargetRequirements, OptionsLocalization.req_featgold.value,         operator="contains")
    req_feat_platinum  = ROptionFilter(RandomizationTargetRequirements, OptionsLocalization.req_featplatinum.value,     operator="contains")
    req_feat_jeweled   = ROptionFilter(RandomizationTargetRequirements, OptionsLocalization.req_featjeweled.value,      operator="contains")
    req_transformation = ROptionFilter(RandomizationTargetRequirements, OptionsLocalization.req_transformation.value,   operator="contains")
    req_loveinterest   = ROptionFilter(RandomizationTargetRequirements, OptionsLocalization.req_loveinterest.value,     operator="contains")
    req_badend         = ROptionFilter(RandomizationTargetRequirements, OptionsLocalization.req_badend.value,           operator="contains")
    req_multipleruns   = ROptionFilter(RandomizationTargetRequirements, OptionsLocalization.req_multipleruns.value,     operator="contains")
    req_difficult      = ROptionFilter(RandomizationTargetRequirements, OptionsLocalization.req_difficult.value,        operator="contains")
    req_seasonal       = ROptionFilter(RandomizationTargetRequirements, OptionsLocalization.req_seasonal.value,         operator="contains")

    _tf_parts = f
    _tf_full = f
    # _tf_parts = ROptionFilter(RandomizeTransformationsType, RandomizeTransformationsType.option_tfparts)
    # _tf_full  = ROptionFilter(RandomizeTransformationsType, RandomizeTransformationsType.option_transformations)

    # NOTE: do not need to add these to gen rules for feats, since its still possible to get them
    # type_upgrade_alexfarm       = ROptionFilter(RandomizeUpgradesType, OptionsLocalization.upgrade_alexfarm.value,         operator="contains")
    # type_upgrade_tentacleforest = ROptionFilter(RandomizeUpgradesType, OptionsLocalization.upgrade_tentacleforest.value,   operator="contains")
    # type_upgrade_general        = ROptionFilter(RandomizeUpgradesType, OptionsLocalization.upgrade_general.value,          operator="contains")
    # type_upgrade_loft           = ROptionFilter(RandomizeUpgradesType, OptionsLocalization.upgrade_orphanageloft.value,    operator="contains")
    type_upgrade_alexfarm = f
    type_upgrade_tentacleforest = f
    type_upgrade_general = f
    type_upgrade_loft = f


    # -- Or States
    tentacles_or_bestiality          = toggle_bestiality | toggle_tentacles
    lactation_or_multipleruns        = req_multipleruns | toggle_lactation
    statrandomized_or_multipleruns   = type_skills | req_multipleruns
    bestiality_or_monsterpeople      = toggle_bestiality | toggle_monsterpeople
    bestiality_or_softvore_or_swarms = toggle_bestiality | toggle_softvore | toggle_swarms
    toggle_transformation_either     = toggle_transformation_animal | toggle_transformation_divine


    # -- Overrides
    # rules to create more locations or less items if needed
    filler_override                = type_antiques | type_skills | (type_feat & (req_feat_copper | req_feat_silver))
    override_feat_transformation   = (~type_feat) & (_tf_parts | _tf_full)
    override_feat_upgrade          = (~type_feat) & type_upgrade
    # override_feat_upgrade_alex     = override_feat_upgrade & type_upgrade_alexfarm
    override_feat_upgrade_tentacle = override_feat_upgrade & type_upgrade_tentacleforest
    override_feat_upgrade_general  = override_feat_upgrade & type_upgrade_general


    # -- Post Overrides
    randomize_tf_parts = _tf_parts & filler_override
    randomize_tf_full = _tf_full | (_tf_parts & ~filler_override)
    randomize_tf_either = _tf_parts | _tf_full

    req_angel = (randomize_tf_either & req_transformation) | req_multipleruns


class DoLRules(Enum):
    # optionfilter...
    # if option X equals option_foo (or whatever is set as condition) 
    # return true or false
    # if true resolve rule as normal
    # else rule = filtered_resolution
    # Filtered() needs all optionfilters to be true


    # -- Convinence Rules
    f = False_()
    t = True_()


    # -- OptionFilters
    # Do NOT add to this unless they're included inside rules.
    # Use DoLGenRules for generation rules
    type_antique                = DoLOptionFilters.type_antiques.value.convert()
    type_skills                 = DoLOptionFilters.type_skills.value.convert()
    type_upgrade                = DoLOptionFilters.type_upgrade.value.convert()
    type_upgrade_alexfarm       = DoLOptionFilters.type_upgrade_alexfarm.value.convert()
    type_upgrade_tentacleforest = DoLOptionFilters.type_upgrade_tentacleforest.value.convert()
    type_upgrade_general        = DoLOptionFilters.type_upgrade_general.value.convert()
    type_accessitem             = DoLOptionFilters.type_accessitem.value.convert()
    type_transformation         = DoLOptionFilters.type_transformation.value.convert()
    
    type_badend                 = DoLOptionFilters.req_badend.value.convert()
    type_seasonal               = DoLOptionFilters.req_seasonal.value.convert()

    toggle_transformation_animal = DoLOptionFilters.toggle_transformation_animal.value.convert()
    toggle_transformation_divine = DoLOptionFilters.toggle_transformation_divine.value.convert()

    toggle_tentacles     = DoLOptionFilters.toggle_tentacles.value.convert()
    toggle_slimes        = DoLOptionFilters.toggle_slimes.value.convert()
    toggle_monsterpeople = DoLOptionFilters.toggle_monsterpeople.value.convert()

    # If option is True, resolve as normal resolution, which is False
    # If option is False, resolve as filtered resolution, which is True
    type_upgrade_false                 = Filtered(f, options=[type_upgrade], filtered_resolution=True)
    type_skills_false                  = Filtered(f, options=[type_skills], filtered_resolution=True)
    type_upgrade_tentacleforest_false  = Filtered(f, options=[type_upgrade_tentacleforest, type_upgrade], filtered_resolution=True)
    type_upgrade_alexfarm_false        = Filtered(f, options=[type_upgrade_alexfarm], filtered_resolution=True)
    type_upgrade_general_false         = Filtered(f, options=[type_upgrade_general, type_upgrade], filtered_resolution=True)
    type_accessitem_false              = Filtered(f, options=[type_accessitem], filtered_resolution=True)
    type_antique_false                 = Filtered(f, options=[type_antique], filtered_resolution=True)
    type_transformation_false          = Filtered(f, options=[type_transformation], filtered_resolution=True)


    # -- Skill Rank Items:
    skulduggery_1  = Has(DoLItemNames.progressive_skulduggery_rank.value, 1)  | type_skills_false   # F+ 
    skulduggery_2  = Has(DoLItemNames.progressive_skulduggery_rank.value, 2)  | type_skills_false   # D
    skulduggery_3  = Has(DoLItemNames.progressive_skulduggery_rank.value, 3)  | type_skills_false   # D+
    skulduggery_4  = Has(DoLItemNames.progressive_skulduggery_rank.value, 4)  | type_skills_false   # C
    skulduggery_5  = Has(DoLItemNames.progressive_skulduggery_rank.value, 5)  | type_skills_false   # C+
    skulduggery_6  = Has(DoLItemNames.progressive_skulduggery_rank.value, 6)  | type_skills_false   # B
    skulduggery_7  = Has(DoLItemNames.progressive_skulduggery_rank.value, 7)  | type_skills_false   # B+
    skulduggery_8  = Has(DoLItemNames.progressive_skulduggery_rank.value, 8)  | type_skills_false   # A
    skulduggery_9  = Has(DoLItemNames.progressive_skulduggery_rank.value, 9)  | type_skills_false   # A+
    skulduggery_10 = Has(DoLItemNames.progressive_skulduggery_rank.value, 10) | type_skills_false   # S

    dancing_1  = Has(DoLItemNames.progressive_dancing_rank.value, 1)  | type_skills_false   # F+
    dancing_2  = Has(DoLItemNames.progressive_dancing_rank.value, 2)  | type_skills_false   # D
    dancing_3  = Has(DoLItemNames.progressive_dancing_rank.value, 3)  | type_skills_false   # D+
    dancing_4  = Has(DoLItemNames.progressive_dancing_rank.value, 4)  | type_skills_false   # C
    dancing_5  = Has(DoLItemNames.progressive_dancing_rank.value, 5)  | type_skills_false   # C+
    dancing_6  = Has(DoLItemNames.progressive_dancing_rank.value, 6)  | type_skills_false   # B
    dancing_7  = Has(DoLItemNames.progressive_dancing_rank.value, 7)  | type_skills_false   # B+
    dancing_8  = Has(DoLItemNames.progressive_dancing_rank.value, 8)  | type_skills_false   # A
    dancing_9  = Has(DoLItemNames.progressive_dancing_rank.value, 9)  | type_skills_false   # A+
    dancing_10 = Has(DoLItemNames.progressive_dancing_rank.value, 10) | type_skills_false   # S

    swimming_1  = Has(DoLItemNames.progressive_swimming_rank.value, 1)  | type_skills_false   # F+
    swimming_2  = Has(DoLItemNames.progressive_swimming_rank.value, 2)  | type_skills_false   # D
    swimming_3  = Has(DoLItemNames.progressive_swimming_rank.value, 3)  | type_skills_false   # D+
    swimming_4  = Has(DoLItemNames.progressive_swimming_rank.value, 4)  | type_skills_false   # C
    swimming_5  = Has(DoLItemNames.progressive_swimming_rank.value, 5)  | type_skills_false   # C+
    swimming_6  = Has(DoLItemNames.progressive_swimming_rank.value, 6)  | type_skills_false   # B
    swimming_7  = Has(DoLItemNames.progressive_swimming_rank.value, 7)  | type_skills_false   # B+
    swimming_8  = Has(DoLItemNames.progressive_swimming_rank.value, 8)  | type_skills_false   # A
    swimming_9  = Has(DoLItemNames.progressive_swimming_rank.value, 9)  | type_skills_false   # A+
    swimming_10 = Has(DoLItemNames.progressive_swimming_rank.value, 10) | type_skills_false   # S

    athletics_1  = Has(DoLItemNames.progressive_athletics_rank.value, 1)  | type_skills_false   # F+
    athletics_2  = Has(DoLItemNames.progressive_athletics_rank.value, 2)  | type_skills_false   # D
    athletics_3  = Has(DoLItemNames.progressive_athletics_rank.value, 3)  | type_skills_false   # D+
    athletics_4  = Has(DoLItemNames.progressive_athletics_rank.value, 4)  | type_skills_false   # C
    athletics_5  = Has(DoLItemNames.progressive_athletics_rank.value, 5)  | type_skills_false   # C+
    athletics_6  = Has(DoLItemNames.progressive_athletics_rank.value, 6)  | type_skills_false   # B
    athletics_7  = Has(DoLItemNames.progressive_athletics_rank.value, 7)  | type_skills_false   # B+
    athletics_8  = Has(DoLItemNames.progressive_athletics_rank.value, 8)  | type_skills_false   # A
    athletics_9  = Has(DoLItemNames.progressive_athletics_rank.value, 9)  | type_skills_false   # A+
    athletics_10 = Has(DoLItemNames.progressive_athletics_rank.value, 10) | type_skills_false   # S

    tending_1  = Has(DoLItemNames.progressive_tending_rank.value, 1)  | type_skills_false   # F+
    tending_2  = Has(DoLItemNames.progressive_tending_rank.value, 2)  | type_skills_false   # D
    tending_3  = Has(DoLItemNames.progressive_tending_rank.value, 3)  | type_skills_false   # D+
    tending_4  = Has(DoLItemNames.progressive_tending_rank.value, 4)  | type_skills_false   # C
    tending_5  = Has(DoLItemNames.progressive_tending_rank.value, 5)  | type_skills_false   # C+
    tending_6  = Has(DoLItemNames.progressive_tending_rank.value, 6)  | type_skills_false   # B
    tending_7  = Has(DoLItemNames.progressive_tending_rank.value, 7)  | type_skills_false   # B+
    tending_8  = Has(DoLItemNames.progressive_tending_rank.value, 8)  | type_skills_false   # A
    tending_9  = Has(DoLItemNames.progressive_tending_rank.value, 9)  | type_skills_false   # A+
    tending_10 = Has(DoLItemNames.progressive_tending_rank.value, 10) | type_skills_false   # S

    housekeeping_1  = Has(DoLItemNames.progressive_housekeeping_rank.value, 1)  | type_skills_false   # F+
    housekeeping_2  = Has(DoLItemNames.progressive_housekeeping_rank.value, 2)  | type_skills_false   # D
    housekeeping_3  = Has(DoLItemNames.progressive_housekeeping_rank.value, 3)  | type_skills_false   # D+
    housekeeping_4  = Has(DoLItemNames.progressive_housekeeping_rank.value, 4)  | type_skills_false   # C
    housekeeping_5  = Has(DoLItemNames.progressive_housekeeping_rank.value, 5)  | type_skills_false   # C+
    housekeeping_6  = Has(DoLItemNames.progressive_housekeeping_rank.value, 6)  | type_skills_false   # B
    housekeeping_7  = Has(DoLItemNames.progressive_housekeeping_rank.value, 7)  | type_skills_false   # B+
    housekeeping_8  = Has(DoLItemNames.progressive_housekeeping_rank.value, 8)  | type_skills_false   # A
    housekeeping_9  = Has(DoLItemNames.progressive_housekeeping_rank.value, 9)  | type_skills_false   # A+
    housekeeping_10 = Has(DoLItemNames.progressive_housekeeping_rank.value, 10) | type_skills_false   # S

    seduction_1 = Has(DoLItemNames.progressive_seduction_rank.value, 1) | type_skills_false  # D
    seduction_2 = Has(DoLItemNames.progressive_seduction_rank.value, 2) | type_skills_false  # C
    seduction_3 = Has(DoLItemNames.progressive_seduction_rank.value, 3) | type_skills_false  # B
    seduction_4 = Has(DoLItemNames.progressive_seduction_rank.value, 4) | type_skills_false  # A
    seduction_5 = Has(DoLItemNames.progressive_seduction_rank.value, 5) | type_skills_false  # S

    oral_1 = Has(DoLItemNames.progressive_oral_rank.value, 1) | type_skills_false  # D
    oral_2 = Has(DoLItemNames.progressive_oral_rank.value, 2) | type_skills_false  # C
    oral_3 = Has(DoLItemNames.progressive_oral_rank.value, 3) | type_skills_false  # B
    oral_4 = Has(DoLItemNames.progressive_oral_rank.value, 4) | type_skills_false  # A
    oral_5 = Has(DoLItemNames.progressive_oral_rank.value, 5) | type_skills_false  # S

    chest_1 = Has(DoLItemNames.progressive_chest_rank.value, 1) | type_skills_false  # D
    chest_2 = Has(DoLItemNames.progressive_chest_rank.value, 2) | type_skills_false  # C
    chest_3 = Has(DoLItemNames.progressive_chest_rank.value, 3) | type_skills_false  # B
    chest_4 = Has(DoLItemNames.progressive_chest_rank.value, 4) | type_skills_false  # A
    chest_5 = Has(DoLItemNames.progressive_chest_rank.value, 5) | type_skills_false  # S

    hands_1 = Has(DoLItemNames.progressive_hands_rank.value, 1) | type_skills_false  # D
    hands_2 = Has(DoLItemNames.progressive_hands_rank.value, 2) | type_skills_false  # C
    hands_3 = Has(DoLItemNames.progressive_hands_rank.value, 3) | type_skills_false  # B
    hands_4 = Has(DoLItemNames.progressive_hands_rank.value, 4) | type_skills_false  # A
    hands_5 = Has(DoLItemNames.progressive_hands_rank.value, 5) | type_skills_false  # S

    buttocks_1 = Has(DoLItemNames.progressive_buttocks_rank.value, 1) | type_skills_false  # D
    buttocks_2 = Has(DoLItemNames.progressive_buttocks_rank.value, 2) | type_skills_false  # C
    buttocks_3 = Has(DoLItemNames.progressive_buttocks_rank.value, 3) | type_skills_false  # B
    buttocks_4 = Has(DoLItemNames.progressive_buttocks_rank.value, 4) | type_skills_false  # A
    buttocks_5 = Has(DoLItemNames.progressive_buttocks_rank.value, 5) | type_skills_false  # S

    privates_1 = Has(DoLItemNames.progressive_privates_rank.value, 1) | type_skills_false  # D
    privates_2 = Has(DoLItemNames.progressive_privates_rank.value, 2) | type_skills_false  # C
    privates_3 = Has(DoLItemNames.progressive_privates_rank.value, 3) | type_skills_false  # B
    privates_4 = Has(DoLItemNames.progressive_privates_rank.value, 4) | type_skills_false  # A
    privates_5 = Has(DoLItemNames.progressive_privates_rank.value, 5) | type_skills_false  # S

    anal_1 = Has(DoLItemNames.progressive_anal_rank.value, 1) | type_skills_false  # D
    anal_2 = Has(DoLItemNames.progressive_anal_rank.value, 2) | type_skills_false  # C
    anal_3 = Has(DoLItemNames.progressive_anal_rank.value, 3) | type_skills_false  # B
    anal_4 = Has(DoLItemNames.progressive_anal_rank.value, 4) | type_skills_false  # A
    anal_5 = Has(DoLItemNames.progressive_anal_rank.value, 5) | type_skills_false  # S

    thighs_1 = Has(DoLItemNames.progressive_thighs_rank.value, 1) | type_skills_false  # D
    thighs_2 = Has(DoLItemNames.progressive_thighs_rank.value, 2) | type_skills_false  # C
    thighs_3 = Has(DoLItemNames.progressive_thighs_rank.value, 3) | type_skills_false  # B
    thighs_4 = Has(DoLItemNames.progressive_thighs_rank.value, 4) | type_skills_false  # A
    thighs_5 = Has(DoLItemNames.progressive_thighs_rank.value, 5) | type_skills_false  # S

    feet_1 = Has(DoLItemNames.progressive_feet_rank.value, 1) | type_skills_false  # D
    feet_2 = Has(DoLItemNames.progressive_feet_rank.value, 2) | type_skills_false  # C
    feet_3 = Has(DoLItemNames.progressive_feet_rank.value, 3) | type_skills_false  # B
    feet_4 = Has(DoLItemNames.progressive_feet_rank.value, 4) | type_skills_false  # A
    feet_5 = Has(DoLItemNames.progressive_feet_rank.value, 5) | type_skills_false  # S

    science_1 = Has(DoLItemNames.progressive_science_rank.value, 1) | type_skills_false  # D : 0 : trait0
    science_2 = Has(DoLItemNames.progressive_science_rank.value, 2) | type_skills_false  # C : 1 : trait1
    science_3 = Has(DoLItemNames.progressive_science_rank.value, 3) | type_skills_false  # B : 2 : trait2
    science_4 = Has(DoLItemNames.progressive_science_rank.value, 4) | type_skills_false  # A : 3 : trait4
    science_5 = Has(DoLItemNames.progressive_science_rank.value, 5) | type_skills_false  # A* : 4 : traitx

    math_1 = Has(DoLItemNames.progressive_math_rank.value, 1) | type_skills_false  # D : 0 : trait0
    math_2 = Has(DoLItemNames.progressive_math_rank.value, 2) | type_skills_false  # C : 1 : trait1
    math_3 = Has(DoLItemNames.progressive_math_rank.value, 3) | type_skills_false  # B : 2 : trait2
    math_4 = Has(DoLItemNames.progressive_math_rank.value, 4) | type_skills_false  # A : 3 : trait4
    math_5 = Has(DoLItemNames.progressive_math_rank.value, 5) | type_skills_false  # A* : 4 : traitx

    english_1 = Has(DoLItemNames.progressive_english_rank.value, 1) | type_skills_false  # D : 0 : trait0
    english_2 = Has(DoLItemNames.progressive_english_rank.value, 2) | type_skills_false  # C : 1 : trait1
    english_3 = Has(DoLItemNames.progressive_english_rank.value, 3) | type_skills_false  # B : 2 : trait2
    english_4 = Has(DoLItemNames.progressive_english_rank.value, 4) | type_skills_false  # A : 3 : trait4
    english_5 = Has(DoLItemNames.progressive_english_rank.value, 5) | type_skills_false  # A* : 4 : traitx

    history_1 = Has(DoLItemNames.progressive_history_rank.value, 1) | type_skills_false  # D : 0 : trait0
    history_2 = Has(DoLItemNames.progressive_history_rank.value, 2) | type_skills_false  # C : 1 : trait1
    history_3 = Has(DoLItemNames.progressive_history_rank.value, 3) | type_skills_false  # B : 2 : trait2
    history_4 = Has(DoLItemNames.progressive_history_rank.value, 4) | type_skills_false  # A : 3 : trait4
    history_5 = Has(DoLItemNames.progressive_history_rank.value, 5) | type_skills_false  # A* : 4 : traitx

    willpower_1 = Has(DoLItemNames.progressive_willpower_rank.value, 1) | type_skills_false  # fainthearted
    willpower_2 = Has(DoLItemNames.progressive_willpower_rank.value, 2) | type_skills_false  # mindful
    willpower_3 = Has(DoLItemNames.progressive_willpower_rank.value, 3) | type_skills_false  # resolved
    willpower_4 = Has(DoLItemNames.progressive_willpower_rank.value, 4) | type_skills_false  # determined
    willpower_5 = Has(DoLItemNames.progressive_willpower_rank.value, 5) | type_skills_false  # tenacious
    willpower_6 = Has(DoLItemNames.progressive_willpower_rank.value, 6) | type_skills_false  # iron

    physique_1 = Has(DoLItemNames.progressive_physique_rank.value, 1) | type_skills_false  # skinny
    physique_2 = Has(DoLItemNames.progressive_physique_rank.value, 2) | type_skills_false  # slender
    physique_3 = Has(DoLItemNames.progressive_physique_rank.value, 3) | type_skills_false  # slim
    physique_4 = Has(DoLItemNames.progressive_physique_rank.value, 4) | type_skills_false  # athletic
    physique_5 = Has(DoLItemNames.progressive_physique_rank.value, 5) | type_skills_false  # firm
    physique_6 = Has(DoLItemNames.progressive_physique_rank.value, 6) | type_skills_false  # powerful

    promiscuity_1 = Has(DoLItemNames.progressive_promiscuity_rank.value, 1) | type_skills_false  # prudish
    promiscuity_2 = Has(DoLItemNames.progressive_promiscuity_rank.value, 2) | type_skills_false  # curious
    promiscuity_3 = Has(DoLItemNames.progressive_promiscuity_rank.value, 3) | type_skills_false  # excited
    promiscuity_4 = Has(DoLItemNames.progressive_promiscuity_rank.value, 4) | type_skills_false  # crave
    promiscuity_5 = Has(DoLItemNames.progressive_promiscuity_rank.value, 5) | type_skills_false  # slut
    promiscuity_6 = Has(DoLItemNames.progressive_promiscuity_rank.value, 6) | type_skills_false  # insatiable

    exhibitionism_1 = Has(DoLItemNames.progressive_exhibitionism_rank.value, 1) | type_skills_false  # shy
    exhibitionism_2 = Has(DoLItemNames.progressive_exhibitionism_rank.value, 2) | type_skills_false  # like
    exhibitionism_3 = Has(DoLItemNames.progressive_exhibitionism_rank.value, 3) | type_skills_false  # enjoy
    exhibitionism_4 = Has(DoLItemNames.progressive_exhibitionism_rank.value, 4) | type_skills_false  # excites
    exhibitionism_5 = Has(DoLItemNames.progressive_exhibitionism_rank.value, 5) | type_skills_false  # shameless
    exhibitionism_6 = Has(DoLItemNames.progressive_exhibitionism_rank.value, 6) | type_skills_false  # wild

    deviancy_1 = Has(DoLItemNames.progressive_deviancy_rank.value, 1) | type_skills_false  # conventional
    deviancy_2 = Has(DoLItemNames.progressive_deviancy_rank.value, 2) | type_skills_false  # strange
    deviancy_3 = Has(DoLItemNames.progressive_deviancy_rank.value, 3) | type_skills_false  # shocking
    deviancy_4 = Has(DoLItemNames.progressive_deviancy_rank.value, 4) | type_skills_false  # scandalous
    deviancy_5 = Has(DoLItemNames.progressive_deviancy_rank.value, 5) | type_skills_false  # crave
    deviancy_6 = Has(DoLItemNames.progressive_deviancy_rank.value, 6) | type_skills_false  # lust
    # if needed later add weapon skills here too


    # -- Museum Items:
    antiques_10 = HasGroupUnique(DoLLocationTypes.antique.value, 10) | type_antique_false
    antiques_20 = HasGroupUnique(DoLLocationTypes.antique.value, 20) | type_antique_false
    has_serpentpainting = Has(DoLItemNames.antique_serpentpainting.value)


    # -- Transformations Items:
    # Only need tffalse on tffull since rules collapse that way
    tfrule_angelfull         = Has(DoLItemNames.transformation_angelfull.value) | type_transformation_false
    
    tfrule_demonfull         = Has(DoLItemNames.transformation_demonfull.value) | type_transformation_false
    tfrule_demonappear       = Has(DoLItemNames.transformation_demonappear.value)
    tfrule_demon_full_appear = tfrule_demonfull | tfrule_demonappear
    
    tfrule_fallenangelfull   = Has(DoLItemNames.transformation_fallenangelfull.value) | type_transformation_false

    tfrule_wolffull          = Has(DoLItemNames.transformation_wolffull.value) | type_transformation_false
    tfrule_wolfappear        = Has(DoLItemNames.transformation_wolfappear.value)
    tfrule_wolf_full_appear  = tfrule_wolffull | tfrule_wolfappear
    
    tfrule_harpyfull         = Has(DoLItemNames.transformation_harpyfull.value) | type_transformation_false
    tfrule_harpyappear       = Has(DoLItemNames.transformation_harpyappear.value)
    tfrule_harpy_full_appear = tfrule_harpyfull | tfrule_harpyappear

    tfrule_foxfull           = Has(DoLItemNames.transformation_foxfull.value) | type_transformation_false
    tfrule_foxapper          = Has(DoLItemNames.transformation_foxappear.value)
    tfrule_fox_full_appear   = tfrule_foxfull | tfrule_foxapper
    
    tfrule_wings             = tfrule_demonfull | tfrule_angelfull | tfrule_harpyfull | Has(DoLItemNames.transformation_wings.value)
    # reminder: recoding flight to include any wings instead of harpy wings
    tfrule_flight            = tfrule_wings & Has(DoLItemNames.transformation_flight.value) | type_transformation_false


    # -- Area Access General:
    access_intown               = CanReachRegion(DoLRegionNames.in_town.value)
    access_orphanage            = CanReachRegion(DoLRegionNames.orphanage.value)
    access_school               = CanReachRegion(DoLRegionNames.school.value)
    access_remyfarm             = CanReachRegion(DoLRegionNames.remy_farm.value)
    access_averymansion         = CanReachRegion(DoLRegionNames.avery_mansion.value)
    access_park                 = CanReachRegion(DoLRegionNames.park.value)
    access_temple               = CanReachRegion(DoLRegionNames.temple.value)
    access_residentialdrain     = CanReachRegion(DoLRegionNames.residential_drain.value)
    access_commercialdrain      = CanReachRegion(DoLRegionNames.commercial_drain.value)
    access_industrialdrain      = CanReachRegion(DoLRegionNames.industrial_drain.value)
    access_forest               = CanReachRegion(DoLRegionNames.forest.value)
    access_beach                = CanReachRegion(DoLRegionNames.beach.value)
    access_cliffstreet          = CanReachRegion(DoLRegionNames.cliff_street.value)
    access_oxfordstreet         = CanReachRegion(DoLRegionNames.oxford_street.value)
    access_moor                 = CanReachRegion(DoLRegionNames.moor.value)
    access_pub                  = CanReachRegion(DoLRegionNames.pub.value)
    access_landfill             = CanReachRegion(DoLRegionNames.landfill.value)
    access_photography          = CanReachRegion(DoLRegionNames.photography_studio.value)
    access_adultshop            = CanReachRegion(DoLRegionNames.adult_shop.value)
    access_brothel              = CanReachRegion(DoLRegionNames.brothel.value)
    access_birdtower            = CanReachRegion(DoLRegionNames.bird_tower.value)
    access_kylarmanor           = CanReachRegion(DoLRegionNames.kylar_manor.value)
    access_museum               = CanReachRegion(DoLRegionNames.museum.value)
    access_tentacleforest       = CanReachRegion(DoLRegionNames.tentacle_forest.value)
    access_mayorsoffice         = CanReachRegion(DoLRegionNames.mayors_office.value)
    access_oldsewers            = CanReachRegion(DoLRegionNames.old_sewers.value)
    access_compound             = CanReachRegion(DoLRegionNames.compound.value)
    access_prison               = CanReachRegion(DoLRegionNames.prison.value)
    access_wolfcave             = CanReachRegion(DoLRegionNames.wolf_cave.value)
    access_tentacleplains       = CanReachRegion(DoLRegionNames.tentacle_plains.value)
    access_alexfarm             = CanReachRegion(DoLRegionNames.alex_farm.value)
    access_forestlake           = CanReachRegion(DoLRegionNames.forest_lake.value)
    access_dancestudio          = CanReachRegion(DoLRegionNames.dance_studio.value)
    access_farmlands            = CanReachRegion(DoLRegionNames.farmlands.value)
    access_ridingschool         = CanReachRegion(DoLRegionNames.riding_school.value)
    access_meadow               = CanReachRegion(DoLRegionNames.meadow.value)
    access_island               = CanReachRegion(DoLRegionNames.island.value)
    access_pirateship           = CanReachRegion(DoLRegionNames.pirate_ship.value)
    access_shoppingcentre       = CanReachRegion(DoLRegionNames.shopping_centre.value)
    access_forestshop           = CanReachRegion(DoLRegionNames.forest_shop.value)
    access_connudatusstreet     = CanReachRegion(DoLRegionNames.connudatus_street.value)
    access_asylum               = CanReachRegion(DoLRegionNames.asylum.value)
    access_edencabin            = CanReachRegion(DoLRegionNames.eden_cabin.value)
    access_costalpath           = CanReachRegion(DoLRegionNames.coastal_path.value)
    access_alleyway_residential = CanReachRegion(DoLRegionNames.residential_alleyways.value)
    access_alleyway_commercial  = CanReachRegion(DoLRegionNames.commercial_alleyways.value)
    access_alleyway_industrial  = CanReachRegion(DoLRegionNames.industrial_alleyways.value)
    access_hookahparlour        = CanReachRegion(DoLRegionNames.hookah_parlour.value)
    access_cafe                 = CanReachRegion(DoLRegionNames.cafe.value)
    access_pharmacy             = CanReachRegion(DoLRegionNames.pharmacy.value)
    access_ocean                = CanReachRegion(DoLRegionNames.ocean.value)
    access_docks                = CanReachRegion(DoLRegionNames.docks.value)
    access_officebuilding       = CanReachRegion(DoLRegionNames.office_building.value)
    access_danubehouses         = CanReachRegion(DoLRegionNames.danube_houses.value)
    access_domushouses          = CanReachRegion(DoLRegionNames.domus_houses.value)
    access_undergroundbrothel   = CanReachRegion(DoLRegionNames.underground_brothel.value)
    access_bog                  = CanReachRegion(DoLRegionNames.bog.value)
    access_arcade               = CanReachRegion(DoLRegionNames.arcade.value)
    access_soupkitchen          = CanReachRegion(DoLRegionNames.soup_kitchen.value)
    access_domusstreet          = CanReachRegion(DoLRegionNames.domus_street.value)
    access_stripclub            = CanReachRegion(DoLRegionNames.strip_club.value)
    access_barbstreet           = CanReachRegion(DoLRegionNames.barb_street.value)
    access_maze                 = CanReachRegion(DoLRegionNames.maze.value)


    # -- World Upgrades:
    access_upgrade_tentacleforest = access_tentacleforest & access_mayorsoffice

    # tent upgrades require their previous upgrade in the chain for non items
    # - Decend
    has_flatsbridge = (
        Has(DoLItemNames.upgrade_flatsbridge.value) | 
        (type_upgrade_tentacleforest_false & access_upgrade_tentacleforest))
    has_forestroad = (
        Has(DoLItemNames.upgrade_forestroad.value) | 
        (type_upgrade_tentacleforest_false & access_upgrade_tentacleforest & 
         access_barbstreet))
    has_fieldoffice = (
        Has(DoLItemNames.upgrade_fieldoffice.value) | 
        (type_upgrade_tentacleforest_false & access_upgrade_tentacleforest & 
         access_barbstreet & access_forest))
    # - Ascend
    has_residentialthicket = (
        Has(DoLItemNames.upgrade_residentialthicket.value) | 
        (type_upgrade_tentacleforest_false & access_upgrade_tentacleforest))
    has_schoolgreen = (
        Has(DoLItemNames.upgrade_schoolgreen.value) | 
        (type_upgrade_tentacleforest_false & access_upgrade_tentacleforest & 
         access_forestlake))
    has_hookahparlourownership = (
        Has(DoLItemNames.upgrade_hookahparlour.value) | 
        (type_upgrade_tentacleforest_false & access_upgrade_tentacleforest & 
         access_forestlake & access_alleyway_residential))
    
    has_adultshopbuilt = Has(DoLItemNames.upgrade_adultshop.value) | (type_upgrade_general_false & access_adultshop)

    has_farmparasitebarn = Has(DoLItemNames.upgrade_farm_parasite.value) | (access_alexfarm & type_upgrade_alexfarm_false & type_upgrade_false)
    has_farmwatchtower = Has(DoLItemNames.upgrade_farm_security.value, 1) | (access_alexfarm & type_upgrade_alexfarm_false & type_upgrade_false)
    

    # -- Access Items:
    has_adoptionpapers   = Has(DoLItemNames.accessitem_adoptionpapers.value)   | (type_accessitem_false & access_orphanage & access_domusstreet)
    has_fakeid           = Has(DoLItemNames.accessitem_fakeid.value)           | (type_accessitem_false & access_brothel)
    has_mazekey          = Has(DoLItemNames.accessitem_mazekey.value)          | (type_accessitem_false & access_domushouses)


    # -- Area Zone Access:
    access_alleyway = access_alleyway_commercial | access_alleyway_industrial | access_alleyway_residential
    access_recipe = access_school | access_averymansion
    access_eventstreet = access_intown | access_alleyway | access_park


    # -- Area Access Rules:
    # INFO Estate Access : by bluecat
    #
    # NOTE: estate includes a file called manor.twee, which is old and does not lead or enter from anywhere
    #
    # To get to the manor, you need to access via bluffing or the fence
    # Also required to get the job from wren or farm stage 5
    #
    # -- Bluffing: 
    # Skul 800, enter
    # 
    # -- Fence:
    # Requires Fence State "bird", "landry", or "secret"
    # Fence State 'secret' is set whenever you enter via bird or landry
    #
    # To get to landry state you just have to ask landry about it
    # after looking at the fence one time
    #
    # To get to bird state you just have to ask great hawk about it
    # after looking at the fence one time
    access_remyestate_rules = skulduggery_5 | access_pub | (access_birdtower & type_badend)

    # INFO Brothel Learning : by bluecat
    #
    # You can learn about the brothel via:
    # -- Brothel Punishment Gloryhole
    #   Pub Seducing or the one pill event to get a fame value high
    # -- Pub Fame Favour
    #   Getting any fame above 400 then going to pub for a random
    #   micky favour (most perm lowers and raises favours)
    # -- ':: Abduction'
    #   Passing out in an alley, park, or street, then
    #   being nice in the encounter
    # -- Strip Club Private Dance
    #   Dunno how to reach this one without strip club access,
    #   don't think its possible
    # -- Strip Club Proposition
    #   Leaving the Strip Club by not having an ID
    access_brothel_rules = access_pub | access_eventstreet | access_stripclub

    # INFO Landfill Access : by bluecat
    #
    # Any of these below:
    # 1. Robin is here
    # 2. Skul gte 800
    # 3. You have trash_key
    #
    # Trash key is unlocked by robbing the compound crystal
    # or searching in the trash once anywhere
    access_landfill_rules = (access_orphanage | skulduggery_8)

    # INFO Compound Access : by bluecat
    #
    # Requires one of:
    # 1. compound.card
    # 2. phials_held gte 1
    # After you get one of those, you can access anytime
    #
    # Compound Card
    # 1. Randomly by stealing in combat
    # 2. Micky Task (any perm raise/lower)
    #
    # Phials
    # Requires reaching stage 9 on the farm
    # and having Alex give you one in the Lab
    access_compound_rules = (access_pub | access_alexfarm | (access_eventstreet & skulduggery_2))


    # -- Outfits 1
    number_outfits = 56
    # NOTE!: outfit_witch, outfit_butterfly, outfit_greater_halloween
    # are all included in the parasites section due to Gwylan
    
    outfit_vampire = access_school # kylar
    outfit_mummy = access_forest # catacombs p  assout
    outfit_scarecrow = access_alexfarm # TODO: heroic victory
    outfit_skeleton = access_forest # catacombs access
    outfit_futuresuit = access_arcade # arcade game win
    outfit_pumpkin = access_recipe # 15 recipe
    outfit_christmas = access_domushouses # steal but leave 1k
    outfit_rosewedding = access_school # kylar dismissal
    # Robin Present Event / Forest Shop noticed steal twice
    outfit_wrap = ((access_orphanage & access_shoppingcentre & type_seasonal) | access_forestshop) 
    
    outfit_sshirt = access_undergroundbrothel
    outfit_sshirt_w = access_undergroundbrothel & type_badend
    outfit_cow = access_remyfarm
    outfit_cow_w = outfit_cow & type_badend
    outfit_prison = access_prison
    outfit_prison_w = outfit_prison & type_badend
    outfit_straightjacket = access_asylum
    outfit_straightjacket_w = outfit_straightjacket & type_badend
    outfit_bird = access_birdtower
    outfit_bird_w = outfit_bird & type_badend
    outfit_loincloth = (access_wolfcave | access_edencabin)
    outfit_loincloth_w = outfit_loincloth & type_badend
    outfit_islandermask = access_island # make mask
    outfit_islandermask_w = outfit_islandermask & type_badend

    outfit_initiate = access_temple
    outfit_monknun = access_temple
    outfit_evangelist = (access_temple & promiscuity_3)
    outfit_confessor = access_temple
    outfit_sparring = access_temple # other than temple no req
    outfit_stole = access_temple
    outfit_templesexy = t # inheritly obtainable anywhere
    outfit_exorcist = (access_dancestudio & skulduggery_10 & dancing_8)
    outfit_stonependant = access_temple # Cleaning Quarters # no min housekeep req
    outfit_holypendant = access_soupkitchen
    outfit_darkpendant = access_orphanage # Loft INTRO, just random orph event
    outfit_foxmask = access_domusstreet # avery card date
    outfit_foreign = access_school # leighton blackmail
    outfit_brothel = access_brothel # brothel show access
    outfit_chef = access_cafe # cafe reopening
    outfit_esotericspecs = (access_hookahparlour & has_hookahparlourownership)
    outfit_fedora = (access_stripclub & has_fakeid) # strip overhear
    outfit_catsuit = (access_docks & skulduggery_4) # container require ~4 skul
    outfit_janet = (access_school & english_4) # read book
    outfit_swam = (access_dancestudio & dancing_8) # dance jobs
    outfit_museum = (antiques_20 & swimming_9 & willpower_4) # ducking and horse
    outfit_vintage = (access_pub & access_museum) # warmest winter
    outfit_chain = (has_serpentpainting & access_museum) # hopeless cycle
    # moor shrine or fox tf
    outfit_shrine = (access_moor | (access_forest & toggle_transformation_animal))
    outfit_succubus = access_eventstreet # demon tf or 15 virginities

    # Outfit Sets, remider: halloween in parasites
    outfit_greater_valentines = (
        outfit_rosewedding & outfit_wrap
    )
    outfit_greater_badend = (
        outfit_sshirt & outfit_cow & outfit_prison &
        outfit_straightjacket & outfit_bird & outfit_loincloth
    )
    outfit_greater_badend_w = outfit_greater_badend & type_badend
    outfit_greater_temple = (
        outfit_initiate & outfit_monknun & outfit_evangelist &
        outfit_confessor & outfit_sparring & outfit_stole &
        outfit_templesexy & outfit_exorcist & outfit_stonependant &
        outfit_holypendant
    )
    outfit_greater_pendant = (
       outfit_stonependant & outfit_holypendant & outfit_darkpendant
    )
    outfit_greater_historic = (
        outfit_museum & outfit_vintage & outfit_chain
    )
    outfit_greater_transformation = (
        outfit_cow_w & outfit_bird & outfit_shrine &
        outfit_succubus
    )
    outfit_greater_mask = (
        outfit_islandermask & outfit_foxmask
    )

    list_outfit_nongwylan_nonparasitic = [
        outfit_greater_valentines,       outfit_greater_badend_w,    outfit_greater_temple,           
        outfit_greater_pendant,          outfit_greater_historic,    outfit_greater_transformation,   
        outfit_greater_mask,
        outfit_vampire,             outfit_mummy,           outfit_scarecrow,       
        outfit_skeleton,            outfit_futuresuit,      outfit_pumpkin,         
        outfit_christmas,           outfit_rosewedding,     outfit_wrap,            
        outfit_sshirt_w,            outfit_cow_w,           outfit_prison_w,        
        outfit_straightjacket_w,    outfit_bird_w,          outfit_loincloth_w,     
        outfit_initiate,            outfit_monknun,         outfit_evangelist,      
        outfit_confessor,           outfit_sparring,        outfit_stole,           
        outfit_templesexy,          outfit_exorcist,        outfit_stonependant,    
        outfit_holypendant,         outfit_darkpendant,     outfit_islandermask_w,  
        outfit_foxmask,             outfit_foreign,         outfit_brothel,         
        outfit_chef,                outfit_esotericspecs,   outfit_fedora,          
        outfit_catsuit,             outfit_janet,           outfit_swam,            
        outfit_museum,              outfit_vintage,         outfit_chain,            
        outfit_shrine,              outfit_succubus,
    ]


    # -- Parasites + Parasite Outfits
    # See broodmother feats for locations
    access_vore_nontentacle = (
        access_edencabin | access_forest | access_orphanage |
        access_forestlake | access_oldsewers
    )

    access_vore_tentacle = (
        (access_birdtower & tfrule_flight) |
        (access_docks & access_orphanage) |
        access_moor | access_beach | access_oldsewers |
        access_ocean | access_moor | access_beach
    )

    access_vore_either = (
        (access_birdtower & tfrule_flight) |
        (access_docks & access_orphanage) |
        access_moor | access_beach | access_oldsewers |
        access_ocean | access_moor | access_beach |
        access_edencabin | access_forest | access_orphanage |
        access_forestlake | access_oldsewers
    )

    access_para_tentacles = (
        (access_orphanage & toggle_slimes) |
        access_ocean | access_eventstreet | access_forest |
        access_forestlake | access_school | access_compound |
        access_vore_tentacle
    )
    outfit_witch = access_para_tentacles
    outfit_greater_halloween = (
        outfit_witch & outfit_vampire & outfit_mummy &
        outfit_scarecrow & outfit_skeleton & outfit_futuresuit &
        outfit_pumpkin
    )

    access_plantpeople = (
        access_forest | access_bog | access_moor |
        access_danubehouses | access_forestlake | 
        # not love % so just 50 flat (/2 because talk + outfit)
        AtLeast(math.ceil(50 * 0.5), outfit_witch, outfit_greater_halloween, *list_outfit_nongwylan_nonparasitic)
    )
    outfit_butterfly = access_plantpeople
    

    # small rules here
    access_para_pale = access_forestlake | access_forest
    access_para_bees = access_forest
    access_para_squid = access_ocean
    access_para_wasp = access_forest

    access_para_fish = (
        (access_beach & deviancy_5) |
        access_forestlake | access_officebuilding
    )
    access_para_snake = (
        (access_brothel & deviancy_5) |
        access_forest
    )
    access_para_spider = (
        (access_brothel & deviancy_5) |
        access_danubehouses
    )
    access_para_slime = (
        (access_hookahparlour & has_hookahparlourownership) |
        access_orphanage | access_prison | access_oldsewers |
        access_industrialdrain | access_residentialdrain | access_commercialdrain |
        access_maze | access_landfill
    )
    access_para_maggot = (
        (access_brothel & deviancy_5) |
        access_landfill
    )
    access_para_worm = (
        (access_brothel & deviancy_5) |
        (access_park & exhibitionism_1) |
        (access_undergroundbrothel & type_badend) |
        access_school
    )
    access_para_eel = (
        (access_brothel & deviancy_5) |
        access_ocean | access_beach | access_oldsewers |
        access_industrialdrain | access_residentialdrain | access_commercialdrain
    )
    access_para_lurker = (
        access_moor | access_forest | access_alexfarm
    )
    access_para_slug = (
        access_oldsewers | access_tentacleforest | access_island
    )
    access_para_vine = ( # no tending requirement
        access_farmlands | access_forest | access_forestlake |
        access_moor | access_edencabin | access_alexfarm | 
        access_temple | access_orphanage | access_plantpeople
    )

    access_parasite_delivery = (
        access_orphanage | access_forestlake | 
        (access_alexfarm & has_farmparasitebarn)
    )
    access_parasite_any = (
        access_para_pale | access_para_bees | access_para_squid |
        access_para_wasp | access_para_pale | access_para_tentacles |
        access_para_fish | access_para_snake | access_para_spider |
        access_para_slime | access_para_maggot | access_para_worm |
        access_para_eel | access_para_lurker | access_para_slug
    )
    access_parasite_all = (
        access_para_pale & access_para_bees & access_para_squid &
        access_para_wasp & access_para_pale & access_para_tentacles &
        access_para_fish & access_para_snake & access_para_spider &
        access_para_slime & access_para_maggot & access_para_worm &
        access_para_eel & access_para_lurker & access_para_slug
    )


    # -- Outfits Cont. + Gwylan
    list_outfit_parasitic = [outfit_witch, outfit_butterfly, outfit_greater_halloween]
    list_outfit_nongwylan = list_outfit_nongwylan_nonparasitic + list_outfit_parasitic


    # Gwylan Rules
    # NOTE: may need to recode these if outfits are randomized later
    # currently they don't use future outfits for love, but will
    # need to add future outfits if gotten from checks

    # Pre First Ritual
    # Jasper: Gold request
    outfit_jasper = ( # (/2 because talk + clothes)
        AtLeast(math.ceil(30 * 0.5), *list_outfit_nongwylan) & access_forestshop & 
        # Gold belt or gold items
        (access_forestlake) | (has_adultshopbuilt & access_adultshop)
    )

    # First Ritual
    gwylan_beast = AtLeast(math.ceil(50 * 0.5), outfit_jasper, *list_outfit_nongwylan) & access_forestshop
    firstverse = gwylan_beast

    # Second Ritual (love requirements start being % instead)
    gwylan_forestvessel = AtLeast(math.ceil(number_outfits * 0.65), outfit_jasper, *list_outfit_nongwylan) & access_forestshop
    outfit_flowers = access_school & (access_orphanage | access_birdtower) & gwylan_forestvessel
    outfit_sagehat = gwylan_forestvessel

    # Partners
    gwylan_partners = AtLeast(math.ceil(number_outfits * 0.8), outfit_jasper, outfit_flowers, outfit_sagehat, *list_outfit_nongwylan) & access_forestshop
    foxbane = gwylan_partners & access_edencabin 
    
    outfit_familiarcollar = AtLeast(math.ceil(number_outfits * 0.85), outfit_jasper, outfit_flowers, outfit_sagehat, *list_outfit_nongwylan) & access_forestshop

    outfit_greater_fox = (
        outfit_foxmask & outfit_shrine & outfit_jasper
    )

    list_outfit_gwylan = [outfit_jasper, outfit_flowers, outfit_sagehat, outfit_familiarcollar, outfit_greater_fox]
    list_outfit = list_outfit_nongwylan + list_outfit_gwylan


    # -- Gwylan Remainder

    # INFO GWYLAN : by bluecat
    #
    # -- Description
    # Gwylans line is separated by events, requests, and rituals
    # You will have an event or several, get a request, 
    # then do a ritual for them. Once you get both rituals, you
    # just need to keep increasing their love and interacting with them
    #
    # When specifying a requirement for an event like 'hat_found', 
    # that means you have to see the event that gives that trigger
    # first, before being able to see this event
    #
    # NOTE: talking about clothes gives small changes to many events
    # and this documentation does not include what clothes changes stuff
    #
    #
    # -- Major Stats
    #
    # - Love/Interest:
    #   Love (or Intrerest) is increased by number of clothes unlocked and talked about, and can be decreased temporarly
    #   "specialClothes" is individual peices of each set (including the rose item not included in sets)
    #   "specialClothesSets" is each set you unlock when unlocking (everything in outfits code)
    #
    #   - Math:
    #   Love =          unlocked sets + number of sets you've talked to gwylan sold at the forest shop
    #   Love Percent =  (love / (totalsets*2)) * 100
    #   NOTE: totalsets*2 because talk + unlock is both 1 love,
    #   so under lovepercent just outfit number matters for calculation
    #
    #   - Code:
    #   unlockedSets = 
    #       getUnlockedSpecialSets(V.specialClothes.filter(c => c.unlocked >= 2).map(c => c.name)) 
    #       .filter(set => setup.specialClothesSets[set].shop.includes("forest"))
    #   NOTE: 2 here in c.unlocked means feat booster counts for sets 
    #         3 means you unlocked it normally, 1 means cheated
    #
    #   totalSets = getSpecialSets(sets => sets.shop.
    #
    #   love = unlockedSets.length + V.gwylanTalked.filter(set => setup.specialClothesSets[set]?.shop.includes("forest")).length
    #   lovepercent = (love / (totalSets.length * 2)) * 100
    #
    #   - Example:
    #   28 pieces unlocked
    #   5 talked about
    #   love = 33
    #   lovepercent = ((33 / (56 * 2)) * 100) = 29.46%
    #
    #
    # - Progress:
    #   Progress is a value that increases
    #   from certain clothes or events involving Gwylan
    #   For clothes you have to use their story not seasonal time
    #   Shrine and Jasper also require specific dialogue
    #   Clothes:
    #       Witch:          +1 # 1
    #       Vampire:        +1
    #       Scarecrow:      +1
    #       Future Suit:    +1
    #       Christmas:      +1
    #       Rose Wed:       +1
    #       Bird:           +1
    #       Exorcist:       +1
    #       T Sexy:         +1
    #       Chain:          +1
    #       Spectales:      +1
    #       Islander M:     +1
    #       Fox Mask:       +1
    #       Shrine (Fx TF): +1
    #       Jasper (blood): +1
    #       Succubus:       +1
    #       SShirt:         +2 # 2
    #       Cow:            +2
    #       Prison:         +2
    #       Confessor:      +2
    #       Asylum:         +3 # 3
    #   Sets:
    #       Historic    +1
    #       bad_end:    +5
    #   Talk:
    #       Time with Eden:     +1
    #       Time with Wolves:   +2
    #   Events:
    #       Chef Speach w/Gwylan Bailey Talk: +2
    #       Mansion Vault Heist: +2
    #
    #
    # - Requests:
    #   When requirements are met, Gwylan can make a request of
    #   you, usually involving you meeting them somewhere and doing something
    #
    #   Except for a few, completing these gives +1 to the gwylan.request value
    #   also if a request is ended without completing it, don't add 1
    #   
    #  - Quest Requests:
    #   'tutorial'
    #   |   info:  Ask if you can help Gwylan
    #   |   req:   None
    #
    #   'meetAtShop'
    #   |   info:  Chain Event, Forest Beast Ritual
    #   |   req:   snoop 3; love 50, talked 10, progress 6, event 'lights'
    #
    #   'meetAtCafe'
    #   |   info:  Chain Event, Struggles Intro
    #   |   req:   progress 15, lovepercent 65, event 'ritual_beast', gwylanbeast date 2, dom 10, lust 25
    #   |   note:  no ++request
    #
    #   'yearning'
    #   |   info:  Chain Event, Scorning
    #   |   req:   doing 'ritual_sex', kissing? Gwylan
    #   |   note:  locks you out of Forest Shop for a bit
    #   |   |      get a note at your window after a while
    #   |   |      time requirement can be shortened by meeting Gwylan at the Pub
    #
    #   'chastity'
    #   |   info:  removal of chastity belt (normal)
    #   |   req:   1. Gwylan mad at you for having one (command)
    #   |   |      2. Asking Gwylan about it
    #   |   note:  if you weren't commanded, no ++request
    #
    #   'chastityIngredients'
    #   |   info:  removal of chastity belt (golden)
    #   |   req:   1. Gwylan mad at you for having one (command)
    #   |   |      2. Asking Gwylan about it
    #   |   note:  if you weren't commanded, no ++request
    #   |   |      if you did it on your own, no ++request
    #
    #  - Normal Requests:
    #   'clothing'
    #   |   info:  Sudo-Random peice of clothing for Gwylan
    #   |   |      gets more 'complex' the more requests you do
    #   |   req:   None
    #
    #   'ingredients'
    #   |   info:  Sudo-Random ingredient for Gwylan
    #   |   |      gets more 'complex' the more requests you do
    #   |   req:   None
    #
    #   'clothingGasMask'
    #   |   info:  get a Gas Mask
    #   |   req:   talk 5
    #   |   note:  onetime, 3x weight
    #
    #   'clothingGold'
    #   |   req:   adultshop built, love 30
    #   |   note:  onetime
    #   |   items: gold choker, gold bracelets, gold anklets
    #
    #   'plums'
    #   |   info:  get plums from woodlands
    #   |   req:   farmwoodland 2, Gwylan preg
    #   |   note:  5x weight
    #
    #   'sample'
    #   |   info:  get a lewd fluid sample 
    #   |   req:   event 'ritual_beast'
    #
    #   'samplePlayer'
    #   |   unused (normal req: event 'cafe_chef_truth')
    #
    #   'preen'
    #   |   info:  Get Feathers for Gwylan
    #   |   req:   talk 'bird', ( (harpy tf, flight) OR (requests 10, not avery questline) )
    #   |   note:  If you have tf and flight, has double weight
    #   |   |      otherwise expects feathers from Great Hawk
    #
    #   'cream'
    #   |   info:  small lewd event
    #   |   req:   status dom or Lust
    #   |   |      any event of ('cream_lick', 'cafe_chef_truth', 'nectar_lick') OR cat tf
    #
    #   'robin'
    #   |   unused (normal req: gwylan.robin >= 5)
    #
    #   'wolfbrew'
    #   |   unused (no made req)
    #
    #   'ghostbrew'
    #   |   unused (no made req)
    #
    #
    # - Status:
    #   met:
    #   |    If you've met Gwylan
    #
    #   aroused:
    #   |   lovepercent 65, event ritual_sex, dom 20
    #   |   lust 40, not status 'cautious', not event 'yearning'
    #
    #   dom:
    #   |   lovepercent 65, event ritual_sex, dom 20
    #   |   lust 40, not status 'cautious',
    #   |   dom gte 100 OR hyponosis dev 3
    #
    #   lust:
    #   |   lovepercent 75, event 'yearning', dom 50
    #   |   lust 30, dom + lust gte 90, not status 'cautious' 
    #
    #   heat:
    #   |   lovepercent 75, event 'yearning', dom 100
    #   |   lust 40, dom + lust gte 160
    #
    #   wantsPregnancy:
    #   |   love 90, dom 140, status 'heat', neither pregnant
    #
    #   cautious:
    #   |   wary 2, status 'scorned'
    #
    #   scarred:
    #   |   Has been Brown Fox Wounded
    #
    #   wounded:
    #   |   Currently Brown Fox Wounded (20, 30, or 40 days depending on outcome)
    #
    #   aurigaScarConfront:
    #   |   Avery Ascended, has scar, event 'auriga_scar'
    #   |   event 'ritual_sex'
    #
    #   reunion:
    #   |   badend and been away for 14 days
    #   |   event 'lights'
    #
    #   badEndReady (not implemented):
    #   |   event 'romance', 
    #   |   status 'aurigaScarConfront' OR
    #   |   dom 125, any devotion, not doing Avery questline, (reunion status OR hunting == 3)
    #
    #
    # - Hunting:
    #   Hunting is accessable in 3 states
    #   1: late on 'meetAtShop' or 'meetAtCafe'
    #   2: event 'yearning', dom 50, ritual missed, rnd(1, 200) lte dom + lust, no wary
    #   3: ^, missed by 14 days and event 'romance'
    #
    #   Depending on this value, events will be added to 
    #   Gwylan stalking you in the forest
    #   At 1, Gwylan will attempt to Hypnotise you to get you to go to the Forest Shop
    #   At 2, Gwylan will force you to go with them
    #   At 3, the same
    #
    #   NOTE: code for this is a bit weird to trigger, 
    #   but discord seems to have seen the event happen
    #
    #
    # - Wary: 
    #   Increased from Avery Skyscraper Ascend, Mansion Party, Nowhere event
    #   Decreased by doing Rituals
    #
    #
    # - Hyponosis Devotion:
    #   Gwylan Hypno Addicition, just increases from doing
    #   events with Hypno with Gwylan, and sometimes they'll
    #   increase it randomly in events. 
    #   The few things that require a specific level already require high love
    #
    #
    #
    # -- Smaller Stats
    # - Talked:             Number of Clothes you've talked to Gwylan about
    # - Dom / Yearning:     As Expected (allowing = increase, disallowing = decrease)
    # - Lust:               As Expected (lewd = increase, encounter = decrease)
    # - date.GwylanBeast:   Beast Ritual Counter
    # - date.GwylanSex:     Forest Sex Counter
    # - gwylan.sea:         Watching Ocean Counter
    # - Robin:              Take robin to Ocean Cafe with Gwylan counter
    #
    #
    #
    # -- Event Details
    # Somewhat chronological event chain for Gwylan
    # Includes details for events mentioned above
    # and some unmentioned
    #
    # - Event: Ask about Clothes
    #   requires: None
    #   gives: 'clothes_intro'
    #
    #
    # - Event: Forest Shop Intruder
    #   requires: love gte 10
    #   gives: 'intruder'
    #
    #
    # - Chain: Snooping
    #   Snoop 1: Hat
    #   requires: love 20, events 'intruder', 'clothes_intro'
    #   gives: 'hat_found'
    #
    #   Shoop 2: Lights
    #   requires: love 35, events 'hat_found', progress 3, requests 2
    #   gives: 'lights'
    #
    #   Snoop 3: Forest Shop Snoop
    #   requires: love 50, events 'lights', talked 10, progress 6
    #   -> Forest Shop Hunt Event
    #
    #
    # - Event: Forest Gwylan Eden
    #   This is an event where Gwylan and Eden
    #   are coming to rescue you at the same time,
    #   triggered by screaming in Forest while you've been
    #   away from Eden too long with any Eden Freedom
    #   Outcomes:
    #   1.  if event 'partners': (much later event)
    #   |   outcome1: go with Gwylan -> Forest Shop Hunt
    #   |   outcome2: go with Eden (end)
    #   2. else:
    #   |   outcome: Eden takes control, Gwylan unable to help
    #
    #
    # - Event: Forest Shop Hunt 
    #   Minigame Event
    #   1. Snooping: 
    #   |   Find the key, then go to the garden (twice)
    #   |   gives: 'caught' or 'caught_no_lewd'
    #   2. Eden Escape:
    #   |   1. stay with Gwylan, gives feat 'foxbane'
    #   |   2. leave with Eden
    #   |   3. find key, escape to the Forest
    #   |   gives: None? (couldn't find anything)
    #
    #
    # - Request: Meet At Shop
    #   requires: 'caught' or 'caught_no_lewd'
    #   -> Ritual: Forest Purge
    #
    #
    # - Ritual: Forest Purge
    #   requires: 'meetAtShop'
    #   toggles: beasts and plantpeople
    #   gives: 
    #   |   1. 'ritual_beast'
    #   |   2. at least 1 success: feat 'First Verse' (firstverse)
    #   |   3. event 'struggles': 'ritual_sex_intro'
    #
    #
    # - Event: Struggles Intro
    #   requires: 
    #   |   progress 15, lovepercent 65, 'ritual_beast', 
    #   |   gwylanbeast date 2, dom 10, lust 25
    #   gives: 'meetAtCafe'
    #
    #
    # - Request: Meet At Cafe
    #   requires: 'meetAtCafe'
    #   gives: 'struggles'
    #   NOTE: there's a lot of dialogue here, however it isn't required, 
    #   just changes a later event slightly
    #
    #
    # - Ritual: Forest Vessel
    #   requires: 'ritual_sex_intro'
    #   toggles: beasts and plantpeople
    #   gives: 'ritual_sex', feat 'wildsong'
    #
    #
    # - Event: Promenade Walk
    #   requires:
    #   |   lovepercent 80, dom 75, date gwylansex 5,
    #   |   gwylansea 5, status lust
    #   gives: 'partners', potential love interest status
    #
    #
    # - Event Flag: 'petplay'
    #   2 different ways to get this
    #   1. Food gift with Gwylan, share it, eat like a pet (dev 2)
    #   2. Rituals having event 'ritual_sex' and status lust or dom
    #   gives: 'petplay'
    #
    #
    # - Event: Deepest Hypnosis
    #   requires: hypno dev 4, lovepercent 80, status lust
    #   gives: 'hypnosis_deepest'
    #
    # 
    # - Event: Familiar Collar
    #   requires: 
    #   |   lovepercent 85, dom 120, hypno dev 3,
    #   |   events all 'partners', 'hypnosis_deepest', 'petplay'
    #   gives: familiar collar
    #
    #
    # - Event: Avery Party Crash
    #   During Avery's mansion party, the 'Brown Fox'
    #   will appear, how you interact with them won't change
    #   much other than screaming which gives 2 wary
    #   You can influence Gwylans injury however:
    #   |   40 day: Cover Blown (scream)
    #   |   20 day: Warn about Remy
    #   |   30 day: none
    #   gives: status 'wounded' and 'scarred'
    #
    #
    # - Event: Avery Skyscraper Ascend
    #   note: part of avery line
    #   gives: var auriga_scar
    #
    #
    # - Event: "Nowhere"
    #   req: status 'aurigaScarConfront'
    #   gives: event 'auriga_scar'
    #   -> soft bad end (not implemented)
    #
    #
    # - Event: "Taken"
    #   req: status 'badEndReady'
    #   note: "Nowhere" takes priority, if you have 'aurigaScarConfront'
    #   -> soft bad end (not implemented)
    #
    #
    # - 'romance'
    #   unimplemented? (cannot find push to list)
    #
    #
    #
    # -- Event Chain (short ver):
    # Events and their requirements sorted by requirement
    # (events forward require the previous events to be done)
    #
    # 'clothes_intro'       - talk
    # 'intruder'            love 10
    # 'hat_found'           love 20 : snoop
    # 'lights'              love 35, progress 3, request 2 : snoop
    # 'caught'/_no_lewd'    love 50, talked 10, progress 6 : snoop
    # 'meetAtShop'          - chain
    # 'ritual_beast'        - chain
    # 'meetAtCafe'          lovepercent 65, progress 15, datebeast 2, dom 10, lust 25
    # 'struggles'           - chain
    # 'ritual_sex_intro'    - do beast ritual
    # 'ritual_sex'          - do vessel ritual
    # 'partners'            lovepercent 80, dom 75, gwylansex 5, gwylansea 5, status lust
    #
    # 'Forest Gwylan Eden'  - prev (partners)
    #
    # 'petplay'             - prev (ritual_sex)
    # 'hypnosis_deepest'    lovepercent 80, hypno dev 4, status lust
    # 'Familiar Collar'     lovepercent 85, dom 120, hypno dev 3, event 'partners'
    # 
    # 
    # 'romance'             unimplemented?
    #
    #
    #
    # -- Clothes (from Gwylan)
    # Sage Hat:     event Ritual Vessel
    # Flowers:      stuff already + event Ritual Vessel
    # Jasper:       request 'clothingGold'
    # F Collar:     event Familiar Collar

    list_gwylan_progress = [
                # +1
            # Outfit:
        outfit_witch,             
        outfit_vampire,
        outfit_scarecrow,
        outfit_futuresuit,
        outfit_christmas,
        outfit_rosewedding,
        outfit_bird,
        outfit_exorcist,
        outfit_templesexy,
        outfit_chain,
        outfit_esotericspecs,
        outfit_islandermask_w,
        outfit_foxmask,
        outfit_shrine & tfrule_fox_full_appear, # missable?
        # NOTE: only Gwylan outfit, may need to change to prevent recursion
        outfit_jasper, # missable?
        outfit_succubus,
            # Set:
        outfit_greater_historic,
            # Talk:
        access_edencabin & type_badend,

        # +2                # duplicates
            # Outfit:
        outfit_sshirt_w,    outfit_sshirt_w,
        outfit_cow_w,       outfit_cow_w,
        outfit_prison_w,    outfit_prison_w,
        outfit_confessor,   outfit_confessor,
            # Talk:
        access_wolfcave & type_badend, access_wolfcave & type_badend,

        # +3                        # duplicates
            # Outfit:
        outfit_straightjacket_w,    outfit_straightjacket_w, outfit_straightjacket_w,

        # +5                        # duplicates
            # Set:
        outfit_greater_badend_w,    outfit_greater_badend_w, outfit_greater_badend_w, outfit_greater_badend_w, outfit_greater_badend_w,
    ]
    calc_gwylan_progress_3 = AtLeast(3, *list_gwylan_progress)
    calc_gwylan_progress_6 = AtLeast(6, *list_gwylan_progress)
    calc_gwylan_progress_15 = AtLeast(15, *list_gwylan_progress)
    

    outfit_100p = AtLeast(number_outfits, *list_outfit)
    outfit_50p = AtLeast(math.ceil(number_outfits * 0.5), *list_outfit)
    outfit_65p = AtLeast(math.ceil(number_outfits * 0.65), *list_outfit)
    outfit_85p = AtLeast(math.ceil(number_outfits * 0.85), *list_outfit)


    # -- School Fairs:
    science_lichen     = access_park & access_temple & access_industrialdrain & access_forest
    science_mushroom   = access_forest
    science_phalli     = access_beach & promiscuity_3
    # cliff street is the location set of the fair so does not be in rule
    sciencefairwinner  = (science_lichen | science_mushroom | science_phalli) & access_school
    sciencefairoffence = science_phalli & access_school
    # just need oxford street for stims, and orphanage for studying
    mathcomp = access_school & access_orphanage & access_oxfordstreet


    # -- Seeds:
    seed_broccoli      = access_moor & tending_4            # 1
    # cabbage req hist 4 because meadow side require 
    # hist 4 to get to, even though mer side is 3
    seed_cabbage       = access_costalpath & history_4      # 2 
    seed_carnation     = access_school & has_schoolgreen    # 3 
    seed_cauliflower   = access_connudatusstreet            # 4
    seed_chilipepper   = access_connudatusstreet            # 5
    seed_daises        = access_school                      # 6
    seed_garlicbulbs   = access_moor & tending_5            # 7
    seed_lillies       = access_forest & science_2          # 8
    seed_lotus         = access_forestlake & science_3      # 9
    seed_onion         = access_moor & tending_4            # 10
    seed_orchid        = access_forest & science_4          # 11
    seed_pepper        = access_connudatusstreet            # 12
    # INFO Pink Rose:
    # find: daisy seed, flower crown robin/hawk, do gwylan ritual
    # then: show an outfit to gwylan
    seed_pinkrose      = outfit_flowers & access_forestshop # 13
    seed_plumeria      = access_island & science_4          # 14
    seed_poppies       = access_asylum | access_edencabin   # 15
    seed_potato        = access_alexfarm                    # 16 # also requires clearing some fields
    seed_redrose       = access_forest & science_3          # 17
    seed_spinach       = access_connudatusstreet            # 18
    seed_strangeflower = access_alexfarm                    # 19
    seed_sunflower     = access_alexfarm                    # 20
    seed_tomato        = access_connudatusstreet            # 21
    seed_tulip         = access_park & science_2            # 22
    seed_turnip        = access_alexfarm                    # 23 # also requires clearing some fields
    seed_wheat         = access_connudatusstreet            # 24
    seed_whiterose     = access_costalpath                  # 25
    seed_carrot        = access_moor & tending_6            # 26
    seed_rice          = access_farmlands                   # 27

    # NOTE: weird wiki mismatch, seedy mentions 26 but breedy says all 27
    # checking ingame it uses (all things with seeds / 2 < seeds discovered )
    # so 27/2 in this case

    
    list_seeds = [
        seed_broccoli,        seed_cabbage,       seed_carnation,
        seed_cauliflower,     seed_chilipepper,   seed_daises,
        seed_garlicbulbs,     seed_lillies,       seed_lotus,
        seed_onion,           seed_orchid,        seed_pepper,
        seed_pinkrose,        seed_plumeria,      seed_poppies,
        seed_potato,          seed_redrose,       seed_spinach, 
        seed_strangeflower,   seed_sunflower,     seed_tomato,
        seed_tulip,           seed_turnip,        seed_wheat, 
        seed_whiterose,       seed_carrot,        seed_rice
    ]
    number_seeds = len(list_seeds)
    seeds_50p = AtLeast(math.ceil(number_seeds * 0.5), *list_seeds)

    seeds_100p = AtLeast(number_seeds, *list_seeds)


    # -- Specific Feats:
    ballroomshowoff                = dancing_8 | promiscuity_2
    shoppingcentre_or_forestshop   = access_shoppingcentre | access_forestshop
    recipe_or_shoppingcentre       = access_recipe | access_shoppingcentre
    has_leathermap                 = Has(DoLItemNames.antique_leathermap.value)
    hand_or_dance_400              = Or(hands_2, dancing_4)
    playingwithfire                = willpower_4 | oral_4
    corneredrogue                  = ((toggle_monsterpeople & athletics_7 & skulduggery_7) | 
                                      (athletics_5 | swimming_5 | tfrule_wings))
    slippery                       = (skulduggery_6 | # 50%
                                      seduction_4 |
                                      athletics_9) # 40%
    intothesunset                  = AtLeast(2, hands_3, physique_4, tending_6)
    tending_or_althletics_500      = tending_5 | athletics_5

    # Special Traits Feat
    access_specialtrait_all = (
        access_eventstreet & access_para_tentacles & access_vore_either
    )

    # currently only 3 species of baby exist
    access_humanbaby = access_eventstreet
    access_wolfbaby = access_forest | access_wolfcave
    access_harpybaby = access_moor | access_birdtower
    list_babytypes = [access_humanbaby, access_wolfbaby, access_harpybaby]
    diversityoflife = AtLeast(3, *list_babytypes)
    topbroodmother = access_para_tentacles | access_para_pale | access_para_lurker

    # add old churchyard
    # here later if I make it its own region
    access_antiques = (
        access_averymansion & access_beach     & access_dancestudio &
        access_compound     & access_landfill  & access_ridingschool &
        access_meadow       & access_forest    & access_forestlake &
        access_island       & access_birdtower & access_oldsewers &
        access_moor         & access_orphanage & access_pirateship &
        access_museum       & access_temple    & access_maze
    )


# Location Data

@dataclass(frozen=True)
class _LocDetail:
    """
    Container for details of a location

    Gen Rules and Locations should be [enumfoo.bar.value]
    
    Obtain Rules should be [enumfoo.bar]

    ### Definition:

    Location_Name = LocDetail(Location ID, 
        [Locations this is from], 
        [Rules to generate the location], 
        [Rules to get to the location],
    )
    """ # no _ so I don't accidently mass replace the docstring
    location_id: int
    locations: list[str]
    # Rules for generation should use world options
    rules_generation: list[Rule]
    rules_obtain: list[DoLRules]

    # function to copy and return the class with changes
    def override(self,
            addloc:list[DoLLocationNames] = None, addgenrule:list[DoLRules] = None, addobtainrule:list[DoLRules] = None,
            swaploc:list[DoLLocationNames] = None, swapgenrule:list[DoLRules] = None, swapobtainrule:list[DoLRules] = None,
        ) -> '_LocDetail':

        addloc = addloc or []
        addgenrule = addgenrule or []
        addobtainrule = addobtainrule or []

        locations = list(swaploc) if swaploc is not None else list(self.locations)
        rules_generation = list(swapgenrule) if swapgenrule is not None else list(self.rules_generation)
        rules_obtain = list(swapobtainrule) if swapobtainrule is not None else list(self.rules_obtain)

        locations.extend(addloc)
        rules_generation.extend(addgenrule)
        rules_obtain.extend(addobtainrule)

        # can keep id the same since we should gen previous
        return _LocDetail(self.location_id, locations, rules_generation, rules_obtain)


# NOTE: [Locations this is from] is ANY location not ALL locations needed
# create a rule if multiple locations are needed
class DoLLocationData(Enum):
    """
    Enum container for all locations

    Locations in this may be defined in items to be generated
    If you want to include a non-location item, use NonLocationItem_Data

    Values containted used the NamedTuple _LocDetail to catch code errors
    and make typing easier

    ### Definition:

    Location_Name = LocDetail(Location ID,
        [Locations this is from],
        [Rules to generate the location],
        [Rules to get to the location],
    )
    """ # no _ a so I don't accidently mass replace the docstring
    
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
        # TODO: CODE (school trait)
        # need to recode this to make sure this isn't based on the school trait...
        # instead based on the value that eats ur skill

        # the notable thing is, school skills do not base off you having earlier skills
        # therefore logic dictates that you can get level 5 in all of them whenever

    # NOTE: Reminder that a rule does not need to be set for
    # the region that it needs to go to, that's already implied

    # Required to build details correctly
    def __new__(cls, value):
        obj = object.__new__(cls)
        obj._value_ = value
        return obj

    # Fixes 'Any' when looking for locdetail
    @property
    def value(self) -> _LocDetail:
        return self._value_


    # ---------------- Antiques ----------------
    
    antique_ivorystatuette = _LocDetail(100, [
            DoLRegionNames.forest.value # old churchyard
        ], [
            DoLOptionFilters.type_antiques.value
        ], []) # antiqueivorystatuette

    antique_silvercoin = _LocDetail(101, [
            DoLRegionNames.forest.value, # old churchyard
        ], [
            DoLOptionFilters.type_antiques.value
        ], []) # antiquesilvercoin
                
    antique_crystal = _LocDetail(102, [
            DoLRegionNames.forest.value # old churchyard
        ], [
            DoLOptionFilters.type_antiques.value
        ], []) # antiquewhitecrystal
                
    antique_silverblade = _LocDetail(103, [
            DoLRegionNames.forest.value # old churchyard
        ], [
            DoLOptionFilters.type_antiques.value
        ], []) # antiquesilverblade
                
    antique_coppercoin = _LocDetail(104, [
            DoLRegionNames.forest.value # old churchyard
        ], [
            DoLOptionFilters.type_antiques.value
        ], []) # antiquecoppercoin
                
    antique_silvergoblet = _LocDetail(105, [
            DoLRegionNames.forest.value # old churchyard
        ], [
            DoLOptionFilters.type_antiques.value
        ], []) # antiquesilvergoblet
                
    antique_fetish = _LocDetail(106, [
            DoLRegionNames.forest.value # old churchyard
        ], [
            DoLOptionFilters.type_antiques.value
        ], []) # antiquestrangefetish
                
    antique_goldcoin = _LocDetail(107, [
            DoLRegionNames.forest.value # old churchyard
        ], [
            DoLOptionFilters.type_antiques.value
        ], []) # antiquegoldcoin
                
    antique_forestdagger = _LocDetail(108, [
            DoLRegionNames.forest.value
        ], [
            DoLOptionFilters.type_antiques.value
        ], []) # antiqueforestdagger
                
    antique_forestgem = _LocDetail(109, [
            DoLRegionNames.forest.value
        ], [
            DoLOptionFilters.type_antiques.value
        ], []) # antiqueforestgem
                
    antique_arrow = _LocDetail(110, [
            DoLRegionNames.forest.value
        ], [
            DoLOptionFilters.type_antiques.value
        ], []) # antiqueforestarrow
                
    antique_ivorynecklace = _LocDetail(111, [
            DoLRegionNames.forest_lake.value
        ], [
            DoLOptionFilters.type_antiques.value
        ], []) # antiqueivorynecklace
                
    antique_ivorybox = _LocDetail(112, [
            DoLRegionNames.forest_lake.value
        ], [
            DoLOptionFilters.type_antiques.value
        ], []) # antiquebox
                
    antique_silverring = _LocDetail(113, [
            DoLRegionNames.forest_lake.value
        ], [
            DoLOptionFilters.type_antiques.value
        ], []) # antiquesilverring
                
    antique_goldnecklace = _LocDetail(114, [
            DoLRegionNames.forest_lake.value
        ], [
            DoLOptionFilters.type_antiques.value
        ], []) # antiquegoldnecklace
                
    antique_chastitybelt = _LocDetail(115, [
            DoLRegionNames.forest_lake.value
        ], [
            DoLOptionFilters.type_antiques.value
        ], []) # antiquegoldchastitybelt
                
    antique_stonetalisman = _LocDetail(116, [
            DoLRegionNames.meadow.value
        ], [
            DoLOptionFilters.type_antiques.value
        ], []) # antiquestonetalisman
                
    antique_horn = _LocDetail(117, [
            DoLRegionNames.maze.value,
            DoLRegionNames.old_sewers.value
        ], [
            DoLOptionFilters.type_antiques.value
        ], []) # antiquehorn
                
    antique_snuffer = _LocDetail(118, [
            DoLRegionNames.maze.value,
        ], [
            DoLOptionFilters.type_antiques.value
        ], []) # antiquesnuffer
                
    antique_bucket = _LocDetail(119, [
            DoLRegionNames.maze.value,
        ], [
            DoLOptionFilters.type_antiques.value
        ], []) # antiquebucket
                
    antique_silvermanacle = _LocDetail(120, [
            DoLRegionNames.maze.value,
        ], [
            DoLOptionFilters.type_antiques.value
        ], []) # antiquesilvermanacle
                
    antique_whip = _LocDetail(121, [
            DoLRegionNames.maze.value,
        ], [
            DoLOptionFilters.type_antiques.value
        ], []) # antiquewhip
                
    antique_goldring = _LocDetail(122, [
            DoLRegionNames.moor.value
        ], [
            DoLOptionFilters.type_antiques.value
        ], []) # antiquegoldring
                
    antique_bell = _LocDetail(123, [
            DoLRegionNames.moor.value
        ], [
            DoLOptionFilters.type_antiques.value
        ], []) # antiquebell
                
    antique_bullet = _LocDetail(124, [
            DoLRegionNames.moor.value,
            DoLRegionNames.bird_tower.value
        ], [
            DoLOptionFilters.type_antiques.value
        ], []) # antiquebullet
                
    antique_artilleryshell = _LocDetail(125, [
            DoLRegionNames.moor.value
        ], [
            DoLOptionFilters.type_antiques.value
        ], []) # antiqueshell
                
    antique_grenade = _LocDetail(126, [
            DoLRegionNames.riding_school.value
        ], [
            DoLOptionFilters.type_antiques.value
        ], []) # antiquegrenade
                
    antique_goldbrooch = _LocDetail(127, [
            DoLRegionNames.dance_studio.value
        ], [
            DoLOptionFilters.type_antiques.value
        ], []) # antiquegoldbrooch
                
    antique_silverbrooch = _LocDetail(128, [
            DoLRegionNames.orphanage.value
        ], [
            DoLOptionFilters.type_antiques.value
        ], []) # antiquesilverbrooch
                
    antique_islanderarrow = _LocDetail(129, [
            DoLRegionNames.island.value
        ], [
            DoLOptionFilters.type_antiques.value,
            DoLOptionFilters.req_badend.value,
        ], []) # antiqueislandarrow
                
    antique_islandermask = _LocDetail(130, [
            DoLRegionNames.island.value
        ], [
            DoLOptionFilters.type_antiques.value,
            DoLOptionFilters.req_badend.value,
        ], []) # antiquewoodenmask
                
    antique_obsidiandisc = _LocDetail(131, [
            DoLRegionNames.island.value
        ], [
            DoLOptionFilters.type_antiques.value,
            DoLOptionFilters.req_badend.value,
        ], []) # antiqueobsidiandisc
                
    antique_trilobitefossil = _LocDetail(132, [
            DoLRegionNames.island.value
        ], [
            DoLOptionFilters.type_antiques.value,
            DoLOptionFilters.req_badend.value,
        ], []) # antiquetrilobitefossil
                
    antique_baileyminesign = _LocDetail(133, [
            DoLRegionNames.landfill.value
        ], [
            DoLOptionFilters.type_antiques.value
        ], []) # antiqueminesign
                
    antique_incenseburner = _LocDetail(134, [
            DoLRegionNames.landfill.value
        ], [
            DoLOptionFilters.type_antiques.value
        ], []) # antiquetrashburner
                
    antique_cup = _LocDetail(135, [
            DoLRegionNames.landfill.value
        ], [
            DoLOptionFilters.type_antiques.value
        ], []) # antiquetrashcup 
                
    antique_silvermask = _LocDetail(136, [
            DoLRegionNames.manors.value
        ], [
            DoLOptionFilters.type_antiques.value
        ], [
            DoLRules.antiques_20
        ]) # antiquesilvermask
                
    antique_silveramulet = _LocDetail(137, [
            DoLRegionNames.compound.value
        ], [
            DoLOptionFilters.type_antiques.value
        ], []) # antiquesilveramulet
                
    antique_hourglass = _LocDetail(138, [
            DoLRegionNames.pirate_ship.value
        ], [
            DoLOptionFilters.type_antiques.value,
            DoLOptionFilters.req_badend.value,
        ], []) # antiquehourglass
                
    antique_swordcane = _LocDetail(139, [
            DoLRegionNames.pirate_ship.value
        ], [
            DoLOptionFilters.type_antiques.value,
            DoLOptionFilters.req_badend.value,
        ], []) # antiqueswordcane
                
    antique_chocolate = _LocDetail(140, [
            DoLRegionNames.pirate_ship.value
        ], [
            DoLOptionFilters.type_antiques.value,
            DoLOptionFilters.req_badend.value,
        ], []) # antiquechocolate
                
    antique_teacaddy = _LocDetail(141, [
            DoLRegionNames.pirate_ship.value
        ], [
            DoLOptionFilters.type_antiques.value,
            DoLOptionFilters.req_badend.value,
        ], []) # antiqueteacaddy
                
    antique_woodenfigurine = _LocDetail(142, [
            DoLRegionNames.pirate_ship.value
        ], [
            DoLOptionFilters.type_antiques.value,
            DoLOptionFilters.req_badend.value,
        ], []) # antiquewoodenfigurine
                
    antique_copperring = _LocDetail(143, [
            DoLRegionNames.pirate_ship.value
        ], [
            DoLOptionFilters.type_antiques.value,
            DoLOptionFilters.req_badend.value,
        ], []) # antiquecopperring
                
    antique_goldcompass = _LocDetail(144, [ # INFO -> feat_lostheirloom
            DoLRegionNames.pirate_ship.value
        ], [
            DoLOptionFilters.type_antiques.value,
            DoLOptionFilters.req_badend.value,
        ], []) # antiquegoldcompass
                
    antique_coppercompass = _LocDetail(145, [
            DoLRegionNames.ocean.value
        ], [
            DoLOptionFilters.type_antiques.value
        ], []) # antiquecoppercompass
                
    antique_coralring = _LocDetail(146, [
            DoLRegionNames.ocean.value
        ], [
            DoLOptionFilters.type_antiques.value
        ], []) # antiquecoralring
                
    antique_diamond = _LocDetail(147, [
            DoLRegionNames.ocean.value
        ], [
            DoLOptionFilters.type_antiques.value
        ], []) # antiquediamond
                
    antique_brassstatuette = _LocDetail(148, [
            DoLRegionNames.temple.value
        ], [
            DoLOptionFilters.type_antiques.value
        ], []) # antiquebrassstatuette
                
    antique_golddagger = _LocDetail(149, [
            DoLRegionNames.avery_mansion.value
        ], [
            DoLOptionFilters.type_antiques.value,
            DoLOptionFilters.req_loveinterest.value,
        ], []) # antiquegolddagger
                
    antique_goldamulet = _LocDetail(150, [
            DoLRegionNames.avery_mansion.value
        ], [
            DoLOptionFilters.type_antiques.value,
            DoLOptionFilters.req_loveinterest.value,
        ], []) # antiquegoldamulet
                
    antique_goldmask = _LocDetail(151, [
            DoLRegionNames.avery_mansion.value
        ], [
            DoLOptionFilters.type_antiques.value,
            DoLOptionFilters.req_loveinterest.value,
        ], []) # antiquegoldmask
                
    antique_silvercompass = _LocDetail(152, [
            DoLRegionNames.beach.value
        ], [
            DoLOptionFilters.type_antiques.value
        ], []) # antiquesilvercompass
                
    antique_leathermap = _LocDetail(153, [
            DoLRegionNames.beach.value
        ], [
            DoLOptionFilters.type_antiques.value
        ], []) # antiqueleathermap
                
    antique_cutlass = _LocDetail(154, [
            DoLRegionNames.beach.value
        ], [
            DoLOptionFilters.type_antiques.value
        ], []) # antiquecutlass
                
    antique_silverdagger = _LocDetail(155, [
            DoLRegionNames.beach.value
        ], [
            DoLOptionFilters.type_antiques.value
        ], []) # antiquesilverdagger
                
    antique_rustedcutlass = _LocDetail(156, [
            DoLRegionNames.beach.value
        ], [
            DoLOptionFilters.type_antiques.value
        ], []) # antiquerustedcutlass
                
    antique_pinkcrystal = _LocDetail(157, [
            DoLRegionNames.old_sewers.value
        ], [
            DoLOptionFilters.type_antiques.value
        ], []) # antiquecrystal
                
    antique_candlestick = _LocDetail(158, [
            DoLRegionNames.old_sewers.value
        ], [
            DoLOptionFilters.type_antiques.value
        ], []) # antiquecandlestick
                
    antique_dildo = _LocDetail(159, [
            DoLRegionNames.old_sewers.value
        ], [
            DoLOptionFilters.type_antiques.value
        ], []) # antiquedildo
                
    antique_watch = _LocDetail(160, [
            DoLRegionNames.old_sewers.value
        ], [
            DoLOptionFilters.type_antiques.value
        ], []) # antiquewatch
                    
    antique_silvercrown = _LocDetail(161, [
            DoLRegionNames.forest.value # old churchyard
        ], [
            DoLOptionFilters.type_antiques.value
        ], []) # antiquesilvercrown
                
    antique_serpentpainting = _LocDetail(162, [
            DoLRegionNames.maze.value,
        ], [
            DoLOptionFilters.type_antiques.value,
        ], []) # serpentpainting


    # ---------------- Skills ----------------
    
    skill_skulduggery_1 = _LocDetail(500, [
            DoLRegionNames.school.value, 
        ], [
            DoLOptionFilters.type_skills.value,
        ], [])
    
    skill_skulduggery_2 = _LocDetail(501, [
            DoLRegionNames.domus_houses.value, 
        ], [
            DoLOptionFilters.type_skills.value,
        ], [])
    
    skill_skulduggery_3 = _LocDetail(502, [
            DoLRegionNames.barb_street.value, 
            DoLRegionNames.connudatus_street.value,
        ], [
            DoLOptionFilters.type_skills.value,
        ], [])
    
    skill_skulduggery_4 = _LocDetail(503, [
            DoLRegionNames.danube_houses.value, 
        ], [
            DoLOptionFilters.type_skills.value,
        ], [
            DoLRules.skulduggery_1,
        ])
    
    skill_skulduggery_5 = _LocDetail(504, [
            DoLRegionNames.docks.value, 
        ], [
            DoLOptionFilters.type_skills.value,
        ], [
            DoLRules.skulduggery_2,
        ])
    
    skill_skulduggery_6 = _LocDetail(505, [
            DoLRegionNames.temple.value,
        ], [
            DoLOptionFilters.type_skills.value,
        ], [
            DoLRules.skulduggery_3,
        ])
    
    skill_skulduggery_7 = _LocDetail(506, [
            DoLRegionNames.manors.value,
        ], [
            DoLOptionFilters.type_skills.value,
        ], [
            DoLRules.skulduggery_4,
        ])
    
    skill_skulduggery_8 = _LocDetail(507, [
            DoLRegionNames.in_town.value, 
        ], [
            DoLOptionFilters.type_skills.value,
        ], [
            DoLRules.skulduggery_5,
        ])
    
    skill_skulduggery_9 = _LocDetail(508, [
            DoLRegionNames.in_town.value, 
        ], [
            DoLOptionFilters.type_skills.value,
        ], [
            DoLRules.skulduggery_6,
        ])
    
    skill_skulduggery_10 = _LocDetail(509, [
            DoLRegionNames.in_town.value, 
        ], [
            DoLOptionFilters.type_skills.value,
        ], [
            DoLRules.skulduggery_7,
        ])



    # Dancing just wants dance studio, but can be leveled in strip club and brothel
    skill_dancing_1 = _LocDetail(510, [
            DoLRegionNames.dance_studio.value,
        ], [
            DoLOptionFilters.type_skills.value,
        ], [])
    
    skill_dancing_2 = _LocDetail(511, [
            DoLRegionNames.dance_studio.value,
        ], [
            DoLOptionFilters.type_skills.value,
        ], [])
    
    skill_dancing_3 = _LocDetail(512, [
            DoLRegionNames.dance_studio.value,
        ], [
            DoLOptionFilters.type_skills.value,
        ], [])
    
    skill_dancing_4 = _LocDetail(513, [
            DoLRegionNames.dance_studio.value,
        ], [
            DoLOptionFilters.type_skills.value,
        ], [])
    
    skill_dancing_5 = _LocDetail(514, [
            DoLRegionNames.dance_studio.value,
        ], [
            DoLOptionFilters.type_skills.value,
        ], [])
    
    skill_dancing_6 = _LocDetail(515, [
            DoLRegionNames.dance_studio.value,
        ], [
            DoLOptionFilters.type_skills.value,
        ], [])
    
    skill_dancing_7 = _LocDetail(516, [
            DoLRegionNames.dance_studio.value,
        ], [
            DoLOptionFilters.type_skills.value,
        ], [])
    
    skill_dancing_8 = _LocDetail(517, [
            DoLRegionNames.dance_studio.value,
        ], [
            DoLOptionFilters.type_skills.value,
        ], [])
    
    skill_dancing_9 = _LocDetail(518, [
            DoLRegionNames.dance_studio.value,
        ], [
            DoLOptionFilters.type_skills.value,
        ], [])
    
    skill_dancing_10 = _LocDetail(519, [
            DoLRegionNames.dance_studio.value,
        ], [
            DoLOptionFilters.type_skills.value,
        ], [])



    # School for at least level 1
    skill_swimming_1 = _LocDetail(520, [
            DoLRegionNames.school.value, 
        ], [
            DoLOptionFilters.type_skills.value,
        ], [])
    
    skill_swimming_2 = _LocDetail(521, [
            DoLRegionNames.school.value, 
        ], [
            DoLOptionFilters.type_skills.value,
        ], [])
    
    skill_swimming_3 = _LocDetail(522, [
            DoLRegionNames.school.value, 
        ], [
            DoLOptionFilters.type_skills.value,
        ], [])
    
    skill_swimming_4 = _LocDetail(523, [
            DoLRegionNames.school.value,
        ], [
            DoLOptionFilters.type_skills.value,
        ], [])
    
    skill_swimming_5 = _LocDetail(524, [
            DoLRegionNames.school.value, 
        ], [
            DoLOptionFilters.type_skills.value,
        ], [])
    
    skill_swimming_6 = _LocDetail(525, [
            DoLRegionNames.school.value, 
        ], [
            DoLOptionFilters.type_skills.value,
        ], [])
    
    skill_swimming_7 = _LocDetail(526, [
            DoLRegionNames.school.value, 
        ], [
            DoLOptionFilters.type_skills.value,
        ], [])
    
    skill_swimming_8 = _LocDetail(527, [
            DoLRegionNames.school.value, 
        ], [
            DoLOptionFilters.type_skills.value,
        ], [])
    
    skill_swimming_9 = _LocDetail(528, [
            DoLRegionNames.school.value, 
        ], [
            DoLOptionFilters.type_skills.value,
        ], [])
    
    skill_swimming_10 = _LocDetail(529, [
            DoLRegionNames.school.value, 
        ], [
            DoLOptionFilters.type_skills.value,
        ], [])



    # Starting levels anywhere, rest park good place to train
    skill_athletics_1 = _LocDetail(530, [
            DoLRegionNames.in_town.value, 
        ], [
            DoLOptionFilters.type_skills.value,
        ], [])
    
    skill_athletics_2 = _LocDetail(531, [
            DoLRegionNames.in_town.value, 
        ], [
            DoLOptionFilters.type_skills.value,
        ], [])
    
    skill_athletics_3 = _LocDetail(532, [
            DoLRegionNames.park.value, 
        ], [
            DoLOptionFilters.type_skills.value,
        ], [])
    
    skill_athletics_4 = _LocDetail(533, [
            DoLRegionNames.park.value, 
        ], [
            DoLOptionFilters.type_skills.value,
        ], [])
    
    skill_athletics_5 = _LocDetail(534, [
            DoLRegionNames.park.value, 
        ], [
            DoLOptionFilters.type_skills.value,
        ], [])
    
    skill_athletics_6 = _LocDetail(535, [
            DoLRegionNames.park.value, 
        ], [
            DoLOptionFilters.type_skills.value,
        ], [])
    
    skill_athletics_7 = _LocDetail(536, [
            DoLRegionNames.park.value,
        ], [
            DoLOptionFilters.type_skills.value,
        ], [])
    
    skill_athletics_8 = _LocDetail(537, [
            DoLRegionNames.park.value, 
        ], [
            DoLOptionFilters.type_skills.value,
        ], [])
    
    skill_athletics_9 = _LocDetail(538, [
            DoLRegionNames.park.value, 
        ], [
            DoLOptionFilters.type_skills.value,
        ], [])
    
    skill_athletics_10 = _LocDetail(539, [
            DoLRegionNames.park.value, 
        ], [
            DoLOptionFilters.type_skills.value,
        ], [])



    skill_tending_1 = _LocDetail(540, [
            DoLRegionNames.in_town.value,
        ], [
            DoLOptionFilters.type_skills.value,
        ], [])
    
    skill_tending_2 = _LocDetail(541, [
            DoLRegionNames.in_town.value,  
        ], [
            DoLOptionFilters.type_skills.value,
        ], [])

    # Farm good place to train further levels
    skill_tending_3 = _LocDetail(542, [
            DoLRegionNames.alex_farm.value, 
        ], [
            DoLOptionFilters.type_skills.value,
        ], [])
    
    skill_tending_4 = _LocDetail(543, [
            DoLRegionNames.alex_farm.value,
        ], [
            DoLOptionFilters.type_skills.value,
        ], [])
    
    skill_tending_5 = _LocDetail(544, [
            DoLRegionNames.alex_farm.value,
        ], [
            DoLOptionFilters.type_skills.value,
        ], [])
    
    skill_tending_6 = _LocDetail(545, [
            DoLRegionNames.alex_farm.value,
        ], [
            DoLOptionFilters.type_skills.value,
        ], [])
    
    skill_tending_7 = _LocDetail(546, [
            DoLRegionNames.alex_farm.value,
        ], [
            DoLOptionFilters.type_skills.value,
        ], [])
    
    skill_tending_8 = _LocDetail(547, [
            DoLRegionNames.alex_farm.value,
        ], [
            DoLOptionFilters.type_skills.value,
        ], [])
    
    skill_tending_9 = _LocDetail(548, [
            DoLRegionNames.alex_farm.value,
        ], [
            DoLOptionFilters.type_skills.value,
        ], [])
    
    skill_tending_10 = _LocDetail(549, [
            DoLRegionNames.alex_farm.value,
        ], [
            DoLOptionFilters.type_skills.value,
        ], [])

    

    skill_housekeeping_1 = _LocDetail(550, [
            DoLRegionNames.domus_houses.value,
        ], [
            DoLOptionFilters.type_skills.value,
        ], [])
    
    skill_housekeeping_2 = _LocDetail(551, [
            DoLRegionNames.flats.value,
        ], [
            DoLOptionFilters.type_skills.value,
        ], [])
    
    skill_housekeeping_3 = _LocDetail(552, [
            DoLRegionNames.starfish_street.value,
        ], [
            DoLOptionFilters.type_skills.value,
        ], [])
    
    skill_housekeeping_4 = _LocDetail(553, [
            DoLRegionNames.danube_street.value,
        ], [
            DoLOptionFilters.type_skills.value,
        ], [])
    
    skill_housekeeping_5 = _LocDetail(554, [
            DoLRegionNames.temple.value,
        ], [
            DoLOptionFilters.type_skills.value,
        ], [])
    
    skill_housekeeping_6 = _LocDetail(555, [
            DoLRegionNames.temple.value,
        ], [
            DoLOptionFilters.type_skills.value,
        ], [])
    
    skill_housekeeping_7 = _LocDetail(556, [
            DoLRegionNames.temple.value,
        ], [
            DoLOptionFilters.type_skills.value,
        ], [])
    
    skill_housekeeping_8 = _LocDetail(557, [
            DoLRegionNames.temple.value,
        ], [
            DoLOptionFilters.type_skills.value,
        ], [])
    
    skill_housekeeping_9 = _LocDetail(558, [
            DoLRegionNames.temple.value,
        ], [
            DoLOptionFilters.type_skills.value,
        ], [])
    
    skill_housekeeping_10 = _LocDetail(559, [
            DoLRegionNames.temple.value,
        ], [
            DoLOptionFilters.type_skills.value,
        ], [])


    # ---------------- Sex Skills ----------------
    # sex skills just require encounters

    skill_seduction_1 = _LocDetail(560, [
            DoLRegionNames.in_town.value,
        ], [
            DoLOptionFilters.type_skills.value,
        ], [])
    
    skill_seduction_2 = _LocDetail(561, [
            DoLRegionNames.in_town.value,
        ], [
            DoLOptionFilters.type_skills.value,
        ], [])
    
    skill_seduction_3 = _LocDetail(562, [
            DoLRegionNames.in_town.value,
        ], [
            DoLOptionFilters.type_skills.value,
        ], [])
    
    skill_seduction_4 = _LocDetail(563, [
            DoLRegionNames.in_town.value,
        ], [
            DoLOptionFilters.type_skills.value,
        ], [])
    
    skill_seduction_5 = _LocDetail(564, [
            DoLRegionNames.in_town.value,
        ], [
            DoLOptionFilters.type_skills.value,
        ], [])




    skill_oral_1 = _LocDetail(565, [
            DoLRegionNames.in_town.value,
        ], [
            DoLOptionFilters.type_skills.value,
        ], [])
    
    skill_oral_2 = _LocDetail(566, [
            DoLRegionNames.in_town.value,
        ], [
            DoLOptionFilters.type_skills.value,
        ], [])
    
    skill_oral_3 = _LocDetail(567, [
            DoLRegionNames.in_town.value,
        ], [
            DoLOptionFilters.type_skills.value,
        ], [
            DoLRules.oral_1
        ])
    
    skill_oral_4 = _LocDetail(568, [
            DoLRegionNames.in_town.value,
        ], [
            DoLOptionFilters.type_skills.value,
        ], [
            DoLRules.oral_2
        ])
    
    skill_oral_5 = _LocDetail(569, [
            DoLRegionNames.in_town.value,
        ], [
            DoLOptionFilters.type_skills.value,
        ], [
            DoLRules.oral_3
        ])



    skill_chest_1 = _LocDetail(570, [
            DoLRegionNames.in_town.value,
        ], [
            DoLOptionFilters.type_skills.value,
        ], [])
    
    skill_chest_2 = _LocDetail(571, [
            DoLRegionNames.in_town.value,
        ], [
            DoLOptionFilters.type_skills.value,
        ], [])
    
    skill_chest_3 = _LocDetail(572, [
            DoLRegionNames.in_town.value,
        ], [
            DoLOptionFilters.type_skills.value,
        ], [
            DoLRules.chest_1,
        ])
    
    skill_chest_4 = _LocDetail(573, [
            DoLRegionNames.in_town.value,
        ], [
            DoLOptionFilters.type_skills.value,
        ], [
            DoLRules.chest_2,
        ])
    
    skill_chest_5 = _LocDetail(574, [
            DoLRegionNames.in_town.value,
        ], [
            DoLOptionFilters.type_skills.value,
        ], [
            DoLRules.chest_3,
        ])



    skill_hands_1 = _LocDetail(575, [
            DoLRegionNames.in_town.value,
        ], [
            DoLOptionFilters.type_skills.value,
        ], [])
    
    skill_hands_2 = _LocDetail(576, [
            DoLRegionNames.in_town.value,
        ], [
            DoLOptionFilters.type_skills.value,
        ], [])
    
    skill_hands_3 = _LocDetail(577, [
            DoLRegionNames.in_town.value,
        ], [
            DoLOptionFilters.type_skills.value,
        ], [
            DoLRules.hands_1,
        ])
    
    skill_hands_4 = _LocDetail(578, [
            DoLRegionNames.in_town.value,
        ], [
            DoLOptionFilters.type_skills.value,
        ], [
            DoLRules.hands_2
        ])
    
    skill_hands_5 = _LocDetail(579, [
            DoLRegionNames.in_town.value,
        ], [
            DoLOptionFilters.type_skills.value,
        ], [
            DoLRules.hands_3
        ])



    skill_buttocks_1 = _LocDetail(580, [
            DoLRegionNames.in_town.value,
        ], [
            DoLOptionFilters.type_skills.value,
        ], [])
    
    skill_buttocks_2 = _LocDetail(581, [
            DoLRegionNames.in_town.value,
        ], [
            DoLOptionFilters.type_skills.value,
        ], [])
    
    skill_buttocks_3 = _LocDetail(582, [
            DoLRegionNames.in_town.value,
        ], [
            DoLOptionFilters.type_skills.value,
        ], [
            DoLRules.buttocks_1,
        ])
    
    skill_buttocks_4 = _LocDetail(583, [
            DoLRegionNames.in_town.value,
        ], [
            DoLOptionFilters.type_skills.value,
        ], [
            DoLRules.buttocks_2,
        ])
    
    skill_buttocks_5 = _LocDetail(584, [
            DoLRegionNames.in_town.value,
        ], [
            DoLOptionFilters.type_skills.value,
        ], [
            DoLRules.buttocks_3,
        ])


                        
    skill_privates_1 = _LocDetail(585, [
            DoLRegionNames.in_town.value,
        ], [
            DoLOptionFilters.type_skills.value,
        ], [])
    
    skill_privates_2 = _LocDetail(586, [
            DoLRegionNames.in_town.value,
        ], [
            DoLOptionFilters.type_skills.value,
        ], [])
    
    skill_privates_3 = _LocDetail(587, [
            DoLRegionNames.in_town.value,
        ], [
            DoLOptionFilters.type_skills.value,
        ], [
            DoLRules.privates_1,
        ])
    
    skill_privates_4 = _LocDetail(588, [
            DoLRegionNames.in_town.value,
        ], [
            DoLOptionFilters.type_skills.value,
        ], [
            DoLRules.privates_2,
        ])
    
    skill_privates_5 = _LocDetail(589, [
            DoLRegionNames.in_town.value,
        ], [
            DoLOptionFilters.type_skills.value,
        ], [
            DoLRules.privates_3,
        ])



    skill_anal_1 = _LocDetail(590, [
            DoLRegionNames.in_town.value,
        ], [
            DoLOptionFilters.type_skills.value,
        ], [])
    
    skill_anal_2 = _LocDetail(591, [
            DoLRegionNames.in_town.value,
        ], [
            DoLOptionFilters.type_skills.value,
        ], [])
    
    skill_anal_3 = _LocDetail(592, [
            DoLRegionNames.in_town.value,
        ], [
            DoLOptionFilters.type_skills.value,
        ], [
            DoLRules.anal_1,
        ])
    
    skill_anal_4 = _LocDetail(593, [
            DoLRegionNames.in_town.value,
        ], [
            DoLOptionFilters.type_skills.value,
        ], [
            DoLRules.anal_2,
        ])
    
    skill_anal_5 = _LocDetail(594, [
            DoLRegionNames.in_town.value,
        ], [
            DoLOptionFilters.type_skills.value,
        ], [
            DoLRules.anal_3,
        ])



    # NOTE: can use riding school for higher levels
    skill_thighs_1 = _LocDetail(595, [
            DoLRegionNames.in_town.value,
        ], [
            DoLOptionFilters.type_skills.value,
        ], [])
    
    skill_thighs_2 = _LocDetail(596, [
            DoLRegionNames.in_town.value,
        ], [
            DoLOptionFilters.type_skills.value,
        ], [])
    
    skill_thighs_3 = _LocDetail(597, [
            DoLRegionNames.in_town.value,
        ], [
            DoLOptionFilters.type_skills.value,
        ], [
            DoLRules.thighs_1,
        ])
    
    skill_thighs_4 = _LocDetail(598, [
            DoLRegionNames.in_town.value,
        ], [
            DoLOptionFilters.type_skills.value,
        ], [
            DoLRules.thighs_2,
        ])
    
    skill_thighs_5 = _LocDetail(599, [
            DoLRegionNames.in_town.value,
        ], [
            DoLOptionFilters.type_skills.value,
        ], [
            DoLRules.thighs_3,
        ])


    # NOTE: can use dance studio for higher levels
    skill_feet_1 = _LocDetail(600, [
            DoLRegionNames.in_town.value,
        ], [
            DoLOptionFilters.type_skills.value,
        ], [])
    
    skill_feet_2 = _LocDetail(601, [
            DoLRegionNames.in_town.value,
        ], [
            DoLOptionFilters.type_skills.value,
        ], [])
    
    skill_feet_3 = _LocDetail(602, [
            DoLRegionNames.in_town.value,
        ], [
            DoLOptionFilters.type_skills.value,
        ], [
            DoLRules.feet_1,
        ])
    
    skill_feet_4 = _LocDetail(603, [
            DoLRegionNames.in_town.value,
        ], [
            DoLOptionFilters.type_skills.value,
        ], [
            DoLRules.feet_2,
        ])
    
    skill_feet_5 = _LocDetail(604, [
            DoLRegionNames.in_town.value,
        ], [
            DoLOptionFilters.type_skills.value,
        ], [
            DoLRules.feet_3,
        ])



    # ---------------- School Skills ----------------
    # pretty much need school for all school skills

    skill_science_1 = _LocDetail(605, [
            DoLRegionNames.school.value,
        ], [
            DoLOptionFilters.type_skills.value,
        ], [])
    
    skill_science_2 = _LocDetail(606, [
            DoLRegionNames.school.value,
        ], [
            DoLOptionFilters.type_skills.value,
        ], [])
    
    skill_science_3 = _LocDetail(607, [
            DoLRegionNames.school.value,
        ], [
            DoLOptionFilters.type_skills.value,
        ], [])
    
    skill_science_4 = _LocDetail(608, [
            DoLRegionNames.school.value,
        ], [
            DoLOptionFilters.type_skills.value,
        ], [])
    
    skill_science_5 = _LocDetail(609, [
            DoLRegionNames.school.value,
        ], [
            DoLOptionFilters.type_skills.value,
        ], [])


                        
    skill_math_1 = _LocDetail(610, [
            DoLRegionNames.school.value,
        ], [
            DoLOptionFilters.type_skills.value,
        ], [])
    
    skill_math_2 = _LocDetail(611, [
            DoLRegionNames.school.value,
        ], [
            DoLOptionFilters.type_skills.value,
        ], [])
    
    skill_math_3 = _LocDetail(612, [
            DoLRegionNames.school.value,
        ], [
            DoLOptionFilters.type_skills.value,
        ], [])
    
    skill_math_4 = _LocDetail(613, [
            DoLRegionNames.school.value,
        ], [
            DoLOptionFilters.type_skills.value,
        ], [])
    
    skill_math_5 = _LocDetail(614, [
            DoLRegionNames.school.value,
        ], [
            DoLOptionFilters.type_skills.value,
        ], [])


    
    skill_english_1 = _LocDetail(615, [
            DoLRegionNames.school.value,
        ], [
            DoLOptionFilters.type_skills.value,
        ], [])
    
    skill_english_2 = _LocDetail(616, [
            DoLRegionNames.school.value,
        ], [
            DoLOptionFilters.type_skills.value,
        ], [])
    
    skill_english_3 = _LocDetail(617, [
            DoLRegionNames.school.value,
        ], [
            DoLOptionFilters.type_skills.value,
        ], [])
    
    skill_english_4 = _LocDetail(618, [
            DoLRegionNames.school.value,
        ], [
            DoLOptionFilters.type_skills.value,
        ], [])
    
    skill_english_5 = _LocDetail(619, [
            DoLRegionNames.school.value,
        ], [
            DoLOptionFilters.type_skills.value,
        ], [])


    
    skill_history_1 = _LocDetail(620, [
            DoLRegionNames.school.value,
        ], [
            DoLOptionFilters.type_skills.value,
        ], [])
    
    skill_history_2 = _LocDetail(621, [
            DoLRegionNames.school.value,
        ], [
            DoLOptionFilters.type_skills.value,
        ], [])
    
    skill_history_3 = _LocDetail(622, [
            DoLRegionNames.school.value,
        ], [
            DoLOptionFilters.type_skills.value,
        ], [])
    
    skill_history_4 = _LocDetail(623, [
            DoLRegionNames.school.value,
        ], [
            DoLOptionFilters.type_skills.value,
        ], [])
    
    skill_history_5 = _LocDetail(624, [
            DoLRegionNames.school.value,
        ], [
            DoLOptionFilters.type_skills.value,
        ], [])



    # ---------------- Core Skills ----------------
    # no strict requirements for any of these stats, outside of doing encounters that grow them
    # willpower: grows via any encounters
    # physique: grows via exercise
    # promiscuity: grows by doing things with this stat
    # exhibitionism: grows by doing things with this stat
    # deviancy: grows via animal encounters

    skill_willpower_1 = _LocDetail(625, [
            DoLRegionNames.in_town.value, 
        ], [
            DoLOptionFilters.type_skills.value,
        ], [])
    
    skill_willpower_2 = _LocDetail(626, [
            DoLRegionNames.in_town.value, 
        ], [
            DoLOptionFilters.type_skills.value,
        ], [])
    
    skill_willpower_3 = _LocDetail(627, [
            DoLRegionNames.in_town.value, 
        ], [
            DoLOptionFilters.type_skills.value,
        ], [])
    
    skill_willpower_4 = _LocDetail(628, [
            DoLRegionNames.in_town.value, 
        ], [
            DoLOptionFilters.type_skills.value,
        ], [])
    
    skill_willpower_5 = _LocDetail(629, [
            DoLRegionNames.in_town.value, 
        ], [
            DoLOptionFilters.type_skills.value,
        ], [])
    
    skill_willpower_6 = _LocDetail(630, [
            DoLRegionNames.in_town.value, 
        ], [
            DoLOptionFilters.type_skills.value,
        ], [])



    # NOTE: park good place to train
    skill_physique_1 = _LocDetail(631, [
            DoLRegionNames.park.value, 
        ], [
            DoLOptionFilters.type_skills.value,
        ], [])
    
    skill_physique_2 = _LocDetail(632, [
            DoLRegionNames.park.value, 
        ], [
            DoLOptionFilters.type_skills.value,
        ], [])
    
    skill_physique_3 = _LocDetail(633, [
            DoLRegionNames.park.value,
        ], [
            DoLOptionFilters.type_skills.value,
        ], [])
    
    skill_physique_4 = _LocDetail(634, [
            DoLRegionNames.park.value,
        ], [
            DoLOptionFilters.type_skills.value,
        ], [])
    
    skill_physique_5 = _LocDetail(635, [
            DoLRegionNames.park.value,
        ], [
            DoLOptionFilters.type_skills.value,
        ], [])
    
    skill_physique_6 = _LocDetail(636, [
            DoLRegionNames.park.value,
        ], [
            DoLOptionFilters.type_skills.value,
        ], [])



    skill_promiscuity_1 = _LocDetail(637, [
            DoLRegionNames.in_town.value,
        ], [
            DoLOptionFilters.type_skills.value,
        ], [])
    
    skill_promiscuity_2 = _LocDetail(638, [
            DoLRegionNames.in_town.value,
        ], [
            DoLOptionFilters.type_skills.value,
        ], [])
    
    skill_promiscuity_3 = _LocDetail(639, [
            DoLRegionNames.in_town.value,
        ], [
            DoLOptionFilters.type_skills.value,
        ], [])
    
    skill_promiscuity_4 = _LocDetail(640, [
            DoLRegionNames.in_town.value,
        ], [
            DoLOptionFilters.type_skills.value,
        ], [])
    
    skill_promiscuity_5 = _LocDetail(641, [
            DoLRegionNames.in_town.value,
        ], [
            DoLOptionFilters.type_skills.value,
        ], [])
    
    skill_promiscuity_6 = _LocDetail(642, [
            DoLRegionNames.in_town.value,
        ], [
            DoLOptionFilters.type_skills.value,
        ], [])



    # NOTE: orph for minimum level + need wardrobe
    skill_exhibitionism_1 = _LocDetail(643, [
            DoLRegionNames.orphanage.value, 
        ], [
            DoLOptionFilters.type_skills.value,
        ], [])
    
    skill_exhibitionism_2 = _LocDetail(644, [
            DoLRegionNames.orphanage.value,
        ], [
            DoLOptionFilters.type_skills.value,
        ], [])
    
    skill_exhibitionism_3 = _LocDetail(645, [
            DoLRegionNames.orphanage.value,
        ], [
            DoLOptionFilters.type_skills.value,
        ], [])
    
    skill_exhibitionism_4 = _LocDetail(646, [
            DoLRegionNames.orphanage.value,
        ], [
            DoLOptionFilters.type_skills.value,
        ], [])
    
    skill_exhibitionism_5 = _LocDetail(647, [
            DoLRegionNames.orphanage.value,
        ], [
            DoLOptionFilters.type_skills.value,
        ], [])
    
    skill_exhibitionism_6 = _LocDetail(648, [
            DoLRegionNames.orphanage.value,
        ], [
            DoLOptionFilters.type_skills.value,
        ], [])


    # NOTE: wiki recommends farm, but can level from anywhere
    skill_deviancy_1 = _LocDetail(649, [
            DoLRegionNames.in_town.value, 
        ], [
            DoLOptionFilters.type_skills.value,
        ], [])
    
    skill_deviancy_2 = _LocDetail(650, [
            DoLRegionNames.in_town.value,
        ], [
            DoLOptionFilters.type_skills.value,
        ], [])
    
    skill_deviancy_3 = _LocDetail(651, [
            DoLRegionNames.in_town.value,
        ], [
            DoLOptionFilters.type_skills.value,
        ], [])
    
    skill_deviancy_4 = _LocDetail(652, [
            DoLRegionNames.in_town.value,
        ], [
            DoLOptionFilters.type_skills.value,
        ], [])
    
    skill_deviancy_5 = _LocDetail(653, [
            DoLRegionNames.in_town.value,
        ], [
            DoLOptionFilters.type_skills.value,
        ], [])
    
    skill_deviancy_6 = _LocDetail(654, [
            DoLRegionNames.in_town.value,
        ], [
            DoLOptionFilters.type_skills.value,
        ], [])


    # ---------------- Feats ----------------

    # keeping money feats as in town for now
    # later can add every loc to make money
    feat_pocketchange = _LocDetail(1000, [
                DoLRegionNames.in_town.value,
            ], [
                DoLOptionFilters.type_feat.value,
                DoLOptionFilters.req_feat_copper.value,
            ], [])

    feat_moneymaker = _LocDetail(1001, [
                DoLRegionNames.in_town.value,
            ], [
                DoLOptionFilters.type_feat.value,
                DoLOptionFilters.req_feat_copper.value,
            ], [])

    feat_tycoon = _LocDetail(1002, [
            DoLRegionNames.in_town.value,
        ], [
            DoLOptionFilters.type_feat.value,
            DoLOptionFilters.req_feat_silver.value,
        ], [])

    feat_millionaire = _LocDetail(1003, [
            DoLRegionNames.in_town.value,
        ], [
            DoLOptionFilters.type_feat.value,
            DoLOptionFilters.req_feat_gold.value,
            DoLOptionFilters.req_difficult.value,
        ], [])

    feat_itbelongsinamuseum = _LocDetail(1004, [
            DoLRegionNames.museum.value,
        ], [
            DoLOptionFilters.type_feat.value,
            DoLOptionFilters.req_feat_gold.value,
            DoLOptionFilters.req_difficult.value,
        ], [
            DoLRules.access_antiques,
        ])

    feat_fullycovered = _LocDetail(1005, [
            DoLRegionNames.in_global.value,
        ], [
            DoLOptionFilters.type_feat.value,
            DoLOptionFilters.req_feat_gold.value,
            DoLOptionFilters.req_difficult.value,
        ], [])

    feat_beingaboy = _LocDetail(1006, [
            DoLRegionNames.in_global.value,
        ], [
            DoLOptionFilters.type_feat.value,
            DoLOptionFilters.req_feat_copper.value,
            DoLOptionFilters.req_multipleruns.value,
        ], [])

    feat_beingagirl = _LocDetail(1007, [
            DoLRegionNames.in_global.value,
        ], [
            DoLOptionFilters.type_feat.value,
            DoLOptionFilters.req_feat_copper.value,
            DoLOptionFilters.req_multipleruns.value,
        ], [])

    feat_beingahermaphrodite = _LocDetail(1008, [
            DoLRegionNames.in_global.value,
        ], [
            DoLOptionFilters.type_feat.value,
            DoLOptionFilters.req_feat_copper.value,
            DoLOptionFilters.req_multipleruns.value,
        ], [])

    feat_beinganorphan = _LocDetail(1009, [
            DoLRegionNames.in_global.value,
        ], [
            DoLOptionFilters.type_feat.value,
            DoLOptionFilters.req_feat_silver.value,
            DoLOptionFilters.req_difficult.value,
        ], [])

    feat_stressfulchallenge = _LocDetail(1010, [
            DoLRegionNames.in_global.value,
        ], [
            DoLOptionFilters.type_feat.value,
            DoLOptionFilters.req_feat_silver.value,
            DoLOptionFilters.req_multipleruns.value,
            DoLOptionFilters.req_difficult.value,
        ], [])

    feat_longstressfulchallenge = _LocDetail(1011, [
            DoLRegionNames.in_global.value,
        ], [
            DoLOptionFilters.type_feat.value,
            DoLOptionFilters.req_feat_gold.value,
            DoLOptionFilters.req_multipleruns.value,
            DoLOptionFilters.req_difficult.value,
            DoLOptionFilters.req_difficult.value,
        ], [])

    feat_billboard = _LocDetail(1012, [
            DoLRegionNames.orphanage.value,
        ], [
            DoLOptionFilters.type_feat.value,
            DoLOptionFilters.req_feat_copper.value,
            DoLOptionFilters.toggle_bodywriting.value,
        ], [])

    feat_alivingcanvas = _LocDetail(1013, [
            DoLRegionNames.remy_farm.value,
            DoLRegionNames.shopping_centre_tattooparlour.value,
        ], [
            DoLOptionFilters.type_feat.value,
            DoLOptionFilters.req_feat_copper.value,
            DoLOptionFilters.toggle_bodywriting.value,
        ], [])

    feat_farmhand = _LocDetail(1014, [
            DoLRegionNames.alex_farm.value,
        ], [
            DoLOptionFilters.type_feat.value,
            DoLOptionFilters.req_feat_silver.value,
        ], [])

    feat_farmer = _LocDetail(1015, [
            DoLRegionNames.alex_farm.value,
        ], [
            DoLOptionFilters.type_feat.value,
            DoLOptionFilters.req_feat_gold.value,
        ], [])

    feat_cultivator = _LocDetail(1016, [
            DoLRegionNames.alex_farm.value,
        ], [
            DoLOptionFilters.type_feat.value,
            DoLOptionFilters.req_feat_gold.value,
        ], [])

    feat_therivalfarm = _LocDetail(1017, [
            DoLRegionNames.alex_farm.value,
        ], [
            DoLOptionFilters.type_feat.value,
            DoLOptionFilters.req_feat_silver.value,
        ], [])

    feat_therivalestate = _LocDetail(1018, [
            DoLRegionNames.alex_farm.value,
        ], [
            DoLOptionFilters.type_feat.value,
            DoLOptionFilters.req_feat_gold.value,
            DoLOptionFilters.req_difficult.value,
        ], [])

    feat_heroicvictory = _LocDetail(1019, [ # TODO: lowprio LOGIC, COMPLEX
            DoLRegionNames.remy_farm.value,
        ], [
            DoLOptionFilters.type_feat.value,
            DoLOptionFilters.req_feat_gold.value,
        ], [
            # min stat requirements
        ])

    feat_fiveinarow = _LocDetail(1020, [
            DoLRegionNames.remy_estate.value,
        ], [
            DoLOptionFilters.type_feat.value,
            DoLOptionFilters.req_feat_copper.value,
        ], [])

    feat_distinction = _LocDetail(1021, [
            DoLRegionNames.school.value,
        ], [
            DoLOptionFilters.type_feat.value,
            DoLOptionFilters.req_feat_copper.value,
        ], [])

    feat_distinctive = _LocDetail(1022, [
            DoLRegionNames.school.value,
        ], [
            DoLOptionFilters.type_feat.value,
            DoLOptionFilters.req_feat_silver.value,
            DoLOptionFilters.req_difficult.value,
        ], [])

    feat_distinguished = _LocDetail(1023, [
            DoLRegionNames.school.value,
        ], [
            DoLOptionFilters.type_feat.value,
            DoLOptionFilters.req_feat_gold.value,
            DoLOptionFilters.req_difficult.value,
        ], [])

    feat_chefdetournant = _LocDetail(1024, [
            DoLRegionNames.school.value,
            DoLRegionNames.avery_mansion.value,
        ], [
            DoLOptionFilters.type_feat.value,
            DoLOptionFilters.req_feat_copper.value
        ], [])

    feat_chefdepartie = _LocDetail(1025, [
            DoLRegionNames.school.value,
            DoLRegionNames.avery_mansion.value,
        ], [
            DoLOptionFilters.type_feat.value,
            DoLOptionFilters.req_feat_silver.value,
        ], [])

    feat_souschef = _LocDetail(1026, [
            DoLRegionNames.school.value,
            DoLRegionNames.avery_mansion.value,
        ], [
            DoLOptionFilters.type_feat.value,
            DoLOptionFilters.req_feat_gold.value,
        ], [])

    feat_sciencefairwinner = _LocDetail(1027, [
            DoLRegionNames.cliff_street.value,
        ], [
            DoLOptionFilters.type_feat.value,
            DoLOptionFilters.req_feat_silver.value,
            DoLOptionFilters.req_seasonal.value,
        ], [
            DoLRules.sciencefairwinner,
        ])

    feat_thesisoffence = _LocDetail(1028, [
        # INFO : by bluecat
        #
        # Win the science fair with the phallus project
        # without any phalluses then pass a physique check
        # need seduction to get any chance to win
        #
        # Ways to get chance
        # Science Fair Sabotage:    skul(400),      +10%
        # Science Fair Flirt:       seddiff(4000),  +10%
        # So you basically have to win with a 20% chance
            DoLRegionNames.cliff_street.value,
        ], [
            DoLOptionFilters.type_feat.value,
            DoLOptionFilters.req_feat_gold.value,
            DoLOptionFilters.req_seasonal.value,
            DoLOptionFilters.req_difficult.value, # rng + seasonal
        ], [
            DoLRules.sciencefairoffence,
            # doing 100% chance because 20% chance total
            DoLRules.physique_6, # physique(4000, 14000) (very high, need large body to guarentee)
            DoLRules.seduction_4, # seduction(4000)
            DoLRules.skulduggery_4, # skul(400) 
        ])

    feat_mathscompetitionwinner = _LocDetail(1029, [
            DoLRegionNames.school.value,
        ], [
            DoLOptionFilters.type_feat.value,
            DoLOptionFilters.req_feat_silver.value,
            DoLOptionFilters.req_seasonal.value,
        ], [
            DoLRules.mathcomp
        ])

    feat_richhearts = _LocDetail(1030, [
            DoLRegionNames.school.value,
        ], [
            DoLOptionFilters.type_feat.value,
            DoLOptionFilters.req_feat_silver.value,
            DoLOptionFilters.req_seasonal.value,
        ], [])


    # Stat Feats
    # NOTE: req for training ones is just min training location for 10

    feat_mostaware = _LocDetail(1031, [
            DoLRegionNames.in_town.value,
        ], [
            DoLOptionFilters.type_feat.value,
            DoLOptionFilters.req_feat_copper.value,
        ], [])

    feat_mostinnocent = _LocDetail(1032, [
            DoLRegionNames.asylum.value,
        ], [
            DoLOptionFilters.type_feat.value,
            DoLOptionFilters.req_feat_copper.value,
        ], [])

    feat_nomorecontrol = _LocDetail(1033, [
            DoLRegionNames.in_town.value,
        ], [
            DoLOptionFilters.type_feat.value,
            DoLOptionFilters.req_feat_silver.value,
            DoLOptionFilters.bestiality_or_monsterpeople.value,
        ], [])

    feat_thief = _LocDetail(1034, [
            # min place for skul 10 is stealing in encounters
            DoLRegionNames.in_town.value,
        ], [
            DoLOptionFilters.type_feat.value,
            DoLOptionFilters.req_feat_silver.value,
        ], [
            DoLRules.skulduggery_7,
        ])

    feat_mayihavethisdance = _LocDetail(1035, [
            DoLRegionNames.dance_studio.value,
            DoLRegionNames.strip_club.value,
            DoLRegionNames.brothel.value,
        ], [
            DoLOptionFilters.type_feat.value,
            DoLOptionFilters.req_feat_copper.value,
        ], [])

    feat_aquanaut = _LocDetail(1036, [
            # school for minimum swimming
            DoLRegionNames.school.value,
        ], [
            DoLOptionFilters.type_feat.value,
            DoLOptionFilters.req_feat_copper.value,
        ], [])

    feat_seductress = _LocDetail(1037, [
            DoLRegionNames.in_town.value,
        ], [
            DoLOptionFilters.type_feat.value,
            DoLOptionFilters.req_feat_copper.value,
        ], [
            DoLRules.seduction_3,
        ])

    feat_greenfingered = _LocDetail(1038, [
            DoLRegionNames.alex_farm.value,
            DoLRegionNames.eden_cabin.value,
            DoLRegionNames.asylum.value,
            DoLRegionNames.orphanage.value,
        ], [
            DoLOptionFilters.type_feat.value,
            DoLOptionFilters.req_feat_copper.value,
        ], [])

    feat_majordomo = _LocDetail(1039, [
            DoLRegionNames.temple.value,
        ], [
            DoLOptionFilters.type_feat.value,
            DoLOptionFilters.req_feat_copper.value,
        ], [
            DoLRules.housekeeping_7,
        ])

    feat_swift = _LocDetail(1040, [
            # park good place to level
            DoLRegionNames.park.value,
        ], [
            DoLOptionFilters.type_feat.value,
            DoLOptionFilters.req_feat_copper.value,
        ], [])

    feat_alluring = _LocDetail(1041, [ # --- Modify?
        # may be a bit mean on logic
            DoLRegionNames.in_global.value,
        ], [
            DoLOptionFilters.type_feat.value,
            DoLOptionFilters.req_feat_silver.value,
        ], [])

    feat_sexspecialist = _LocDetail(1042, [ # maybe modify loc (max seduction)
            DoLRegionNames.in_town.value,
        ], [
            DoLOptionFilters.type_feat.value,
            DoLOptionFilters.req_feat_gold.value,
        ], [])

    feat_perfectrecord = _LocDetail(1043, [
            DoLRegionNames.school.value,
        ], [
            DoLOptionFilters.type_feat.value,
            DoLOptionFilters.req_feat_silver.value,
        ], [])

    feat_perfectsub = _LocDetail(1044, [ # maybe modify loc (high sub)
            DoLRegionNames.in_town.value,
        ], [
            DoLOptionFilters.type_feat.value,
            DoLOptionFilters.req_feat_silver.value,
            DoLOptionFilters.req_difficult.value,
        ], [])

    feat_defyingtheodds = _LocDetail(1045, [ # maybe modify loc (low sub)
            DoLRegionNames.in_town.value,
        ], [
            DoLOptionFilters.type_feat.value,
            DoLOptionFilters.req_feat_silver.value,
            DoLOptionFilters.req_difficult.value,
        ], [])

    feat_hawker = _LocDetail(1046, [
            DoLRegionNames.connudatus_street.value,
        ], [
            DoLOptionFilters.type_feat.value,
            DoLOptionFilters.req_feat_copper.value,
            DoLOptionFilters.req_difficult.value,
        ], [
            # Don't need farm access? this should be possible
        ])

    feat_vendor = _LocDetail(1047, [
            DoLRegionNames.connudatus_street.value,
        ], [
            DoLOptionFilters.type_feat.value,
            DoLOptionFilters.req_feat_silver.value,
        ], [
            DoLRules.access_alexfarm,
        ])

    feat_merchant = _LocDetail(1048, [
            DoLRegionNames.connudatus_street.value,
        ], [
            DoLOptionFilters.type_feat.value,
            DoLOptionFilters.req_feat_silver.value,
        ], [
            DoLRules.access_alexfarm,
        ])

    feat_twisteddesire = _LocDetail(1049, [ # maybe modify loc (maso)
            DoLRegionNames.in_town.value,
        ], [
            DoLOptionFilters.type_feat.value,
            DoLOptionFilters.req_feat_silver.value,
            DoLOptionFilters.req_difficult.value,
        ], [])

    feat_servedhot = _LocDetail(1050, [ # maybe modify loc (sad)
            DoLRegionNames.in_town.value,
        ], [
            DoLOptionFilters.type_feat.value,
            DoLOptionFilters.req_feat_silver.value,
            # sadist is easy, don't need difficult
        ], [])

    feat_sadomasochist = _LocDetail(1051, [ # maybe modify loc (sadomaso)
            DoLRegionNames.in_town.value,
        ], [
            DoLOptionFilters.type_feat.value,
            DoLOptionFilters.req_feat_gold.value,
            DoLOptionFilters.req_difficult.value,
        ], [])

    feat_shiningreputation = _LocDetail(1052, [
            DoLRegionNames.pub.value,
        ], [
            DoLOptionFilters.type_feat.value,
            DoLOptionFilters.req_feat_gold.value,
            DoLOptionFilters.req_difficult.value,
        ], [])


    # Social Feats

    feat_socialbutterfly = _LocDetail(1053, [
            DoLRegionNames.school.value,
        ], [
            DoLOptionFilters.type_feat.value,
            DoLOptionFilters.req_feat_copper.value,
        ], [])

    feat_unsocialmoth = _LocDetail(1054, [
            DoLRegionNames.school.value,
        ], [
            DoLOptionFilters.type_feat.value,
            DoLOptionFilters.req_feat_copper.value,
        ], [])

    feat_teacherspet = _LocDetail(1055, [
            DoLRegionNames.school.value,
        ], [
            DoLOptionFilters.type_feat.value,
            DoLOptionFilters.req_feat_copper.value,
        ], [])

    feat_teachersnightmare = _LocDetail(1056, [
            DoLRegionNames.school.value,
        ], [
            DoLOptionFilters.type_feat.value,
            DoLOptionFilters.req_feat_copper.value,
        ], [])

    feat_robinthelover = _LocDetail(1057, [
            DoLRegionNames.orphanage.value,
        ], [
            DoLOptionFilters.type_feat.value,
            DoLOptionFilters.req_feat_silver.value,
            DoLOptionFilters.req_loveinterest.value,
            DoLOptionFilters.req_multipleruns.value,
        ], [])

    feat_hungryorphan = _LocDetail(1058, [
            DoLRegionNames.orphanage.value
        ], [
            DoLOptionFilters.type_feat.value,
            DoLOptionFilters.req_feat_silver.value,
            DoLOptionFilters.req_loveinterest.value,
        ], [
            DoLRules.access_orphanage,
            DoLRules.access_recipe,
        ])

    feat_robinssong = _LocDetail(1059, [
            DoLRegionNames.orphanage.value,
        ], [
            DoLOptionFilters.type_feat.value,
            DoLOptionFilters.req_feat_silver.value,
            DoLOptionFilters.req_loveinterest.value,
            DoLOptionFilters.req_seasonal.value,
        ], [
            DoLRules.shoppingcentre_or_forestshop,
            DoLRules.access_school,
        ])

    feat_whitneythebully = _LocDetail(1060, [
            DoLRegionNames.school.value,
        ], [
            DoLOptionFilters.type_feat.value,
            DoLOptionFilters.req_feat_silver.value,
            DoLOptionFilters.req_loveinterest.value,
            DoLOptionFilters.req_multipleruns.value,
        ], [])

    feat_thebullystithe = _LocDetail(1061, [
            DoLRegionNames.school.value,
        ], [
            DoLOptionFilters.type_feat.value,
            DoLOptionFilters.req_feat_silver.value,
            DoLOptionFilters.req_loveinterest.value,
        ], [
            # redundant rule, school place means access recipe
            # DoLRules.access_recipe
        ])

    feat_delinquentantics = _LocDetail(1062, [
            DoLRegionNames.school.value,
        ], [
            DoLOptionFilters.type_feat.value,
            DoLOptionFilters.req_feat_copper.value,
            DoLOptionFilters.req_loveinterest.value,
        ], [])

    feat_giddyup = _LocDetail(1063, [
            DoLRegionNames.school.value,
        ], [
            DoLOptionFilters.type_feat.value,
            DoLOptionFilters.req_feat_silver.value,
            DoLOptionFilters.req_loveinterest.value,
            DoLOptionFilters.statrandomized_or_multipleruns.value,
        ], [
            DoLRules.physique_6
        ])

    feat_whitneyssecret = _LocDetail(1064, [ # TODO: ITEM
            DoLRegionNames.barb_street.value,
        ], [
            DoLOptionFilters.type_feat.value,
            DoLOptionFilters.req_feat_silver.value,
            DoLOptionFilters.req_loveinterest.value,
        ], [
            DoLRules.access_alleyway,
            # whitney's upgrade to orphanage loft
        ])

    feat_kylartheobsessed = _LocDetail(1065, [
            # need school to meet kylar
            DoLRegionNames.school.value,
        ], [
            DoLOptionFilters.type_feat.value,
            DoLOptionFilters.req_feat_silver.value,
            DoLOptionFilters.req_loveinterest.value,
            DoLOptionFilters.req_multipleruns.value,
        ], [])

    feat_notforrats = _LocDetail(1066, [
            # need school to meet kylar
            DoLRegionNames.school.value,
        ], [
            DoLOptionFilters.type_feat.value,
            DoLOptionFilters.req_feat_silver.value,
            DoLOptionFilters.req_loveinterest.value,
        ], [
            # Redudant rule, need school for recipe but loc at school
            #DoLRules.access_recipe
        ])

    feat_edenthelonely = _LocDetail(1067, [
            DoLRegionNames.eden_cabin.value,
        ], [
            DoLOptionFilters.type_feat.value,
            DoLOptionFilters.req_feat_silver.value,
            DoLOptionFilters.req_loveinterest.value,
            DoLOptionFilters.req_badend.value,
            DoLOptionFilters.req_multipleruns.value,
        ], [])

    feat_sweetandtender = _LocDetail(1068, [
            DoLRegionNames.school.value,
            DoLRegionNames.avery_mansion.value,
        ], [
            DoLOptionFilters.type_feat.value,
            DoLOptionFilters.req_feat_silver.value,
            DoLOptionFilters.req_loveinterest.value,
            DoLOptionFilters.req_badend.value,
        ], [])

    feat_averythemoneybags = _LocDetail(1069, [
            DoLRegionNames.domus_street.value,
        ], [
            DoLOptionFilters.type_feat.value,
            DoLOptionFilters.req_feat_silver.value,
            DoLOptionFilters.req_multipleruns.value,
            DoLOptionFilters.req_loveinterest.value,
        ], [])

    feat_kept = _LocDetail(1070, [
            DoLRegionNames.avery_mansion.value,
        ], [
            DoLOptionFilters.type_feat.value,
            DoLOptionFilters.req_feat_silver.value,
            DoLOptionFilters.req_loveinterest.value,
        ], [])

    feat_whatgoesaround = _LocDetail(1071, [
            DoLRegionNames.avery_mansion.value,
        ], [
            DoLOptionFilters.type_feat.value,
            DoLOptionFilters.req_feat_silver.value,
            DoLOptionFilters.req_loveinterest.value,
        ], [])

    feat_mostexclusive = _LocDetail(1072, [
            DoLRegionNames.avery_mansion.value,
        ], [
            DoLOptionFilters.type_feat.value,
            DoLOptionFilters.req_feat_silver.value,
            DoLOptionFilters.req_loveinterest.value,
            DoLOptionFilters.req_seasonal.value,
        ], [])

    feat_pridecometh = _LocDetail(1073, [
            DoLRegionNames.avery_mansion.value,
        ], [
            DoLOptionFilters.type_feat.value,
            DoLOptionFilters.req_feat_gold.value,
            DoLOptionFilters.req_loveinterest.value,
        ], [])

    feat_hautecuisine = _LocDetail(1074, [
            DoLRegionNames.avery_mansion.value,
        ], [
            DoLOptionFilters.type_feat.value,
            DoLOptionFilters.req_feat_silver.value,
            DoLOptionFilters.req_loveinterest.value,
        ], [
            # redundant rule, recipe access implied by avery mansion
            # DoLRules.access_recipe
        ])

    feat_leightontheshady = _LocDetail(1075, [
            # wiki also lists avery date, however I think this is too hard
            DoLRegionNames.brothel.value,
        ], [
            DoLOptionFilters.type_feat.value,
            DoLOptionFilters.req_feat_silver.value,
            DoLOptionFilters.req_loveinterest.value,
            DoLOptionFilters.req_multipleruns.value,
        ], [])

    feat_alextherobust = _LocDetail(1076, [
            DoLRegionNames.alex_farm.value,
        ], [
            DoLOptionFilters.type_feat.value,
            DoLOptionFilters.req_feat_silver.value,
            DoLOptionFilters.req_loveinterest.value,
            DoLOptionFilters.req_multipleruns.value,
        ], [])

    feat_homecooking = _LocDetail(1077, [
            DoLRegionNames.alex_farm.value,
        ], [
            DoLOptionFilters.type_feat.value,
            DoLOptionFilters.req_feat_silver.value,
            DoLOptionFilters.req_loveinterest.value,
        ], [
            DoLRules.access_recipe,
        ])

    feat_greathawktheterror = _LocDetail(1078, [
            DoLRegionNames.bird_tower.value,
        ], [
            DoLOptionFilters.type_feat.value,
            DoLOptionFilters.req_feat_silver.value,
            DoLOptionFilters.req_loveinterest.value,
            DoLOptionFilters.req_badend.value,
            DoLOptionFilters.req_multipleruns.value,
        ], [])

    feat_returnthefavour = _LocDetail(1079, [
            DoLRegionNames.bird_tower.value,
        ], [
            DoLOptionFilters.type_feat.value,
            DoLOptionFilters.req_feat_silver.value,
            DoLOptionFilters.req_loveinterest.value,
            DoLOptionFilters.req_badend.value,
        ], [
            DoLRules.access_recipe,
        ])

    feat_feathertrick = _LocDetail(1080, [
            DoLRegionNames.bird_tower.value,
        ], [
            DoLOptionFilters.type_feat.value,
            DoLOptionFilters.req_feat_silver.value,
            DoLOptionFilters.req_loveinterest.value,
            DoLOptionFilters.req_transformation.value,
            DoLOptionFilters.toggle_transformation_either.value, # need flight
            DoLOptionFilters.req_badend.value,
        ], [
            DoLRules.dancing_9, # 50%
            DoLRules.tending_4, # 57%
            # for you to get the ability to hunt
            # for lurkers, you need harpy tf to eat one
            # and like eating one. HOWEVER, this is for
            # targeted hunts and you seem to still be able
            # to get one randomly
            # DoLRules.tfrule_harpy_full_appear,
            DoLRules.tfrule_flight,
            # NOTE: from what it looks like, lurkers
            # do not need to be enabled for this
        ])

    feat_wrenthesly = _LocDetail(1081, [
            DoLRegionNames.remy_estate.value,
        ], [
            DoLOptionFilters.type_feat.value,
            DoLOptionFilters.req_feat_silver.value,
            DoLOptionFilters.req_loveinterest.value,
            DoLOptionFilters.req_multipleruns.value,
        ], [])

    feat_blackwolfthealpha = _LocDetail(1082, [
            DoLRegionNames.forest.value,
            DoLRegionNames.wolf_cave.value,
        ], [
            DoLOptionFilters.type_feat.value,
            DoLOptionFilters.req_feat_silver.value,
            DoLOptionFilters.req_loveinterest.value,
            DoLOptionFilters.req_badend.value,
            DoLOptionFilters.req_multipleruns.value,
            DoLOptionFilters.toggle_bestiality.value,
        ], [])

    feat_encroachingcivilisation = _LocDetail(1083, [    
            DoLRegionNames.wolf_cave.value,
        ], [
            DoLOptionFilters.type_feat.value,
            DoLOptionFilters.req_feat_silver.value,
            DoLOptionFilters.req_loveinterest.value,
            DoLOptionFilters.req_badend.value,
        ], [
            DoLRules.access_recipe,
        ])

    feat_sydneythepurehearted = _LocDetail(1084, [
        # reminder: this is sydney's virginity, not yours
            DoLRegionNames.temple.value,
        ], [
            DoLOptionFilters.type_feat.value,
            DoLOptionFilters.req_feat_silver.value,
            DoLOptionFilters.req_loveinterest.value,
        ], [])

    feat_communion = _LocDetail(1085, [
            DoLRegionNames.school.value,
            DoLRegionNames.temple.value,
        ], [
            DoLOptionFilters.type_feat.value,
            DoLOptionFilters.req_feat_silver.value,
            DoLOptionFilters.req_loveinterest.value,
        ], [
            DoLRules.access_recipe,
        ])

    feat_harperthehypnotist = _LocDetail(1086, [
            DoLRegionNames.asylum.value,
            DoLRegionNames.remy_farm.value,
        ], [
            DoLOptionFilters.type_feat.value,
            DoLOptionFilters.req_feat_silver.value,
            DoLOptionFilters.req_badend.value,
            DoLOptionFilters.req_multipleruns.value,
            DoLOptionFilters.req_loveinterest.value,
            DoLOptionFilters.req_difficult.value, # guessing its difficult?
        ], [
            # remy's farm also requires skul, 
            # however since its asylum also not listed here
            # maybe make a longer rule in future
        ])

    feat_morganthelost = _LocDetail(1087, [
            DoLRegionNames.old_sewers.value
        ], [
            DoLOptionFilters.type_feat.value,
            DoLOptionFilters.req_feat_silver.value,
            DoLOptionFilters.req_multipleruns.value,
            DoLOptionFilters.req_loveinterest.value,
        ], [])

    feat_gwylanthebewitching = _LocDetail(1088, [
            DoLRegionNames.forest_shop.value,
        ], [
            DoLOptionFilters.type_feat.value,
            DoLOptionFilters.req_feat_silver.value,
            DoLOptionFilters.req_multipleruns.value,
            DoLOptionFilters.req_loveinterest.value,
            DoLOptionFilters.req_difficult.value, # guessing its difficult?
        ], [
            DoLRules.gwylan_forestvessel,
        ])

    feat_covencomforts = _LocDetail(1089, [
            DoLRegionNames.forest_shop.value,
        ], [
            DoLOptionFilters.type_feat.value,
            DoLOptionFilters.req_feat_silver.value,
            DoLOptionFilters.req_loveinterest.value,
        ], [
            DoLRules.access_recipe,
        ])

    feat_lovetriangles = _LocDetail(1090, [
            # need school for kylar and whitney
            DoLRegionNames.school.value,
        ], [
            DoLOptionFilters.type_feat.value,
            DoLOptionFilters.req_feat_silver.value,
            DoLOptionFilters.req_loveinterest.value,
        ], [])

    feat_lovetrapezoids = _LocDetail(1091, [
            # need school for kylar and whitney
            DoLRegionNames.school.value,
        ], [
            DoLOptionFilters.type_feat.value,
            DoLOptionFilters.req_feat_gold.value,
            DoLOptionFilters.req_loveinterest.value,
        ], [])

    feat_bemyvalentine = _LocDetail(1092, 
            DoLRegionGroups.loveinterest.value
        , [
            DoLOptionFilters.type_feat.value,
            DoLOptionFilters.req_feat_copper.value,
            DoLOptionFilters.req_loveinterest.value,
            DoLOptionFilters.req_seasonal.value,
        ], [
            DoLRules.recipe_or_shoppingcentre,
        ])

    feat_ballroomshowoff = _LocDetail(1093, [
            DoLRegionNames.domus_street.value,
        ], [
            DoLOptionFilters.type_feat.value,
            DoLOptionFilters.req_feat_copper.value,
            DoLOptionFilters.req_loveinterest.value,
        ], [
            DoLRules.ballroomshowoff
        ])

    feat_underthetable = _LocDetail(1094, [
            DoLRegionNames.docks.value,
        ], [
            DoLOptionFilters.type_feat.value,
            DoLOptionFilters.req_feat_copper.value,
        ], [])

    feat_pubcrawlvictors = _LocDetail(1095, [ # INFO
        # INFO : by bluecat
        #
        # Questions:
        # - science gte (1, 1000)
        # - math gte (1, 1000)
        # - english gte (1, 1000)
        # - history gte (1, 1000)
        # - promiscuity gte (1, 100)
        #
        # 5 questions are chosen, can have duplicates
        #
        # If you let your dockers handle it, they have a 50/50 shot
        # the enemy always has a 50/50 shot
        #
        # this should mean you always have at least a 50/50
        # unless you gamble with bad stats
            DoLRegionNames.docks.value,
        ], [
            DoLOptionFilters.type_feat.value,
            DoLOptionFilters.req_feat_copper.value,
        ], [])

    feat_masonssecret = _LocDetail(1096, [
            DoLRegionNames.forest_lake.value,
        ], [
            DoLOptionFilters.type_feat.value,
            DoLOptionFilters.req_feat_silver.value,
            DoLOptionFilters.req_loveinterest.value,
        ], [
            DoLRules.access_school,
        ])

    feat_masonsshame = _LocDetail(1097, [
            DoLRegionNames.school.value,
        ], [
            DoLOptionFilters.type_feat.value,
            DoLOptionFilters.req_feat_silver.value,
            DoLOptionFilters.req_loveinterest.value,
        ], [])

    feat_animaltender = _LocDetail(1098, [ # TODO: LOGIC tending req
            DoLRegionNames.alex_farm.value,
        ], [
            DoLOptionFilters.type_feat.value,
            DoLOptionFilters.req_feat_silver.value,
        ], [])

    feat_ispy = _LocDetail(1099, [
            DoLRegionNames.alex_farm.value,
        ], [
            DoLOptionFilters.type_feat.value,
            DoLOptionFilters.req_feat_copper.value,
        ], [
            DoLRules.skulduggery_4, # ~50%
        ])

    feat_firstkiss = _LocDetail(1100, 
            DoLRegionGroups.loveinterest.value
        , [
            DoLOptionFilters.type_feat.value,
            DoLOptionFilters.req_feat_copper.value,
            DoLOptionFilters.req_loveinterest.value,
            DoLOptionFilters.req_multipleruns.value,
        ], [])

    feat_acrimemostfoul = _LocDetail(1101, [
            DoLRegionNames.school.value,
        ], [
            DoLOptionFilters.type_feat.value,
            DoLOptionFilters.req_feat_silver.value,
            DoLOptionFilters.req_loveinterest.value,
            DoLOptionFilters.toggle_bodywriting.value # sydney will write on you unless you have bodywriting **off**
        ], [])

    feat_longing = _LocDetail(1102, [
            DoLRegionNames.kylar_manor.value,
        ], [
            DoLOptionFilters.type_feat.value,
            DoLOptionFilters.req_feat_gold.value,
            DoLOptionFilters.req_loveinterest.value,
            DoLOptionFilters.req_badend.value,
        ], [])

    feat_paganrite = _LocDetail(1103, [
            DoLRegionNames.temple.value,
        ], [
            DoLOptionFilters.type_feat.value,
            DoLOptionFilters.req_feat_copper.value,
            DoLOptionFilters.req_loveinterest.value,
            DoLOptionFilters.req_badend.value,
        ], [
            DoLRules.access_kylarmanor,
            DoLRules.access_intown,
        ])

    feat_warmestwinter = _LocDetail(1104, [
            DoLRegionNames.pub.value,
        ], [
            DoLOptionFilters.type_feat.value,
            DoLOptionFilters.req_feat_silver.value,
        ], [
            DoLRules.access_museum,
        ])

    feat_trialsoffaith = _LocDetail(1105, [
            DoLRegionNames.museum.value,
        ], [
            DoLOptionFilters.type_feat.value,
            DoLOptionFilters.req_feat_platinum.value,
        ], [
            DoLRules.has_serpentpainting,
        ])

    feat_firstverse = _LocDetail(1106, [
            DoLRegionNames.forest_shop.value,
        ], [
            DoLOptionFilters.type_feat.value,
            DoLOptionFilters.req_feat_copper.value,
            DoLOptionFilters.req_loveinterest.value,
        ], [
            DoLRules.firstverse,
        ]) 

    feat_wildsong = _LocDetail(1107, [
            DoLRegionNames.forest_shop.value,
        ], [
            DoLOptionFilters.type_feat.value,
            DoLOptionFilters.req_feat_silver.value,
            DoLOptionFilters.req_loveinterest.value,
        ], [
            DoLRules.gwylan_forestvessel,
        ]) 

    feat_foxbane = _LocDetail(1108, [
            DoLRegionNames.forest.value,
        ], [
            DoLOptionFilters.type_feat.value,
            DoLOptionFilters.req_feat_silver.value,
            DoLOptionFilters.req_loveinterest.value,
        ], [
            DoLRules.foxbane,
        ])


    # Transformation feats

    feat_purrfect = _LocDetail(1109, [
            DoLRegionNames.cafe.value, # deluxe cream buns
            # wiki also lists cows with mouth on alex with dev 4
            # and teasing dogs on domus street
        ], [
            DoLOptionFilters.type_feat.value,
            DoLOptionFilters.req_feat_copper.value,
            DoLOptionFilters.req_transformation.value,
            DoLOptionFilters.toggle_transformation_animal.value,
        ], [])

    feat_howlatthemoon = _LocDetail(1110, [
            DoLRegionNames.forest.value, # wolfshrooms can be eaten to do wolf w/o bestiality
            DoLRegionNames.wolf_cave.value, # wolf cave doesn't gen connections w/o bestiality
        ], [
            DoLOptionFilters.type_feat.value,
            DoLOptionFilters.req_feat_copper.value,
            DoLOptionFilters.req_transformation.value,
            DoLOptionFilters.toggle_transformation_animal.value,
        ], [])

    feat_messwiththebull = _LocDetail(1111, [
            DoLRegionNames.remy_farm.value,
        ], [
            DoLOptionFilters.type_feat.value,
            DoLOptionFilters.req_feat_copper.value,
            DoLOptionFilters.req_transformation.value,
            DoLOptionFilters.req_badend.value,
            DoLOptionFilters.toggle_transformation_animal.value,
        ], [])

    feat_flylikeaneagle = _LocDetail(1112, [
            DoLRegionNames.bird_tower.value,
        ], [
            DoLOptionFilters.type_feat.value,
            DoLOptionFilters.req_feat_copper.value,
            DoLOptionFilters.req_transformation.value,
            DoLOptionFilters.req_badend.value,
            DoLOptionFilters.toggle_transformation_animal.value,
            # beast req?
        ], [])

    feat_youslyfox = _LocDetail(1113, [
            DoLRegionNames.forest.value,
            # maybe add more locations
        ], [
            DoLOptionFilters.type_feat.value,
            DoLOptionFilters.req_feat_copper.value,
            DoLOptionFilters.req_transformation.value,
            DoLOptionFilters.toggle_transformation_animal.value,
        ], [])

    feat_walklikeanangel = _LocDetail(1114, [
            DoLRegionNames.temple.value,
        ], [
            DoLOptionFilters.type_feat.value,
            DoLOptionFilters.req_feat_copper.value,
            DoLOptionFilters.req_transformation.value,
            DoLOptionFilters.toggle_transformation_divine.value,
            DoLOptionFilters.req_multipleruns.value,
        ], [])

    feat_fallingfallingfalling = _LocDetail(1115, [
            DoLRegionNames.temple.value,
        ], [
            DoLOptionFilters.type_feat.value,
            DoLOptionFilters.req_feat_copper.value,
            DoLOptionFilters.req_transformation.value,
            DoLOptionFilters.toggle_transformation_divine.value,
            DoLOptionFilters.req_multipleruns.value,
        ], [])

    feat_devilishlooks = _LocDetail(1116, [
            DoLRegionNames.in_town.value,
        ], [
            DoLOptionFilters.type_feat.value,
            DoLOptionFilters.req_feat_copper.value,
            DoLOptionFilters.req_transformation.value,
            DoLOptionFilters.toggle_transformation_divine.value,
        ], [])


    # Discovery - In Town feats

    feat_headchef = _LocDetail(1117, [
            DoLRegionNames.cafe.value,
        ], [
            DoLOptionFilters.type_feat.value,
            DoLOptionFilters.req_feat_silver.value,
            # no req timeframe, no multipleruns needed
        ], [])

    feat_laughingstock = _LocDetail(1118, [
            DoLRegionNames.police_station.value,
        ], [
            DoLOptionFilters.type_feat.value,
            DoLOptionFilters.req_feat_silver.value,
        ], [
            DoLRules.access_pub,
            # no skul req?
        ])

    feat_yourethelaughingstock = _LocDetail(1119, [
            DoLRegionNames.jail.value, 
        ], [
            DoLOptionFilters.type_feat.value,
            DoLOptionFilters.req_feat_silver.value,
        ], [])

    feat_illicitscience = _LocDetail(1120, [
            DoLRegionNames.compound.value,
        ], [
            DoLOptionFilters.type_feat.value,
            DoLOptionFilters.req_feat_copper.value,
        ], []) # rules to get handled by access rules

    feat_mouthsealedshut = _LocDetail(1121, [ # INFO
        # INFO feat_mouthseledshut : by bluecat
        #
        # win: 
        #   .honest + .lie + .mock + .beg + .flirt gte 10
        # lose:
        #   if .honest gte 5
        #   if pain gte 100 and willpowerpain = 0
        #   if arousal gte arousalmax
        #
        # options:
        # .honest:  <<arousal 3000>><<pain -3>><<stress 6>>
        #
        # .lie:     <<arousal -1000>><<pain 7>><<trauma 6>><<stress 6>>
        #
        # .mock:    req: submissive lte 500
        #           <<arousal -2000>><<pain 7>><<stress 6>>
        #
        # .beg:     req: $submissive gte 1500
        #           <<arousal 3000>><<pain -5>><<stress 6>>
        #
        # .flirt:   req promiscutiy: 0, 2, 3, 4, 5
        #           <<pain -3>>
        #
        # lie max: 4 
        # honest max: 4
        # flirt max: 5
        #
        # Pain Based on Science (no maso):
        # reminder: sciencetrait is 0, 200, 400, 700, 1000
        # pain 7: 7, 6.3, 5.6, 4.9, 4.2
        #
        # seems pain is not an issue, just arousal
        # reminder: arousal base cap is 10k
        #
        # to math it out, ignoring mock and beg, and assuming base stats
        # .flirt 1  (pain  -3)
        # .lie 4    (pain  28)  (arousal -4000)
        # .honest 4 (pain -12)  (arousal 12000)
        #
        # total: 9 passages, pain 13, arousal 8000
        # meaning we do need at least 1 extra flirt from min stats
        #
        # arousal is a bit high though so I will make it
        # pros 3 minimum instead of pros 2
        # in the future I can also add submissive/bratty items
        # as req to reduce pros requirement, as bratty reduces arousal
            DoLRegionNames.compound.value,
        ], [
            DoLOptionFilters.type_feat.value,
            DoLOptionFilters.req_feat_copper.value,
        ], [
            DoLRules.promiscuity_3,
        ])

    feat_neckdeep = _LocDetail(1122, [ # INFO
        # INFO feat_neckdeep : by bluecat
        #
        # requires 8 passage movements
        # if you reach max aros or pain, you fail event
        #
        # choice 1: pain++
        # choice 2: willpower check
        #
        # max sci can do 3 pain checks
        # otherwise 2-3 pain checks
        #
        # willpower check adds 2k arousal if failed (10k aros cap default)
        #
        # Conclusion:
        # being leinaint, we could fail 3 willpower checks, meaning we have to do
        # 3 willpower checks, 2 pain checks
        # meaning 50% chance to completion would be a 
        # ~80% chance to succeed willpower
        # willpower_5 = 875, 1, 1000 range so 87.49%
        # so in total 66.9% chance
            DoLRegionNames.industrial_alleyways.value,
        ], [
            DoLOptionFilters.type_feat.value,
            DoLOptionFilters.req_feat_copper.value,
        ], [
            DoLRules.willpower_5,
        ])

    feat_seedy = _LocDetail(1123, [
            DoLRegionNames.in_global.value, # global cause seed is loc req
        ], [
            DoLOptionFilters.type_feat.value,
            DoLOptionFilters.req_feat_copper.value,
        ], [
            DoLRules.seeds_50p
        ])

    feat_breedy = _LocDetail(1124, [
            DoLRegionNames.in_global.value, # global cause seed is loc req
        ], [
            DoLOptionFilters.type_feat.value,
            DoLOptionFilters.req_feat_silver.value,
            DoLOptionFilters.req_loveinterest.value, # gwylan required for 100% seeds
            DoLOptionFilters.req_badend.value, # asylum/edens required for 100% seeds
        ], [
            DoLRules.seeds_100p
        ])

    feat_athunderousresponse = _LocDetail(1125, [
            DoLRegionNames.commercial_alleyways.value,
        ], [
            DoLOptionFilters.type_feat.value,
            DoLOptionFilters.req_feat_silver.value,
        ], [
            DoLRules.exhibitionism_5,
        ])

    feat_alewdadventure = _LocDetail(1126, [
            DoLRegionNames.commercial_alleyways.value,
        ], [
            DoLOptionFilters.type_feat.value,
            DoLOptionFilters.req_feat_copper.value,
        ], [
            DoLRules.exhibitionism_5,
        ])

    feat_sourdealing = _LocDetail(1127, [
            DoLRegionNames.oxford_street.value,
        ], [
            DoLOptionFilters.type_feat.value,
            DoLOptionFilters.req_feat_copper.value,
            DoLOptionFilters.req_seasonal.value,
            # just need to steal from dealer, lower skul the better
            # but eventually rises to 1200 making it always possible to lose
        ], [])

    feat_painrider = _LocDetail(1128, # INFO
        # INFO feat_painrider : by bluecat
        #
        # extreme 1:
        #   then:   <<masopain 5>>, <<masopain 20>>
        # extreme 2:
        #   check:  willpower / 10 gte ($pain - 100) + random(1, 100)
        #   then:   <<masopain 20>>
        # extreme 3:
        #   check:  willpower / 10 gte ($pain - 100) + random(1, 100)
        #   then:   <<earnfeat>>
        #
        # masopain: 
        #   pain += amount * (1 - V.masochism / 1200) * 4 
        #   arousal(amount * (0 + V.masochism / 18) * 4)
        # NOTE: this is NOT effected by science, since it adds pain directly
        # reminder: pain is a value from 0 to 100
        #
        # 100 maso:  5 = 18.3, 20 = 73.3 (total: 164.9), need 650 - 1650 willpower
        # 500 maso:  5 = 11.6, 20 = 46.6 (total: 104.8), need  48 - 1048 willpower
        # 750 maso:  5 =  7.5, 20 = 30   (total:  67.5), need   0 -  675 willpower
        # 1000 maso: 5 =  3.3, 20 = 13.3 (total: 29.93), need   0 -  299 willpower
        # reminder: maso is a value from 0 to 1000 (0-99 maso does not apply)
        #
        # this event seems weirdly super random chance if you're not near max maso and willpower
        # since maso isn't randomized, and 500 maso is 2 50%'s at 500, I'd say will 4 (571)
        # is a good point to allow the rule, even if chance is slightly higher at start
        [
            DoLRegionNames.museum.value,
        ], [
            DoLOptionFilters.type_feat.value,
            DoLOptionFilters.req_feat_silver.value,
        ], [
            DoLRules.antiques_10,
            DoLRules.willpower_4
        ])

    feat_submerged = _LocDetail(1129, [
            DoLRegionNames.museum.value,
        ], [
            DoLOptionFilters.type_feat.value,
            DoLOptionFilters.req_feat_silver.value,
        ], [
            DoLRules.antiques_20,
            DoLRules.swimming_9,
        ])

    feat_wrongsize = _LocDetail(1130, [
            DoLRegionNames.school.value,
        ], [
            DoLOptionFilters.type_feat.value,
            DoLOptionFilters.req_feat_copper.value,
            DoLOptionFilters.req_multipleruns.value,
        ], [
            DoLRules.skulduggery_4,
        ])

    feat_idlehands = _LocDetail(1131, # INFO
        # INFO feat_submerged : by bluecat
        #
        # extreme 1: nothing (swim check for 3 here)
        # extreme 2: nothing
        # extreme 3: 
        #   check:  <<swimmingdifficulty 1 400>>, 
        #           <<wraithevent>> (random chance to fail based on wraith lust and wraith hauting)
        # extreme 4: 
        #   check:  <<swimmingdifficulty 300 1000>>
        #           <<wraithevent>> (random chance to fail based on wraith lust and wraith hauting)
        # extreme 5:
        #   check:  <<swimmingdifficulty 600 1400>> ( 50% chance even at S Rank)
        #   then:   <<earnfeat>>, <<museumantiquestatus>>
        # NOTE: wiki lists requiring high willpower, but didn't find any
        # probably meant swimming when edited
        #
        # with above info (excluding wraith):
        # stat       chances                total chance
        # 600 swim:  (100%, 42.86%, 0%)     0%
        # 700 swim:  (100%, 57.14%, 12.5%)  7.14%   (~1/14)
        # 800 swim:  (100%, 71.43%, 25%)    17.86%  (~1/6)
        # 900 swim:  (100%, 85.71%, 37.5%)  32.14%  (~1/3)
        # 1000 swim: (100%, 100%,   50%)    50%     (1/2)
        # 1/3 isn't unbelievable so will go with that
        [
            DoLRegionNames.spa.value,
        ], [
            DoLOptionFilters.type_feat.value,
            DoLOptionFilters.req_feat_copper.value,
        ], [
            DoLRules.skulduggery_1, # (1/3 at f+)
            # spa req: 6/7 max beauty or handskill >= 400
            # since beauty isn't randomized, we can technically
            # not have a req for hands, but include anyway
            DoLRules.hands_2
        ])

    feat_stolentechnology = _LocDetail(1132, [
            DoLRegionNames.brothel.value,
        ], [
            DoLOptionFilters.type_feat.value,
            DoLOptionFilters.req_feat_silver.value,
        ], [
            DoLRules.access_landfill,
            # brothel show req just needs finding
            # the canister in the trash, access landfill enough
        ])

    feat_spelunking = _LocDetail(1133, [
            DoLRegionNames.beach.value, # smug cave beach entrance
        ], [
            DoLOptionFilters.type_feat.value,
            DoLOptionFilters.req_feat_copper.value,
        ], [])

    feat_xmarksthespot = _LocDetail(1134, [
            DoLRegionNames.old_sewers.value,
        ], [
            DoLOptionFilters.type_feat.value,
            DoLOptionFilters.req_feat_silver.value,
        ], [
            DoLRules.skulduggery_4, # 40%, 5 = 60%
        ])

    feat_buriedtreasure = _LocDetail(1135, [
            DoLRegionNames.moor.value,
        ], [
            DoLOptionFilters.type_feat.value,
            DoLOptionFilters.req_feat_gold.value,
        ], [
            DoLRules.has_leathermap
        ]) 

    feat_flurry = _LocDetail(1136, # INFO
        # INFO feat_flurry : by bluecat
        #
        # Flurry thread:
        # 'Wait'|Robin Choclate Wait -> end event
        # 'Challenge the Leader'|Robin Chocolate Challenge
        #   | Robin Chocolate Challenge Attack: hand gte rand(1, 800)
        #   | Robin Chocolate Bide:             dance 1 800
        #   | Robin Chocolate Cover:            end event
        # 'Take Them all on'|Robin Chocolate Take
        #   | Robin Chocolate Audacious:    handskill 1 to 2000 or robin dom >= 20 and tra < 40: 1200
        #   | Robin Chocolate Paitent:      dancediff 1 to 1200
        #   | Robin Chocolate Cover:        end event     
        #
        # event is a lot easier if you just challenge
        # dance on challenge is 400 for ~50%
        # and hand is just random so also 400
        [
            DoLRegionNames.park.value,
        ], [
            DoLOptionFilters.type_feat.value,
            DoLOptionFilters.req_feat_copper.value,
            DoLOptionFilters.req_loveinterest.value,
            DoLOptionFilters.req_seasonal.value,
        ], [
            DoLRules.hand_or_dance_400,
        ])

    feat_afestivehome = _LocDetail(1137, [
            # if christmas, dec 25th, clothes present
            DoLRegionNames.orphanage.value, 
        ], [
            DoLOptionFilters.type_feat.value,
            DoLOptionFilters.req_feat_copper.value,
            DoLOptionFilters.req_seasonal.value,
        ], [
            DoLRules.access_shoppingcentre,
        ])

    feat_employeebenefits = _LocDetail(1138, [
            DoLRegionNames.docks.value,
        ], [
            DoLOptionFilters.type_feat.value,
            DoLOptionFilters.req_feat_gold.value,
        ], [
            # need 400 to examine a container, this
            # goes into another check, but its easier
            DoLRules.skulduggery_4
        ])

    feat_dealing = _LocDetail(1139, [
            DoLRegionNames.compound.value,
        ], [
            DoLOptionFilters.type_feat.value,
            DoLOptionFilters.req_feat_copper.value,
        ], [
            DoLRules.access_alexfarm,
        ]) 

    feat_bentcopper = _LocDetail(1140, [
            DoLRegionNames.police_station.value,
        ], [
            DoLOptionFilters.type_feat.value,
            DoLOptionFilters.req_feat_copper.value,
        ], [
            DoLRules.skulduggery_4,
        ])

    feat_socialcontract = _LocDetail(1141, [
            DoLRegionNames.police_station.value,
        ], [
            DoLOptionFilters.type_feat.value,
            DoLOptionFilters.req_feat_silver.value,
        ], [])

    feat_slipthroughthebackdoor = _LocDetail(1142, [
            DoLRegionNames.pub.value,
        ], [
            DoLOptionFilters.type_feat.value,
            DoLOptionFilters.req_feat_silver.value,
        ], [
            DoLRules.access_orphanage,
        ])

    # dance job offering has a min req of 800 dance (the 3 feats below)
    feat_lifeoftheparty = _LocDetail(1143, [
            DoLRegionNames.dance_studio.value,
        ], [
            DoLOptionFilters.type_feat.value,
            DoLOptionFilters.req_feat_copper.value,
        ], [
            DoLRules.dancing_8,
        ])

    feat_belleoftheball = _LocDetail(1144, [
            DoLRegionNames.dance_studio.value,
        ], [
            DoLOptionFilters.type_feat.value,
            DoLOptionFilters.req_feat_silver.value,
        ], [
            DoLRules.exhibitionism_5,
            DoLRules.dancing_8,
        ])

    feat_breakingthestone = _LocDetail(1145, [
            DoLRegionNames.dance_studio.value,
        ], [
            DoLOptionFilters.type_feat.value,
            DoLOptionFilters.req_feat_gold.value,
        ], [
            DoLRules.skulduggery_10,
            DoLRules.dancing_8,
        ])

    feat_poundalpha = _LocDetail(1146, [
            DoLRegionNames.dog_pound_ending.value,
        ], [
            DoLOptionFilters.type_feat.value,
            DoLOptionFilters.req_feat_copper.value,
            DoLOptionFilters.req_badend.value,
        ], [])

    feat_poundrunt = _LocDetail(1147, [
            DoLRegionNames.dog_pound_ending.value,
        ], [
            DoLOptionFilters.type_feat.value,
            DoLOptionFilters.req_feat_copper.value,
            DoLOptionFilters.req_badend.value,
        ], [])

    feat_poundedpound = _LocDetail(1148, [ # INFO
        # INFO feat_poundedpound : by bluecat
        #
        # to win you need compete score gte 5
        # Pound Show Compete
        # | Intimidate: poundstatus gte rand(40, 100), +1 score
        # | Skill:      dance(1, 1000), +1 score
        # Compete 2
        # | Intimidate: poundstatus gte rand(40, 100), +1 score
        # | Skill:      if $physiquesize gte 15000, physique(12000, 15000)
        # |             12000,  diff(6000, 12000)
        # |             9000,   diff(2000, 8000)
        # |             else,   diff(   1, 2000)
        # |             +1 score if pass
        # Compete 3
        # | Intimidate: poundstatus gte rand(40, 100), +1 score
        # | Skill:      athletics(1, 1000), +1 score
        # Compete 4
        # | Intimidate: poundstatus gte rand(40, 100), +1 score
        # | Skill:      swim(1, 1000), +1 score
        # Compete 5:
        # | Intimidate: poundstatus gte rand(40, 100), +1 score
        # | Skill:      athletics(1, 1000), +1 score
        # END
        #
        # Should be possible to get by using status alone, and
        # the skill just makes it easier
        #
        # OR
        # you can when escaping do a diff 1000 skul check and give
        # a document to bailey later
            DoLRegionNames.dog_pound_ending.value,
        ], [
            DoLOptionFilters.type_feat.value,
            DoLOptionFilters.req_feat_silver.value,
            DoLOptionFilters.req_badend.value,
        ], [
            # technically no min req, but can add some later
        ])

    feat_poundliberator = _LocDetail(1149, [
            DoLRegionNames.dog_pound.value,
        ], [
            DoLOptionFilters.type_feat.value,
            DoLOptionFilters.req_feat_silver.value,
            DoLOptionFilters.req_badend.value,
        ], [
            DoLRules.tending_4, # tending(1, 1000)
            DoLRules.skulduggery_2,
        ])

    feat_thevalueofpain = _LocDetail(1150, [
            DoLRegionNames.domus_houses.value,
        ], [
            DoLOptionFilters.type_feat.value,
            DoLOptionFilters.req_feat_copper.value,
            DoLOptionFilters.req_transformation.value,
            DoLOptionFilters.toggle_transformation_divine.value,
        ], [
            DoLRules.tfrule_demon_full_appear,
        ])

    feat_bewitchingechoes = _LocDetail(1151, [ # INFO
        # INFO feat_bewitchingechos : by bluecat
        #
        # demon tf is req to start the job
        # need to 'Aggressive seduction' with audiance 3 times
        # 'Flirt' makes it so aggressive seduction requires 6k seduction
        # 'Gentle' makes it so aggressive seduction requires 
        # 4k seduction if flirted already, otherwise 8k sedution
        # otherwise seduction req is 10k
        # if brothel security gte 6, event ends
        #
        # flirt: +1 security, reduced sed
        # gentle: +1 security, reduced sed
        # aggressive flirt: +2 security, +1 crazed
        #
        # since security needs to be above 6, 
        # flirt, agr, agr, agr should work, 
        # since it doesn't go to gte 6 until it goes to 7
        # we can't do flirt, gentle since that would take up 2
            DoLRegionNames.brothel.value,
        ], [
            DoLOptionFilters.type_feat.value,
            DoLOptionFilters.req_feat_copper.value,
            DoLOptionFilters.req_transformation.value,
            DoLOptionFilters.toggle_transformation_divine.value,
        ], [
            DoLRules.tfrule_demon_full_appear,
            DoLRules.seduction_4,
        ])


    # Tentacle Forest / Hookah Parlour Feats Info
        # for fun, I'm putting the location of the tentacle
        # forest checks at their discovery location, while mayors
        # office is technically the correct location

        # all of these use their respective var 
        # at 4 to determine if their project is done and feat earned
        # 3 if it the completion hasn't been seen yet (need to see it for dialog and feat)
        # 2 if needs funding and talking to mayor
        # 1 if you haven't looked at in the real world yet
        # bridge = $town_projects.bridge
        # road = $town_projects.road
        # archeological office = $town_projects.diving
        # residential thicket = $town_projects.thicket
        # school green = $town_projects.green 

    # Tentacle Forest Money Check, decend 1
    feat_bridgingthepast = _LocDetail(1152, [ # .bridge
            DoLRegionNames.barb_street.value,
        ], [
            DoLOptionFilters.type_feat.value,
            DoLOptionFilters.req_feat_copper.value,
            DoLOptionFilters.toggle_tentacles.value,
        ], [
            DoLRules.access_tentacleforest,
            DoLRules.access_mayorsoffice,
        ]) 

    # Tentacle Forest Money Check, decend 2
    feat_safetrail = _LocDetail(1153, [ # .road
            DoLRegionNames.forest.value,
        ], [
            DoLOptionFilters.type_feat.value,
            DoLOptionFilters.req_feat_copper.value,
            DoLOptionFilters.toggle_tentacles.value,
        ], [
            DoLRules.access_tentacleforest,
            DoLRules.access_mayorsoffice,
            # requires all previous decend items
            DoLRules.has_flatsbridge,
        ]) 

    # Tentacle Forest Money Check, decend 3
    feat_fieldwork = _LocDetail(1154, [ # .diving
            DoLRegionNames.forest_lake.value,
        ], [
            DoLOptionFilters.type_feat.value,
            DoLOptionFilters.req_feat_copper.value,
            DoLOptionFilters.toggle_tentacles.value,
        ], [
            DoLRules.access_tentacleforest,
            DoLRules.access_mayorsoffice,
            # requires all previous decend items
            DoLRules.has_flatsbridge,
            DoLRules.has_forestroad,
        ])

    # Tentacle Forest Money Check, ascend 1
    feat_concretewoodland = _LocDetail(1155, [ # .thicket
            DoLRegionNames.residential_alleyways.value,
        ], [
            DoLOptionFilters.type_feat.value,
            DoLOptionFilters.req_feat_copper.value,
            DoLOptionFilters.toggle_tentacles.value,
        ], [
            DoLRules.access_tentacleforest,
            DoLRules.access_mayorsoffice,
        ]) 

    # Tentacle Forest Money Check, ascend 2
    feat_schoolgreen = _LocDetail(1156, [ # .green
            DoLRegionNames.school.value,
        ], [
            DoLOptionFilters.type_feat.value,
            DoLOptionFilters.req_feat_copper.value,
            DoLOptionFilters.toggle_tentacles.value,
        ], [
            DoLRules.access_tentacleforest,
            DoLRules.access_mayorsoffice,
            # requires all previous ascend items
            DoLRules.has_residentialthicket,
        ])

    # free check after tentacle forest stuff, "ascend 3"
    feat_hookahmaster = _LocDetail(1157, [
            DoLRegionNames.tentacle_forest.value, # event is in tent forest
        ], [
            DoLOptionFilters.type_feat.value,
            DoLOptionFilters.req_feat_silver.value,
            DoLOptionFilters.toggle_tentacles.value,
        ], [
            # requires all previous decend items
            DoLRules.has_flatsbridge,
            DoLRules.has_forestroad,
            DoLRules.has_fieldoffice,
            # requires all previous ascend items
            DoLRules.has_residentialthicket,
            DoLRules.has_schoolgreen,
        ])

    # free check after tentacle forest stuff
    feat_sinsofthepast = _LocDetail(1158, [
            DoLRegionNames.mayors_office.value,
        ], [
            DoLOptionFilters.type_feat.value,
            DoLOptionFilters.req_feat_gold.value,
            DoLOptionFilters.toggle_tentacles.value,
        ], [
            # Mimic Rules from Hookah Master
            DoLRules.access_tentacleforest,
            # requires all previous decend items
            DoLRules.has_flatsbridge,
            DoLRules.has_forestroad,
            DoLRules.has_fieldoffice,
            # requires all previous ascend items
            DoLRules.has_residentialthicket,
            DoLRules.has_schoolgreen,
        ]) 

    # end tentacle forest stuff


    feat_panicroom = _LocDetail(1159, [ # INFO
        # INFO feat_panicroom : by bluecat
        #
        # 3 ways to get feat
        # 1. Flats Sneak Physique, break through the door, physique(1, 35000)
        # 2. make enemy arousal max
        # 3. kill enemy
        #
        # you start out with 5 time slots to try to break out
        # to get feat you just have to spend 5 on trying to hit the physique check
        # if you fail, you have to win a fight with 2 cops in the 2 above ways
            DoLRegionNames.flats.value,
        ], [
            DoLOptionFilters.type_feat.value,
            DoLOptionFilters.req_feat_copper.value,
        ], [
            DoLRules.skulduggery_2,
            # min physique / able to win encounter
        ])

    feat_defythenight = _LocDetail(1160, [
            DoLRegionNames.temple.value,
        ], [
            DoLOptionFilters.type_feat.value,
            DoLOptionFilters.req_feat_silver.value,
        ], [
            DoLRules.willpower_5,
            DoLRules.science_4,
            # ^ wiki recommendation
        ])

    feat_witheringtruth = _LocDetail(1161, [
        # If you offer sex during a confessional, you have about
        # a 50% chance to get the bowl after the sex, then you
        # just have to keep acceping the purge with the bowl
            DoLRegionNames.temple.value,
        ], [
            DoLOptionFilters.type_feat.value,
            DoLOptionFilters.req_feat_gold.value,
        ], [
            # willpower requirement is
            # just for ending the encounter
        ])

    feat_backroomdeals = _LocDetail(1162, [
            DoLRegionNames.domus_street.value,
        ], [
            DoLOptionFilters.type_feat.value,
            DoLOptionFilters.req_feat_copper.value,
            DoLOptionFilters.req_loveinterest.value,
        ], [])


    # INFO Photography Event : by bluecat
    #
    # feat goals: 100 and 250 flyers
    #
    # Basics:
    # - you start out on a 120 time slot timer
    # - if your attention in area (photo_attention) is high, you have a chance of lewd events
    # - if stress caps out you lose 60 time and suit loss process
    # - when doing any action you pick from the event pool
    # - arousal capping just gives 3 attention
    # - end if timer reaches 0
    # 
    # Heat:
    #   heat is a value 0, 100 that increases stress each event
    #   each time its increased, its multiplied by the temperature too
    #   events have a chance to increase it, and increases by 1 from any action
    #   if heat is gte 60: stress 12, 30: stress 6, else nothing
    #   you can rest to reduce heat by gte 60: -12, 30: -8, else -4
    #
    # Reminder: stress
    #   stress is a value with a 10k cap, however by default
    #   all stress is *40'd, meaning its actually like 250 cap
    #   note: alcohol may lower this
    #
    # 
    # Actions:
    # Hand Out Flyers:  -1 time, +3 flyers
    # Walk Seaward:     -1 time, +1 Location (max 7)
    # Walk Forestward:  -1 time, -1 Location (min 1)
    # Rest in Shade:    -5 time, -heat
    #
    # Possible Locations:
    # 1: Near Forest
    # 2: Park
    # 3: Shopping Centre
    # 4: Games Shop      (start)
    # 5: Bus Stop
    # 6: Square
    # 7: Near the Coast
    # 
    #  --- Event Pool photo_high:
    # photo_high_1:     +3 flyers
    # photo_high_2:     stress 6, attention 1
    # photo_high_3:     attention 1
    # photo_high_4:     dance gte rand(1, 1000), else -1 time, +1 heat
    # photo_high_5:     nothing
    # photo_high_6:     nothing
    # photo_high_7:     nothing
    # photo_high_8:     1/3: if not cool, trauma and stress, else nothing (optional)
    #                   | 2/3: +2 flyers
    # photo_high_9:     nothing
    # photo_high_10:    attention 1, can growl back for +4 flyers
    #
    #  --- Event Pool Weather:
    # raining:          nothing
    # snowing:          stress 6, attention 1
    #
    #  --- Event Pool Attention:
    # NOTE: defined as attention req, weight (these events have slight weightings)
    #
    # danger_1(2, 1.15):    best outcome: nothing
    #
    # danger_2(4, 1.3):     attention 1, arousal 600
    #                       | (1 attention, -6 stress) OR (trauma 6, stress 6)
    #
    # danger_3(6, 1.45):    pain 4, stress 6
    #
    # danger_4(8, 1.6):     trauma 6, stress 6
    #                       | if physique(1, 16000), stress -3, else attention 2, trauma 6, stress 6
    #                       | NOTE: danger 5 scales off attention/10 (not 1 + at/10)
    #
    # danger_5(12, dynam):  costume is stolen, must get back, takes 5 time
    #                       | if naked/underwear, clothes stolen process
    #
    #
    #  --- Event Pool Area:
    # NOTE: requires being in the area
    #
    # forest(,1.2):         nothing
    #
    # park(,1.2):           if willpower(1, 1000) nothing 
    #                       | if clothed, attention 1
    #                       | if naked, attention 2, trama 6, stress 6, then
    #                       |   if attention gte 6, event, best case nothing
    #
    # shopcentre(,1.2):     if dance(1, 600) +12 (!!) flyers (can refuse)
    #                       | else, attention 1 
    #
    # gamesshop(,1.2):      attention 1, +3 flyers (can refuse)
    # busstop(,1.2):        +12 (!!) flyers
    # square(,1.2):         attention 1
    # nearcoast(,1.2):      stress 6, attention 1
    #
    #
    #  --- Event Pool Modelfame:
    # NOTE: the weights of these events are based on 1 + attention/10, max of 2 weight
    # model1(200, dynam):   nothing
    # model2(400, dynam):   +6 flyers
    # model3(600, dynam):   optional event, bestcase nothing
    # model4(800, dynam):   nothing
    # model5(1000, dynam):  reduces heat, -1/-5 time, no difference in options
    #
    #
    # Costume Stolen Process:
    # If Clothed, -5 time, back to game store
    # If naked/underwear:
    #   skul 800:   -1 time, per distance from start
    #   skul 300:   -5 time, per distance from start
    # or
    #   Naked Exhib 5 / Underwear Exhib 3:
    #   run with chance for abduction, no time taken
    #
    # If you're abducted, you have a time wasting event, if you go along no time is wasted
    #
    # 
    # Rules:
    # testing, I was able to hand out 100 flyers by just avoiding attention 
    # and moving when attention was high, with no resting
    #
    # If you want to get 250 however, you probably need to rest for times
    # NOTE: wearing clothes doesn't add extra heat, just increases the temp
    # NOTE: it is hard to lower stress, heat just increases it
    #
    # I will probably make the ruling for 250 req exh 3 to make it easier.
    # Doing it just requires a bit of skill and resting, there's
    # not enough extra stat checks for flyers either

    feat_stompingdownthestreet = _LocDetail(1163, [
            DoLRegionNames.photography_studio.value,
        ], [
            DoLOptionFilters.type_feat.value,
            DoLOptionFilters.req_feat_copper.value,
        ], [
            # no min
        ])

    feat_hearmeroar = _LocDetail(1164, [
            DoLRegionNames.photography_studio.value,
        ], [
            DoLOptionFilters.type_feat.value,
            DoLOptionFilters.req_feat_silver.value,
            # maybe make difficult
        ], [
            DoLRules.exhibitionism_3,
        ])

    feat_maxthoseshots = _LocDetail(1165, [
            DoLRegionNames.old_sewers.value,
            DoLRegionNames.tentacle_plains.value,
            DoLRegionNames.compound.value,
            DoLRegionNames.wolf_cave.value,
            DoLRegionNames.remy_farm.value,
            DoLRegionNames.prison.value,
            DoLRegionNames.bird_tower.value,
        ], [
            DoLOptionFilters.type_feat.value,
            DoLOptionFilters.req_feat_silver.value,
            DoLOptionFilters.toggle_tentacles.value, # tent plains
            DoLOptionFilters.toggle_bestiality.value, # wolfcave
            DoLOptionFilters.req_badend.value, # wolfcave, prison, tower
        ], [
            # 1 from tutorial
            DoLRules.access_oldsewers, # 2
            DoLRules.access_tentacleplains, # 3
            DoLRules.access_compound, # 4
            DoLRules.access_wolfcave, # 5
            DoLRules.access_remyfarm, # 6
            DoLRules.access_prison, # 7
            DoLRules.access_birdtower, # 8
        ])

    feat_openedpandorasbox = _LocDetail(1166, [
            DoLRegionNames.adult_shop.value,
        ], [
            DoLOptionFilters.type_feat.value,
            DoLOptionFilters.req_feat_copper.value,
            DoLOptionFilters.req_multipleruns.value,
        ], [])

    feat_openedpandorascocks = _LocDetail(1167, [
            DoLRegionNames.adult_shop.value,
        ], [
            DoLOptionFilters.type_feat.value,
            DoLOptionFilters.req_feat_gold.value,
            DoLOptionFilters.req_multipleruns.value,
        ], [])

    feat_brothelprovider = _LocDetail(1168, [
            DoLRegionNames.school.value,
        ], [
            DoLOptionFilters.type_feat.value,
            DoLOptionFilters.req_feat_silver.value,
        ], [
            DoLRules.access_brothel,
            DoLRules.has_adultshopbuilt,
            DoLRules.access_adultshop,
            DoLRules.access_shoppingcentre,
            DoLRules.access_pharmacy,
        ])

    feat_playerofthematch = _LocDetail(1169, [
        # You need to sneak (600 skul) before the job end, then
        # 800 skul check to get the ball
            DoLRegionNames.pub.value,
        ], [
            DoLOptionFilters.type_feat.value,
            DoLOptionFilters.req_feat_silver.value,
        ], [
            DoLRules.skulduggery_5 # (~9/10, ~1/2)
        ])


    # Discovery Feats - outside town

    feat_lockedingold = _LocDetail(1170, [
            DoLRegionNames.forest.value,
        ], [
            DoLOptionFilters.type_feat.value,
            DoLOptionFilters.req_feat_silver.value,
        ], [])

    feat_theendlessdeep = _LocDetail(1171, [
            DoLRegionNames.ocean.value,
        ], [
            DoLOptionFilters.type_feat.value,
            DoLOptionFilters.req_feat_silver.value,
        ], [
            # min swimming is 3, and not to max out with it if you play nice
            DoLRules.swimming_3,
        ])

    feat_wetandruined = _LocDetail(1172, [
            DoLRegionNames.moor.value,
        ], [
            DoLOptionFilters.type_feat.value,
            DoLOptionFilters.req_feat_silver.value,
        ], [])

    feat_terrorsequal = _LocDetail(1173, [
            DoLRegionNames.bird_tower.value,
        ], [
            DoLOptionFilters.type_feat.value,
            DoLOptionFilters.req_feat_gold.value,
            DoLOptionFilters.req_loveinterest.value,
            DoLOptionFilters.req_transformation.value, # need* flight to get items
            DoLOptionFilters.req_badend.value,
            DoLOptionFilters.toggle_transformation_either.value # flight
        ], [
            DoLRules.tfrule_flight, # need* flight to get items
        ])

    feat_birdsofafeather = _LocDetail(1174, [
            DoLRegionNames.bird_tower.value,
        ], [
            DoLOptionFilters.type_feat.value,
            DoLOptionFilters.req_feat_silver.value,
            DoLOptionFilters.req_loveinterest.value,
            DoLOptionFilters.req_badend.value,
            DoLOptionFilters.req_transformation.value, # Hunt Feat
            DoLOptionFilters.toggle_transformation_either.value, # just need flight
            # I don't think this req preg?
            # it pushs to your babies, but no explicit
            # checks for it anywhere
        ], [
            DoLRules.tfrule_flight,
        ])

    feat_runawaycattle = _LocDetail(1175, [
            DoLRegionNames.remy_farm.value,
        ], [
            DoLOptionFilters.type_feat.value,
            DoLOptionFilters.req_feat_copper.value,
            DoLOptionFilters.req_badend.value,
        ], [])

    feat_equinerescue = _LocDetail(1176, [
            DoLRegionNames.remy_farm.value,
        ], [
            DoLOptionFilters.type_feat.value,
            DoLOptionFilters.req_feat_copper.value,
            DoLOptionFilters.req_badend.value,
            DoLOptionFilters.bestiality_or_monsterpeople.value, 
        ], [])

    feat_rearpassenger = _LocDetail(1177, [
            DoLRegionNames.farmlands_road.value,
        ], [
            DoLOptionFilters.type_feat.value,
            DoLOptionFilters.req_feat_copper.value,
        ], [
            DoLRules.promiscuity_4,
        ]) 

    feat_corneredrogue = _LocDetail(1178, [ # INFO
        # INFO feat_corneredrogue : by bluecat
        #
        # when relaxing in the meadow, if rng >= 91 and you're not exposed,
        # 50/50 to either chase it up a hill or just chase it
        #
        # 1. Meadow Chase:
        #   - Start
        #       | Burrow:     if fox tf you get to pass
        #       | Squeeze:    if physiquesize lte 9000 you get to pass
        #       | Craw:       encounter then continue
        #   - Meadow Tunnel (cont.)
        #       | Climb down: althletics check 1, 1000
        #       | Glide down: wings check
        #       | Dive:       swim check 1, 1000
        # If you fail a check you're sent back to meadow
        # otherwise then Meadow Cave -> Cave 2 -> Feat
        #
        # 2. Meadow Chase Hill:
        #   athletics check 1, 1000
        #   skul gte rand 1, 1050
        # if it is a monster, you do get the feat
        # otherwise you cannot geat the feat
        # NOTE: why??? ^
            DoLRegionNames.meadow.value,
        ], [
            DoLOptionFilters.type_feat.value,
            DoLOptionFilters.req_feat_copper.value,
            # I thought about putting the rng option here
            # however this is just spamming meadow relax button
        ], [
            DoLRules.corneredrogue,
        ])

    feat_farmprotector = _LocDetail(1179, [
            DoLRegionNames.alex_farm.value,
        ], [
            DoLOptionFilters.type_feat.value,
            DoLOptionFilters.req_feat_silver.value,
        ], [])

    feat_aknottoremember = _LocDetail(1180, [
            DoLRegionNames.alex_farm.value,
        ], [
            DoLOptionFilters.type_feat.value,
            DoLOptionFilters.req_feat_copper.value,
            DoLOptionFilters.toggle_bestiality.value,
        ], [])

    feat_abnormalmollusc = _LocDetail(1181, [ # INFO
        # INFO feat_abnormalmollusc : by bluecat
        # the beach slug event has you escaping a slug, doing a 
        # vareity of checks until you escape the cave. If you fail
        # enough times pursuit increases to 3 then vore scene with the slug 
        # or if disabled passout
        # if you escape the slug pursuit is reset to 1 then continue
        #
        # Events:
        # Slime Pool:   1. jump: athletics(400, 1100)
        #               |   if fail, swarm event if enabled, +1 pursuit/time
        #               |   otherwise just +1 pursuit
        #               |   if pursuit gte 3 on finish, caught
        #               2. walk around: +1 pursuit
        #
        # Slug Spit:    1. dodge: dance(400, 1100)
        #               |   if win, pursuit -1
        #               |   if fail, encounter, +1 pursuit/time
        #               |   if pursuit gte 3 on finish, caught
        #               2. brace: pursuit +1
        #
        # Slug Slam:    always: physique(1, 18000)
        #               |   if fail, pursuit +1
        #
        # Slug Run:     1. sprint: athletics(600, 1200)
        #               |   if win, pursuit -1
        #               |   if fail, pursuit +1
        #               2. careful: nothing
        #
        # cave exit is a randomly chosen cave from a choice of
        # lichen, mushroom, dark, watery
        # getting to the exit before fainting counts as a win
        #
        # since going for at least ~50%, you shouldn't need any
        # of these stats to reach the exit, since you can go to each
        # tunnel per pursuit
            DoLRegionNames.old_sewers.value, # smug cave tunnel
        ], [
            DoLOptionFilters.type_feat.value,
            DoLOptionFilters.req_feat_silver.value,
            DoLOptionFilters.bestiality_or_softvore_or_swarms.value,
            DoLOptionFilters.toggle_slugs.value,
        ], [])

    feat_leverage = _LocDetail(1182, [ # TODO: ITEM
            DoLRegionNames.old_sewers.value, # smug cave
        ], [
            DoLOptionFilters.type_feat.value,
            DoLOptionFilters.req_feat_gold.value,
        ], [
            # defiant trait displaydefiantoption(500)
            DoLRules.dancing_6, # dance(200, 1000)
            DoLRules.english_3, # english(200, 1000)
        ])

    feat_undertheice = _LocDetail(1183, [
            DoLRegionNames.forest_lake.value,
        ], [
            DoLOptionFilters.type_feat.value,
            DoLOptionFilters.req_feat_copper.value,
            DoLOptionFilters.req_seasonal.value,
        ], [])

    feat_inredlight = _LocDetail(1184, [
            DoLRegionNames.forest.value,
        ], [
            DoLOptionFilters.type_feat.value,
            DoLOptionFilters.req_feat_silver.value,
        ], [])

    feat_ohbother = _LocDetail(1185, [
            DoLRegionNames.forest.value,
        ], [
            DoLOptionFilters.type_feat.value,
            DoLOptionFilters.req_feat_copper.value,
            # req bees and beast enabled
            DoLOptionFilters.toggle_bestiality.value,
            DoLOptionFilters.toggle_bees.value,
        ], [
            DoLRules.tending_8, # tending gte 800
        ])

    feat_notlikethemovies = _LocDetail(1186, [
        # need to get caught in quicksand 5 times to earn
            DoLRegionNames.moor.value,
        ], [
            DoLOptionFilters.type_feat.value,
            DoLOptionFilters.req_feat_silver.value,
        ], [
            # higher than 200 because it needs to happen 5 times
            DoLRules.willpower_3 # willpower(1, 400)
        ])

    feat_slippery = _LocDetail(1187, [ # INFO
        # INFO feat_slippery : by bluecat
        #
        # need to get abducted in moor, then escape:
        # Sneak:      -             skul(900)
        # Lock:       -             skul gte 700
        # Attack:     -             break bindings, then don't faint in fight
        # Seduce:     -             seduction(8000)
        # Mire Run:   moor gte 51,  athletics(900, 1900)
        # Rock Run:   moor gte 21,  athletics(800, 1500)
        # Plain Run:  not ^,        athletics(500, 1500)
        # NOTE: you can run at any point, do not need to do bindings
            DoLRegionNames.moor.value,
        ], [
            DoLOptionFilters.type_feat.value,
            DoLOptionFilters.req_feat_copper.value,
        ], [
            DoLRules.slippery,
        ])

    feat_highreflection = _LocDetail(1188, [
            DoLRegionNames.bird_tower.value,
        ], [
            DoLOptionFilters.type_feat.value,
            DoLOptionFilters.req_feat_copper.value,
            DoLOptionFilters.req_badend.value,
        ], [])

    feat_schism = _LocDetail(1189, [ # TODO: CODE
            # potentially allow you to force this? (ignore trauma req)
            DoLRegionNames.forest_lake.value,
        ], [ 
            DoLOptionFilters.type_feat.value,
            DoLOptionFilters.req_feat_gold.value,
        ], [])

    feat_catchthewind = _LocDetail(1190, [
            DoLRegionNames.bird_tower.value,
        ], [
            DoLOptionFilters.type_feat.value,
            DoLOptionFilters.req_feat_silver.value,
            DoLOptionFilters.req_loveinterest.value,
            DoLOptionFilters.req_transformation.value,
            DoLOptionFilters.req_badend.value,
            DoLOptionFilters.toggle_transformation_animal.value, # need harpy tf to learn flight
        ], [
            # this is learning to fly, so doesn't require flight
            DoLRules.tfrule_harpy_full_appear
        ])

    feat_tradingdignity = _LocDetail(1191, [
            DoLRegionNames.remy_farm.value, # replace w remy estate?
        ], [
            DoLOptionFilters.type_feat.value,
            DoLOptionFilters.req_feat_copper.value,
        ], [])

    feat_playingwithfire = _LocDetail(1192, [ # INFO
        # INFO feat_playingwithfire : by bluecat
        #
        # requires reaching cards.lust 10 after losing in cards
        # ways to increase lust:
        #   desire.twirl:        +1
        #   desire.bend:         +1
        #   desire.chest_grope:  +1
        #   desire.bottom_grope: +1
        #   desire.pussy_grope:  +1
        #   desire.penis_grope:  +1
        #   desire.kiss:         +1
        #   |   when kissing if you kiss back and
        #   |   oral gte rand(400, 1000), instead add +3
        #
        # doing stuff flaughtingly doesn't matter, only
        # kiss back does anything useful
        #
        # Wren chooses stripping you fully first,
        # then, have you twirl then bend
        # afterwards, put you and them on a chair together
        # then choosing to kiss or grope you randomly
        #
        # other than twirl and bend which gives nothing, 
        # no matter what is picked you either have to pass willpower(1, 1000) 
        # or take 1500 arousal (reminder: base max 10k)
        # NOTE: maxxing out on arousal at the same time as lust 10
        # will still result in your success
        #
        # starting with 0 arousal means you can fail 6 times and have 1k remaining
        # meaning you have to either:
        # pass 3 times and fail on last
        # kiss back and fail on last
        #
        # kiss can be rng if its picked, but its only a 1/3
        # so rule is enough willpower to pass 3 times or kiss back once
            DoLRegionNames.remy_estate.value,
        ], [
            DoLOptionFilters.type_feat.value,
            DoLOptionFilters.req_feat_silver.value,
        ], [
            DoLRules.playingwithfire,
        ])

    feat_firestarter = _LocDetail(1193, [
            DoLRegionNames.remy_farm.value,
        ], [
            DoLOptionFilters.type_feat.value,
            DoLOptionFilters.req_feat_copper.value,
        ], [])

    feat_towatchthefields = _LocDetail(1194, [
            DoLRegionNames.pub.value,
        ], [
            DoLOptionFilters.type_feat.value,
            DoLOptionFilters.req_feat_copper.value,
        ], [
            # access to alex farm implied if you don't have upgrades randomized
            DoLRules.has_farmwatchtower,
        ])

    feat_reliableemployer = _LocDetail(1195, [
            DoLRegionNames.alex_farm.value,
        ], [
            DoLOptionFilters.type_feat.value,
            DoLOptionFilters.req_feat_silver.value,
        ], [
            DoLRules.access_pub,
            DoLRules.has_farmwatchtower,
        ])

    feat_intothesunset = _LocDetail(1196, [ # INFO
        # INFO feat_intothesunset : by bluecat
        #
        # feat is a bit weird, but you have to pick 2 of
        # grab, punch, reassure
        # grab:     hand(1, 1000)
        # punch:    physique(1, 15000)
        # reassure: tending(1, 1000)
            DoLRegionNames.alex_farm.value,
        ], [
            DoLOptionFilters.type_feat.value,
            DoLOptionFilters.req_feat_copper.value,
        ], [
            DoLRules.intothesunset,
        ])

    feat_institutionalised = _LocDetail(1197, [
            DoLRegionNames.prison.value,
        ], [
            DoLOptionFilters.type_feat.value,
            DoLOptionFilters.req_feat_copper.value,
            DoLOptionFilters.req_badend.value,
        ], [])

    feat_breaker = _LocDetail(1198, [
            DoLRegionNames.prison.value,
        ], [
            DoLOptionFilters.type_feat.value,
            DoLOptionFilters.req_feat_copper.value,
            DoLOptionFilters.req_badend.value,
        ], [])

    feat_timeandpressure = _LocDetail(1199, [
            DoLRegionNames.prison.value,
        ], [
            DoLOptionFilters.type_feat.value,
            DoLOptionFilters.req_feat_copper.value,
            DoLOptionFilters.req_badend.value,
        ], [])

    feat_morethananumber = _LocDetail(1200, [ # INFO
        # INFO feat_morethananumber : by bluecat
        #
        # requires knowing the names of:
        # - scarred inmate
        # - relaxed guard
        # - anxious guard
        # - veteran guard
        # - methodical guard
        #
        # Scarred Inmate:
        #   requires love gte 60, 
        #   go along with their demands, 
        #   go on walks, sit on lap, etc
        #   then ask them what's wrong in their cell
        #
        # Relaxed Guard:
        #   requires love gte 60,
        #   requires playing game in laundry
        # 
        # Anxious Guard:
        #   requires love gte 60,
        #   working in the spire, or tending
        #   checks can give love
        #
        # Veteran Guard:
        #   love gte 60,
        #   talking to them in the yard, or
        #   servicing the pimp for love
        #
        # Methodical Guard:
        #   love gte 1
        #   when doing normal work, a monster
        #   will appear, and no matter what you 
        #   choose with 1 love you get the name
        #   however...
        #   you need to succeed an athletics check with
        #   the monster or a tending check to get any love
        #   athletics(1, 1000) or tending gte (1, 1000)
            DoLRegionNames.prison.value,
        ], [
            DoLOptionFilters.type_feat.value,
            DoLOptionFilters.req_feat_silver.value,
            DoLOptionFilters.req_badend.value,
        ], [
            # just methodical guard
            DoLRules.tending_or_althletics_500,
        ])

    feat_friendsinthesky = _LocDetail(1201, [
            DoLRegionNames.prison.value,
        ], [
            DoLOptionFilters.type_feat.value,
            DoLOptionFilters.req_feat_silver.value,
            DoLOptionFilters.req_badend.value,
        ], [])

    feat_notmeanttobecaged = _LocDetail(1202, [
            DoLRegionNames.prison.value,
        ], [
            DoLOptionFilters.type_feat.value,
            DoLOptionFilters.req_feat_gold.value,
            DoLOptionFilters.req_badend.value,
        ], [])

    feat_freebooze = _LocDetail(1203, [ # INFO
        # INFO feat_freebooze : by bluecat
        #
        # willpower(1, $drunk) to earn feat
        # requires moor_youths 6 to get ^
        #
        # stuff after ; will always happen
        #
        # events:
        # 0: drink:
        #    |  ; drunk 180, +1 moor_youths
        # 1: virgin question: 
        #    |  not virgin: +2 moor_youths, 
        #    |  virgin: +1 moor_youths, 
        #    |  refuse: +0
        #    |  ; drunk 60, +1 moor_youths
        # 2: waist event, 
        #    |  may be skipped:
        #    |  ; drink 60, +1 moor_youths
        # 3: same^: may be skipped
        # 4: Kiss: 
        #    | allow: +1 moor_youths
        #    | refuse: +0 
        #    | ; drink 60, +1 moor_youths
        # 5: same^: may be skipped
        # 6: final: refuse for feat
        #
        # in total, the minimum amount would be 180 + 60 + 60
        # meaning we need a willpower(1, 300)
        # (maximum is 480, with lightweight type 1.5x, so 720)
        # NOTE: wiki says high requirement for some reason?
            DoLRegionNames.moor.value,
        ], [
            DoLOptionFilters.type_feat.value,
            DoLOptionFilters.req_feat_copper.value,
        ], [
            DoLRules.willpower_2,
        ])

    feat_darkdelvings = _LocDetail(1204, [
            DoLRegionNames.forest.value, # old churchyard
        ], [
            DoLOptionFilters.type_feat.value,
            DoLOptionFilters.req_feat_silver.value,
        ], [
            DoLRules.skulduggery_5,
        ])

    feat_lurkerbeyond = _LocDetail(1205, [
            DoLRegionNames.tentacle_forest.value,
        ], [
            DoLOptionFilters.type_feat.value,
            DoLOptionFilters.req_feat_gold.value,
            DoLOptionFilters.toggle_tentacles.value,
        ], [
            # arousalmax, then skulduggery 1000
            DoLRules.skulduggery_7,
        ])

    feat_downbelow = _LocDetail(1206, [
            DoLRegionNames.flats.value,
        ], [
            DoLOptionFilters.type_feat.value,
            DoLOptionFilters.req_feat_silver.value,
            DoLOptionFilters.req_badend.value,
        ], [])

    feat_lostworld = _LocDetail(1207, [
            DoLRegionNames.island.value,
        ], [
            DoLOptionFilters.type_feat.value,
            DoLOptionFilters.req_feat_copper.value,
            DoLOptionFilters.req_badend.value,
        ], [])

    feat_prehistoriclandscape = _LocDetail(1208, [
            DoLRegionNames.island.value,
        ], [
            DoLOptionFilters.type_feat.value,
            DoLOptionFilters.req_feat_silver.value,
            DoLOptionFilters.req_badend.value,
        ], [])

    feat_faceofaguardian = _LocDetail(1209, [
            DoLRegionNames.island.value,
        ], [
            DoLOptionFilters.type_feat.value,
            DoLOptionFilters.req_feat_silver.value,
            DoLOptionFilters.req_badend.value,
        ], [])

    feat_wildmonarch = _LocDetail(1210, [
            DoLRegionNames.island.value,
        ], [
            DoLOptionFilters.type_feat.value,
            DoLOptionFilters.req_feat_silver.value,
            DoLOptionFilters.req_badend.value,
        ], [
            DoLRules.housekeeping_10,
        ])

    feat_naturalised = _LocDetail(1211, [
            DoLRegionNames.island.value,
        ], [
            DoLOptionFilters.type_feat.value,
            DoLOptionFilters.req_feat_gold.value,
            DoLOptionFilters.req_badend.value,
        ], [])

    feat_gildedspear = _LocDetail(1212, [
            DoLRegionNames.island.value,
        ], [
            DoLOptionFilters.type_feat.value,
            DoLOptionFilters.req_feat_gold.value,
            DoLOptionFilters.req_badend.value,
        ], [])

    feat_lostheirloom = _LocDetail(1213, [ # INFO
        # also gives golden compass

        # INFO feat_lostheirloom : by bluecat
        #
        # random event, zephyr wants you to distract, get attention to 10
        # event starts with an encounter, into a pool of events
        # you have to go through 9 events after and if you have
        # 10 attention, you get the feat and compass
        #
        # Event Start:
        # Pirate Attack Scum 3:
        #   | warn: encounter, no benefits
        #   | distract: encounter, +1 attention
        #   | silent: encounter, -12 pain
        # then,
        # Encounter -> Pirate Attack Scum Main
        # NOTE: this encounter can give attention 
        # like the one in the below pool
        # 
        # eventpool (9 times)
        # -- Events:
        # Pose:
        #   | dignity, +1 attention
        #   | erotic, req exh 5, +2 attention
        #   | refuse, nothing
        # Dance:
        #   | aud arousal 100: +3 attention
        #   | aud arousal 60: +2 attention
        #   | aud arousal 20 +1 attention
        # Cream:
        #   | Allow: +2k arousal, +1 attention
        #   | | if arousalmax +3 attention
        # Encounter:
        #   | You arousalmax: +1 attention
        #   | Enemyhealth 0: +1 attention
        #
        # -- If Attention gte rnd(1, 20), replace with these events:
        # 50/50 for Trio Encounter OR Duo Encounter:
        #   | Same rules as normal, but 3/2 people
        #
        # Conclusion:
        # as long as you don't refuse anything, you should win this event
        # also starting with high arousal may be good
            DoLRegionNames.pirate_ship.value, 
        ], [
            DoLOptionFilters.type_feat.value,
            DoLOptionFilters.req_feat_silver.value,
            DoLOptionFilters.req_badend.value,
        ], [])


    # Special Feats

    feat_50shadesoftan = _LocDetail(1214, [
            DoLRegionNames.spa.value,
        ], [
            DoLOptionFilters.type_feat.value,
            DoLOptionFilters.req_feat_silver.value,
        ], [])


    # INFO Special Traits
    # Check wiki for exact requirements
    # just listing location requirements here
    #
    # O Addict / Hedonist : orgasm number, anywhere
    # Asphyxiophilia : choking req, eventtown
    # Dump / Cumoisseur : covering req, eventtown
    # Plaything / Graceful : event req, eventtown
    # toy / survivor : event req, eventtown
    # bitch / tamer : beast req, # eventtown for dogs, but can be many
    # prey / witch : tent req, para_tentacle
    # tasty / daredevil : vore req, vore_either
    # milk addict/enth : milk req, eventtown

    feat_aspecialtrait = _LocDetail(1215, [
            DoLRegionNames.in_global.value,
        ], [
            DoLOptionFilters.type_feat.value,
            DoLOptionFilters.req_feat_silver.value,
            # feat just requires one trait so no rules req
        ], [
            # many different locations can be accessed for this
            # should be possible about anywhere
        ])

    feat_aspecialtraitcollector = _LocDetail(1216, [
            DoLRegionNames.in_global.value,
        ], [
            DoLOptionFilters.type_feat.value,
            DoLOptionFilters.req_feat_gold.value,
            DoLOptionFilters.toggle_bestiality.value,
            DoLOptionFilters.toggle_tentacles.value,
            DoLOptionFilters.toggle_softvore.value,
            DoLOptionFilters.toggle_lactation.value,
            DoLOptionFilters.req_difficult.value,
        ], [
            DoLRules.access_specialtrait_all
        ])

    feat_produceroflewdfluids = _LocDetail(1217, [
            # orph for long mast session maybe?
            DoLRegionNames.orphanage.value,
        ], [
            DoLOptionFilters.type_feat.value,
            DoLOptionFilters.req_feat_copper.value,
        ], [])

    feat_literallybuckets = _LocDetail(1218, [
            # orph for long mast session maybe?
            DoLRegionNames.orphanage.value,
        ], [
            DoLOptionFilters.type_feat.value,
            DoLOptionFilters.req_feat_silver.value,
        ], [])

    feat_feelingfull = _LocDetail(1219, [
            DoLRegionNames.in_global.value,
        ], [
            DoLOptionFilters.type_feat.value,
            DoLOptionFilters.req_feat_copper.value,
            DoLOptionFilters.lactation_or_multipleruns.value,
        ], [])

    feat_baileystroublemaker = _LocDetail(1220, [ # TODO: lowprio, LOGIC COMPLEX 
            DoLRegionNames.orphanage.value,
        ], [
            DoLOptionFilters.type_feat.value,
            DoLOptionFilters.req_feat_gold.value,
        ], [
            # check min requirements for this
        ])

    feat_leightonsnightmare = _LocDetail(1221, [ # TODO: lowprio, LOGIC COMPLEX 
            DoLRegionNames.school.value,
        ], [
            DoLOptionFilters.type_feat.value,
            DoLOptionFilters.req_feat_gold.value,
        ], [
            # check min requirements for this
        ])

    feat_alexspartner = _LocDetail(1222, [
            DoLRegionNames.alex_farm.value,
        ], [
            DoLOptionFilters.type_feat.value,
            DoLOptionFilters.req_feat_gold.value,
            DoLOptionFilters.req_loveinterest.value,
        ], [])

    feat_harpersbane = _LocDetail(1223, [
            DoLRegionNames.remy_farm.value,
        ], [
            DoLOptionFilters.type_feat.value,
            DoLOptionFilters.req_feat_gold.value,
            DoLOptionFilters.req_badend.value,
        ], [])

    feat_headofthepack = _LocDetail(1224, [
            DoLRegionNames.wolf_cave.value,
        ], [
            DoLOptionFilters.type_feat.value,
            DoLOptionFilters.req_feat_silver.value,
            DoLOptionFilters.req_badend.value,
            DoLOptionFilters.toggle_bestiality.value,
        ], [])

    feat_topofthefoodchain = _LocDetail(1225, [
            DoLRegionNames.wolf_cave.value,
        ], [
            DoLOptionFilters.type_feat.value,
            DoLOptionFilters.req_feat_silver.value,
            DoLOptionFilters.req_badend.value,
            DoLOptionFilters.toggle_bestiality.value,
        ], [])

    feat_prideofthefarm = _LocDetail(1226, [
            DoLRegionNames.remy_farm.value,
        ], [
            DoLOptionFilters.type_feat.value,
            DoLOptionFilters.req_feat_silver.value,
            DoLOptionFilters.req_badend.value,
            DoLOptionFilters.toggle_lactation.value,
        ], [])

    feat_dawntodusk = _LocDetail(1227, [
        # From testing, doesn't seem very hard
            DoLRegionNames.alex_farm.value,
        ], [
            DoLOptionFilters.type_feat.value,
            DoLOptionFilters.req_feat_copper.value,
        ], [])

    feat_earslimelover = _LocDetail(1228, [
            DoLRegionNames.landfill.value,
        ], [
            DoLOptionFilters.type_feat.value,
            DoLOptionFilters.req_feat_gold.value,
            DoLOptionFilters.toggle_parasites.value,
        ], [])

    feat_earslimeamalgam = _LocDetail(1229, [
            DoLRegionNames.landfill.value,
        ], [
            DoLOptionFilters.type_feat.value,
            DoLOptionFilters.req_feat_gold.value,
            DoLOptionFilters.toggle_parasites.value,
        ], [])

    feat_thepathtoredemption = _LocDetail(1230, [
            DoLRegionNames.in_town.value, # demon req in town, so this in global
        ], [
            DoLOptionFilters.type_feat.value,
            DoLOptionFilters.req_feat_gold.value,
            DoLOptionFilters.req_transformation.value,
            DoLOptionFilters.toggle_transformation_divine.value,
        ], [])

    feat_anewlife = _LocDetail(1231, [ # TODO: LOGIC + ITEM (disabled)
            DoLRegionNames.in_global.value,
        ], [
            DoLOptionFilters.type_feat.value,
            DoLOptionFilters.req_feat_copper.value,
            DoLOptionFilters.req_multipleruns.value,
            DoLOptionFilters.f.value,
        ], [
            # has vrelcoin count
            # has feat booster unlocked
        ])

    feat_negotiator = _LocDetail(1232, [ # TODO: lowprio LOCATION + LOGIC
            # check how possible anywhere is
            # strip club, bartender, etc
            DoLRegionNames.spa.value,
        ], [
            DoLOptionFilters.type_feat.value,
            DoLOptionFilters.req_feat_gold.value,
        ], [
            # spa req: 6/7 max beauty or handskill >= 400
            # since beauty isn't randomized, we can technically
            # not have a req for hands, but include anyway
            DoLRules.hands_2
        ])


    # INFO Outfits : by bluecat
    #
    # This details all specific sets of clothing,
    # it doesn't matter how many you have unlocked, but
    # how many sets you have unlocked for both feats
    #
    # Greater sets encapsulate minor sets, and still
    # count towards the count for the feat. Best
    # documented on the wiki
    #
    # -- Greater Sets:
    # Halloween
    # Valentines
    # Bad End
    # Temple
    # Pendant
    # Historic
    # Transformation
    # Mask
    # Fox
    #
    # -- Seasonal Outfits:
    # Witch:            prey/witch trait
    # Vampire:          Stockholm Kylar
    # Mummy:            Catacombs Passout
    # Scarecrow:        Heroic Victory Feat
    # Skeleton:         Catacombs Access
    # Future Suit:      Arcade Game Win
    # Pumpkin:          15 recipes
    # Chistmas Set:     Domus Houses: leave 1k when stealing
    # Rose Wedding:     Kylar Dimissal
    # Wrap:             Noticed Stealing twice or Robin Christmas Event
    #
    # -- Location Outfits
    # SShirt:           Underground Brothel
    # Cow Outfit:       Remy's Farm
    # Prison Outfit:    Prison
    # Straightjacket:   Asylum
    # Initiate Robe:    Temple
    # Monk/Nun:         Temple Trial
    # Evangelist:       Temple Solicit (req: pros 3)
    # Confessors:       Temple Confess
    # Sparring:         Temple Weapon Rank
    # Stole:            Temple Grace
    # Stone Pendant:    Temple Quarters
    # Holy Pendant:     Soup Kitchen
    # Dark Pendant:     Orphanage Loft
    # Islander Mask:    Island
    # Fox Mask:         Avery Card Date (avery victory)
    # Jasper:           Forest Shop Gold Request (or remove gold chasity here)
    # Foreign:          Leighton Blackmail # NOTE: wiki lists math req, cannot find one
    # Brothel:          Brothel Shows # just little bit of pros fame
    # Chef:             Cafe Re-Opening
    # Esoteric Specs:   Hookah Ownership
    # Fedora:           Strip Club Smugglers
    # Catsuit           Docks Raiding Catsuit # skul ~4
    # Flowers:          Gwylan Ritual AND Daisy Seeds AND Flower Crown
    # Janet:            Library Book (req: eng gte 600)
    # Swan:             Dance Jobs (req: dance 800)
    # Butterfly:        Plant Lover Trait
    #
    # -- Transformation Outfits
    # Shrine:           Fox TF OR Moor Shrine
    # Succubus:         Demon TF OR 15 virginities taken
    #
    # -- Stockholm Outfits
    # Bird Outfit:      Great Hawk
    # Loincloth:        Eden or Wolves
    #
    # -- Feat Outfits
    # Museum Rags:      Museum Horse and Duck (req: success swimming_9, willpower_4)
    # Vintage:          Warmest Winter Feat
    # Exorcist:         Breaking the Stone Feat
    # Chain:            Trials of Faith Feat
    #
    # -- Other
    # Temple Sexy:      World Corruption gte 30
    #
    # -- Gwylan
    # Sage Hat:         Wildsong Feat
    # familiar Collar:   familiar Collar
    #
    # -- Uncounted
    # Rose:             Gwylan ritual

    # figure out how I wanna handle clothing % feats 
    feat_curiousattire = _LocDetail(1233, [ # TODO: lowprio, LOGIC (disabled) (clothing)
            DoLRegionNames.forest_shop.value,
        ], [
            DoLOptionFilters.type_feat.value,
            DoLOptionFilters.req_feat_silver.value,
            DoLOptionFilters.f.value, # disabled for now
        ], [
            DoLRules.outfit_50p,
        ])

    feat_wickedwardrobe = _LocDetail(1234, [ # TODO: lowprio, LOGIC (disabled) (clothing)
            DoLRegionNames.forest_shop.value,
        ], [
            DoLOptionFilters.type_feat.value,
            DoLOptionFilters.req_feat_gold.value,
            DoLOptionFilters.req_badend.value,
            DoLOptionFilters.req_difficult.value,
            DoLOptionFilters.f.value, # disabled for now
        ], [
            DoLRules.outfit_100p,
        ])

    # figure out how I wanna handle these (feat%)
    feat_mycollectionoffeats = _LocDetail(1235, [ # TODO: lowprio (disabled) (feat%)
            DoLRegionNames.in_global.value,
        ], [
            DoLOptionFilters.type_feat.value,
            DoLOptionFilters.req_feat_gold.value,
            DoLOptionFilters.req_multipleruns.value,
            DoLOptionFilters.req_difficult.value,
            DoLOptionFilters.f.value, # disabled for now
        ], [
            # has access to feats for 50% of coins
        ])

    feat_mytimelesscollectionoffeats = _LocDetail(1236, [ # TODO: lowprio (disabled) (feat%)
        ], [
            DoLOptionFilters.type_feat.value,
            DoLOptionFilters.req_feat_jeweled.value,
            DoLOptionFilters.req_multipleruns.value,
            DoLOptionFilters.req_difficult.value,
            DoLOptionFilters.f.value, # disabled for now
        ], [
            # has access to feats for 95% of coins
        ])


    # Preg Feats

    # INFO Parasite Locations : by bluecat 
    #
    # -- Tentacles:
    # Ocean
    # Town # via <<eventstreet>>
    # Forest
    # Forest Lake
    # Orpanage Bath # req slimes
    # School while exposed
    # Compound Crystal
    # non-snake softvore locs # locations below
    #
    # -- Vore:
    # Snake:                Forest Eden Hunt (no tentacles)
    # Snake:                Forest (no tentacles)
    # Snake:                Forest Robin Date (no tentacles)
    # Frog:                 Forest Lake (no tentacles)
    # Lizard:               Old Sewers (no tentacles)
    # Giant Lurker:         Moor Bird Hunt
    # Slime:                Maze
    # Oyster:               Ocean Rocks (Loc Beach)
    # Slug:                 Beach Cave (old sewers)
    # 'Creature':           Tentacle Forest (non encounter) (no 'tentacles')
    # 'Creature'/Oyster:    Ocean
    # 'Creature':           Docks Robin Capture
    # 'Creature':           Moor
    # 'Creature':           Beach Walk
    #
    #
    # -- Fish:
    # Forest Lake
    # Ocean Rocks (beach) # Deviancy 5 
    # Office Building
    #
    # -- Snakes: 
    # Forest
    # Brothel Show # Deviancy 5 
    #
    # -- Spiders: 
    # Danube Houses
    # Brothel Show # Deviancy 5 
    #
    # -- Slimes: 
    # Orphanage 
    # Prison 
    # Hookah Parlour # requires ownership
    # Sewers
    # Old Sewers
    # Maze
    # Landfill arousalmax
    #
    # -- Maggots:
    # Landfill
    # Brothel Show # Deviancy 5 
    #
    # -- Worms:
    # School
    # Underground Brothel
    # Brothel Show # Deviancy 5 
    # Park Crate while exposed # exhb 1
    # NOTE: wiki mentions docks, however cannot find any
    #
    # -- Eels:
    # Ocean
    # Beach # possible via <<eventseabeach>>
    # Sewers 
    # Brothel Show # Deviancy 5 
    #
    # -- Bees:
    # Forest # Can always fail tend
    #
    # -- Lurkers:
    # Moor
    # Churchyard (forest)
    # Alex Farm
    #
    # -- Slugs:
    # Smug Cave (Old Sewers)
    # Tentacle Forest # no loc requirement
    # Island 
    #
    # -- Squids:
    # Ocean
    #
    # -- Wasps:
    # Forest
    #
    # -- Vines:
    # Farmlands # while exposed
    # Forest
    # Forest Lake Fishing
    # Plantpeople (check below)
    # Moor (Phallic plant)
    # Tending in edens, alexs, temple, and orphanage
    #
    # -- Plantpeople:
    # Forest
    # Forest Lake Fishing
    # Bog
    # Gwylan Ritual (complex)
    # Moor
    # Danube Houses
    #
    #
    # -- Pale Slime/Tentacle: # NOTE: either one works
    # Ivory Wraith
    # Forest Lake (blood moon)
    # Forest (Wraith Hunting) (slimes)
    # Forest Event River Swimming (blood moon) (slimes)
    #
    # -- Metal Tentacle:
    # Landfill
    # Brothel Show Sex Machine with Pros 5
    # 


    # INFO Ivory Wraith : by bluecat
    #
    # -- Wraith Forms:
    # Ivory Wraith can spawn in different forms,
    # which can determine their spawn. Forms are:
    #   Man (no tentacles/slimes)
    #   Arms (no tentacles/slimes)
    #   Tentacles
    #   Slime Tentacles (unused, go to tentacles)
    #   Slime
    #   Abomination (tentacle man)
    #
    # If a state is randomly chosen, if man is chosen and
    # the wraith is haunting or its bloodmoon, choose abomination instead
    # If a state requires slimes/tentacles toggles, default to arms if disabled
    #
    # -- Wraith Event:
    # (hallucinating gte lust* and lust gte rand) or bloodmoon 
    # set this value to true, else false
    #
    # -- Wraith Apologise:
    # If you apologise to a wraith while they are Man, Arms, or Abomination,
    # you can skip future(?) combats, granted you have seen the vision in its prison.
    # also goes on cooldown afterwards until the wraith is unset, which wraithApologise
    # will also be unset and you will have to apologise again
    #
    # -- Wraith State:
    # just based on who the theif of the necklace
    # you: haunt, diver: depsair, none: active
    # Also some checks check if their spawn from you is dead or sold
    # spawn being parasites like pale slimes or tentacles
    #
    # -- Wraith Lust:
    # Refered to as wraith obsession, using <gobsession> / <lobession>, this
    # is increased in events or when killing/selling its children from you
    # its decreased when taking care/helping its children, or being in its prison
    # When a wraith is init'd, its set to 0 if not haunting, else 20
    # If you've seen the prison vision, its set to 15 instead
    #
    # -- Wraith Hunting:
    # Wraith can hunt you during bloodmoons which causes the eventpools
    # marked with hunt to trigger randomly, based on hunt value.
    # Hunt value is init'd differently based on the area you are in
    # but for the most part the hunt is based on the lust of the wraith 
    #
    #
    # -- General Events:
    # Haunt : Asylum (Abomination)
    # Haunt : Pub (Random)
    # Haunt : Farm Assult (Man, Arms, or Abomination)
    # WraithEvent : Moor Swimming (Random)
    # Haunt or Dead : Compound (Abomination)
    # Haunt/Despair or Dead/Sold : WraithEvent : Kylar (Abomination)
    # WraithEvent : Robin (Abomination)
    #
    #
    # -- EventPools:
    # - Street Events Hunt:
    # Hunt gte 5:
    #   Caught
    #   Run 
    #   Tentacle (Banish, Grab, Encounter, Run) (if disabled +1 hunt)
    #   Nothing (double weight)
    #   Water Drench (+1 Hunt)
    # else/and:
    #   6 nothing/stress events (varying weight)
    #
    # - Sewer Events Hunt:
    # Hunt gte 10:
    #   Insta Caught
    # Hunt gte 5:
    #   Caught
    #   Run
    #   Tentacle (Banish, Grab, Encounter, Run) (if disabled +1 hunt)
    #   Slimes (if disabled +1 Hunt)
    # else/and:
    #   4 nothing/stress events (varying weight)
    #
    # - Drains Events Hunt:
    # Hunt gte 10:
    #   Caught
    #
    # - Also:
    #   If you take a bus +1 hunt
    #   NOTE: this ignores base value, and
    #   can take you to hunt events even with a below start
    #
    # -- Conclusion
    # Wraith events hardly start until you get haunt events,
    # which mainly requires stealing the necklace from the wraith
    # or killing/selling their offspring. 
    # However to get access to their offspring without 
    # the wraith you would have to specifically go 
    # to the forest lake on a blood moon, to which you
    # should already have access to the wraith. 
    # Therefore logic will only dictate forest lake is required


    feat_broodmotherhost = _LocDetail(1237, 
            DoLRegionGroups.parasitedelivery.value
        , [
            DoLOptionFilters.type_feat.value,
            DoLOptionFilters.req_feat_silver.value,
            DoLOptionFilters.toggle_parasiticpregnancy.value,
            DoLOptionFilters.tentacles_or_bestiality.value,
        ], [
            DoLRules.access_parasite_delivery,
            DoLRules.access_parasite_any,
        ])

    feat_topbroodmotherhost = _LocDetail(1238,
            DoLRegionGroups.parasitedelivery.value
        , [
            DoLOptionFilters.type_feat.value,
            DoLOptionFilters.req_feat_gold.value,
            DoLOptionFilters.toggle_parasiticpregnancy.value,
            DoLOptionFilters.tentacles_or_bestiality.value,
            DoLOptionFilters.req_difficult.value,
        ], [
            DoLRules.topbroodmother,
        ])

    feat_broodmotherzoologist = _LocDetail(1239, 
            DoLRegionGroups.parasitedelivery.value
        , [
            DoLOptionFilters.type_feat.value,
            DoLOptionFilters.req_feat_gold.value,
            DoLOptionFilters.toggle_parasiticpregnancy.value,
            DoLOptionFilters.toggle_tentacles.value,
            DoLOptionFilters.toggle_bestiality.value,
        ], [
            DoLRules.access_parasite_all,
        ])

    feat_miracleoflife = _LocDetail(1240, [
            DoLRegionNames.in_town.value,
            DoLRegionNames.forest.value,
            DoLRegionNames.wolf_cave.value,
            DoLRegionNames.moor.value,
            DoLRegionNames.bird_tower.value,
        ], [
            DoLOptionFilters.type_feat.value,
            DoLOptionFilters.req_feat_silver.value,
            DoLOptionFilters.toggle_pregnancy.value,
        ], [])

    feat_firstfatherhood = _LocDetail(1241, [
            DoLRegionNames.in_town.value,
        ], [
            DoLOptionFilters.type_feat.value,
            DoLOptionFilters.req_feat_silver.value,
            DoLOptionFilters.toggle_pregnancy.value,
        ], [])

    feat_hailmary = _LocDetail(1242, [
            # orph for herm mast?
            DoLRegionNames.orphanage.value,
        ], [
            DoLOptionFilters.type_feat.value,
            DoLOptionFilters.req_feat_platinum.value,
            DoLOptionFilters.req_multipleruns.value,
            DoLOptionFilters.req_difficult.value,
        ], [])

    feat_bicyclemother = _LocDetail(1243, [
            DoLRegionNames.in_town.value,
            DoLRegionNames.forest.value,
            DoLRegionNames.wolf_cave.value,
            DoLRegionNames.moor.value,
            DoLRegionNames.bird_tower.value,
        ], [
            DoLOptionFilters.type_feat.value,
            DoLOptionFilters.req_feat_silver.value,
            DoLOptionFilters.toggle_pregnancy.value,
        ], [])

    feat_lifecomesinthrees = _LocDetail(1244, [
            # pharmacy for fert pills (0.12% chance otherwise)
            DoLRegionNames.pharmacy.value,
        ], [
            DoLOptionFilters.type_feat.value,
            DoLOptionFilters.req_feat_silver.value,
            DoLOptionFilters.toggle_pregnancy.value,
        ], [])

    feat_lifebeginswhenyouleastexpect = _LocDetail(1245, [
            DoLRegionNames.in_town.value,
            DoLRegionNames.forest.value,
            DoLRegionNames.wolf_cave.value,
            DoLRegionNames.moor.value,
            DoLRegionNames.bird_tower.value,
        ], [
            DoLOptionFilters.type_feat.value,
            DoLOptionFilters.req_feat_silver.value,
            DoLOptionFilters.toggle_pregnancy.value,
            DoLOptionFilters.req_multipleruns.value,
            DoLOptionFilters.toggle_parasites.value,
        ], [])

    feat_diversityoflife = _LocDetail(1246, [
            DoLRegionNames.hospital.value,
        ], [
            DoLOptionFilters.type_feat.value,
            DoLOptionFilters.req_feat_platinum.value,
            DoLOptionFilters.toggle_pregnancy.value,
        ], [
            DoLRules.diversityoflife,
        ])


    # ---------------- Upgrades ----------------
    upgrade_farm_wall_1 = _LocDetail(1500, [
            DoLRegionNames.alex_farm.value,    
        ], [
            DoLOptionFilters.type_upgrade.value,
            DoLOptionFilters.type_upgrade_alexfarm.value,
        ], [])

    upgrade_farm_wall_2 = _LocDetail(1501, [
            DoLRegionNames.alex_farm.value,    
        ], [
            DoLOptionFilters.type_upgrade.value,
            DoLOptionFilters.type_upgrade_alexfarm.value,
        ], [])

    upgrade_farm_wall_3 = _LocDetail(1502, [
            DoLRegionNames.alex_farm.value,    
        ], [
            DoLOptionFilters.type_upgrade.value,
            DoLOptionFilters.type_upgrade_alexfarm.value,
        ], [])

    upgrade_farm_wall_4 = _LocDetail(1503, [
            DoLRegionNames.alex_farm.value,    
        ], [
            DoLOptionFilters.type_upgrade.value,
            DoLOptionFilters.type_upgrade_alexfarm.value,
        ], [])

    upgrade_farm_security_1 = _LocDetail(1504, [
            DoLRegionNames.alex_farm.value,    
        ], [
            DoLOptionFilters.type_upgrade.value,
            DoLOptionFilters.type_upgrade_alexfarm.value,
        ], [])

    upgrade_farm_security_2 = _LocDetail(1505, [
            DoLRegionNames.alex_farm.value,    
        ], [
            DoLOptionFilters.type_upgrade.value,
            DoLOptionFilters.type_upgrade_alexfarm.value,
        ], [])

    upgrade_farm_kennel = _LocDetail(1506, [
            DoLRegionNames.alex_farm.value,    
        ], [
            DoLOptionFilters.type_upgrade.value,
            DoLOptionFilters.type_upgrade_alexfarm.value,
        ], [])

    upgrade_farm_woodland_1 = _LocDetail(1507, [
            DoLRegionNames.alex_farm.value,    
        ], [
            DoLOptionFilters.type_upgrade.value,
            DoLOptionFilters.type_upgrade_alexfarm.value,
        ], [])

    upgrade_farm_woodland_2 = _LocDetail(1508, [
            DoLRegionNames.alex_farm.value,    
        ], [
            DoLOptionFilters.type_upgrade.value,
            DoLOptionFilters.type_upgrade_alexfarm.value,
        ], [])

    upgrade_farm_woodland_3 = _LocDetail(1509, [
            DoLRegionNames.alex_farm.value,    
        ], [
            DoLOptionFilters.type_upgrade.value,
            DoLOptionFilters.type_upgrade_alexfarm.value,
        ], [])

    upgrade_farm_barn_1 = _LocDetail(1510, [
            DoLRegionNames.alex_farm.value,    
        ], [
            DoLOptionFilters.type_upgrade.value,
            DoLOptionFilters.type_upgrade_alexfarm.value,
        ], [])

    upgrade_farm_barn_2 = _LocDetail(1511, [
            DoLRegionNames.alex_farm.value,    
        ], [
            DoLOptionFilters.type_upgrade.value,
            DoLOptionFilters.type_upgrade_alexfarm.value,
        ], [])

    upgrade_farm_coop_1 = _LocDetail(1512, [
            DoLRegionNames.alex_farm.value,    
        ], [
            DoLOptionFilters.type_upgrade.value,
            DoLOptionFilters.type_upgrade_alexfarm.value,
        ], [])

    upgrade_farm_coop_2 = _LocDetail(1513, [
            DoLRegionNames.alex_farm.value,    
        ], [
            DoLOptionFilters.type_upgrade.value,
            DoLOptionFilters.type_upgrade_alexfarm.value,
        ], [])

    upgrade_farm_irrigation = _LocDetail(1514, [
            DoLRegionNames.alex_farm.value,    
        ], [
            DoLOptionFilters.type_upgrade.value,
            DoLOptionFilters.type_upgrade_alexfarm.value,
        ], [])

    upgrade_farm_stable = _LocDetail(1515, [
            DoLRegionNames.alex_farm.value,    
        ], [
            DoLOptionFilters.type_upgrade.value,
            DoLOptionFilters.type_upgrade_alexfarm.value,
        ], [])

    upgrade_farm_parasite_1 = _LocDetail(1516, [
            DoLRegionNames.alex_farm.value,    
        ], [
            DoLOptionFilters.type_upgrade.value,
            DoLOptionFilters.type_upgrade_alexfarm.value,
        ], [])

    upgrade_farm_parasite_2 = _LocDetail(1517, [
            DoLRegionNames.alex_farm.value,    
        ], [
            DoLOptionFilters.type_upgrade.value,
            DoLOptionFilters.type_upgrade_alexfarm.value,
        ], [])

    upgrade_farm_greenhouse = _LocDetail(1518, [
            DoLRegionNames.alex_farm.value,    
        ], [
            DoLOptionFilters.type_upgrade.value,
            DoLOptionFilters.type_upgrade_alexfarm.value,
        ], [])

    upgrade_loft_pepperspraylab = _LocDetail(1519, [
            DoLRegionNames.orphanage.value,
        ], [
            DoLOptionFilters.type_upgrade.value,
            DoLOptionFilters.type_upgrade_loft.value,
            DoLOptionFilters.req_loveinterest.value, # Kylar
        ], [
            DoLRules.access_school,
        ])

    upgrade_loft_kitchen = _LocDetail(1520, [ # TODO: LOGIC
            DoLRegionNames.orphanage.value,
        ], [
            DoLOptionFilters.type_upgrade.value,
            DoLOptionFilters.type_upgrade_loft.value,
            # River, non LI
        ], [
            # River 80% love location
            DoLRules.access_soupkitchen, # talk to River at soup kitchen
        ])

    upgrade_loft_window = _LocDetail(1521, [
            DoLRegionNames.orphanage.value,
        ], [
            DoLOptionFilters.type_upgrade.value,
            DoLOptionFilters.type_upgrade_loft.value,
            DoLOptionFilters.req_badend.value, # Great Hawk stockholm
            DoLOptionFilters.req_loveinterest.value,
        ], [
            DoLRules.access_birdtower,
            DoLRules.tfrule_harpy_full_appear, # sing at birdtower
            DoLRules.access_pub, # also need to ask Landry about this
        ])

    upgrade_loft_nook = _LocDetail(1522, [ # TODO: LOGIC
            # NOTE: typo in wiki 'Reading Dook'
            # wiki is offline right now so would fix this if it wasn't
            DoLRegionNames.orphanage.value,
        ], [
            DoLOptionFilters.type_upgrade.value,
            DoLOptionFilters.type_upgrade_loft.value,
            # Doren, non LI
        ], [
            # doren love to 50% location
            # doren flat unlock and location
            DoLRules.access_park, # talk to doren at park
        ])

    upgrade_loft_coffee = _LocDetail(1523, [
        # chef at cafe with sam 90% love
            DoLRegionNames.orphanage.value,
        ], [
            DoLOptionFilters.type_upgrade.value,
            DoLOptionFilters.type_upgrade_loft.value,
            # Sam, non LI
        ], [
            DoLRules.access_cafe, 
        ])

    upgrade_loft_whitney = _LocDetail(1524, [ # TODO: LOGIC
            DoLRegionNames.commercial_alleyways.value,
        ], [
            DoLOptionFilters.type_upgrade.value,
            DoLOptionFilters.type_upgrade_loft.value,
            DoLOptionFilters.req_loveinterest.value, # whitney
        ], [
            DoLRules.access_orphanage
            # I remember reading through this code for whitney
            # but have lost memory of it, I think it
            # was just any alleyways or eventstreet though
        ])


    # ---------------- Upgrades ----------------
    accessitem_fakeid = _LocDetail(2000, [
            DoLRegionNames.brothel.value,
        ], [
            DoLOptionFilters.type_accessitem.value,
        ], [])

    accessitem_mazekey = _LocDetail(2001, [
            DoLRegionNames.domus_houses.value,
        ], [
            DoLOptionFilters.type_accessitem.value,
        ], [])

    accessitem_adoptionpapers = _LocDetail(2002, [
            DoLRegionNames.orphanage.value,
        ], [
            DoLOptionFilters.type_accessitem.value,
        ], [])


    # ----- Overrides
    # we need overrides incase feats are disabled, but 
    # we have stuff like transformations randomized, and need
    # a location to put them.
    # These should have rules set up to not generate if the original does
    override_transformation_cat         = feat_purrfect.override(swapgenrule=[DoLOptionFilters.override_feat_transformation.value])
    override_transformation_wolf        = feat_howlatthemoon.override(swapgenrule=[DoLOptionFilters.override_feat_transformation.value])
    override_transformation_cow         = feat_messwiththebull.override(swapgenrule=[DoLOptionFilters.override_feat_transformation.value])
    override_transformation_harpy       = feat_flylikeaneagle.override(swapgenrule=[DoLOptionFilters.override_feat_transformation.value])
    override_transformation_fox         = feat_youslyfox.override(swapgenrule=[DoLOptionFilters.override_feat_transformation.value])
    override_transformation_angel       = feat_walklikeanangel.override(swapgenrule=[DoLOptionFilters.override_feat_transformation.value])
    override_transformation_fallenangel = feat_fallingfallingfalling.override(swapgenrule=[DoLOptionFilters.override_feat_transformation.value])
    override_transformation_demon       = feat_devilishlooks.override(swapgenrule=[DoLOptionFilters.override_feat_transformation.value])
    
    # no need for alex upgrades as they
    # have no associated feats
    override_upgrade_flatsbridge        = feat_bridgingthepast.override(swapgenrule=[DoLOptionFilters.override_feat_upgrade_tentacle.value])
    override_upgrade_forestroad         = feat_safetrail.override(swapgenrule=[DoLOptionFilters.override_feat_upgrade_tentacle.value])
    override_upgrade_fieldoffice        = feat_fieldwork.override(swapgenrule=[DoLOptionFilters.override_feat_upgrade_tentacle.value])
    override_upgrade_residentialthicket = feat_concretewoodland.override(swapgenrule=[DoLOptionFilters.override_feat_upgrade_tentacle.value])
    override_upgrade_schoolgreen        = feat_schoolgreen.override(swapgenrule=[DoLOptionFilters.override_feat_upgrade_tentacle.value])
    override_upgrade_hookahparlour      = feat_hookahmaster.override(swapgenrule=[DoLOptionFilters.override_feat_upgrade_tentacle.value])
    override_upgrade_adultshop          = feat_openedpandorasbox.override(swapgenrule=[DoLOptionFilters.override_feat_upgrade_general.value])
    override_upgrade_cafeopening        = feat_headchef.override(swapgenrule=[DoLOptionFilters.override_feat_upgrade_general.value])


@dataclass(frozen=True)
class _ItemDetail:
    """
    Container for details of a location

    ### Definition:

    ItemName = ItemDetail(Location ID, Item Count
        [Item Classification], 
        [Item Generation Rules], 
    )
    """ # no _ so I don't accidently mass replace the docstring
    item_id: int
    item_multiplier: int
    types: ItemClassification
    # Rules for generation should use world options
    rules_generation: list[Rule] | list[ROptionFilter]


class DoLItemData(Enum):
    """
    Container of data for all items for this game

    ### Definition:

    ItemName = ItemDetail(Location ID, Item Count
        [Item Classification], 
        [Item Generation Rules], 
    )
    """ # no _ so I don't accidently mass replace the docstring


    # Required to build details correctly
    def __new__(cls, value):
        obj = object.__new__(cls)
        obj._value_ = value
        return obj

    # Fixes 'Any' when looking for locdetail
    @property
    def value(self) -> _ItemDetail:
        return self._value_

    # Trap
    #"Force Combat Encounter Trap": ItemClassification.trap, # TBA
    #"Force Stalk Encounter Trap": ItemClassification.trap, # TBA
    #"Teleportion Trap": ItemClassification.trap, # TBA

    # Filler
    money_100 = _ItemDetail(1, 0, ItemClassification.filler, [])

    # -- Antiques
    antique_ivorystatuette = _ItemDetail(2, 1, 
            ItemClassification.progression
        , [
            DoLOptionFilters.type_antiques.value])

    antique_silvercoin = _ItemDetail(3, 1, 
            ItemClassification.progression
        , [
            DoLOptionFilters.type_antiques.value])

    antique_silvercrown = _ItemDetail(4, 1, 
            ItemClassification.progression
        , [
            DoLOptionFilters.type_antiques.value])

    antique_crystal = _ItemDetail(5, 1, 
            ItemClassification.progression
        , [
            DoLOptionFilters.type_antiques.value])

    antique_silverblade = _ItemDetail(6, 1, 
            ItemClassification.progression
        , [
            DoLOptionFilters.type_antiques.value])

    antique_coppercoin = _ItemDetail(7, 1, 
            ItemClassification.progression
        , [
            DoLOptionFilters.type_antiques.value])

    antique_silvergoblet = _ItemDetail(8, 1, 
            ItemClassification.progression
        , [
            DoLOptionFilters.type_antiques.value])

    antique_fetish = _ItemDetail(9, 1, 
            ItemClassification.progression
        , [
            DoLOptionFilters.type_antiques.value])

    antique_goldcoin = _ItemDetail(10, 1, 
            ItemClassification.progression
        , [
            DoLOptionFilters.type_antiques.value])

    antique_forestdagger = _ItemDetail(11, 1, 
            ItemClassification.progression
        , [
            DoLOptionFilters.type_antiques.value])

    antique_forestgem = _ItemDetail(12, 1, 
            ItemClassification.progression
        , [
            DoLOptionFilters.type_antiques.value])

    antique_arrow = _ItemDetail(13, 1, 
            ItemClassification.progression
        , [
            DoLOptionFilters.type_antiques.value])

    antique_ivorynecklace = _ItemDetail(14, 1, 
            ItemClassification.progression
        , [
            DoLOptionFilters.type_antiques.value])

    antique_ivorybox = _ItemDetail(15, 1, 
            ItemClassification.progression
        , [
            DoLOptionFilters.type_antiques.value])

    antique_silverring = _ItemDetail(16, 1, 
            ItemClassification.progression
        , [
            DoLOptionFilters.type_antiques.value])

    antique_goldnecklace = _ItemDetail(17, 1, 
            ItemClassification.progression
        , [
            DoLOptionFilters.type_antiques.value])

    antique_chastitybelt = _ItemDetail(18, 1, 
            ItemClassification.progression
        , [
            DoLOptionFilters.type_antiques.value])

    antique_stonetalisman = _ItemDetail(19, 1, 
            ItemClassification.progression
        , [
            DoLOptionFilters.type_antiques.value])

    antique_horn = _ItemDetail(20, 1, 
            ItemClassification.progression
        , [
            DoLOptionFilters.type_antiques.value])

    antique_snuffer = _ItemDetail(21, 1, 
            ItemClassification.progression
        , [
            DoLOptionFilters.type_antiques.value])

    antique_bucket = _ItemDetail(22, 1, 
            ItemClassification.progression
        , [
            DoLOptionFilters.type_antiques.value])

    antique_silvermanacle = _ItemDetail(23, 1, 
            ItemClassification.progression
        , [
            DoLOptionFilters.type_antiques.value])

    antique_whip = _ItemDetail(24, 1, 
            ItemClassification.progression
        , [
            DoLOptionFilters.type_antiques.value])

    antique_goldring = _ItemDetail(25, 1, 
            ItemClassification.progression
        , [
            DoLOptionFilters.type_antiques.value])

    antique_bell = _ItemDetail(26, 1, 
            ItemClassification.progression
        , [
            DoLOptionFilters.type_antiques.value])

    antique_bullet = _ItemDetail(27, 1, 
            ItemClassification.progression
        , [
            DoLOptionFilters.type_antiques.value])

    antique_artilleryshell = _ItemDetail(28, 1, 
            ItemClassification.progression
        , [
            DoLOptionFilters.type_antiques.value])

    antique_grenade = _ItemDetail(29, 1, 
            ItemClassification.progression
        , [
            DoLOptionFilters.type_antiques.value])

    antique_goldbrooch = _ItemDetail(30, 1, 
            ItemClassification.progression
        , [
            DoLOptionFilters.type_antiques.value])

    antique_silverbrooch = _ItemDetail(31, 1, 
            ItemClassification.progression
        , [
            DoLOptionFilters.type_antiques.value])

    antique_islanderarrow = _ItemDetail(32, 1, 
            ItemClassification.progression
        , [
            DoLOptionFilters.type_antiques.value])

    antique_islandermask = _ItemDetail(33, 1, 
            ItemClassification.progression
        , [
            DoLOptionFilters.type_antiques.value])

    antique_obsidiandisc = _ItemDetail(34, 1, 
            ItemClassification.progression
        , [
            DoLOptionFilters.type_antiques.value])

    antique_trilobitefossil = _ItemDetail(35, 1, 
            ItemClassification.progression
        , [
            DoLOptionFilters.type_antiques.value])

    antique_baileyminesign = _ItemDetail(36, 1, 
            ItemClassification.progression
        , [
            DoLOptionFilters.type_antiques.value])

    antique_incenseburner = _ItemDetail(37, 1, 
            ItemClassification.progression
        , [
            DoLOptionFilters.type_antiques.value])

    antique_cup = _ItemDetail(38, 1, 
            ItemClassification.progression
        , [
            DoLOptionFilters.type_antiques.value])

    antique_silvermask = _ItemDetail(39, 1, 
            ItemClassification.progression
        , [
            DoLOptionFilters.type_antiques.value])

    antique_silveramulet = _ItemDetail(40, 1, 
            ItemClassification.progression
        , [
            DoLOptionFilters.type_antiques.value])

    antique_hourglass = _ItemDetail(41, 1, 
            ItemClassification.progression
        , [
            DoLOptionFilters.type_antiques.value])

    antique_swordcane = _ItemDetail(42, 1, 
            ItemClassification.progression
        , [
            DoLOptionFilters.type_antiques.value])

    antique_chocolate = _ItemDetail(43, 1, 
            ItemClassification.progression
        , [
            DoLOptionFilters.type_antiques.value])

    antique_teacaddy = _ItemDetail(44, 1, 
            ItemClassification.progression
        , [
            DoLOptionFilters.type_antiques.value])

    antique_woodenfigurine = _ItemDetail(45, 1, 
            ItemClassification.progression
        , [
            DoLOptionFilters.type_antiques.value])

    antique_copperring = _ItemDetail(46, 1, 
            ItemClassification.progression
        , [
            DoLOptionFilters.type_antiques.value])

    antique_goldcompass = _ItemDetail(47, 1, 
            ItemClassification.progression
        , [
            DoLOptionFilters.type_antiques.value])

    antique_coppercompass = _ItemDetail(48, 1, 
            ItemClassification.progression
        , [
            DoLOptionFilters.type_antiques.value])

    antique_coralring = _ItemDetail(49, 1, 
            ItemClassification.progression
        , [
            DoLOptionFilters.type_antiques.value])

    antique_diamond = _ItemDetail(50, 1, 
            ItemClassification.progression
        , [
            DoLOptionFilters.type_antiques.value])

    antique_brassstatuette = _ItemDetail(51, 1, 
            ItemClassification.progression
        , [
            DoLOptionFilters.type_antiques.value])

    antique_golddagger = _ItemDetail(52, 1, 
            ItemClassification.progression
        , [
            DoLOptionFilters.type_antiques.value])

    antique_goldamulet = _ItemDetail(53, 1, 
            ItemClassification.progression
        , [
            DoLOptionFilters.type_antiques.value])

    antique_goldmask = _ItemDetail(54, 1, 
            ItemClassification.progression
        , [
            DoLOptionFilters.type_antiques.value])

    antique_silvercompass = _ItemDetail(55, 1, 
            ItemClassification.progression
        , [
            DoLOptionFilters.type_antiques.value])

    antique_leathermap = _ItemDetail(56, 1, 
            ItemClassification.progression
        , [
            DoLOptionFilters.type_antiques.value])

    antique_cutlass = _ItemDetail(57, 1, 
            ItemClassification.progression
        , [
            DoLOptionFilters.type_antiques.value])

    antique_silverdagger = _ItemDetail(58, 1, 
            ItemClassification.progression
        , [
            DoLOptionFilters.type_antiques.value])

    antique_rustedcutlass = _ItemDetail(59, 1, 
            ItemClassification.progression
        , [
            DoLOptionFilters.type_antiques.value])

    antique_pinkcrystal = _ItemDetail(60, 1, 
            ItemClassification.progression
        , [
            DoLOptionFilters.type_antiques.value])

    antique_candlestick = _ItemDetail(61, 1, 
            ItemClassification.progression
        , [
            DoLOptionFilters.type_antiques.value])

    antique_dildo = _ItemDetail(62, 1, 
            ItemClassification.progression
        , [
            DoLOptionFilters.type_antiques.value])

    antique_watch = _ItemDetail(63, 1, 
            ItemClassification.progression
        , [
            DoLOptionFilters.type_antiques.value])

    # Serpant Painting is not an antique, but still randomized by them
    antique_serpentpainting = _ItemDetail(64, 1, 
            ItemClassification.progression
        , [
            DoLOptionFilters.type_antiques.value])


    # -- Skills
    progressive_skulduggery_rank = _ItemDetail(65, 10, 
            ItemClassification.progression 
        , [
            DoLOptionFilters.type_skills.value])

    progressive_dancing_rank = _ItemDetail(66, 10, 
            ItemClassification.progression 
        , [
            DoLOptionFilters.type_skills.value])

    progressive_swimming_rank = _ItemDetail(67, 10, 
            ItemClassification.progression 
        , [
            DoLOptionFilters.type_skills.value])

    progressive_athletics_rank = _ItemDetail(68, 10, 
            ItemClassification.progression 
        , [
            DoLOptionFilters.type_skills.value])

    progressive_tending_rank = _ItemDetail(69, 10, 
            ItemClassification.progression 
        , [
            DoLOptionFilters.type_skills.value])

    progressive_housekeeping_rank = _ItemDetail(70, 10, 
            ItemClassification.progression 
        , [
            DoLOptionFilters.type_skills.value])

    progressive_seduction_rank = _ItemDetail(71, 5, 
            ItemClassification.progression 
        , [
            DoLOptionFilters.type_skills.value])

    progressive_oral_rank = _ItemDetail(72, 5, 
            ItemClassification.progression 
        , [
            DoLOptionFilters.type_skills.value])

    progressive_chest_rank = _ItemDetail(73, 5, 
            ItemClassification.progression 
        , [
            DoLOptionFilters.type_skills.value])

    progressive_hands_rank = _ItemDetail(74, 5, 
            ItemClassification.progression 
        , [
            DoLOptionFilters.type_skills.value])

    progressive_buttocks_rank = _ItemDetail(75, 5, 
            ItemClassification.progression 
        , [
            DoLOptionFilters.type_skills.value])

    progressive_privates_rank = _ItemDetail(76, 5, 
            ItemClassification.progression 
        , [
            DoLOptionFilters.type_skills.value])

    progressive_anal_rank = _ItemDetail(77, 5, 
            ItemClassification.progression 
        , [
            DoLOptionFilters.type_skills.value])

    progressive_thighs_rank = _ItemDetail(78, 5, 
            ItemClassification.progression 
        , [
            DoLOptionFilters.type_skills.value])

    progressive_feet_rank = _ItemDetail(79, 5, 
            ItemClassification.progression 
        , [
            DoLOptionFilters.type_skills.value])

    progressive_science_rank = _ItemDetail(80, 5, 
            ItemClassification.progression 
        , [
            DoLOptionFilters.type_skills.value])

    progressive_math_rank = _ItemDetail(81, 5, 
            ItemClassification.progression 
        , [
            DoLOptionFilters.type_skills.value])

    progressive_english_rank = _ItemDetail(82, 5, 
            ItemClassification.progression 
        , [
            DoLOptionFilters.type_skills.value])

    progressive_history_rank = _ItemDetail(83, 5, 
            ItemClassification.progression 
        , [
            DoLOptionFilters.type_skills.value])

    progressive_willpower_rank = _ItemDetail(84, 6, 
            ItemClassification.progression 
        , [
            DoLOptionFilters.type_skills.value])

    progressive_physique_rank = _ItemDetail(85, 6, 
            ItemClassification.progression 
        , [
            DoLOptionFilters.type_skills.value])

    progressive_promiscuity_rank = _ItemDetail(86, 6, 
            ItemClassification.progression 
        , [
            DoLOptionFilters.type_skills.value])

    progressive_exhibitionism_rank = _ItemDetail(87, 6, 
            ItemClassification.progression 
        , [
            DoLOptionFilters.type_skills.value])

    progressive_deviancy_rank = _ItemDetail(88, 6, 
            ItemClassification.progression 
        , [
            DoLOptionFilters.type_skills.value])


    # -- Tentacle Forest Upgrades
    upgrade_flatsbridge = _ItemDetail(89, 1,
            ItemClassification.progression  
        , [
            DoLOptionFilters.type_upgrade.value, 
            DoLOptionFilters.type_upgrade_tentacleforest.value
    ])
    
    upgrade_forestroad = _ItemDetail(90, 1,
            ItemClassification.progression  
        , [
            DoLOptionFilters.type_upgrade.value, 
            DoLOptionFilters.type_upgrade_tentacleforest.value
    ])
    
    upgrade_fieldoffice = _ItemDetail(91, 1,
            ItemClassification.progression  
        , [
            DoLOptionFilters.type_upgrade.value, 
            DoLOptionFilters.type_upgrade_tentacleforest.value
    ])
    
    upgrade_residentialthicket = _ItemDetail(92, 1,
            ItemClassification.progression  
        , [
            DoLOptionFilters.type_upgrade.value, 
            DoLOptionFilters.type_upgrade_tentacleforest.value
    ])
    
    upgrade_schoolgreen = _ItemDetail(93, 1,
            ItemClassification.progression  
        , [
            DoLOptionFilters.type_upgrade.value, 
            DoLOptionFilters.type_upgrade_tentacleforest.value
    ])

    upgrade_hookahparlour = _ItemDetail(94, 1,
            ItemClassification.progression  
        , [
            DoLOptionFilters.type_upgrade.value, 
            DoLOptionFilters.type_upgrade_general.value
    ])


    # -- General World Upgrades
    upgrade_cafe = _ItemDetail(95, 1,
            ItemClassification.filler  # just gives more tips and a small new event  
        , [
            DoLOptionFilters.type_upgrade.value, 
            DoLOptionFilters.type_upgrade_general.value
    ])

    upgrade_adultshop = _ItemDetail(96, 1,
            ItemClassification.useful  
        , [
            DoLOptionFilters.type_upgrade.value, 
            DoLOptionFilters.type_upgrade_general.value
    ])


    # -- Alex Farm Upgrades
    upgrade_farm_wall = _ItemDetail(97, 4,
            ItemClassification.useful  
        , [
            DoLOptionFilters.type_upgrade.value, 
            DoLOptionFilters.type_upgrade_alexfarm.value
    ])

    upgrade_farm_security = _ItemDetail(98, 2,
            ItemClassification.progression  # watchtower feat  
        , [
            DoLOptionFilters.type_upgrade.value, 
            DoLOptionFilters.type_upgrade_alexfarm.value
    ])

    upgrade_farm_kennel = _ItemDetail(99, 1,
            ItemClassification.useful  
        , [
            DoLOptionFilters.type_upgrade.value, 
            DoLOptionFilters.type_upgrade_alexfarm.value
    ])

    upgrade_farm_woodland = _ItemDetail(100, 3,
            ItemClassification.useful  
        , [
            DoLOptionFilters.type_upgrade.value, 
            DoLOptionFilters.type_upgrade_alexfarm.value
    ])

    upgrade_farm_barn = _ItemDetail(101, 2,
            ItemClassification.useful  
        , [
            DoLOptionFilters.type_upgrade.value, 
            DoLOptionFilters.type_upgrade_alexfarm.value
    ])

    upgrade_farm_coop = _ItemDetail(102, 2,
            ItemClassification.useful  
        , [
            DoLOptionFilters.type_upgrade.value, 
            DoLOptionFilters.type_upgrade_alexfarm.value
    ])

    upgrade_farm_irrigation = _ItemDetail(103, 1,
            ItemClassification.useful  
        , [
            DoLOptionFilters.type_upgrade.value, 
            DoLOptionFilters.type_upgrade_alexfarm.value
    ])

    upgrade_farm_stable = _ItemDetail(104, 1,
            ItemClassification.useful  
        , [
            DoLOptionFilters.type_upgrade.value, 
            DoLOptionFilters.type_upgrade_alexfarm.value
    ])

    upgrade_farm_parasite = _ItemDetail(105, 2,
            ItemClassification.progression  # parasite barn required to deliver  
        , [
            DoLOptionFilters.type_upgrade.value, 
            DoLOptionFilters.type_upgrade_alexfarm.value
    ])

    upgrade_farm_greenhouse = _ItemDetail(106, 1,
            ItemClassification.useful  
        , [
            DoLOptionFilters.type_upgrade.value, 
            DoLOptionFilters.type_upgrade_alexfarm.value
    ])


    # -- Transformations
    # NOTE: not 1:1'd with locations because of overrides and
    # tf_parts being seperate
    # NOTE: appearance for some TF's is required for some checks
    # also appearance is planned to also give the race trait

    transformation_wolffull = _ItemDetail(107, 1,
            ItemClassification.progression # dog pound
        , [
            DoLOptionFilters.type_transformation.value, 
            DoLOptionFilters.randomize_tf_full.value, 
            DoLOptionFilters.toggle_transformation_animal.value])
    
    transformation_catfull = _ItemDetail(108, 1,
            ItemClassification.useful
        , [
            DoLOptionFilters.type_transformation.value, 
            DoLOptionFilters.randomize_tf_full.value, 
            DoLOptionFilters.toggle_transformation_animal.value])
    
    transformation_cowfull = _ItemDetail(109, 1,
            ItemClassification.useful 
        , [
            DoLOptionFilters.type_transformation.value, 
            DoLOptionFilters.randomize_tf_full.value, 
            DoLOptionFilters.toggle_transformation_animal.value])
    
    transformation_harpyfull = _ItemDetail(110, 1,
            ItemClassification.progression   # Wings, Flight feat
        , [
            DoLOptionFilters.type_transformation.value, 
            DoLOptionFilters.randomize_tf_full.value, 
            DoLOptionFilters.toggle_transformation_animal.value])
    
    transformation_foxfull = _ItemDetail(111, 1,
            ItemClassification.progression   # Gwylan Outfit  
        , [
            DoLOptionFilters.type_transformation.value, 
            DoLOptionFilters.randomize_tf_full.value, 
            DoLOptionFilters.toggle_transformation_animal.value])
    
    transformation_angelfull = _ItemDetail(112, 1,
            ItemClassification.progression   # Wings
        , [
            DoLOptionFilters.type_transformation.value, 
            DoLOptionFilters.randomize_tf_full.value, 
            DoLOptionFilters.toggle_transformation_divine.value])
    
    transformation_fallenangelfull = _ItemDetail(113, 1,
            ItemClassification.progression   # Wings
        , [
            DoLOptionFilters.type_transformation.value, 
            DoLOptionFilters.randomize_tf_full.value, 
            DoLOptionFilters.toggle_transformation_divine.value])
    
    transformation_demonfull = _ItemDetail(114, 1,
            ItemClassification.progression   # Wings
        , [
            DoLOptionFilters.type_transformation.value, 
            DoLOptionFilters.randomize_tf_full.value, 
            DoLOptionFilters.toggle_transformation_divine.value])


    transformation_wolfappear = _ItemDetail(115, 1,
            ItemClassification.progression # dog pound
        , [
            DoLOptionFilters.type_transformation.value, 
            DoLOptionFilters.randomize_tf_parts.value, 
            DoLOptionFilters.toggle_transformation_animal.value])
    
    transformation_catappear = _ItemDetail(116, 1,
            ItemClassification.useful
        , [
            DoLOptionFilters.type_transformation.value, 
            DoLOptionFilters.randomize_tf_parts.value, 
            DoLOptionFilters.toggle_transformation_animal.value])
    
    transformation_cowappear = _ItemDetail(117, 1,
            ItemClassification.useful
        , [
            DoLOptionFilters.type_transformation.value, 
            DoLOptionFilters.randomize_tf_parts.value, 
            DoLOptionFilters.toggle_transformation_animal.value])
    
    transformation_harpyappear = _ItemDetail(118, 1,
            ItemClassification.progression   # flight learn req
        , [
            DoLOptionFilters.type_transformation.value, 
            DoLOptionFilters.randomize_tf_parts.value, 
            DoLOptionFilters.toggle_transformation_animal.value])
    
    transformation_foxappear = _ItemDetail(119, 1,
            ItemClassification.progression   # Gwylan Outfit
        , [
            DoLOptionFilters.type_transformation.value, 
            DoLOptionFilters.randomize_tf_parts.value, 
            DoLOptionFilters.toggle_transformation_animal.value])
    
    transformation_angelappear = _ItemDetail(120, 1,
            ItemClassification.useful
        , [
            DoLOptionFilters.type_transformation.value, 
            DoLOptionFilters.randomize_tf_parts.value, 
            DoLOptionFilters.toggle_transformation_divine.value])
    
    transformation_fallenangelappear = _ItemDetail(121, 1,
            ItemClassification.useful
        , [
            DoLOptionFilters.type_transformation.value, 
            DoLOptionFilters.randomize_tf_parts.value, 
            DoLOptionFilters.toggle_transformation_divine.value])
    
    transformation_demonappear = _ItemDetail(122, 1,
            ItemClassification.progression   # feat req
        , [
            DoLOptionFilters.type_transformation.value, 
            DoLOptionFilters.randomize_tf_parts.value, 
            DoLOptionFilters.toggle_transformation_divine.value])


    transformation_heterochromia = _ItemDetail(123, 1,
            ItemClassification.filler
        , [
            DoLOptionFilters.type_transformation.value, 
            DoLOptionFilters.randomize_tf_parts.value, 
            DoLOptionFilters.toggle_transformation_animal.value])
    
    transformation_sturyhorns = _ItemDetail(124, 1,
            ItemClassification.useful
        , [
            DoLOptionFilters.type_transformation.value, 
            DoLOptionFilters.randomize_tf_parts.value, 
            DoLOptionFilters.toggle_transformation_animal.value])
    
    transformation_strongwings = _ItemDetail(125, 1,
            ItemClassification.useful
        , [
            DoLOptionFilters.type_transformation.value, 
            DoLOptionFilters.randomize_tf_parts.value, 
            DoLOptionFilters.toggle_transformation_animal.value])
    
    transformation_thrillofthechase = _ItemDetail(126, 1,
            ItemClassification.useful
        , [
            DoLOptionFilters.type_transformation.value, 
            DoLOptionFilters.randomize_tf_parts.value, 
            DoLOptionFilters.toggle_transformation_animal.value])
    
    transformation_fangs = _ItemDetail(127, 1,
            ItemClassification.useful
        , [
            DoLOptionFilters.type_transformation.value, 
            DoLOptionFilters.randomize_tf_parts.value, 
            DoLOptionFilters.toggle_transformation_animal.value])
    
    transformation_sharpeyes = _ItemDetail(128, 1,
            ItemClassification.useful
        , [
            DoLOptionFilters.type_transformation.value, 
            DoLOptionFilters.randomize_tf_parts.value, 
            DoLOptionFilters.toggle_transformation_animal.value])
    
    transformation_mateforlife = _ItemDetail(129, 1,
            ItemClassification.useful
        , [
            DoLOptionFilters.type_transformation.value, 
            DoLOptionFilters.randomize_tf_parts.value, 
            DoLOptionFilters.toggle_transformation_animal.value])
    
    transformation_radiant = _ItemDetail(130, 1,
            ItemClassification.useful
        , [
            DoLOptionFilters.type_transformation.value, 
            DoLOptionFilters.randomize_tf_parts.value, 
            DoLOptionFilters.toggle_transformation_divine.value])
    
    transformation_darkhorns = _ItemDetail(131, 1,
            ItemClassification.useful
        , [
            DoLOptionFilters.type_transformation.value, 
            DoLOptionFilters.randomize_tf_parts.value, 
            DoLOptionFilters.toggle_transformation_divine.value])
    
    transformation_wings = _ItemDetail(132, 1,
            ItemClassification.progression
        , [
            DoLOptionFilters.type_transformation.value, 
            DoLOptionFilters.randomize_tf_parts.value, 
            DoLOptionFilters.toggle_transformation_either.value])

    transformation_flight = _ItemDetail(133, 1,
            ItemClassification.progression
        , [
            DoLOptionFilters.type_transformation.value, 
            DoLOptionFilters.toggle_transformation_either.value])


    # -- Access Items
    accessitem_adoptionpapers = _ItemDetail(134, 1,
            ItemClassification.progression
        , [    
            DoLOptionFilters.type_accessitem.value])

    accessitem_fakeid = _ItemDetail(135, 1,
            ItemClassification.progression
        , [    
            DoLOptionFilters.type_accessitem.value])

    accessitem_mazekey = _ItemDetail(136, 1,
            ItemClassification.progression
        , [    
            DoLOptionFilters.type_accessitem.value])


DEFAULT_ITEM_CLASSIFICATIONS = {DoLItemNames[item.name].value: item.value.types for item in DoLItemData}
ITEM_NAME_TO_ID = {DoLItemNames[item.name].value: item.value.item_id for item in DoLItemData}