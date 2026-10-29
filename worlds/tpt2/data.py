from __future__ import annotations

from dataclasses import dataclass
from enum import Enum, StrEnum
import operator
from typing import Any, Callable, Final, Literal, TYPE_CHECKING

from BaseClasses import ItemClassification
from rule_builder.options import OptionFilter, OPERATORS as standardOPERATORS, OPERATOR_STRINGS as standardOPERATOR_STRINGS

from .options import TPT2_OPTION_NAME, RandomizationTargets
from .en import TPT2ItemNames, TPT2RegionNames, TPT2OptionsLocalization

if TYPE_CHECKING:
    from worlds.AutoWorld import World
    from Options import Option
    from rule_builder.rules import Rule

# Misc Data

class TPT2TypeNames(StrEnum):
    module = "Modules"


# Rule Data

# Operators based off APWorld Main operators for OptionFilter
OperatorsList = Literal["eq", "ne", "gt", "lt", "ge", "le", "contains", "in", "not-contains", "not-in", "and", "or"]
OPERATORS: Final[dict[OperatorsList, Callable[..., bool]]] = {
    "eq": operator.eq,
    "ne": operator.ne,
    "gt": operator.gt,
    "lt": operator.lt,
    "ge": operator.ge,
    "le": operator.le,

    # New
    "contains": operator.contains,
    "in": lambda option, value: operator.contains(value, option),
    "not-contains": lambda option, value: not operator.contains(option, value),
    "not-in": lambda option, value: not operator.contains(value, option),
    "and": operator.and_,
    "or": operator.or_,
}
OPERATOR_STRINGS: Final[dict[OperatorsList, str]] = {
    "eq": "==",
    "ne": "!=",
    "gt": ">",
    "lt": "<",
    "ge": ">=",
    "le": "<=",
}


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
    option: type[Option[Any]] | ROptionFilter
    value: bool | str | int | ROptionFilter
    operator: OperatorsList = "eq"

    def resolve(self, world:World):
        """
        Pass the current world and resolve the rule once you're running
        inside the world functions
        """
        # print(f"Running {self.option} '{self.operator}', '{self.value}'")

        if isinstance(self.option, ROptionFilter): option = self.option.resolve(world)
        else: option = getattr(world.options, TPT2_OPTION_NAME[self.option])

        if isinstance(self.value, ROptionFilter): value = self.value.resolve(world)
        else: value = self.value

        if not (self.operator in OPERATORS): raise ValueError("Invalid ROptionFilter Operator")
        final = OPERATORS[self.operator](option, value)
        
        # print(f"Resolution for {self.option}: '{option}', '{self.operator}', '{value}' IS {final}")
        return final

    def convert(self):
        """
        Returns an OptionFilter of the current data
        Current data must follow OptionFilter construction requirements 
        (normal operators, no ROptionFilter in option or value)
        """
        if isinstance(self.option, ROptionFilter) or isinstance(self.value, ROptionFilter) or (not (self.operator in standardOPERATORS) and not (self.operator in standardOPERATOR_STRINGS)):
            raise ValueError("When converting ROptionFilter; Option, Value, and Operator must be normal OptionFilter components")
        return OptionFilter(self.option, self.value, self.operator)

    def __and__(self, other:ROptionFilter | bool | str | int):
        return ROptionFilter(ROptionFilter(self.option, self.value, self.operator), other, "and")
    
    def __rand__(self, other:ROptionFilter | type[Option[Any]]):
        return ROptionFilter(other, ROptionFilter(self.option, self.value, self.operator), "and")
    
    def __or__(self, other:ROptionFilter | bool | str | int):
        return ROptionFilter(ROptionFilter(self.option, self.value, self.operator), other, "or")

    def __ror__(self, other:ROptionFilter | type[Option[Any]]):
        return ROptionFilter(other, ROptionFilter(self.option, self.value, self.operator), "or")

    def __invert__(self):
        # Reminder:
        # (True == False) = False
        # (False == False) = True
        return ROptionFilter(ROptionFilter(self.option, self.value, self.operator), False)

    def __bool__(self):
        raise TypeError("Use '|', '&', and '~' to handle rules")

class TPT2OptionFilters(Enum):
    type_module = ROptionFilter(RandomizationTargets, TPT2OptionsLocalization.target_modules.value, "contains")


# Location Data

@dataclass(frozen=True)
class _LocDetail:
    """
    Container for details of a location

    ### Definition:

    Location_Name = LocDetail(Location ID, 
        [Locations this is from], 
        [Rules to generate the location], 
        [Rules to get to the location],
    )
    """ # no _ in locdetail so I don't accidently mass replace the docstring
    location_id: int
    locations: list[str]
    # Rules for generation should use world options
    rules_generation: list[ROptionFilter]
    rules_obtain: list[Rule[Any]]

    # function to copy and return the class with changes
    # useful for if a locations gen rules would prevent it from
    # generating, but still need a location of that type, you can
    # create an override location that only generates if all the genrules
    # of the previous are not true
    def override(self,
            addloc:list[str] | None = None, addgenrule:list[ROptionFilter] | None = None, addobtainrule:list[Rule[Any]] | None = None,
            swaploc:list[str] | None = None, swapgenrule:list[ROptionFilter] | None = None, swapobtainrule:list[Rule[Any]] | None = None,
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

        # can keep id the same since we shouldn't gen previous
        return _LocDetail(self.location_id, locations, rules_generation, rules_obtain)


class TPT2LocationData(Enum):
    module_aquaticabsorption = _LocDetail(100, [
            TPT2RegionNames.town.value,
        ], [
            TPT2OptionFilters.type_module.value,
        ], [])

    module_hurricane = _LocDetail(101, [
            TPT2RegionNames.town.value,
        ], [
            TPT2OptionFilters.type_module.value,
        ], [])

    module_neutralamplifier = _LocDetail(102, [
            TPT2RegionNames.town.value,
        ], [
            TPT2OptionFilters.type_module.value,
        ], [])

    module_refinedarmor = _LocDetail(103, [
            TPT2RegionNames.town.value,
        ], [
            TPT2OptionFilters.type_module.value,
        ], [])

    module_airattack = _LocDetail(104, [
            TPT2RegionNames.town.value,
        ], [
            TPT2OptionFilters.type_module.value,
        ], [])

    module_bash = _LocDetail(105, [
            TPT2RegionNames.town.value,
        ], [
            TPT2OptionFilters.type_module.value,
        ], [])

    module_basicattack = _LocDetail(106, [
            TPT2RegionNames.town.value,
        ], [
            TPT2OptionFilters.type_module.value,
        ], [])

    module_gaiaspath = _LocDetail(107, [
            TPT2RegionNames.town.value,
        ], [
            TPT2OptionFilters.type_module.value,
        ], [])

    module_basicbouncing = _LocDetail(108, [
            TPT2RegionNames.town.value,
        ], [
            TPT2OptionFilters.type_module.value,
        ], [])

    module_phoenixbounce = _LocDetail(109, [
            TPT2RegionNames.town.value,
        ], [
            TPT2OptionFilters.type_module.value,
        ], [])

    module_burningattack = _LocDetail(110, [
            TPT2RegionNames.town.value,
        ], [
            TPT2OptionFilters.type_module.value,
        ], [])

    module_combustion = _LocDetail(111, [
            TPT2RegionNames.town.value,
        ], [
            TPT2OptionFilters.type_module.value,
        ], [])

    module_darknessattack = _LocDetail(112, [
            TPT2RegionNames.town.value,
        ], [
            TPT2OptionFilters.type_module.value,
        ], [])

    module_deathwish = _LocDetail(113, [
            TPT2RegionNames.town.value,
        ], [
            TPT2OptionFilters.type_module.value,
        ], [])

    module_earthattack = _LocDetail(114, [
            TPT2RegionNames.town.value,
        ], [
            TPT2OptionFilters.type_module.value,
        ], [])

    module_electricityattack = _LocDetail(115, [
            TPT2RegionNames.town.value,
        ], [
            TPT2OptionFilters.type_module.value,
        ], [])

    module_execution = _LocDetail(116, [
            TPT2RegionNames.town.value,
        ], [
            TPT2OptionFilters.type_module.value,
        ], [])

    module_fireattack = _LocDetail(117, [
            TPT2RegionNames.town.value,
        ], [
            TPT2OptionFilters.type_module.value,
        ], [])

    module_firebreath = _LocDetail(118, [
            TPT2RegionNames.town.value,
        ], [
            TPT2OptionFilters.type_module.value,
        ], [])

    module_icebreath = _LocDetail(119, [
            TPT2RegionNames.town.value,
        ], [
            TPT2OptionFilters.type_module.value,
        ], [])

    module_impetus = _LocDetail(120, [
            TPT2RegionNames.town.value,
        ], [
            TPT2OptionFilters.type_module.value,
        ], [])

    module_infinityattack = _LocDetail(121, [
            TPT2RegionNames.town.value,
        ], [
            TPT2OptionFilters.type_module.value,
        ], [])

    module_lifesteal = _LocDetail(122, [
            TPT2RegionNames.town.value,
        ], [
            TPT2OptionFilters.type_module.value,
        ], [])

    module_lightattack = _LocDetail(123, [
            TPT2RegionNames.town.value,
        ], [
            TPT2OptionFilters.type_module.value,
        ], [])

    module_multishot = _LocDetail(124, [
            TPT2RegionNames.town.value,
        ], [
            TPT2OptionFilters.type_module.value,
        ], [])

    module_natureattack = _LocDetail(125, [
            TPT2RegionNames.town.value,
        ], [
            TPT2OptionFilters.type_module.value,
        ], [])

    module_naturestouch = _LocDetail(126, [
            TPT2RegionNames.town.value,
        ], [
            TPT2OptionFilters.type_module.value,
        ], [])

    module_rapidfire = _LocDetail(127, [
            TPT2RegionNames.town.value,
        ], [
            TPT2OptionFilters.type_module.value,
        ], [])

    module_shatter = _LocDetail(128, [
            TPT2RegionNames.town.value,
        ], [
            TPT2OptionFilters.type_module.value,
        ], [])

    module_sparks = _LocDetail(129, [
            TPT2RegionNames.town.value,
        ], [
            TPT2OptionFilters.type_module.value,
        ], [])

    module_attackspeed = _LocDetail(130, [
            TPT2RegionNames.town.value,
        ], [
            TPT2OptionFilters.type_module.value,
        ], [])

    module_universalattack = _LocDetail(131, [
            TPT2RegionNames.town.value,
        ], [
            TPT2OptionFilters.type_module.value,
        ], [])

    module_waterattack = _LocDetail(132, [
            TPT2RegionNames.town.value,
        ], [
            TPT2OptionFilters.type_module.value,
        ], [])

    module_checkerboardaura = _LocDetail(133, [
            TPT2RegionNames.town.value,
        ], [
            TPT2OptionFilters.type_module.value,
        ], [])

    module_deathaura = _LocDetail(134, [
            TPT2RegionNames.town.value,
        ], [
            TPT2OptionFilters.type_module.value,
        ], [])

    module_drynessaura = _LocDetail(135, [
            TPT2RegionNames.town.value,
        ], [
            TPT2OptionFilters.type_module.value,
        ], [])

    module_fieryaura = _LocDetail(136, [
            TPT2RegionNames.town.value,
        ], [
            TPT2OptionFilters.type_module.value,
        ], [])

    module_frostaura = _LocDetail(137, [
            TPT2RegionNames.town.value,
        ], [
            TPT2OptionFilters.type_module.value,
        ], [])

    module_heartstopperaura = _LocDetail(138, [
            TPT2RegionNames.town.value,
        ], [
            TPT2OptionFilters.type_module.value,
        ], [])

    module_monsoonaura = _LocDetail(139, [
            TPT2RegionNames.town.value,
        ], [
            TPT2OptionFilters.type_module.value,
        ], [])

    module_nullifyingaura = _LocDetail(140, [
            TPT2RegionNames.town.value,
        ], [
            TPT2OptionFilters.type_module.value,
        ], [])

    module_stormaura = _LocDetail(141, [
            TPT2RegionNames.town.value,
        ], [
            TPT2OptionFilters.type_module.value,
        ], [])

    module_unholyaura = _LocDetail(142, [
            TPT2RegionNames.town.value,
        ], [
            TPT2OptionFilters.type_module.value,
        ], [])

    module_whirlwindaura = _LocDetail(143, [
            TPT2RegionNames.town.value,
        ], [
            TPT2OptionFilters.type_module.value,
        ], [])

    module_airbarrier = _LocDetail(144, [
            TPT2RegionNames.town.value,
        ], [
            TPT2OptionFilters.type_module.value,
        ], [])

    module_darknessbarrier = _LocDetail(145, [
            TPT2RegionNames.town.value,
        ], [
            TPT2OptionFilters.type_module.value,
        ], [])

    module_earthbarrier = _LocDetail(146, [
            TPT2RegionNames.town.value,
        ], [
            TPT2OptionFilters.type_module.value,
        ], [])

    module_electricitybarrier = _LocDetail(147, [
            TPT2RegionNames.town.value,
        ], [
            TPT2OptionFilters.type_module.value,
        ], [])

    module_firebarrier = _LocDetail(148, [
            TPT2RegionNames.town.value,
        ], [
            TPT2OptionFilters.type_module.value,
        ], [])

    module_lightbarrier = _LocDetail(149, [
            TPT2RegionNames.town.value,
        ], [
            TPT2OptionFilters.type_module.value,
        ], [])

    module_naturebarrier = _LocDetail(150, [
            TPT2RegionNames.town.value,
        ], [
            TPT2OptionFilters.type_module.value,
        ], [])

    module_temporalbarrier = _LocDetail(151, [
            TPT2RegionNames.town.value,
        ], [
            TPT2OptionFilters.type_module.value,
        ], [])

    module_waterbarrier = _LocDetail(152, [
            TPT2RegionNames.town.value,
        ], [
            TPT2OptionFilters.type_module.value,
        ], [])

    module_divineblessing = _LocDetail(153, [
            TPT2RegionNames.town.value,
        ], [
            TPT2OptionFilters.type_module.value,
        ], [])

    module_onyxsblessing = _LocDetail(154, [
            TPT2RegionNames.town.value,
        ], [
            TPT2OptionFilters.type_module.value,
        ], [])

    module_skyblessing = _LocDetail(155, [
            TPT2RegionNames.town.value,
        ], [
            TPT2OptionFilters.type_module.value,
        ], [])

    module_airblock = _LocDetail(156, [
            TPT2RegionNames.town.value,
        ], [
            TPT2OptionFilters.type_module.value,
        ], [])

    module_darknessblock = _LocDetail(157, [
            TPT2RegionNames.town.value,
        ], [
            TPT2OptionFilters.type_module.value,
        ], [])

    module_earthblock = _LocDetail(158, [
            TPT2RegionNames.town.value,
        ], [
            TPT2OptionFilters.type_module.value,
        ], [])

    module_electricityblock = _LocDetail(159, [
            TPT2RegionNames.town.value,
        ], [
            TPT2OptionFilters.type_module.value,
        ], [])

    module_fireblock = _LocDetail(160, [
            TPT2RegionNames.town.value,
        ], [
            TPT2OptionFilters.type_module.value,
        ], [])

    module_lightblock = _LocDetail(161, [
            TPT2RegionNames.town.value,
        ], [
            TPT2OptionFilters.type_module.value,
        ], [])

    module_natureblock = _LocDetail(162, [
            TPT2RegionNames.town.value,
        ], [
            TPT2OptionFilters.type_module.value,
        ], [])

    module_neutralblock = _LocDetail(163, [
            TPT2RegionNames.town.value,
        ], [
            TPT2OptionFilters.type_module.value,
        ], [])

    module_universalblock = _LocDetail(164, [
            TPT2RegionNames.town.value,
        ], [
            TPT2OptionFilters.type_module.value,
        ], [])

    module_waterblock = _LocDetail(165, [
            TPT2RegionNames.town.value,
        ], [
            TPT2OptionFilters.type_module.value,
        ], [])

    module_condense = _LocDetail(166, [
            TPT2RegionNames.town.value,
        ], [
            TPT2OptionFilters.type_module.value,
        ], [])

    module_defensivepack = _LocDetail(167, [
            TPT2RegionNames.town.value,
        ], [
            TPT2OptionFilters.type_module.value,
        ], [])

    module_offensivepack = _LocDetail(168, [
            TPT2RegionNames.town.value,
        ], [
            TPT2OptionFilters.type_module.value,
        ], [])

    module_pressurize = _LocDetail(169, [
            TPT2RegionNames.town.value,
        ], [
            TPT2OptionFilters.type_module.value,
        ], [])

    module_transmute = _LocDetail(170, [
            TPT2RegionNames.town.value,
        ], [
            TPT2OptionFilters.type_module.value,
        ], [])

    module_waveresources = _LocDetail(171, [
            TPT2RegionNames.town.value,
        ], [
            TPT2OptionFilters.type_module.value,
        ], [])

    module_antiairprojectiles = _LocDetail(172, [
            TPT2RegionNames.town.value,
        ], [
            TPT2OptionFilters.type_module.value,
        ], [])

    module_antidarknessprojectiles = _LocDetail(173, [
            TPT2RegionNames.town.value,
        ], [
            TPT2OptionFilters.type_module.value,
        ], [])

    module_antiearthprojectiles = _LocDetail(174, [
            TPT2RegionNames.town.value,
        ], [
            TPT2OptionFilters.type_module.value,
        ], [])

    module_antielectricityprojectiles = _LocDetail(175, [
            TPT2RegionNames.town.value,
        ], [
            TPT2OptionFilters.type_module.value,
        ], [])

    module_antifireprojectiles = _LocDetail(176, [
            TPT2RegionNames.town.value,
        ], [
            TPT2OptionFilters.type_module.value,
        ], [])

    module_antilightprojectiles = _LocDetail(177, [
            TPT2RegionNames.town.value,
        ], [
            TPT2OptionFilters.type_module.value,
        ], [])

    module_antinatureprojectiles = _LocDetail(178, [
            TPT2RegionNames.town.value,
        ], [
            TPT2OptionFilters.type_module.value,
        ], [])

    module_antineutralprojectiles = _LocDetail(179, [
            TPT2RegionNames.town.value,
        ], [
            TPT2OptionFilters.type_module.value,
        ], [])

    module_shorelineboost = _LocDetail(180, [
            TPT2RegionNames.town.value,
        ], [
            TPT2OptionFilters.type_module.value,
        ], [])

    module_antiuniversalprojectiles = _LocDetail(181, [
            TPT2RegionNames.town.value,
        ], [
            TPT2OptionFilters.type_module.value,
        ], [])

    module_antiwaterprojectiles = _LocDetail(182, [
            TPT2RegionNames.town.value,
        ], [
            TPT2OptionFilters.type_module.value,
        ], [])

    module_borf = _LocDetail(183, [
            TPT2RegionNames.town.value,
        ], [
            TPT2OptionFilters.type_module.value,
        ], [])

    module_airburst = _LocDetail(184, [
            TPT2RegionNames.town.value,
        ], [
            TPT2OptionFilters.type_module.value,
        ], [])

    module_darknessburst = _LocDetail(185, [
            TPT2RegionNames.town.value,
        ], [
            TPT2OptionFilters.type_module.value,
        ], [])

    module_earthburst = _LocDetail(186, [
            TPT2RegionNames.town.value,
        ], [
            TPT2OptionFilters.type_module.value,
        ], [])

    module_electricityburst = _LocDetail(187, [
            TPT2RegionNames.town.value,
        ], [
            TPT2OptionFilters.type_module.value,
        ], [])

    module_fireburst = _LocDetail(188, [
            TPT2RegionNames.town.value,
        ], [
            TPT2OptionFilters.type_module.value,
        ], [])

    module_infinityburst = _LocDetail(189, [
            TPT2RegionNames.town.value,
        ], [
            TPT2OptionFilters.type_module.value,
        ], [])

    module_lightburst = _LocDetail(190, [
            TPT2RegionNames.town.value,
        ], [
            TPT2OptionFilters.type_module.value,
        ], [])

    module_natureburst = _LocDetail(191, [
            TPT2RegionNames.town.value,
        ], [
            TPT2OptionFilters.type_module.value,
        ], [])

    module_neutralburst = _LocDetail(192, [
            TPT2RegionNames.town.value,
        ], [
            TPT2OptionFilters.type_module.value,
        ], [])

    module_universalburst = _LocDetail(193, [
            TPT2RegionNames.town.value,
        ], [
            TPT2OptionFilters.type_module.value,
        ], [])

    module_waterburst = _LocDetail(194, [
            TPT2RegionNames.town.value,
        ], [
            TPT2OptionFilters.type_module.value,
        ], [])

    module_powerofthecat = _LocDetail(195, [
            TPT2RegionNames.town.value,
        ], [
            TPT2OptionFilters.type_module.value,
        ], [])

    module_unholycloak = _LocDetail(196, [
            TPT2RegionNames.town.value,
        ], [
            TPT2OptionFilters.type_module.value,
        ], [])

    module_powerconversion = _LocDetail(197, [
            TPT2RegionNames.town.value,
        ], [
            TPT2OptionFilters.type_module.value,
        ], [])

    module_aerocore = _LocDetail(198, [
            TPT2RegionNames.town.value,
        ], [
            TPT2OptionFilters.type_module.value,
        ], [])

    module_angeliccore = _LocDetail(199, [
            TPT2RegionNames.town.value,
        ], [
            TPT2OptionFilters.type_module.value,
        ], [])

    module_magneticcore = _LocDetail(200, [
            TPT2RegionNames.town.value,
        ], [
            TPT2OptionFilters.type_module.value,
        ], [])

    module_moltencore = _LocDetail(201, [
            TPT2RegionNames.town.value,
        ], [
            TPT2OptionFilters.type_module.value,
        ], [])

    module_oceancore = _LocDetail(202, [
            TPT2RegionNames.town.value,
        ], [
            TPT2OptionFilters.type_module.value,
        ], [])

    module_soulcore = _LocDetail(203, [
            TPT2RegionNames.town.value,
        ], [
            TPT2OptionFilters.type_module.value,
        ], [])

    module_crateofrex = _LocDetail(204, [
            TPT2RegionNames.town.value,
        ], [
            TPT2OptionFilters.type_module.value,
        ], [])

    module_antiaircrit = _LocDetail(205, [
            TPT2RegionNames.town.value,
        ], [
            TPT2OptionFilters.type_module.value,
        ], [])

    module_aircrit = _LocDetail(206, [
            TPT2RegionNames.town.value,
        ], [
            TPT2OptionFilters.type_module.value,
        ], [])

    module_criticalstrike = _LocDetail(207, [
            TPT2RegionNames.town.value,
        ], [
            TPT2OptionFilters.type_module.value,
        ], [])

    module_antidarknesscrit = _LocDetail(208, [
            TPT2RegionNames.town.value,
        ], [
            TPT2OptionFilters.type_module.value,
        ], [])

    module_darknesscrit = _LocDetail(209, [
            TPT2RegionNames.town.value,
        ], [
            TPT2OptionFilters.type_module.value,
        ], [])

    module_antiearthcrit = _LocDetail(210, [
            TPT2RegionNames.town.value,
        ], [
            TPT2OptionFilters.type_module.value,
        ], [])

    module_earthcrit = _LocDetail(211, [
            TPT2RegionNames.town.value,
        ], [
            TPT2OptionFilters.type_module.value,
        ], [])

    module_antielectricitycrit = _LocDetail(212, [
            TPT2RegionNames.town.value,
        ], [
            TPT2OptionFilters.type_module.value,
        ], [])

    module_electricitycrit = _LocDetail(213, [
            TPT2RegionNames.town.value,
        ], [
            TPT2OptionFilters.type_module.value,
        ], [])

    module_emergencycrit = _LocDetail(214, [
            TPT2RegionNames.town.value,
        ], [
            TPT2OptionFilters.type_module.value,
        ], [])

    module_antifirecrit = _LocDetail(215, [
            TPT2RegionNames.town.value,
        ], [
            TPT2OptionFilters.type_module.value,
        ], [])

    module_firecrit = _LocDetail(216, [
            TPT2RegionNames.town.value,
        ], [
            TPT2OptionFilters.type_module.value,
        ], [])

    module_infinitycrit = _LocDetail(217, [
            TPT2RegionNames.town.value,
        ], [
            TPT2OptionFilters.type_module.value,
        ], [])

    module_antilightcrit = _LocDetail(218, [
            TPT2RegionNames.town.value,
        ], [
            TPT2OptionFilters.type_module.value,
        ], [])

    module_lightcrit = _LocDetail(219, [
            TPT2RegionNames.town.value,
        ], [
            TPT2OptionFilters.type_module.value,
        ], [])

    module_antinaturecrit = _LocDetail(220, [
            TPT2RegionNames.town.value,
        ], [
            TPT2OptionFilters.type_module.value,
        ], [])

    module_naturecrit = _LocDetail(221, [
            TPT2RegionNames.town.value,
        ], [
            TPT2OptionFilters.type_module.value,
        ], [])

    module_antineutralcrit = _LocDetail(222, [
            TPT2RegionNames.town.value,
        ], [
            TPT2OptionFilters.type_module.value,
        ], [])

    module_neutralcrit = _LocDetail(223, [
            TPT2RegionNames.town.value,
        ], [
            TPT2OptionFilters.type_module.value,
        ], [])

    module_antiuniversalcrit = _LocDetail(224, [
            TPT2RegionNames.town.value,
        ], [
            TPT2OptionFilters.type_module.value,
        ], [])

    module_universalcrit = _LocDetail(225, [
            TPT2RegionNames.town.value,
        ], [
            TPT2OptionFilters.type_module.value,
        ], [])

    module_antiwatercrit = _LocDetail(226, [
            TPT2RegionNames.town.value,
        ], [
            TPT2OptionFilters.type_module.value,
        ], [])

    module_watercrit = _LocDetail(227, [
            TPT2RegionNames.town.value,
        ], [
            TPT2OptionFilters.type_module.value,
        ], [])

    module_omniversaldamage = _LocDetail(228, [
            TPT2RegionNames.town.value,
        ], [
            TPT2OptionFilters.type_module.value,
        ], [])

    module_aftershock = _LocDetail(229, [
            TPT2RegionNames.town.value,
        ], [
            TPT2OptionFilters.type_module.value,
        ], [])

    module_bulletproof = _LocDetail(230, [
            TPT2RegionNames.town.value,
        ], [
            TPT2OptionFilters.type_module.value,
        ], [])

    module_bulwark = _LocDetail(231, [
            TPT2RegionNames.town.value,
        ], [
            TPT2OptionFilters.type_module.value,
        ], [])

    module_conductor = _LocDetail(232, [
            TPT2RegionNames.town.value,
        ], [
            TPT2OptionFilters.type_module.value,
        ], [])

    module_daigoparry = _LocDetail(233, [
            TPT2RegionNames.town.value,
        ], [
            TPT2OptionFilters.type_module.value,
        ], [])

    module_defiance = _LocDetail(234, [
            TPT2RegionNames.town.value,
        ], [
            TPT2OptionFilters.type_module.value,
        ], [])

    module_heatwave = _LocDetail(235, [
            TPT2RegionNames.town.value,
        ], [
            TPT2OptionFilters.type_module.value,
        ], [])

    module_metalplating = _LocDetail(236, [
            TPT2RegionNames.town.value,
        ], [
            TPT2OptionFilters.type_module.value,
        ], [])

    module_overcharge = _LocDetail(237, [
            TPT2RegionNames.town.value,
        ], [
            TPT2OptionFilters.type_module.value,
        ], [])

    module_quantumdefense = _LocDetail(238, [
            TPT2RegionNames.town.value,
        ], [
            TPT2OptionFilters.type_module.value,
        ], [])

    module_reflect = _LocDetail(239, [
            TPT2RegionNames.town.value,
        ], [
            TPT2OptionFilters.type_module.value,
        ], [])

    module_shelter = _LocDetail(240, [
            TPT2RegionNames.town.value,
        ], [
            TPT2OptionFilters.type_module.value,
        ], [])

    module_stabprevention = _LocDetail(241, [
            TPT2RegionNames.town.value,
        ], [
            TPT2OptionFilters.type_module.value,
        ], [])

    module_stoneskin = _LocDetail(242, [
            TPT2RegionNames.town.value,
        ], [
            TPT2OptionFilters.type_module.value,
        ], [])

    module_strikeback = _LocDetail(243, [
            TPT2RegionNames.town.value,
        ], [
            TPT2OptionFilters.type_module.value,
        ], [])

    module_diceoffate = _LocDetail(244, [
            TPT2RegionNames.town.value,
        ], [
            TPT2OptionFilters.type_module.value,
        ], [])

    module_avalanche = _LocDetail(245, [
            TPT2RegionNames.town.value,
        ], [
            TPT2OptionFilters.type_module.value,
        ], [])

    module_gravel = _LocDetail(246, [
            TPT2RegionNames.town.value,
        ], [
            TPT2OptionFilters.type_module.value,
        ], [])

    module_mjölnir = _LocDetail(247, [
            TPT2RegionNames.town.value,
        ], [
            TPT2OptionFilters.type_module.value,
        ], [])

    module_relay = _LocDetail(248, [
            TPT2RegionNames.town.value,
        ], [
            TPT2OptionFilters.type_module.value,
        ], [])

    module_energy = _LocDetail(249, [
            TPT2RegionNames.town.value,
        ], [
            TPT2OptionFilters.type_module.value,
        ], [])

    module_energyflow = _LocDetail(250, [
            TPT2RegionNames.town.value,
        ], [
            TPT2OptionFilters.type_module.value,
        ], [])

    module_infinityenergy = _LocDetail(251, [
            TPT2RegionNames.town.value,
        ], [
            TPT2OptionFilters.type_module.value,
        ], [])

    module_moonenergy = _LocDetail(252, [
            TPT2RegionNames.town.value,
        ], [
            TPT2OptionFilters.type_module.value,
        ], [])

    module_energyrecycling = _LocDetail(253, [
            TPT2RegionNames.town.value,
        ], [
            TPT2OptionFilters.type_module.value,
        ], [])

    module_energyregeneration = _LocDetail(254, [
            TPT2RegionNames.town.value,
        ], [
            TPT2OptionFilters.type_module.value,
        ], [])

    module_sunenergy = _LocDetail(255, [
            TPT2RegionNames.town.value,
        ], [
            TPT2OptionFilters.type_module.value,
        ], [])

    module_auraenhancement = _LocDetail(256, [
            TPT2RegionNames.town.value,
        ], [
            TPT2OptionFilters.type_module.value,
        ], [])

    module_simpleevasion = _LocDetail(257, [
            TPT2RegionNames.town.value,
        ], [
            TPT2OptionFilters.type_module.value,
        ], [])

    module_airexchange = _LocDetail(258, [
            TPT2RegionNames.town.value,
        ], [
            TPT2OptionFilters.type_module.value,
        ], [])

    module_darknessexchange = _LocDetail(259, [
            TPT2RegionNames.town.value,
        ], [
            TPT2OptionFilters.type_module.value,
        ], [])

    module_earthexchange = _LocDetail(260, [
            TPT2RegionNames.town.value,
        ], [
            TPT2OptionFilters.type_module.value,
        ], [])

    module_electricityexchange = _LocDetail(261, [
            TPT2RegionNames.town.value,
        ], [
            TPT2OptionFilters.type_module.value,
        ], [])

    module_fireexchange = _LocDetail(262, [
            TPT2RegionNames.town.value,
        ], [
            TPT2OptionFilters.type_module.value,
        ], [])

    module_lightexchange = _LocDetail(263, [
            TPT2RegionNames.town.value,
        ], [
            TPT2OptionFilters.type_module.value,
        ], [])

    module_natureexchange = _LocDetail(264, [
            TPT2RegionNames.town.value,
        ], [
            TPT2OptionFilters.type_module.value,
        ], [])

    module_neutralexchange = _LocDetail(265, [
            TPT2RegionNames.town.value,
        ], [
            TPT2OptionFilters.type_module.value,
        ], [])

    module_universalexchange = _LocDetail(266, [
            TPT2RegionNames.town.value,
        ], [
            TPT2OptionFilters.type_module.value,
        ], [])

    module_waterexchange = _LocDetail(267, [
            TPT2RegionNames.town.value,
        ], [
            TPT2OptionFilters.type_module.value,
        ], [])

    module_quantumfading = _LocDetail(268, [
            TPT2RegionNames.town.value,
        ], [
            TPT2OptionFilters.type_module.value,
        ], [])

    module_martyrdom = _LocDetail(269, [
            TPT2RegionNames.town.value,
        ], [
            TPT2OptionFilters.type_module.value,
        ], [])

    module_incineration = _LocDetail(270, [
            TPT2RegionNames.town.value,
        ], [
            TPT2OptionFilters.type_module.value,
        ], [])

    module_airfocus = _LocDetail(271, [
            TPT2RegionNames.town.value,
        ], [
            TPT2OptionFilters.type_module.value,
        ], [])

    module_darknessfocus = _LocDetail(272, [
            TPT2RegionNames.town.value,
        ], [
            TPT2OptionFilters.type_module.value,
        ], [])

    module_earthfocus = _LocDetail(273, [
            TPT2RegionNames.town.value,
        ], [
            TPT2OptionFilters.type_module.value,
        ], [])

    module_electricityfocus = _LocDetail(274, [
            TPT2RegionNames.town.value,
        ], [
            TPT2OptionFilters.type_module.value,
        ], [])

    module_firefocus = _LocDetail(275, [
            TPT2RegionNames.town.value,
        ], [
            TPT2OptionFilters.type_module.value,
        ], [])

    module_lightfocus = _LocDetail(276, [
            TPT2RegionNames.town.value,
        ], [
            TPT2OptionFilters.type_module.value,
        ], [])

    module_naturefocus = _LocDetail(277, [
            TPT2RegionNames.town.value,
        ], [
            TPT2OptionFilters.type_module.value,
        ], [])

    module_neutralfocus = _LocDetail(278, [
            TPT2RegionNames.town.value,
        ], [
            TPT2OptionFilters.type_module.value,
        ], [])

    module_universalfocus = _LocDetail(279, [
            TPT2RegionNames.town.value,
        ], [
            TPT2OptionFilters.type_module.value,
        ], [])

    module_waterfocus = _LocDetail(280, [
            TPT2RegionNames.town.value,
        ], [
            TPT2OptionFilters.type_module.value,
        ], [])

    module_batteryfoundation = _LocDetail(281, [
            TPT2RegionNames.town.value,
        ], [
            TPT2OptionFilters.type_module.value,
        ], [])

    module_diamondfoundation = _LocDetail(282, [
            TPT2RegionNames.town.value,
        ], [
            TPT2OptionFilters.type_module.value,
        ], [])

    module_granitefoundation = _LocDetail(283, [
            TPT2RegionNames.town.value,
        ], [
            TPT2OptionFilters.type_module.value,
        ], [])

    module_infinityfoundation = _LocDetail(284, [
            TPT2RegionNames.town.value,
        ], [
            TPT2OptionFilters.type_module.value,
        ], [])

    module_magmafoundation = _LocDetail(285, [
            TPT2RegionNames.town.value,
        ], [
            TPT2OptionFilters.type_module.value,
        ], [])

    module_marblefoundation = _LocDetail(286, [
            TPT2RegionNames.town.value,
        ], [
            TPT2OptionFilters.type_module.value,
        ], [])

    module_steelfoundation = _LocDetail(287, [
            TPT2RegionNames.town.value,
        ], [
            TPT2OptionFilters.type_module.value,
        ], [])

    module_stonefoundation = _LocDetail(288, [
            TPT2RegionNames.town.value,
        ], [
            TPT2OptionFilters.type_module.value,
        ], [])

    module_beachgift = _LocDetail(289, [
            TPT2RegionNames.town.value,
        ], [
            TPT2OptionFilters.type_module.value,
        ], [])

    module_chaosgift = _LocDetail(290, [
            TPT2RegionNames.town.value,
        ], [
            TPT2OptionFilters.type_module.value,
        ], [])

    module_darkrealmgift = _LocDetail(291, [
            TPT2RegionNames.town.value,
        ], [
            TPT2OptionFilters.type_module.value,
        ], [])

    module_desertgift = _LocDetail(292, [
            TPT2RegionNames.town.value,
        ], [
            TPT2OptionFilters.type_module.value,
        ], [])

    module_forestgift = _LocDetail(293, [
            TPT2RegionNames.town.value,
        ], [
            TPT2OptionFilters.type_module.value,
        ], [])

    module_heavengift = _LocDetail(294, [
            TPT2RegionNames.town.value,
        ], [
            TPT2OptionFilters.type_module.value,
        ], [])

    module_highmountaingift = _LocDetail(295, [
            TPT2RegionNames.town.value,
        ], [
            TPT2OptionFilters.type_module.value,
        ], [])

    module_junglegift = _LocDetail(296, [
            TPT2RegionNames.town.value,
        ], [
            TPT2OptionFilters.type_module.value,
        ], [])

    module_metallicruinsgift = _LocDetail(297, [
            TPT2RegionNames.town.value,
        ], [
            TPT2OptionFilters.type_module.value,
        ], [])

    module_neutralgift = _LocDetail(298, [
            TPT2RegionNames.town.value,
        ], [
            TPT2OptionFilters.type_module.value,
        ], [])

    module_oceangift = _LocDetail(299, [
            TPT2RegionNames.town.value,
        ], [
            TPT2OptionFilters.type_module.value,
        ], [])

    module_undergroundgift = _LocDetail(300, [
            TPT2RegionNames.town.value,
        ], [
            TPT2OptionFilters.type_module.value,
        ], [])

    module_universegift = _LocDetail(301, [
            TPT2RegionNames.town.value,
        ], [
            TPT2OptionFilters.type_module.value,
        ], [])

    module_volcanogift = _LocDetail(302, [
            TPT2RegionNames.town.value,
        ], [
            TPT2OptionFilters.type_module.value,
        ], [])

    module_wintergift = _LocDetail(303, [
            TPT2RegionNames.town.value,
        ], [
            TPT2OptionFilters.type_module.value,
        ], [])

    module_googlesinfluence = _LocDetail(304, [
            TPT2RegionNames.town.value,
        ], [
            TPT2OptionFilters.type_module.value,
        ], [])

    module_grimreaper = _LocDetail(305, [
            TPT2RegionNames.town.value,
        ], [
            TPT2OptionFilters.type_module.value,
        ], [])

    module_spaceguns = _LocDetail(306, [
            TPT2RegionNames.town.value,
        ], [
            TPT2OptionFilters.type_module.value,
        ], [])

    module_bluecatsharmonizer = _LocDetail(307, [
            TPT2RegionNames.town.value,
        ], [
            TPT2OptionFilters.type_module.value,
        ], [])

    module_titaniumhull = _LocDetail(308, [
            TPT2RegionNames.town.value,
        ], [
            TPT2OptionFilters.type_module.value,
        ], [])

    module_gravitationalimpact = _LocDetail(309, [
            TPT2RegionNames.town.value,
        ], [
            TPT2OptionFilters.type_module.value,
        ], [])

    module_airimpetus = _LocDetail(310, [
            TPT2RegionNames.town.value,
        ], [
            TPT2OptionFilters.type_module.value,
        ], [])

    module_darknessimpetus = _LocDetail(311, [
            TPT2RegionNames.town.value,
        ], [
            TPT2OptionFilters.type_module.value,
        ], [])

    module_earthimpetus = _LocDetail(312, [
            TPT2RegionNames.town.value,
        ], [
            TPT2OptionFilters.type_module.value,
        ], [])

    module_electricityimpetus = _LocDetail(313, [
            TPT2RegionNames.town.value,
        ], [
            TPT2OptionFilters.type_module.value,
        ], [])

    module_fireimpetus = _LocDetail(314, [
            TPT2RegionNames.town.value,
        ], [
            TPT2OptionFilters.type_module.value,
        ], [])

    module_lightimpetus = _LocDetail(315, [
            TPT2RegionNames.town.value,
        ], [
            TPT2OptionFilters.type_module.value,
        ], [])

    module_natureimpetus = _LocDetail(316, [
            TPT2RegionNames.town.value,
        ], [
            TPT2OptionFilters.type_module.value,
        ], [])

    module_waterimpetus = _LocDetail(317, [
            TPT2RegionNames.town.value,
        ], [
            TPT2OptionFilters.type_module.value,
        ], [])

    module_quantumspeed = _LocDetail(318, [
            TPT2RegionNames.town.value,
        ], [
            TPT2OptionFilters.type_module.value,
        ], [])

    module_infinityimpetus = _LocDetail(319, [
            TPT2RegionNames.town.value,
        ], [
            TPT2OptionFilters.type_module.value,
        ], [])

    module_infinityrange = _LocDetail(320, [
            TPT2RegionNames.town.value,
        ], [
            TPT2OptionFilters.type_module.value,
        ], [])

    module_infinityreflect = _LocDetail(321, [
            TPT2RegionNames.town.value,
        ], [
            TPT2OptionFilters.type_module.value,
        ], [])

    module_infinitysplash = _LocDetail(322, [
            TPT2RegionNames.town.value,
        ], [
            TPT2OptionFilters.type_module.value,
        ], [])

    module_universalinfinity = _LocDetail(323, [
            TPT2RegionNames.town.value,
        ], [
            TPT2OptionFilters.type_module.value,
        ], [])

    module_knightsboostofpower = _LocDetail(324, [
            TPT2RegionNames.town.value,
        ], [
            TPT2OptionFilters.type_module.value,
        ], [])

    module_tacticalmaneuver = _LocDetail(325, [
            TPT2RegionNames.town.value,
        ], [
            TPT2OptionFilters.type_module.value,
        ], [])

    module_seriousmissile = _LocDetail(326, [
            TPT2RegionNames.town.value,
        ], [
            TPT2OptionFilters.type_module.value,
        ], [])

    module_unholymissile = _LocDetail(327, [
            TPT2RegionNames.town.value,
        ], [
            TPT2OptionFilters.type_module.value,
        ], [])

    module_focusedmultishot = _LocDetail(328, [
            TPT2RegionNames.town.value,
        ], [
            TPT2OptionFilters.type_module.value,
        ], [])

    module_daybloom = _LocDetail(329, [
            TPT2RegionNames.town.value,
        ], [
            TPT2OptionFilters.type_module.value,
        ], [])

    module_growth = _LocDetail(330, [
            TPT2RegionNames.town.value,
        ], [
            TPT2OptionFilters.type_module.value,
        ], [])

    module_photosynthesis = _LocDetail(331, [
            TPT2RegionNames.town.value,
        ], [
            TPT2OptionFilters.type_module.value,
        ], [])

    module_rejuvenate = _LocDetail(332, [
            TPT2RegionNames.town.value,
        ], [
            TPT2OptionFilters.type_module.value,
        ], [])

    module_natureswrath = _LocDetail(333, [
            TPT2RegionNames.town.value,
        ], [
            TPT2OptionFilters.type_module.value,
        ], [])

    module_gnarlyobsidian = _LocDetail(334, [
            TPT2RegionNames.town.value,
        ], [
            TPT2OptionFilters.type_module.value,
        ], [])

    module_headhunting = _LocDetail(335, [
            TPT2RegionNames.town.value,
        ], [
            TPT2OptionFilters.type_module.value,
        ], [])

    module_defenseoverload = _LocDetail(336, [
            TPT2RegionNames.town.value,
        ], [
            TPT2OptionFilters.type_module.value,
        ], [])

    module_gaiasprotection = _LocDetail(337, [
            TPT2RegionNames.town.value,
        ], [
            TPT2OptionFilters.type_module.value,
        ], [])

    module_magicalprotection = _LocDetail(338, [
            TPT2RegionNames.town.value,
        ], [
            TPT2OptionFilters.type_module.value,
        ], [])

    module_montoyaprotocol = _LocDetail(339, [
            TPT2RegionNames.town.value,
        ], [
            TPT2OptionFilters.type_module.value,
        ], [])

    module_shieldrecharger = _LocDetail(340, [
            TPT2RegionNames.town.value,
        ], [
            TPT2OptionFilters.type_module.value,
        ], [])

    module_captainsreflect = _LocDetail(341, [
            TPT2RegionNames.town.value,
        ], [
            TPT2OptionFilters.type_module.value,
        ], [])

    module_wince = _LocDetail(342, [
            TPT2RegionNames.town.value,
        ], [
            TPT2OptionFilters.type_module.value,
        ], [])

    module_basicregeneration = _LocDetail(343, [
            TPT2RegionNames.town.value,
        ], [
            TPT2OptionFilters.type_module.value,
        ], [])

    module_infinityregeneration = _LocDetail(344, [
            TPT2RegionNames.town.value,
        ], [
            TPT2OptionFilters.type_module.value,
        ], [])

    module_adaptiveregeneration = _LocDetail(345, [
            TPT2RegionNames.town.value,
        ], [
            TPT2OptionFilters.type_module.value,
        ], [])

    module_airarmor = _LocDetail(346, [
            TPT2RegionNames.town.value,
        ], [
            TPT2OptionFilters.type_module.value,
        ], [])

    module_darknessarmor = _LocDetail(347, [
            TPT2RegionNames.town.value,
        ], [
            TPT2OptionFilters.type_module.value,
        ], [])

    module_eartharmor = _LocDetail(348, [
            TPT2RegionNames.town.value,
        ], [
            TPT2OptionFilters.type_module.value,
        ], [])

    module_electricityarmor = _LocDetail(349, [
            TPT2RegionNames.town.value,
        ], [
            TPT2OptionFilters.type_module.value,
        ], [])

    module_firearmor = _LocDetail(350, [
            TPT2RegionNames.town.value,
        ], [
            TPT2OptionFilters.type_module.value,
        ], [])

    module_lightarmor = _LocDetail(351, [
            TPT2RegionNames.town.value,
        ], [
            TPT2OptionFilters.type_module.value,
        ], [])

    module_genericarmor = _LocDetail(352, [
            TPT2RegionNames.town.value,
        ], [
            TPT2OptionFilters.type_module.value,
        ], [])

    module_naturearmor = _LocDetail(353, [
            TPT2RegionNames.town.value,
        ], [
            TPT2OptionFilters.type_module.value,
        ], [])

    module_waterarmor = _LocDetail(354, [
            TPT2RegionNames.town.value,
        ], [
            TPT2OptionFilters.type_module.value,
        ], [])

    module_airresistance = _LocDetail(355, [
            TPT2RegionNames.town.value,
        ], [
            TPT2OptionFilters.type_module.value,
        ], [])

    module_darknessresistance = _LocDetail(356, [
            TPT2RegionNames.town.value,
        ], [
            TPT2OptionFilters.type_module.value,
        ], [])

    module_earthresistance = _LocDetail(357, [
            TPT2RegionNames.town.value,
        ], [
            TPT2OptionFilters.type_module.value,
        ], [])

    module_electricityresistance = _LocDetail(358, [
            TPT2RegionNames.town.value,
        ], [
            TPT2OptionFilters.type_module.value,
        ], [])

    module_elementalresistance = _LocDetail(359, [
            TPT2RegionNames.town.value,
        ], [
            TPT2OptionFilters.type_module.value,
        ], [])

    module_fireresistance = _LocDetail(360, [
            TPT2RegionNames.town.value,
        ], [
            TPT2OptionFilters.type_module.value,
        ], [])

    module_genericresistance = _LocDetail(361, [
            TPT2RegionNames.town.value,
        ], [
            TPT2OptionFilters.type_module.value,
        ], [])

    module_lightresistance = _LocDetail(362, [
            TPT2RegionNames.town.value,
        ], [
            TPT2OptionFilters.type_module.value,
        ], [])

    module_natureresistance = _LocDetail(363, [
            TPT2RegionNames.town.value,
        ], [
            TPT2OptionFilters.type_module.value,
        ], [])

    module_neutralresistance = _LocDetail(364, [
            TPT2RegionNames.town.value,
        ], [
            TPT2OptionFilters.type_module.value,
        ], [])

    module_universalresistance = _LocDetail(365, [
            TPT2RegionNames.town.value,
        ], [
            TPT2OptionFilters.type_module.value,
        ], [])

    module_waterresistance = _LocDetail(366, [
            TPT2RegionNames.town.value,
        ], [
            TPT2OptionFilters.type_module.value,
        ], [])

    module_returntomonkey = _LocDetail(367, [
            TPT2RegionNames.town.value,
        ], [
            TPT2OptionFilters.type_module.value,
        ], [])

    module_darksacrifice = _LocDetail(368, [
            TPT2RegionNames.town.value,
        ], [
            TPT2OptionFilters.type_module.value,
        ], [])

    module_violentseeds = _LocDetail(369, [
            TPT2RegionNames.town.value,
        ], [
            TPT2OptionFilters.type_module.value,
        ], [])

    module_iceshards = _LocDetail(370, [
            TPT2RegionNames.town.value,
        ], [
            TPT2OptionFilters.type_module.value,
        ], [])

    module_airshell = _LocDetail(371, [
            TPT2RegionNames.town.value,
        ], [
            TPT2OptionFilters.type_module.value,
        ], [])

    module_darknessshell = _LocDetail(372, [
            TPT2RegionNames.town.value,
        ], [
            TPT2OptionFilters.type_module.value,
        ], [])

    module_earthshell = _LocDetail(373, [
            TPT2RegionNames.town.value,
        ], [
            TPT2OptionFilters.type_module.value,
        ], [])

    module_electricityshell = _LocDetail(374, [
            TPT2RegionNames.town.value,
        ], [
            TPT2OptionFilters.type_module.value,
        ], [])

    module_fireshell = _LocDetail(375, [
            TPT2RegionNames.town.value,
        ], [
            TPT2OptionFilters.type_module.value,
        ], [])

    module_lightshell = _LocDetail(376, [
            TPT2RegionNames.town.value,
        ], [
            TPT2OptionFilters.type_module.value,
        ], [])

    module_natureshell = _LocDetail(377, [
            TPT2RegionNames.town.value,
        ], [
            TPT2OptionFilters.type_module.value,
        ], [])

    module_watershell = _LocDetail(378, [
            TPT2RegionNames.town.value,
        ], [
            TPT2OptionFilters.type_module.value,
        ], [])

    module_advancedshield = _LocDetail(379, [
            TPT2RegionNames.town.value,
        ], [
            TPT2OptionFilters.type_module.value,
        ], [])

    module_shieldofair = _LocDetail(380, [
            TPT2RegionNames.town.value,
        ], [
            TPT2OptionFilters.type_module.value,
        ], [])

    module_shieldamplifier = _LocDetail(381, [
            TPT2RegionNames.town.value,
        ], [
            TPT2OptionFilters.type_module.value,
        ], [])

    module_airprotection = _LocDetail(382, [
            TPT2RegionNames.town.value,
        ], [
            TPT2OptionFilters.type_module.value,
        ], [])

    module_darknessprotection = _LocDetail(383, [
            TPT2RegionNames.town.value,
        ], [
            TPT2OptionFilters.type_module.value,
        ], [])

    module_earthprotection = _LocDetail(384, [
            TPT2RegionNames.town.value,
        ], [
            TPT2OptionFilters.type_module.value,
        ], [])

    module_electricityprotection = _LocDetail(385, [
            TPT2RegionNames.town.value,
        ], [
            TPT2OptionFilters.type_module.value,
        ], [])

    module_fireprotection = _LocDetail(386, [
            TPT2RegionNames.town.value,
        ], [
            TPT2OptionFilters.type_module.value,
        ], [])

    module_lightprotection = _LocDetail(387, [
            TPT2RegionNames.town.value,
        ], [
            TPT2OptionFilters.type_module.value,
        ], [])

    module_natureprotection = _LocDetail(388, [
            TPT2RegionNames.town.value,
        ], [
            TPT2OptionFilters.type_module.value,
        ], [])

    module_waterprotection = _LocDetail(389, [
            TPT2RegionNames.town.value,
        ], [
            TPT2OptionFilters.type_module.value,
        ], [])

    module_basicshield = _LocDetail(390, [
            TPT2RegionNames.town.value,
        ], [
            TPT2OptionFilters.type_module.value,
        ], [])

    module_bossshield = _LocDetail(391, [
            TPT2RegionNames.town.value,
        ], [
            TPT2OptionFilters.type_module.value,
        ], [])

    module_shieldofdarkness = _LocDetail(392, [
            TPT2RegionNames.town.value,
        ], [
            TPT2OptionFilters.type_module.value,
        ], [])

    module_diversshield = _LocDetail(393, [
            TPT2RegionNames.town.value,
        ], [
            TPT2OptionFilters.type_module.value,
        ], [])

    module_divisionshield = _LocDetail(394, [
            TPT2RegionNames.town.value,
        ], [
            TPT2OptionFilters.type_module.value,
        ], [])

    module_shieldoffire = _LocDetail(395, [
            TPT2RegionNames.town.value,
        ], [
            TPT2OptionFilters.type_module.value,
        ], [])

    module_shieldoffrost = _LocDetail(396, [
            TPT2RegionNames.town.value,
        ], [
            TPT2OptionFilters.type_module.value,
        ], [])

    module_immortalityshield = _LocDetail(397, [
            TPT2RegionNames.town.value,
        ], [
            TPT2OptionFilters.type_module.value,
        ], [])

    module_infinityshield = _LocDetail(398, [
            TPT2RegionNames.town.value,
        ], [
            TPT2OptionFilters.type_module.value,
        ], [])

    module_shieldofnature = _LocDetail(399, [
            TPT2RegionNames.town.value,
        ], [
            TPT2OptionFilters.type_module.value,
        ], [])

    module_phasing = _LocDetail(400, [
            TPT2RegionNames.town.value,
        ], [
            TPT2OptionFilters.type_module.value,
        ], [])

    module_transformator = _LocDetail(401, [
            TPT2RegionNames.town.value,
        ], [
            TPT2OptionFilters.type_module.value,
        ], [])

    module_unfolding = _LocDetail(402, [
            TPT2RegionNames.town.value,
        ], [
            TPT2OptionFilters.type_module.value,
        ], [])

    module_universalshield = _LocDetail(403, [
            TPT2RegionNames.town.value,
        ], [
            TPT2OptionFilters.type_module.value,
        ], [])

    module_luckyshot = _LocDetail(404, [
            TPT2RegionNames.town.value,
        ], [
            TPT2OptionFilters.type_module.value,
        ], [])

    module_deepslumber = _LocDetail(405, [
            TPT2RegionNames.town.value,
        ], [
            TPT2OptionFilters.type_module.value,
        ], [])

    module_soulharvesting = _LocDetail(406, [
            TPT2RegionNames.town.value,
        ], [
            TPT2OptionFilters.type_module.value,
        ], [])

    module_advancedheal = _LocDetail(407, [
            TPT2RegionNames.town.value,
        ], [
            TPT2OptionFilters.type_module.value,
        ], [])

    module_rainofashes = _LocDetail(408, [
            TPT2RegionNames.town.value,
        ], [
            TPT2OptionFilters.type_module.value,
        ], [])

    module_awareness = _LocDetail(409, [
            TPT2RegionNames.town.value,
        ], [
            TPT2OptionFilters.type_module.value,
        ], [])

    module_confusionfield = _LocDetail(410, [
            TPT2RegionNames.town.value,
        ], [
            TPT2OptionFilters.type_module.value,
        ], [])

    module_coolingcell = _LocDetail(411, [
            TPT2RegionNames.town.value,
        ], [
            TPT2OptionFilters.type_module.value,
        ], [])

    module_desperado = _LocDetail(412, [
            TPT2RegionNames.town.value,
        ], [
            TPT2OptionFilters.type_module.value,
        ], [])

    module_dispel = _LocDetail(413, [
            TPT2RegionNames.town.value,
        ], [
            TPT2OptionFilters.type_module.value,
        ], [])

    module_losodronesystem = _LocDetail(414, [
            TPT2RegionNames.town.value,
        ], [
            TPT2OptionFilters.type_module.value,
        ], [])

    module_earthquake = _LocDetail(415, [
            TPT2RegionNames.town.value,
        ], [
            TPT2OptionFilters.type_module.value,
        ], [])

    module_firebomb = _LocDetail(416, [
            TPT2RegionNames.town.value,
        ], [
            TPT2OptionFilters.type_module.value,
        ], [])

    module_firestorm = _LocDetail(417, [
            TPT2RegionNames.town.value,
        ], [
            TPT2OptionFilters.type_module.value,
        ], [])

    module_magicalstoneoffloof = _LocDetail(418, [
            TPT2RegionNames.town.value,
        ], [
            TPT2OptionFilters.type_module.value,
        ], [])

    module_fracture = _LocDetail(419, [
            TPT2RegionNames.town.value,
        ], [
            TPT2OptionFilters.type_module.value,
        ], [])

    module_frostnova = _LocDetail(420, [
            TPT2RegionNames.town.value,
        ], [
            TPT2OptionFilters.type_module.value,
        ], [])

    module_glacierspikes = _LocDetail(421, [
            TPT2RegionNames.town.value,
        ], [
            TPT2OptionFilters.type_module.value,
        ], [])

    module_immolation = _LocDetail(422, [
            TPT2RegionNames.town.value,
        ], [
            TPT2OptionFilters.type_module.value,
        ], [])

    module_lifeleech = _LocDetail(423, [
            TPT2RegionNames.town.value,
        ], [
            TPT2OptionFilters.type_module.value,
        ], [])

    module_lightning = _LocDetail(424, [
            TPT2RegionNames.town.value,
        ], [
            TPT2OptionFilters.type_module.value,
        ], [])

    module_supermultishot = _LocDetail(425, [
            TPT2RegionNames.town.value,
        ], [
            TPT2OptionFilters.type_module.value,
        ], [])

    module_magicalorbs = _LocDetail(426, [
            TPT2RegionNames.town.value,
        ], [
            TPT2OptionFilters.type_module.value,
        ], [])

    module_radar = _LocDetail(427, [
            TPT2RegionNames.town.value,
        ], [
            TPT2OptionFilters.type_module.value,
        ], [])

    module_rakscurse = _LocDetail(428, [
            TPT2RegionNames.town.value,
        ], [
            TPT2OptionFilters.type_module.value,
        ], [])

    module_reboot = _LocDetail(429, [
            TPT2RegionNames.town.value,
        ], [
            TPT2OptionFilters.type_module.value,
        ], [])

    module_recharge = _LocDetail(430, [
            TPT2RegionNames.town.value,
        ], [
            TPT2OptionFilters.type_module.value,
        ], [])

    module_redirect = _LocDetail(431, [
            TPT2RegionNames.town.value,
        ], [
            TPT2OptionFilters.type_module.value,
        ], [])

    module_refresh = _LocDetail(432, [
            TPT2RegionNames.town.value,
        ], [
            TPT2OptionFilters.type_module.value,
        ], [])

    module_neutralresponse = _LocDetail(433, [
            TPT2RegionNames.town.value,
        ], [
            TPT2OptionFilters.type_module.value,
        ], [])

    module_sandstorm = _LocDetail(434, [
            TPT2RegionNames.town.value,
        ], [
            TPT2OptionFilters.type_module.value,
        ], [])

    module_shockwave = _LocDetail(435, [
            TPT2RegionNames.town.value,
        ], [
            TPT2OptionFilters.type_module.value,
        ], [])

    module_simpleheal = _LocDetail(436, [
            TPT2RegionNames.town.value,
        ], [
            TPT2OptionFilters.type_module.value,
        ], [])

    module_snapofdestiny = _LocDetail(437, [
            TPT2RegionNames.town.value,
        ], [
            TPT2OptionFilters.type_module.value,
        ], [])

    module_snowstorm = _LocDetail(438, [
            TPT2RegionNames.town.value,
        ], [
            TPT2OptionFilters.type_module.value,
        ], [])

    module_something = _LocDetail(439, [
            TPT2RegionNames.town.value,
        ], [
            TPT2OptionFilters.type_module.value,
        ], [])

    module_superbounce = _LocDetail(440, [
            TPT2RegionNames.town.value,
        ], [
            TPT2OptionFilters.type_module.value,
        ], [])

    module_tideshift = _LocDetail(441, [
            TPT2RegionNames.town.value,
        ], [
            TPT2OptionFilters.type_module.value,
        ], [])

    module_toxicpiranhaivy = _LocDetail(442, [
            TPT2RegionNames.town.value,
        ], [
            TPT2OptionFilters.type_module.value,
        ], [])

    module_tremors = _LocDetail(443, [
            TPT2RegionNames.town.value,
        ], [
            TPT2OptionFilters.type_module.value,
        ], [])

    module_giganticvines = _LocDetail(444, [
            TPT2RegionNames.town.value,
        ], [
            TPT2OptionFilters.type_module.value,
        ], [])

    module_void = _LocDetail(445, [
            TPT2RegionNames.town.value,
        ], [
            TPT2OptionFilters.type_module.value,
        ], [])

    module_shockward = _LocDetail(446, [
            TPT2RegionNames.town.value,
        ], [
            TPT2OptionFilters.type_module.value,
        ], [])

    module_energysphere = _LocDetail(447, [
            TPT2RegionNames.town.value,
        ], [
            TPT2OptionFilters.type_module.value,
        ], [])

    module_advancedsplash = _LocDetail(448, [
            TPT2RegionNames.town.value,
        ], [
            TPT2OptionFilters.type_module.value,
        ], [])

    module_airslice = _LocDetail(449, [
            TPT2RegionNames.town.value,
        ], [
            TPT2OptionFilters.type_module.value,
        ], [])

    module_splash = _LocDetail(450, [
            TPT2RegionNames.town.value,
        ], [
            TPT2OptionFilters.type_module.value,
        ], [])

    module_airsplash = _LocDetail(451, [
            TPT2RegionNames.town.value,
        ], [
            TPT2OptionFilters.type_module.value,
        ], [])

    module_darknesssplash = _LocDetail(452, [
            TPT2RegionNames.town.value,
        ], [
            TPT2OptionFilters.type_module.value,
        ], [])

    module_earthsplash = _LocDetail(453, [
            TPT2RegionNames.town.value,
        ], [
            TPT2OptionFilters.type_module.value,
        ], [])

    module_electricitysplash = _LocDetail(454, [
            TPT2RegionNames.town.value,
        ], [
            TPT2OptionFilters.type_module.value,
        ], [])

    module_firesplash = _LocDetail(455, [
            TPT2RegionNames.town.value,
        ], [
            TPT2OptionFilters.type_module.value,
        ], [])

    module_lightsplash = _LocDetail(456, [
            TPT2RegionNames.town.value,
        ], [
            TPT2OptionFilters.type_module.value,
        ], [])

    module_naturesplash = _LocDetail(457, [
            TPT2RegionNames.town.value,
        ], [
            TPT2OptionFilters.type_module.value,
        ], [])

    module_watersplash = _LocDetail(458, [
            TPT2RegionNames.town.value,
        ], [
            TPT2OptionFilters.type_module.value,
        ], [])

    module_frostsplash = _LocDetail(459, [
            TPT2RegionNames.town.value,
        ], [
            TPT2OptionFilters.type_module.value,
        ], [])

    module_stampede = _LocDetail(460, [
            TPT2RegionNames.town.value,
        ], [
            TPT2OptionFilters.type_module.value,
        ], [])

    module_steinischainedball = _LocDetail(461, [
            TPT2RegionNames.town.value,
        ], [
            TPT2OptionFilters.type_module.value,
        ], [])

    module_poisonsting = _LocDetail(462, [
            TPT2RegionNames.town.value,
        ], [
            TPT2OptionFilters.type_module.value,
        ], [])

    module_streamoflife = _LocDetail(463, [
            TPT2RegionNames.town.value,
        ], [
            TPT2OptionFilters.type_module.value,
        ], [])

    module_plannedstrike = _LocDetail(464, [
            TPT2RegionNames.town.value,
        ], [
            TPT2OptionFilters.type_module.value,
        ], [])

    module_solarstrike = _LocDetail(465, [
            TPT2RegionNames.town.value,
        ], [
            TPT2OptionFilters.type_module.value,
        ], [])

    module_airsubsistence = _LocDetail(466, [
            TPT2RegionNames.town.value,
        ], [
            TPT2OptionFilters.type_module.value,
        ], [])

    module_darknesssubsistence = _LocDetail(467, [
            TPT2RegionNames.town.value,
        ], [
            TPT2OptionFilters.type_module.value,
        ], [])

    module_earthsubsistence = _LocDetail(468, [
            TPT2RegionNames.town.value,
        ], [
            TPT2OptionFilters.type_module.value,
        ], [])

    module_electricitysubsistence = _LocDetail(469, [
            TPT2RegionNames.town.value,
        ], [
            TPT2OptionFilters.type_module.value,
        ], [])

    module_firesubsistence = _LocDetail(470, [
            TPT2RegionNames.town.value,
        ], [
            TPT2OptionFilters.type_module.value,
        ], [])

    module_lightsubsistence = _LocDetail(471, [
            TPT2RegionNames.town.value,
        ], [
            TPT2OptionFilters.type_module.value,
        ], [])

    module_naturesubsistence = _LocDetail(472, [
            TPT2RegionNames.town.value,
        ], [
            TPT2OptionFilters.type_module.value,
        ], [])

    module_watersubsistence = _LocDetail(473, [
            TPT2RegionNames.town.value,
        ], [
            TPT2OptionFilters.type_module.value,
        ], [])

    module_gaiasynergy = _LocDetail(474, [
            TPT2RegionNames.town.value,
        ], [
            TPT2OptionFilters.type_module.value,
        ], [])

    module_omegasynergy = _LocDetail(475, [
            TPT2RegionNames.town.value,
        ], [
            TPT2OptionFilters.type_module.value,
        ], [])

    module_stormsynergy = _LocDetail(476, [
            TPT2RegionNames.town.value,
        ], [
            TPT2OptionFilters.type_module.value,
        ], [])

    module_sunsynergy = _LocDetail(477, [
            TPT2RegionNames.town.value,
        ], [
            TPT2OptionFilters.type_module.value,
        ], [])

    module_voidsynergy = _LocDetail(478, [
            TPT2RegionNames.town.value,
        ], [
            TPT2OptionFilters.type_module.value,
        ], [])

    module_airtaste = _LocDetail(479, [
            TPT2RegionNames.town.value,
        ], [
            TPT2OptionFilters.type_module.value,
        ], [])

    module_darknesstaste = _LocDetail(480, [
            TPT2RegionNames.town.value,
        ], [
            TPT2OptionFilters.type_module.value,
        ], [])

    module_earthtaste = _LocDetail(481, [
            TPT2RegionNames.town.value,
        ], [
            TPT2OptionFilters.type_module.value,
        ], [])

    module_electricitytaste = _LocDetail(482, [
            TPT2RegionNames.town.value,
        ], [
            TPT2OptionFilters.type_module.value,
        ], [])

    module_firetaste = _LocDetail(483, [
            TPT2RegionNames.town.value,
        ], [
            TPT2OptionFilters.type_module.value,
        ], [])

    module_lighttaste = _LocDetail(484, [
            TPT2RegionNames.town.value,
        ], [
            TPT2OptionFilters.type_module.value,
        ], [])

    module_naturetaste = _LocDetail(485, [
            TPT2RegionNames.town.value,
        ], [
            TPT2OptionFilters.type_module.value,
        ], [])

    module_neutraltaste = _LocDetail(486, [
            TPT2RegionNames.town.value,
        ], [
            TPT2OptionFilters.type_module.value,
        ], [])

    module_watertaste = _LocDetail(487, [
            TPT2RegionNames.town.value,
        ], [
            TPT2OptionFilters.type_module.value,
        ], [])

    module_theexecutive = _LocDetail(488, [
            TPT2RegionNames.town.value,
        ], [
            TPT2OptionFilters.type_module.value,
        ], [])

    module_hightide = _LocDetail(489, [
            TPT2RegionNames.town.value,
        ], [
            TPT2OptionFilters.type_module.value,
        ], [])

    module_lowtide = _LocDetail(490, [
            TPT2RegionNames.town.value,
        ], [
            TPT2OptionFilters.type_module.value,
        ], [])

    module_kitstoolkit = _LocDetail(491, [
            TPT2RegionNames.town.value,
        ], [
            TPT2OptionFilters.type_module.value,
        ], [])

    module_absolutezero = _LocDetail(492, [
            TPT2RegionNames.town.value,
        ], [
            TPT2OptionFilters.type_module.value,
        ], [])

    module_supertower = _LocDetail(493, [
            TPT2RegionNames.town.value,
        ], [
            TPT2OptionFilters.type_module.value,
        ], [])

    module_supertower2 = _LocDetail(494, [
            TPT2RegionNames.town.value,
        ], [
            TPT2OptionFilters.type_module.value,
        ], [])

    module_supertower3 = _LocDetail(495, [
            TPT2RegionNames.town.value,
        ], [
            TPT2OptionFilters.type_module.value,
        ], [])

    module_universal = _LocDetail(496, [
            TPT2RegionNames.town.value,
        ], [
            TPT2OptionFilters.type_module.value,
        ], [])

    module_eternalwall = _LocDetail(497, [
            TPT2RegionNames.town.value,
        ], [
            TPT2OptionFilters.type_module.value,
        ], [])

    module_extinguish = _LocDetail(498, [
            TPT2RegionNames.town.value,
        ], [
            TPT2OptionFilters.type_module.value,
        ], [])

    module_xpbonus = _LocDetail(499, [
            TPT2RegionNames.town.value,
        ], [
            TPT2OptionFilters.type_module.value,
        ], [])

    module_symbiotic = _LocDetail(500, [
            TPT2RegionNames.town.value,
        ], [
            TPT2OptionFilters.type_module.value,
        ], [])


# Item Data

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
    rules_generation: list[ROptionFilter]


class TPT2ItemData(Enum):
    filler_doubleresources = _ItemDetail(1, 0, ItemClassification.filler, [])

    module_aquaticabsorption = _ItemDetail(100, 1,
            ItemClassification.progression
        , [
            TPT2OptionFilters.type_module.value,
        ])

    module_hurricane = _ItemDetail(101, 1,
            ItemClassification.progression
        , [
            TPT2OptionFilters.type_module.value,
        ])

    module_neutralamplifier = _ItemDetail(102, 1,
            ItemClassification.progression
        , [
            TPT2OptionFilters.type_module.value,
        ])

    module_refinedarmor = _ItemDetail(103, 1,
            ItemClassification.progression
        , [
            TPT2OptionFilters.type_module.value,
        ])

    module_airattack = _ItemDetail(104, 1,
            ItemClassification.progression
        , [
            TPT2OptionFilters.type_module.value,
        ])

    module_bash = _ItemDetail(105, 1,
            ItemClassification.progression
        , [
            TPT2OptionFilters.type_module.value,
        ])

    module_basicattack = _ItemDetail(106, 1,
            ItemClassification.progression
        , [
            TPT2OptionFilters.type_module.value,
        ])

    module_gaiaspath = _ItemDetail(107, 1,
            ItemClassification.progression
        , [
            TPT2OptionFilters.type_module.value,
        ])

    module_basicbouncing = _ItemDetail(108, 1,
            ItemClassification.progression
        , [
            TPT2OptionFilters.type_module.value,
        ])

    module_phoenixbounce = _ItemDetail(109, 1,
            ItemClassification.progression
        , [
            TPT2OptionFilters.type_module.value,
        ])

    module_burningattack = _ItemDetail(110, 1,
            ItemClassification.progression
        , [
            TPT2OptionFilters.type_module.value,
        ])

    module_combustion = _ItemDetail(111, 1,
            ItemClassification.progression
        , [
            TPT2OptionFilters.type_module.value,
        ])

    module_darknessattack = _ItemDetail(112, 1,
            ItemClassification.progression
        , [
            TPT2OptionFilters.type_module.value,
        ])

    module_deathwish = _ItemDetail(113, 1,
            ItemClassification.progression
        , [
            TPT2OptionFilters.type_module.value,
        ])

    module_earthattack = _ItemDetail(114, 1,
            ItemClassification.progression
        , [
            TPT2OptionFilters.type_module.value,
        ])

    module_electricityattack = _ItemDetail(115, 1,
            ItemClassification.progression
        , [
            TPT2OptionFilters.type_module.value,
        ])

    module_execution = _ItemDetail(116, 1,
            ItemClassification.progression
        , [
            TPT2OptionFilters.type_module.value,
        ])

    module_fireattack = _ItemDetail(117, 1,
            ItemClassification.progression
        , [
            TPT2OptionFilters.type_module.value,
        ])

    module_firebreath = _ItemDetail(118, 1,
            ItemClassification.progression
        , [
            TPT2OptionFilters.type_module.value,
        ])

    module_icebreath = _ItemDetail(119, 1,
            ItemClassification.progression
        , [
            TPT2OptionFilters.type_module.value,
        ])

    module_impetus = _ItemDetail(120, 1,
            ItemClassification.progression
        , [
            TPT2OptionFilters.type_module.value,
        ])

    module_infinityattack = _ItemDetail(121, 1,
            ItemClassification.progression
        , [
            TPT2OptionFilters.type_module.value,
        ])

    module_lifesteal = _ItemDetail(122, 1,
            ItemClassification.progression
        , [
            TPT2OptionFilters.type_module.value,
        ])

    module_lightattack = _ItemDetail(123, 1,
            ItemClassification.progression
        , [
            TPT2OptionFilters.type_module.value,
        ])

    module_multishot = _ItemDetail(124, 1,
            ItemClassification.progression
        , [
            TPT2OptionFilters.type_module.value,
        ])

    module_natureattack = _ItemDetail(125, 1,
            ItemClassification.progression
        , [
            TPT2OptionFilters.type_module.value,
        ])

    module_naturestouch = _ItemDetail(126, 1,
            ItemClassification.progression
        , [
            TPT2OptionFilters.type_module.value,
        ])

    module_rapidfire = _ItemDetail(127, 1,
            ItemClassification.progression
        , [
            TPT2OptionFilters.type_module.value,
        ])

    module_shatter = _ItemDetail(128, 1,
            ItemClassification.progression
        , [
            TPT2OptionFilters.type_module.value,
        ])

    module_sparks = _ItemDetail(129, 1,
            ItemClassification.progression
        , [
            TPT2OptionFilters.type_module.value,
        ])

    module_attackspeed = _ItemDetail(130, 1,
            ItemClassification.progression
        , [
            TPT2OptionFilters.type_module.value,
        ])

    module_universalattack = _ItemDetail(131, 1,
            ItemClassification.progression
        , [
            TPT2OptionFilters.type_module.value,
        ])

    module_waterattack = _ItemDetail(132, 1,
            ItemClassification.progression
        , [
            TPT2OptionFilters.type_module.value,
        ])

    module_checkerboardaura = _ItemDetail(133, 1,
            ItemClassification.progression
        , [
            TPT2OptionFilters.type_module.value,
        ])

    module_deathaura = _ItemDetail(134, 1,
            ItemClassification.progression
        , [
            TPT2OptionFilters.type_module.value,
        ])

    module_drynessaura = _ItemDetail(135, 1,
            ItemClassification.progression
        , [
            TPT2OptionFilters.type_module.value,
        ])

    module_fieryaura = _ItemDetail(136, 1,
            ItemClassification.progression
        , [
            TPT2OptionFilters.type_module.value,
        ])

    module_frostaura = _ItemDetail(137, 1,
            ItemClassification.progression
        , [
            TPT2OptionFilters.type_module.value,
        ])

    module_heartstopperaura = _ItemDetail(138, 1,
            ItemClassification.progression
        , [
            TPT2OptionFilters.type_module.value,
        ])

    module_monsoonaura = _ItemDetail(139, 1,
            ItemClassification.progression
        , [
            TPT2OptionFilters.type_module.value,
        ])

    module_nullifyingaura = _ItemDetail(140, 1,
            ItemClassification.progression
        , [
            TPT2OptionFilters.type_module.value,
        ])

    module_stormaura = _ItemDetail(141, 1,
            ItemClassification.progression
        , [
            TPT2OptionFilters.type_module.value,
        ])

    module_unholyaura = _ItemDetail(142, 1,
            ItemClassification.progression
        , [
            TPT2OptionFilters.type_module.value,
        ])

    module_whirlwindaura = _ItemDetail(143, 1,
            ItemClassification.progression
        , [
            TPT2OptionFilters.type_module.value,
        ])

    module_airbarrier = _ItemDetail(144, 1,
            ItemClassification.progression
        , [
            TPT2OptionFilters.type_module.value,
        ])

    module_darknessbarrier = _ItemDetail(145, 1,
            ItemClassification.progression
        , [
            TPT2OptionFilters.type_module.value,
        ])

    module_earthbarrier = _ItemDetail(146, 1,
            ItemClassification.progression
        , [
            TPT2OptionFilters.type_module.value,
        ])

    module_electricitybarrier = _ItemDetail(147, 1,
            ItemClassification.progression
        , [
            TPT2OptionFilters.type_module.value,
        ])

    module_firebarrier = _ItemDetail(148, 1,
            ItemClassification.progression
        , [
            TPT2OptionFilters.type_module.value,
        ])

    module_lightbarrier = _ItemDetail(149, 1,
            ItemClassification.progression
        , [
            TPT2OptionFilters.type_module.value,
        ])

    module_naturebarrier = _ItemDetail(150, 1,
            ItemClassification.progression
        , [
            TPT2OptionFilters.type_module.value,
        ])

    module_temporalbarrier = _ItemDetail(151, 1,
            ItemClassification.progression
        , [
            TPT2OptionFilters.type_module.value,
        ])

    module_waterbarrier = _ItemDetail(152, 1,
            ItemClassification.progression
        , [
            TPT2OptionFilters.type_module.value,
        ])

    module_divineblessing = _ItemDetail(153, 1,
            ItemClassification.progression
        , [
            TPT2OptionFilters.type_module.value,
        ])

    module_onyxsblessing = _ItemDetail(154, 1,
            ItemClassification.progression
        , [
            TPT2OptionFilters.type_module.value,
        ])

    module_skyblessing = _ItemDetail(155, 1,
            ItemClassification.progression
        , [
            TPT2OptionFilters.type_module.value,
        ])

    module_airblock = _ItemDetail(156, 1,
            ItemClassification.progression
        , [
            TPT2OptionFilters.type_module.value,
        ])

    module_darknessblock = _ItemDetail(157, 1,
            ItemClassification.progression
        , [
            TPT2OptionFilters.type_module.value,
        ])

    module_earthblock = _ItemDetail(158, 1,
            ItemClassification.progression
        , [
            TPT2OptionFilters.type_module.value,
        ])

    module_electricityblock = _ItemDetail(159, 1,
            ItemClassification.progression
        , [
            TPT2OptionFilters.type_module.value,
        ])

    module_fireblock = _ItemDetail(160, 1,
            ItemClassification.progression
        , [
            TPT2OptionFilters.type_module.value,
        ])

    module_lightblock = _ItemDetail(161, 1,
            ItemClassification.progression
        , [
            TPT2OptionFilters.type_module.value,
        ])

    module_natureblock = _ItemDetail(162, 1,
            ItemClassification.progression
        , [
            TPT2OptionFilters.type_module.value,
        ])

    module_neutralblock = _ItemDetail(163, 1,
            ItemClassification.progression
        , [
            TPT2OptionFilters.type_module.value,
        ])

    module_universalblock = _ItemDetail(164, 1,
            ItemClassification.progression
        , [
            TPT2OptionFilters.type_module.value,
        ])

    module_waterblock = _ItemDetail(165, 1,
            ItemClassification.progression
        , [
            TPT2OptionFilters.type_module.value,
        ])

    module_condense = _ItemDetail(166, 1,
            ItemClassification.progression
        , [
            TPT2OptionFilters.type_module.value,
        ])

    module_defensivepack = _ItemDetail(167, 1,
            ItemClassification.progression
        , [
            TPT2OptionFilters.type_module.value,
        ])

    module_offensivepack = _ItemDetail(168, 1,
            ItemClassification.progression
        , [
            TPT2OptionFilters.type_module.value,
        ])

    module_pressurize = _ItemDetail(169, 1,
            ItemClassification.progression
        , [
            TPT2OptionFilters.type_module.value,
        ])

    module_transmute = _ItemDetail(170, 1,
            ItemClassification.progression
        , [
            TPT2OptionFilters.type_module.value,
        ])

    module_waveresources = _ItemDetail(171, 1,
            ItemClassification.progression
        , [
            TPT2OptionFilters.type_module.value,
        ])

    module_antiairprojectiles = _ItemDetail(172, 1,
            ItemClassification.progression
        , [
            TPT2OptionFilters.type_module.value,
        ])

    module_antidarknessprojectiles = _ItemDetail(173, 1,
            ItemClassification.progression
        , [
            TPT2OptionFilters.type_module.value,
        ])

    module_antiearthprojectiles = _ItemDetail(174, 1,
            ItemClassification.progression
        , [
            TPT2OptionFilters.type_module.value,
        ])

    module_antielectricityprojectiles = _ItemDetail(175, 1,
            ItemClassification.progression
        , [
            TPT2OptionFilters.type_module.value,
        ])

    module_antifireprojectiles = _ItemDetail(176, 1,
            ItemClassification.progression
        , [
            TPT2OptionFilters.type_module.value,
        ])

    module_antilightprojectiles = _ItemDetail(177, 1,
            ItemClassification.progression
        , [
            TPT2OptionFilters.type_module.value,
        ])

    module_antinatureprojectiles = _ItemDetail(178, 1,
            ItemClassification.progression
        , [
            TPT2OptionFilters.type_module.value,
        ])

    module_antineutralprojectiles = _ItemDetail(179, 1,
            ItemClassification.progression
        , [
            TPT2OptionFilters.type_module.value,
        ])

    module_shorelineboost = _ItemDetail(180, 1,
            ItemClassification.progression
        , [
            TPT2OptionFilters.type_module.value,
        ])

    module_antiuniversalprojectiles = _ItemDetail(181, 1,
            ItemClassification.progression
        , [
            TPT2OptionFilters.type_module.value,
        ])

    module_antiwaterprojectiles = _ItemDetail(182, 1,
            ItemClassification.progression
        , [
            TPT2OptionFilters.type_module.value,
        ])

    module_borf = _ItemDetail(183, 1,
            ItemClassification.progression
        , [
            TPT2OptionFilters.type_module.value,
        ])

    module_airburst = _ItemDetail(184, 1,
            ItemClassification.progression
        , [
            TPT2OptionFilters.type_module.value,
        ])

    module_darknessburst = _ItemDetail(185, 1,
            ItemClassification.progression
        , [
            TPT2OptionFilters.type_module.value,
        ])

    module_earthburst = _ItemDetail(186, 1,
            ItemClassification.progression
        , [
            TPT2OptionFilters.type_module.value,
        ])

    module_electricityburst = _ItemDetail(187, 1,
            ItemClassification.progression
        , [
            TPT2OptionFilters.type_module.value,
        ])

    module_fireburst = _ItemDetail(188, 1,
            ItemClassification.progression
        , [
            TPT2OptionFilters.type_module.value,
        ])

    module_infinityburst = _ItemDetail(189, 1,
            ItemClassification.progression
        , [
            TPT2OptionFilters.type_module.value,
        ])

    module_lightburst = _ItemDetail(190, 1,
            ItemClassification.progression
        , [
            TPT2OptionFilters.type_module.value,
        ])

    module_natureburst = _ItemDetail(191, 1,
            ItemClassification.progression
        , [
            TPT2OptionFilters.type_module.value,
        ])

    module_neutralburst = _ItemDetail(192, 1,
            ItemClassification.progression
        , [
            TPT2OptionFilters.type_module.value,
        ])

    module_universalburst = _ItemDetail(193, 1,
            ItemClassification.progression
        , [
            TPT2OptionFilters.type_module.value,
        ])

    module_waterburst = _ItemDetail(194, 1,
            ItemClassification.progression
        , [
            TPT2OptionFilters.type_module.value,
        ])

    module_powerofthecat = _ItemDetail(195, 1,
            ItemClassification.progression
        , [
            TPT2OptionFilters.type_module.value,
        ])

    module_unholycloak = _ItemDetail(196, 1,
            ItemClassification.progression
        , [
            TPT2OptionFilters.type_module.value,
        ])

    module_powerconversion = _ItemDetail(197, 1,
            ItemClassification.progression
        , [
            TPT2OptionFilters.type_module.value,
        ])

    module_aerocore = _ItemDetail(198, 1,
            ItemClassification.progression
        , [
            TPT2OptionFilters.type_module.value,
        ])

    module_angeliccore = _ItemDetail(199, 1,
            ItemClassification.progression
        , [
            TPT2OptionFilters.type_module.value,
        ])

    module_magneticcore = _ItemDetail(200, 1,
            ItemClassification.progression
        , [
            TPT2OptionFilters.type_module.value,
        ])

    module_moltencore = _ItemDetail(201, 1,
            ItemClassification.progression
        , [
            TPT2OptionFilters.type_module.value,
        ])

    module_oceancore = _ItemDetail(202, 1,
            ItemClassification.progression
        , [
            TPT2OptionFilters.type_module.value,
        ])

    module_soulcore = _ItemDetail(203, 1,
            ItemClassification.progression
        , [
            TPT2OptionFilters.type_module.value,
        ])

    module_crateofrex = _ItemDetail(204, 1,
            ItemClassification.progression
        , [
            TPT2OptionFilters.type_module.value,
        ])

    module_antiaircrit = _ItemDetail(205, 1,
            ItemClassification.progression
        , [
            TPT2OptionFilters.type_module.value,
        ])

    module_aircrit = _ItemDetail(206, 1,
            ItemClassification.progression
        , [
            TPT2OptionFilters.type_module.value,
        ])

    module_criticalstrike = _ItemDetail(207, 1,
            ItemClassification.progression
        , [
            TPT2OptionFilters.type_module.value,
        ])

    module_antidarknesscrit = _ItemDetail(208, 1,
            ItemClassification.progression
        , [
            TPT2OptionFilters.type_module.value,
        ])

    module_darknesscrit = _ItemDetail(209, 1,
            ItemClassification.progression
        , [
            TPT2OptionFilters.type_module.value,
        ])

    module_antiearthcrit = _ItemDetail(210, 1,
            ItemClassification.progression
        , [
            TPT2OptionFilters.type_module.value,
        ])

    module_earthcrit = _ItemDetail(211, 1,
            ItemClassification.progression
        , [
            TPT2OptionFilters.type_module.value,
        ])

    module_antielectricitycrit = _ItemDetail(212, 1,
            ItemClassification.progression
        , [
            TPT2OptionFilters.type_module.value,
        ])

    module_electricitycrit = _ItemDetail(213, 1,
            ItemClassification.progression
        , [
            TPT2OptionFilters.type_module.value,
        ])

    module_emergencycrit = _ItemDetail(214, 1,
            ItemClassification.progression
        , [
            TPT2OptionFilters.type_module.value,
        ])

    module_antifirecrit = _ItemDetail(215, 1,
            ItemClassification.progression
        , [
            TPT2OptionFilters.type_module.value,
        ])

    module_firecrit = _ItemDetail(216, 1,
            ItemClassification.progression
        , [
            TPT2OptionFilters.type_module.value,
        ])

    module_infinitycrit = _ItemDetail(217, 1,
            ItemClassification.progression
        , [
            TPT2OptionFilters.type_module.value,
        ])

    module_antilightcrit = _ItemDetail(218, 1,
            ItemClassification.progression
        , [
            TPT2OptionFilters.type_module.value,
        ])

    module_lightcrit = _ItemDetail(219, 1,
            ItemClassification.progression
        , [
            TPT2OptionFilters.type_module.value,
        ])

    module_antinaturecrit = _ItemDetail(220, 1,
            ItemClassification.progression
        , [
            TPT2OptionFilters.type_module.value,
        ])

    module_naturecrit = _ItemDetail(221, 1,
            ItemClassification.progression
        , [
            TPT2OptionFilters.type_module.value,
        ])

    module_antineutralcrit = _ItemDetail(222, 1,
            ItemClassification.progression
        , [
            TPT2OptionFilters.type_module.value,
        ])

    module_neutralcrit = _ItemDetail(223, 1,
            ItemClassification.progression
        , [
            TPT2OptionFilters.type_module.value,
        ])

    module_antiuniversalcrit = _ItemDetail(224, 1,
            ItemClassification.progression
        , [
            TPT2OptionFilters.type_module.value,
        ])

    module_universalcrit = _ItemDetail(225, 1,
            ItemClassification.progression
        , [
            TPT2OptionFilters.type_module.value,
        ])

    module_antiwatercrit = _ItemDetail(226, 1,
            ItemClassification.progression
        , [
            TPT2OptionFilters.type_module.value,
        ])

    module_watercrit = _ItemDetail(227, 1,
            ItemClassification.progression
        , [
            TPT2OptionFilters.type_module.value,
        ])

    module_omniversaldamage = _ItemDetail(228, 1,
            ItemClassification.progression
        , [
            TPT2OptionFilters.type_module.value,
        ])

    module_aftershock = _ItemDetail(229, 1,
            ItemClassification.progression
        , [
            TPT2OptionFilters.type_module.value,
        ])

    module_bulletproof = _ItemDetail(230, 1,
            ItemClassification.progression
        , [
            TPT2OptionFilters.type_module.value,
        ])

    module_bulwark = _ItemDetail(231, 1,
            ItemClassification.progression
        , [
            TPT2OptionFilters.type_module.value,
        ])

    module_conductor = _ItemDetail(232, 1,
            ItemClassification.progression
        , [
            TPT2OptionFilters.type_module.value,
        ])

    module_daigoparry = _ItemDetail(233, 1,
            ItemClassification.progression
        , [
            TPT2OptionFilters.type_module.value,
        ])

    module_defiance = _ItemDetail(234, 1,
            ItemClassification.progression
        , [
            TPT2OptionFilters.type_module.value,
        ])

    module_heatwave = _ItemDetail(235, 1,
            ItemClassification.progression
        , [
            TPT2OptionFilters.type_module.value,
        ])

    module_metalplating = _ItemDetail(236, 1,
            ItemClassification.progression
        , [
            TPT2OptionFilters.type_module.value,
        ])

    module_overcharge = _ItemDetail(237, 1,
            ItemClassification.progression
        , [
            TPT2OptionFilters.type_module.value,
        ])

    module_quantumdefense = _ItemDetail(238, 1,
            ItemClassification.progression
        , [
            TPT2OptionFilters.type_module.value,
        ])

    module_reflect = _ItemDetail(239, 1,
            ItemClassification.progression
        , [
            TPT2OptionFilters.type_module.value,
        ])

    module_shelter = _ItemDetail(240, 1,
            ItemClassification.progression
        , [
            TPT2OptionFilters.type_module.value,
        ])

    module_stabprevention = _ItemDetail(241, 1,
            ItemClassification.progression
        , [
            TPT2OptionFilters.type_module.value,
        ])

    module_stoneskin = _ItemDetail(242, 1,
            ItemClassification.progression
        , [
            TPT2OptionFilters.type_module.value,
        ])

    module_strikeback = _ItemDetail(243, 1,
            ItemClassification.progression
        , [
            TPT2OptionFilters.type_module.value,
        ])

    module_diceoffate = _ItemDetail(244, 1,
            ItemClassification.progression
        , [
            TPT2OptionFilters.type_module.value,
        ])

    module_avalanche = _ItemDetail(245, 1,
            ItemClassification.progression
        , [
            TPT2OptionFilters.type_module.value,
        ])

    module_gravel = _ItemDetail(246, 1,
            ItemClassification.progression
        , [
            TPT2OptionFilters.type_module.value,
        ])

    module_mjölnir = _ItemDetail(247, 1,
            ItemClassification.progression
        , [
            TPT2OptionFilters.type_module.value,
        ])

    module_relay = _ItemDetail(248, 1,
            ItemClassification.progression
        , [
            TPT2OptionFilters.type_module.value,
        ])

    module_energy = _ItemDetail(249, 1,
            ItemClassification.progression
        , [
            TPT2OptionFilters.type_module.value,
        ])

    module_energyflow = _ItemDetail(250, 1,
            ItemClassification.progression
        , [
            TPT2OptionFilters.type_module.value,
        ])

    module_infinityenergy = _ItemDetail(251, 1,
            ItemClassification.progression
        , [
            TPT2OptionFilters.type_module.value,
        ])

    module_moonenergy = _ItemDetail(252, 1,
            ItemClassification.progression
        , [
            TPT2OptionFilters.type_module.value,
        ])

    module_energyrecycling = _ItemDetail(253, 1,
            ItemClassification.progression
        , [
            TPT2OptionFilters.type_module.value,
        ])

    module_energyregeneration = _ItemDetail(254, 1,
            ItemClassification.progression
        , [
            TPT2OptionFilters.type_module.value,
        ])

    module_sunenergy = _ItemDetail(255, 1,
            ItemClassification.progression
        , [
            TPT2OptionFilters.type_module.value,
        ])

    module_auraenhancement = _ItemDetail(256, 1,
            ItemClassification.progression
        , [
            TPT2OptionFilters.type_module.value,
        ])

    module_simpleevasion = _ItemDetail(257, 1,
            ItemClassification.progression
        , [
            TPT2OptionFilters.type_module.value,
        ])

    module_airexchange = _ItemDetail(258, 1,
            ItemClassification.progression
        , [
            TPT2OptionFilters.type_module.value,
        ])

    module_darknessexchange = _ItemDetail(259, 1,
            ItemClassification.progression
        , [
            TPT2OptionFilters.type_module.value,
        ])

    module_earthexchange = _ItemDetail(260, 1,
            ItemClassification.progression
        , [
            TPT2OptionFilters.type_module.value,
        ])

    module_electricityexchange = _ItemDetail(261, 1,
            ItemClassification.progression
        , [
            TPT2OptionFilters.type_module.value,
        ])

    module_fireexchange = _ItemDetail(262, 1,
            ItemClassification.progression
        , [
            TPT2OptionFilters.type_module.value,
        ])

    module_lightexchange = _ItemDetail(263, 1,
            ItemClassification.progression
        , [
            TPT2OptionFilters.type_module.value,
        ])

    module_natureexchange = _ItemDetail(264, 1,
            ItemClassification.progression
        , [
            TPT2OptionFilters.type_module.value,
        ])

    module_neutralexchange = _ItemDetail(265, 1,
            ItemClassification.progression
        , [
            TPT2OptionFilters.type_module.value,
        ])

    module_universalexchange = _ItemDetail(266, 1,
            ItemClassification.progression
        , [
            TPT2OptionFilters.type_module.value,
        ])

    module_waterexchange = _ItemDetail(267, 1,
            ItemClassification.progression
        , [
            TPT2OptionFilters.type_module.value,
        ])

    module_quantumfading = _ItemDetail(268, 1,
            ItemClassification.progression
        , [
            TPT2OptionFilters.type_module.value,
        ])

    module_martyrdom = _ItemDetail(269, 1,
            ItemClassification.progression
        , [
            TPT2OptionFilters.type_module.value,
        ])

    module_incineration = _ItemDetail(270, 1,
            ItemClassification.progression
        , [
            TPT2OptionFilters.type_module.value,
        ])

    module_airfocus = _ItemDetail(271, 1,
            ItemClassification.progression
        , [
            TPT2OptionFilters.type_module.value,
        ])

    module_darknessfocus = _ItemDetail(272, 1,
            ItemClassification.progression
        , [
            TPT2OptionFilters.type_module.value,
        ])

    module_earthfocus = _ItemDetail(273, 1,
            ItemClassification.progression
        , [
            TPT2OptionFilters.type_module.value,
        ])

    module_electricityfocus = _ItemDetail(274, 1,
            ItemClassification.progression
        , [
            TPT2OptionFilters.type_module.value,
        ])

    module_firefocus = _ItemDetail(275, 1,
            ItemClassification.progression
        , [
            TPT2OptionFilters.type_module.value,
        ])

    module_lightfocus = _ItemDetail(276, 1,
            ItemClassification.progression
        , [
            TPT2OptionFilters.type_module.value,
        ])

    module_naturefocus = _ItemDetail(277, 1,
            ItemClassification.progression
        , [
            TPT2OptionFilters.type_module.value,
        ])

    module_neutralfocus = _ItemDetail(278, 1,
            ItemClassification.progression
        , [
            TPT2OptionFilters.type_module.value,
        ])

    module_universalfocus = _ItemDetail(279, 1,
            ItemClassification.progression
        , [
            TPT2OptionFilters.type_module.value,
        ])

    module_waterfocus = _ItemDetail(280, 1,
            ItemClassification.progression
        , [
            TPT2OptionFilters.type_module.value,
        ])

    module_batteryfoundation = _ItemDetail(281, 1,
            ItemClassification.progression
        , [
            TPT2OptionFilters.type_module.value,
        ])

    module_diamondfoundation = _ItemDetail(282, 1,
            ItemClassification.progression
        , [
            TPT2OptionFilters.type_module.value,
        ])

    module_granitefoundation = _ItemDetail(283, 1,
            ItemClassification.progression
        , [
            TPT2OptionFilters.type_module.value,
        ])

    module_infinityfoundation = _ItemDetail(284, 1,
            ItemClassification.progression
        , [
            TPT2OptionFilters.type_module.value,
        ])

    module_magmafoundation = _ItemDetail(285, 1,
            ItemClassification.progression
        , [
            TPT2OptionFilters.type_module.value,
        ])

    module_marblefoundation = _ItemDetail(286, 1,
            ItemClassification.progression
        , [
            TPT2OptionFilters.type_module.value,
        ])

    module_steelfoundation = _ItemDetail(287, 1,
            ItemClassification.progression
        , [
            TPT2OptionFilters.type_module.value,
        ])

    module_stonefoundation = _ItemDetail(288, 1,
            ItemClassification.progression
        , [
            TPT2OptionFilters.type_module.value,
        ])

    module_beachgift = _ItemDetail(289, 1,
            ItemClassification.progression
        , [
            TPT2OptionFilters.type_module.value,
        ])

    module_chaosgift = _ItemDetail(290, 1,
            ItemClassification.progression
        , [
            TPT2OptionFilters.type_module.value,
        ])

    module_darkrealmgift = _ItemDetail(291, 1,
            ItemClassification.progression
        , [
            TPT2OptionFilters.type_module.value,
        ])

    module_desertgift = _ItemDetail(292, 1,
            ItemClassification.progression
        , [
            TPT2OptionFilters.type_module.value,
        ])

    module_forestgift = _ItemDetail(293, 1,
            ItemClassification.progression
        , [
            TPT2OptionFilters.type_module.value,
        ])

    module_heavengift = _ItemDetail(294, 1,
            ItemClassification.progression
        , [
            TPT2OptionFilters.type_module.value,
        ])

    module_highmountaingift = _ItemDetail(295, 1,
            ItemClassification.progression
        , [
            TPT2OptionFilters.type_module.value,
        ])

    module_junglegift = _ItemDetail(296, 1,
            ItemClassification.progression
        , [
            TPT2OptionFilters.type_module.value,
        ])

    module_metallicruinsgift = _ItemDetail(297, 1,
            ItemClassification.progression
        , [
            TPT2OptionFilters.type_module.value,
        ])

    module_neutralgift = _ItemDetail(298, 1,
            ItemClassification.progression
        , [
            TPT2OptionFilters.type_module.value,
        ])

    module_oceangift = _ItemDetail(299, 1,
            ItemClassification.progression
        , [
            TPT2OptionFilters.type_module.value,
        ])

    module_undergroundgift = _ItemDetail(300, 1,
            ItemClassification.progression
        , [
            TPT2OptionFilters.type_module.value,
        ])

    module_universegift = _ItemDetail(301, 1,
            ItemClassification.progression
        , [
            TPT2OptionFilters.type_module.value,
        ])

    module_volcanogift = _ItemDetail(302, 1,
            ItemClassification.progression
        , [
            TPT2OptionFilters.type_module.value,
        ])

    module_wintergift = _ItemDetail(303, 1,
            ItemClassification.progression
        , [
            TPT2OptionFilters.type_module.value,
        ])

    module_googlesinfluence = _ItemDetail(304, 1,
            ItemClassification.progression
        , [
            TPT2OptionFilters.type_module.value,
        ])

    module_grimreaper = _ItemDetail(305, 1,
            ItemClassification.progression
        , [
            TPT2OptionFilters.type_module.value,
        ])

    module_spaceguns = _ItemDetail(306, 1,
            ItemClassification.progression
        , [
            TPT2OptionFilters.type_module.value,
        ])

    module_bluecatsharmonizer = _ItemDetail(307, 1,
            ItemClassification.progression
        , [
            TPT2OptionFilters.type_module.value,
        ])

    module_titaniumhull = _ItemDetail(308, 1,
            ItemClassification.progression
        , [
            TPT2OptionFilters.type_module.value,
        ])

    module_gravitationalimpact = _ItemDetail(309, 1,
            ItemClassification.progression
        , [
            TPT2OptionFilters.type_module.value,
        ])

    module_airimpetus = _ItemDetail(310, 1,
            ItemClassification.progression
        , [
            TPT2OptionFilters.type_module.value,
        ])

    module_darknessimpetus = _ItemDetail(311, 1,
            ItemClassification.progression
        , [
            TPT2OptionFilters.type_module.value,
        ])

    module_earthimpetus = _ItemDetail(312, 1,
            ItemClassification.progression
        , [
            TPT2OptionFilters.type_module.value,
        ])

    module_electricityimpetus = _ItemDetail(313, 1,
            ItemClassification.progression
        , [
            TPT2OptionFilters.type_module.value,
        ])

    module_fireimpetus = _ItemDetail(314, 1,
            ItemClassification.progression
        , [
            TPT2OptionFilters.type_module.value,
        ])

    module_lightimpetus = _ItemDetail(315, 1,
            ItemClassification.progression
        , [
            TPT2OptionFilters.type_module.value,
        ])

    module_natureimpetus = _ItemDetail(316, 1,
            ItemClassification.progression
        , [
            TPT2OptionFilters.type_module.value,
        ])

    module_waterimpetus = _ItemDetail(317, 1,
            ItemClassification.progression
        , [
            TPT2OptionFilters.type_module.value,
        ])

    module_quantumspeed = _ItemDetail(318, 1,
            ItemClassification.progression
        , [
            TPT2OptionFilters.type_module.value,
        ])

    module_infinityimpetus = _ItemDetail(319, 1,
            ItemClassification.progression
        , [
            TPT2OptionFilters.type_module.value,
        ])

    module_infinityrange = _ItemDetail(320, 1,
            ItemClassification.progression
        , [
            TPT2OptionFilters.type_module.value,
        ])

    module_infinityreflect = _ItemDetail(321, 1,
            ItemClassification.progression
        , [
            TPT2OptionFilters.type_module.value,
        ])

    module_infinitysplash = _ItemDetail(322, 1,
            ItemClassification.progression
        , [
            TPT2OptionFilters.type_module.value,
        ])

    module_universalinfinity = _ItemDetail(323, 1,
            ItemClassification.progression
        , [
            TPT2OptionFilters.type_module.value,
        ])

    module_knightsboostofpower = _ItemDetail(324, 1,
            ItemClassification.progression
        , [
            TPT2OptionFilters.type_module.value,
        ])

    module_tacticalmaneuver = _ItemDetail(325, 1,
            ItemClassification.progression
        , [
            TPT2OptionFilters.type_module.value,
        ])

    module_seriousmissile = _ItemDetail(326, 1,
            ItemClassification.progression
        , [
            TPT2OptionFilters.type_module.value,
        ])

    module_unholymissile = _ItemDetail(327, 1,
            ItemClassification.progression
        , [
            TPT2OptionFilters.type_module.value,
        ])

    module_focusedmultishot = _ItemDetail(328, 1,
            ItemClassification.progression
        , [
            TPT2OptionFilters.type_module.value,
        ])

    module_daybloom = _ItemDetail(329, 1,
            ItemClassification.progression
        , [
            TPT2OptionFilters.type_module.value,
        ])

    module_growth = _ItemDetail(330, 1,
            ItemClassification.progression
        , [
            TPT2OptionFilters.type_module.value,
        ])

    module_photosynthesis = _ItemDetail(331, 1,
            ItemClassification.progression
        , [
            TPT2OptionFilters.type_module.value,
        ])

    module_rejuvenate = _ItemDetail(332, 1,
            ItemClassification.progression
        , [
            TPT2OptionFilters.type_module.value,
        ])

    module_natureswrath = _ItemDetail(333, 1,
            ItemClassification.progression
        , [
            TPT2OptionFilters.type_module.value,
        ])

    module_gnarlyobsidian = _ItemDetail(334, 1,
            ItemClassification.progression
        , [
            TPT2OptionFilters.type_module.value,
        ])

    module_headhunting = _ItemDetail(335, 1,
            ItemClassification.progression
        , [
            TPT2OptionFilters.type_module.value,
        ])

    module_defenseoverload = _ItemDetail(336, 1,
            ItemClassification.progression
        , [
            TPT2OptionFilters.type_module.value,
        ])

    module_gaiasprotection = _ItemDetail(337, 1,
            ItemClassification.progression
        , [
            TPT2OptionFilters.type_module.value,
        ])

    module_magicalprotection = _ItemDetail(338, 1,
            ItemClassification.progression
        , [
            TPT2OptionFilters.type_module.value,
        ])

    module_montoyaprotocol = _ItemDetail(339, 1,
            ItemClassification.progression
        , [
            TPT2OptionFilters.type_module.value,
        ])

    module_shieldrecharger = _ItemDetail(340, 1,
            ItemClassification.progression
        , [
            TPT2OptionFilters.type_module.value,
        ])

    module_captainsreflect = _ItemDetail(341, 1,
            ItemClassification.progression
        , [
            TPT2OptionFilters.type_module.value,
        ])

    module_wince = _ItemDetail(342, 1,
            ItemClassification.progression
        , [
            TPT2OptionFilters.type_module.value,
        ])

    module_basicregeneration = _ItemDetail(343, 1,
            ItemClassification.progression
        , [
            TPT2OptionFilters.type_module.value,
        ])

    module_infinityregeneration = _ItemDetail(344, 1,
            ItemClassification.progression
        , [
            TPT2OptionFilters.type_module.value,
        ])

    module_adaptiveregeneration = _ItemDetail(345, 1,
            ItemClassification.progression
        , [
            TPT2OptionFilters.type_module.value,
        ])

    module_airarmor = _ItemDetail(346, 1,
            ItemClassification.progression
        , [
            TPT2OptionFilters.type_module.value,
        ])

    module_darknessarmor = _ItemDetail(347, 1,
            ItemClassification.progression
        , [
            TPT2OptionFilters.type_module.value,
        ])

    module_eartharmor = _ItemDetail(348, 1,
            ItemClassification.progression
        , [
            TPT2OptionFilters.type_module.value,
        ])

    module_electricityarmor = _ItemDetail(349, 1,
            ItemClassification.progression
        , [
            TPT2OptionFilters.type_module.value,
        ])

    module_firearmor = _ItemDetail(350, 1,
            ItemClassification.progression
        , [
            TPT2OptionFilters.type_module.value,
        ])

    module_lightarmor = _ItemDetail(351, 1,
            ItemClassification.progression
        , [
            TPT2OptionFilters.type_module.value,
        ])

    module_genericarmor = _ItemDetail(352, 1,
            ItemClassification.progression
        , [
            TPT2OptionFilters.type_module.value,
        ])

    module_naturearmor = _ItemDetail(353, 1,
            ItemClassification.progression
        , [
            TPT2OptionFilters.type_module.value,
        ])

    module_waterarmor = _ItemDetail(354, 1,
            ItemClassification.progression
        , [
            TPT2OptionFilters.type_module.value,
        ])

    module_airresistance = _ItemDetail(355, 1,
            ItemClassification.progression
        , [
            TPT2OptionFilters.type_module.value,
        ])

    module_darknessresistance = _ItemDetail(356, 1,
            ItemClassification.progression
        , [
            TPT2OptionFilters.type_module.value,
        ])

    module_earthresistance = _ItemDetail(357, 1,
            ItemClassification.progression
        , [
            TPT2OptionFilters.type_module.value,
        ])

    module_electricityresistance = _ItemDetail(358, 1,
            ItemClassification.progression
        , [
            TPT2OptionFilters.type_module.value,
        ])

    module_elementalresistance = _ItemDetail(359, 1,
            ItemClassification.progression
        , [
            TPT2OptionFilters.type_module.value,
        ])

    module_fireresistance = _ItemDetail(360, 1,
            ItemClassification.progression
        , [
            TPT2OptionFilters.type_module.value,
        ])

    module_genericresistance = _ItemDetail(361, 1,
            ItemClassification.progression
        , [
            TPT2OptionFilters.type_module.value,
        ])

    module_lightresistance = _ItemDetail(362, 1,
            ItemClassification.progression
        , [
            TPT2OptionFilters.type_module.value,
        ])

    module_natureresistance = _ItemDetail(363, 1,
            ItemClassification.progression
        , [
            TPT2OptionFilters.type_module.value,
        ])

    module_neutralresistance = _ItemDetail(364, 1,
            ItemClassification.progression
        , [
            TPT2OptionFilters.type_module.value,
        ])

    module_universalresistance = _ItemDetail(365, 1,
            ItemClassification.progression
        , [
            TPT2OptionFilters.type_module.value,
        ])

    module_waterresistance = _ItemDetail(366, 1,
            ItemClassification.progression
        , [
            TPT2OptionFilters.type_module.value,
        ])

    module_returntomonkey = _ItemDetail(367, 1,
            ItemClassification.progression
        , [
            TPT2OptionFilters.type_module.value,
        ])

    module_darksacrifice = _ItemDetail(368, 1,
            ItemClassification.progression
        , [
            TPT2OptionFilters.type_module.value,
        ])

    module_violentseeds = _ItemDetail(369, 1,
            ItemClassification.progression
        , [
            TPT2OptionFilters.type_module.value,
        ])

    module_iceshards = _ItemDetail(370, 1,
            ItemClassification.progression
        , [
            TPT2OptionFilters.type_module.value,
        ])

    module_airshell = _ItemDetail(371, 1,
            ItemClassification.progression
        , [
            TPT2OptionFilters.type_module.value,
        ])

    module_darknessshell = _ItemDetail(372, 1,
            ItemClassification.progression
        , [
            TPT2OptionFilters.type_module.value,
        ])

    module_earthshell = _ItemDetail(373, 1,
            ItemClassification.progression
        , [
            TPT2OptionFilters.type_module.value,
        ])

    module_electricityshell = _ItemDetail(374, 1,
            ItemClassification.progression
        , [
            TPT2OptionFilters.type_module.value,
        ])

    module_fireshell = _ItemDetail(375, 1,
            ItemClassification.progression
        , [
            TPT2OptionFilters.type_module.value,
        ])

    module_lightshell = _ItemDetail(376, 1,
            ItemClassification.progression
        , [
            TPT2OptionFilters.type_module.value,
        ])

    module_natureshell = _ItemDetail(377, 1,
            ItemClassification.progression
        , [
            TPT2OptionFilters.type_module.value,
        ])

    module_watershell = _ItemDetail(378, 1,
            ItemClassification.progression
        , [
            TPT2OptionFilters.type_module.value,
        ])

    module_advancedshield = _ItemDetail(379, 1,
            ItemClassification.progression
        , [
            TPT2OptionFilters.type_module.value,
        ])

    module_shieldofair = _ItemDetail(380, 1,
            ItemClassification.progression
        , [
            TPT2OptionFilters.type_module.value,
        ])

    module_shieldamplifier = _ItemDetail(381, 1,
            ItemClassification.progression
        , [
            TPT2OptionFilters.type_module.value,
        ])

    module_airprotection = _ItemDetail(382, 1,
            ItemClassification.progression
        , [
            TPT2OptionFilters.type_module.value,
        ])

    module_darknessprotection = _ItemDetail(383, 1,
            ItemClassification.progression
        , [
            TPT2OptionFilters.type_module.value,
        ])

    module_earthprotection = _ItemDetail(384, 1,
            ItemClassification.progression
        , [
            TPT2OptionFilters.type_module.value,
        ])

    module_electricityprotection = _ItemDetail(385, 1,
            ItemClassification.progression
        , [
            TPT2OptionFilters.type_module.value,
        ])

    module_fireprotection = _ItemDetail(386, 1,
            ItemClassification.progression
        , [
            TPT2OptionFilters.type_module.value,
        ])

    module_lightprotection = _ItemDetail(387, 1,
            ItemClassification.progression
        , [
            TPT2OptionFilters.type_module.value,
        ])

    module_natureprotection = _ItemDetail(388, 1,
            ItemClassification.progression
        , [
            TPT2OptionFilters.type_module.value,
        ])

    module_waterprotection = _ItemDetail(389, 1,
            ItemClassification.progression
        , [
            TPT2OptionFilters.type_module.value,
        ])

    module_basicshield = _ItemDetail(390, 1,
            ItemClassification.progression
        , [
            TPT2OptionFilters.type_module.value,
        ])

    module_bossshield = _ItemDetail(391, 1,
            ItemClassification.progression
        , [
            TPT2OptionFilters.type_module.value,
        ])

    module_shieldofdarkness = _ItemDetail(392, 1,
            ItemClassification.progression
        , [
            TPT2OptionFilters.type_module.value,
        ])

    module_diversshield = _ItemDetail(393, 1,
            ItemClassification.progression
        , [
            TPT2OptionFilters.type_module.value,
        ])

    module_divisionshield = _ItemDetail(394, 1,
            ItemClassification.progression
        , [
            TPT2OptionFilters.type_module.value,
        ])

    module_shieldoffire = _ItemDetail(395, 1,
            ItemClassification.progression
        , [
            TPT2OptionFilters.type_module.value,
        ])

    module_shieldoffrost = _ItemDetail(396, 1,
            ItemClassification.progression
        , [
            TPT2OptionFilters.type_module.value,
        ])

    module_immortalityshield = _ItemDetail(397, 1,
            ItemClassification.progression
        , [
            TPT2OptionFilters.type_module.value,
        ])

    module_infinityshield = _ItemDetail(398, 1,
            ItemClassification.progression
        , [
            TPT2OptionFilters.type_module.value,
        ])

    module_shieldofnature = _ItemDetail(399, 1,
            ItemClassification.progression
        , [
            TPT2OptionFilters.type_module.value,
        ])

    module_phasing = _ItemDetail(400, 1,
            ItemClassification.progression
        , [
            TPT2OptionFilters.type_module.value,
        ])

    module_transformator = _ItemDetail(401, 1,
            ItemClassification.progression
        , [
            TPT2OptionFilters.type_module.value,
        ])

    module_unfolding = _ItemDetail(402, 1,
            ItemClassification.progression
        , [
            TPT2OptionFilters.type_module.value,
        ])

    module_universalshield = _ItemDetail(403, 1,
            ItemClassification.progression
        , [
            TPT2OptionFilters.type_module.value,
        ])

    module_luckyshot = _ItemDetail(404, 1,
            ItemClassification.progression
        , [
            TPT2OptionFilters.type_module.value,
        ])

    module_deepslumber = _ItemDetail(405, 1,
            ItemClassification.progression
        , [
            TPT2OptionFilters.type_module.value,
        ])

    module_soulharvesting = _ItemDetail(406, 1,
            ItemClassification.progression
        , [
            TPT2OptionFilters.type_module.value,
        ])

    module_advancedheal = _ItemDetail(407, 1,
            ItemClassification.progression
        , [
            TPT2OptionFilters.type_module.value,
        ])

    module_rainofashes = _ItemDetail(408, 1,
            ItemClassification.progression
        , [
            TPT2OptionFilters.type_module.value,
        ])

    module_awareness = _ItemDetail(409, 1,
            ItemClassification.progression
        , [
            TPT2OptionFilters.type_module.value,
        ])

    module_confusionfield = _ItemDetail(410, 1,
            ItemClassification.progression
        , [
            TPT2OptionFilters.type_module.value,
        ])

    module_coolingcell = _ItemDetail(411, 1,
            ItemClassification.progression
        , [
            TPT2OptionFilters.type_module.value,
        ])

    module_desperado = _ItemDetail(412, 1,
            ItemClassification.progression
        , [
            TPT2OptionFilters.type_module.value,
        ])

    module_dispel = _ItemDetail(413, 1,
            ItemClassification.progression
        , [
            TPT2OptionFilters.type_module.value,
        ])

    module_losodronesystem = _ItemDetail(414, 1,
            ItemClassification.progression
        , [
            TPT2OptionFilters.type_module.value,
        ])

    module_earthquake = _ItemDetail(415, 1,
            ItemClassification.progression
        , [
            TPT2OptionFilters.type_module.value,
        ])

    module_firebomb = _ItemDetail(416, 1,
            ItemClassification.progression
        , [
            TPT2OptionFilters.type_module.value,
        ])

    module_firestorm = _ItemDetail(417, 1,
            ItemClassification.progression
        , [
            TPT2OptionFilters.type_module.value,
        ])

    module_magicalstoneoffloof = _ItemDetail(418, 1,
            ItemClassification.progression
        , [
            TPT2OptionFilters.type_module.value,
        ])

    module_fracture = _ItemDetail(419, 1,
            ItemClassification.progression
        , [
            TPT2OptionFilters.type_module.value,
        ])

    module_frostnova = _ItemDetail(420, 1,
            ItemClassification.progression
        , [
            TPT2OptionFilters.type_module.value,
        ])

    module_glacierspikes = _ItemDetail(421, 1,
            ItemClassification.progression
        , [
            TPT2OptionFilters.type_module.value,
        ])

    module_immolation = _ItemDetail(422, 1,
            ItemClassification.progression
        , [
            TPT2OptionFilters.type_module.value,
        ])

    module_lifeleech = _ItemDetail(423, 1,
            ItemClassification.progression
        , [
            TPT2OptionFilters.type_module.value,
        ])

    module_lightning = _ItemDetail(424, 1,
            ItemClassification.progression
        , [
            TPT2OptionFilters.type_module.value,
        ])

    module_supermultishot = _ItemDetail(425, 1,
            ItemClassification.progression
        , [
            TPT2OptionFilters.type_module.value,
        ])

    module_magicalorbs = _ItemDetail(426, 1,
            ItemClassification.progression
        , [
            TPT2OptionFilters.type_module.value,
        ])

    module_radar = _ItemDetail(427, 1,
            ItemClassification.progression
        , [
            TPT2OptionFilters.type_module.value,
        ])

    module_rakscurse = _ItemDetail(428, 1,
            ItemClassification.progression
        , [
            TPT2OptionFilters.type_module.value,
        ])

    module_reboot = _ItemDetail(429, 1,
            ItemClassification.progression
        , [
            TPT2OptionFilters.type_module.value,
        ])

    module_recharge = _ItemDetail(430, 1,
            ItemClassification.progression
        , [
            TPT2OptionFilters.type_module.value,
        ])

    module_redirect = _ItemDetail(431, 1,
            ItemClassification.progression
        , [
            TPT2OptionFilters.type_module.value,
        ])

    module_refresh = _ItemDetail(432, 1,
            ItemClassification.progression
        , [
            TPT2OptionFilters.type_module.value,
        ])

    module_neutralresponse = _ItemDetail(433, 1,
            ItemClassification.progression
        , [
            TPT2OptionFilters.type_module.value,
        ])

    module_sandstorm = _ItemDetail(434, 1,
            ItemClassification.progression
        , [
            TPT2OptionFilters.type_module.value,
        ])

    module_shockwave = _ItemDetail(435, 1,
            ItemClassification.progression
        , [
            TPT2OptionFilters.type_module.value,
        ])

    module_simpleheal = _ItemDetail(436, 1,
            ItemClassification.progression
        , [
            TPT2OptionFilters.type_module.value,
        ])

    module_snapofdestiny = _ItemDetail(437, 1,
            ItemClassification.progression
        , [
            TPT2OptionFilters.type_module.value,
        ])

    module_snowstorm = _ItemDetail(438, 1,
            ItemClassification.progression
        , [
            TPT2OptionFilters.type_module.value,
        ])

    module_something = _ItemDetail(439, 1,
            ItemClassification.progression
        , [
            TPT2OptionFilters.type_module.value,
        ])

    module_superbounce = _ItemDetail(440, 1,
            ItemClassification.progression
        , [
            TPT2OptionFilters.type_module.value,
        ])

    module_tideshift = _ItemDetail(441, 1,
            ItemClassification.progression
        , [
            TPT2OptionFilters.type_module.value,
        ])

    module_toxicpiranhaivy = _ItemDetail(442, 1,
            ItemClassification.progression
        , [
            TPT2OptionFilters.type_module.value,
        ])

    module_tremors = _ItemDetail(443, 1,
            ItemClassification.progression
        , [
            TPT2OptionFilters.type_module.value,
        ])

    module_giganticvines = _ItemDetail(444, 1,
            ItemClassification.progression
        , [
            TPT2OptionFilters.type_module.value,
        ])

    module_void = _ItemDetail(445, 1,
            ItemClassification.progression
        , [
            TPT2OptionFilters.type_module.value,
        ])

    module_shockward = _ItemDetail(446, 1,
            ItemClassification.progression
        , [
            TPT2OptionFilters.type_module.value,
        ])

    module_energysphere = _ItemDetail(447, 1,
            ItemClassification.progression
        , [
            TPT2OptionFilters.type_module.value,
        ])

    module_advancedsplash = _ItemDetail(448, 1,
            ItemClassification.progression
        , [
            TPT2OptionFilters.type_module.value,
        ])

    module_airslice = _ItemDetail(449, 1,
            ItemClassification.progression
        , [
            TPT2OptionFilters.type_module.value,
        ])

    module_splash = _ItemDetail(450, 1,
            ItemClassification.progression
        , [
            TPT2OptionFilters.type_module.value,
        ])

    module_airsplash = _ItemDetail(451, 1,
            ItemClassification.progression
        , [
            TPT2OptionFilters.type_module.value,
        ])

    module_darknesssplash = _ItemDetail(452, 1,
            ItemClassification.progression
        , [
            TPT2OptionFilters.type_module.value,
        ])

    module_earthsplash = _ItemDetail(453, 1,
            ItemClassification.progression
        , [
            TPT2OptionFilters.type_module.value,
        ])

    module_electricitysplash = _ItemDetail(454, 1,
            ItemClassification.progression
        , [
            TPT2OptionFilters.type_module.value,
        ])

    module_firesplash = _ItemDetail(455, 1,
            ItemClassification.progression
        , [
            TPT2OptionFilters.type_module.value,
        ])

    module_lightsplash = _ItemDetail(456, 1,
            ItemClassification.progression
        , [
            TPT2OptionFilters.type_module.value,
        ])

    module_naturesplash = _ItemDetail(457, 1,
            ItemClassification.progression
        , [
            TPT2OptionFilters.type_module.value,
        ])

    module_watersplash = _ItemDetail(458, 1,
            ItemClassification.progression
        , [
            TPT2OptionFilters.type_module.value,
        ])

    module_frostsplash = _ItemDetail(459, 1,
            ItemClassification.progression
        , [
            TPT2OptionFilters.type_module.value,
        ])

    module_stampede = _ItemDetail(460, 1,
            ItemClassification.progression
        , [
            TPT2OptionFilters.type_module.value,
        ])

    module_steinischainedball = _ItemDetail(461, 1,
            ItemClassification.progression
        , [
            TPT2OptionFilters.type_module.value,
        ])

    module_poisonsting = _ItemDetail(462, 1,
            ItemClassification.progression
        , [
            TPT2OptionFilters.type_module.value,
        ])

    module_streamoflife = _ItemDetail(463, 1,
            ItemClassification.progression
        , [
            TPT2OptionFilters.type_module.value,
        ])

    module_plannedstrike = _ItemDetail(464, 1,
            ItemClassification.progression
        , [
            TPT2OptionFilters.type_module.value,
        ])

    module_solarstrike = _ItemDetail(465, 1,
            ItemClassification.progression
        , [
            TPT2OptionFilters.type_module.value,
        ])

    module_airsubsistence = _ItemDetail(466, 1,
            ItemClassification.progression
        , [
            TPT2OptionFilters.type_module.value,
        ])

    module_darknesssubsistence = _ItemDetail(467, 1,
            ItemClassification.progression
        , [
            TPT2OptionFilters.type_module.value,
        ])

    module_earthsubsistence = _ItemDetail(468, 1,
            ItemClassification.progression
        , [
            TPT2OptionFilters.type_module.value,
        ])

    module_electricitysubsistence = _ItemDetail(469, 1,
            ItemClassification.progression
        , [
            TPT2OptionFilters.type_module.value,
        ])

    module_firesubsistence = _ItemDetail(470, 1,
            ItemClassification.progression
        , [
            TPT2OptionFilters.type_module.value,
        ])

    module_lightsubsistence = _ItemDetail(471, 1,
            ItemClassification.progression
        , [
            TPT2OptionFilters.type_module.value,
        ])

    module_naturesubsistence = _ItemDetail(472, 1,
            ItemClassification.progression
        , [
            TPT2OptionFilters.type_module.value,
        ])

    module_watersubsistence = _ItemDetail(473, 1,
            ItemClassification.progression
        , [
            TPT2OptionFilters.type_module.value,
        ])

    module_gaiasynergy = _ItemDetail(474, 1,
            ItemClassification.progression
        , [
            TPT2OptionFilters.type_module.value,
        ])

    module_omegasynergy = _ItemDetail(475, 1,
            ItemClassification.progression
        , [
            TPT2OptionFilters.type_module.value,
        ])

    module_stormsynergy = _ItemDetail(476, 1,
            ItemClassification.progression
        , [
            TPT2OptionFilters.type_module.value,
        ])

    module_sunsynergy = _ItemDetail(477, 1,
            ItemClassification.progression
        , [
            TPT2OptionFilters.type_module.value,
        ])

    module_voidsynergy = _ItemDetail(478, 1,
            ItemClassification.progression
        , [
            TPT2OptionFilters.type_module.value,
        ])

    module_airtaste = _ItemDetail(479, 1,
            ItemClassification.progression
        , [
            TPT2OptionFilters.type_module.value,
        ])

    module_darknesstaste = _ItemDetail(480, 1,
            ItemClassification.progression
        , [
            TPT2OptionFilters.type_module.value,
        ])

    module_earthtaste = _ItemDetail(481, 1,
            ItemClassification.progression
        , [
            TPT2OptionFilters.type_module.value,
        ])

    module_electricitytaste = _ItemDetail(482, 1,
            ItemClassification.progression
        , [
            TPT2OptionFilters.type_module.value,
        ])

    module_firetaste = _ItemDetail(483, 1,
            ItemClassification.progression
        , [
            TPT2OptionFilters.type_module.value,
        ])

    module_lighttaste = _ItemDetail(484, 1,
            ItemClassification.progression
        , [
            TPT2OptionFilters.type_module.value,
        ])

    module_naturetaste = _ItemDetail(485, 1,
            ItemClassification.progression
        , [
            TPT2OptionFilters.type_module.value,
        ])

    module_neutraltaste = _ItemDetail(486, 1,
            ItemClassification.progression
        , [
            TPT2OptionFilters.type_module.value,
        ])

    module_watertaste = _ItemDetail(487, 1,
            ItemClassification.progression
        , [
            TPT2OptionFilters.type_module.value,
        ])

    module_theexecutive = _ItemDetail(488, 1,
            ItemClassification.progression
        , [
            TPT2OptionFilters.type_module.value,
        ])

    module_hightide = _ItemDetail(489, 1,
            ItemClassification.progression
        , [
            TPT2OptionFilters.type_module.value,
        ])

    module_lowtide = _ItemDetail(490, 1,
            ItemClassification.progression
        , [
            TPT2OptionFilters.type_module.value,
        ])

    module_kitstoolkit = _ItemDetail(491, 1,
            ItemClassification.progression
        , [
            TPT2OptionFilters.type_module.value,
        ])

    module_absolutezero = _ItemDetail(492, 1,
            ItemClassification.progression
        , [
            TPT2OptionFilters.type_module.value,
        ])

    module_supertower = _ItemDetail(493, 1,
            ItemClassification.progression
        , [
            TPT2OptionFilters.type_module.value,
        ])

    module_supertower2 = _ItemDetail(494, 1,
            ItemClassification.progression
        , [
            TPT2OptionFilters.type_module.value,
        ])

    module_supertower3 = _ItemDetail(495, 1,
            ItemClassification.progression
        , [
            TPT2OptionFilters.type_module.value,
        ])

    module_universal = _ItemDetail(496, 1,
            ItemClassification.progression
        , [
            TPT2OptionFilters.type_module.value,
        ])

    module_eternalwall = _ItemDetail(497, 1,
            ItemClassification.progression
        , [
            TPT2OptionFilters.type_module.value,
        ])

    module_extinguish = _ItemDetail(498, 1,
            ItemClassification.progression
        , [
            TPT2OptionFilters.type_module.value,
        ])

    module_xpbonus = _ItemDetail(499, 1,
            ItemClassification.progression
        , [
            TPT2OptionFilters.type_module.value,
        ])

    module_symbiotic = _ItemDetail(500, 1,
            ItemClassification.progression
        , [
            TPT2OptionFilters.type_module.value,
        ])


DEFAULT_ITEM_CLASSIFICATIONS = {TPT2ItemNames[item.name].value: item.value.types for item in TPT2ItemData}
ITEM_NAME_TO_ID = {TPT2ItemNames[item.name].value: item.value.item_id for item in TPT2ItemData}