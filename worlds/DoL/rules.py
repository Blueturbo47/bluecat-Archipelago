from __future__ import annotations

from typing import TYPE_CHECKING
from enum import Enum
from rule_builder.options import OptionFilter
from rule_builder.rules import Has, HasAll, Rule, FieldResolver
from .options import * # TODO: replace this with nonstar and make an enum or something

if TYPE_CHECKING:
    from .world import DoLWorld

# TODO: fill out rules
class DoLRules(Enum):
    skulduggery_1 = Has("Progressive Skulduggery Rank", 1) # F+ 
    skulduggery_2 = Has("Progressive Skulduggery Rank", 2) # D
    skulduggery_3 = Has("Progressive Skulduggery Rank", 3) # D+
    skulduggery_4 = Has("Progressive Skulduggery Rank", 4) # C
    skulduggery_5 = Has("Progressive Skulduggery Rank", 5) # C+
    skulduggery_6 = Has("Progressive Skulduggery Rank", 6) # B
    skulduggery_7 = Has("Progressive Skulduggery Rank", 7) # B+
    skulduggery_8 = Has("Progressive Skulduggery Rank", 8) # A
    skulduggery_9 = Has("Progressive Skulduggery Rank", 9) # A+
    skulduggery_10 = Has("Progressive Skulduggery Rank", 10) # S

    dancing_1 = Has("Progressive Dancing Rank", 1) # F+
    dancing_2 = Has("Progressive Dancing Rank", 2) # D
    dancing_3 = Has("Progressive Dancing Rank", 3) # D+
    dancing_4 = Has("Progressive Dancing Rank", 4) # C
    dancing_5 = Has("Progressive Dancing Rank", 5) # C+
    dancing_6 = Has("Progressive Dancing Rank", 6) # B
    dancing_7 = Has("Progressive Dancing Rank", 7) # B+
    dancing_8 = Has("Progressive Dancing Rank", 8) # A
    dancing_9 = Has("Progressive Dancing Rank", 9) # A+
    dancing_10 = Has("Progressive Dancing Rank", 10) # S

    swimming_1 = Has("Progressive Swimming Rank", 1) # F+
    swimming_2 = Has("Progressive Swimming Rank", 2) # D
    swimming_3 = Has("Progressive Swimming Rank", 3) # D+
    swimming_4 = Has("Progressive Swimming Rank", 4) # C
    swimming_5 = Has("Progressive Swimming Rank", 5) # C+
    swimming_6 = Has("Progressive Swimming Rank", 6) # B
    swimming_7 = Has("Progressive Swimming Rank", 7) # B+
    swimming_8 = Has("Progressive Swimming Rank", 8) # A
    swimming_9 = Has("Progressive Swimming Rank", 9) # A+
    swimming_10 = Has("Progressive Swimming Rank", 10) # S

    athletics_1 = Has("Progressive Athletics Rank", 1) # F+
    athletics_2 = Has("Progressive Athletics Rank", 2) # D
    athletics_3 = Has("Progressive Athletics Rank", 3) # D+
    athletics_4 = Has("Progressive Athletics Rank", 4) # C
    athletics_5 = Has("Progressive Athletics Rank", 5) # C+
    athletics_6 = Has("Progressive Athletics Rank", 6) # B
    athletics_7 = Has("Progressive Athletics Rank", 7) # B+
    athletics_8 = Has("Progressive Athletics Rank", 8) # A
    athletics_9 = Has("Progressive Athletics Rank", 9) # A+
    athletics_10 = Has("Progressive Athletics Rank", 10) # S

    tending_1 = Has("Progressive Tending Rank", 1) # F+
    tending_2 = Has("Progressive Tending Rank", 2) # D
    tending_3 = Has("Progressive Tending Rank", 3) # D+
    tending_4 = Has("Progressive Tending Rank", 4) # C
    tending_5 = Has("Progressive Tending Rank", 5) # C+
    tending_6 = Has("Progressive Tending Rank", 6) # B
    tending_7 = Has("Progressive Tending Rank", 7) # B+
    tending_8 = Has("Progressive Tending Rank", 8) # A
    tending_9 = Has("Progressive Tending Rank", 9) # A+
    tending_10 = Has("Progressive Tending Rank", 10) # S

    housekeeping_1 = Has("Progressive Housekeeping Rank", 1) # F+
    housekeeping_2 = Has("Progressive Housekeeping Rank", 2) # D
    housekeeping_3 = Has("Progressive Housekeeping Rank", 3) # D+
    housekeeping_4 = Has("Progressive Housekeeping Rank", 4) # C
    housekeeping_5 = Has("Progressive Housekeeping Rank", 5) # C+
    housekeeping_6 = Has("Progressive Housekeeping Rank", 6) # B
    housekeeping_7 = Has("Progressive Housekeeping Rank", 7) # B+
    housekeeping_8 = Has("Progressive Housekeeping Rank", 8) # A
    housekeeping_9 = Has("Progressive Housekeeping Rank", 9) # A+
    housekeeping_10 = Has("Progressive Housekeeping Rank", 10) # S

    seduction_1 = Has("Progressive Seduction Rank", 1) # D
    seduction_2 = Has("Progressive Seduction Rank", 2) # C
    seduction_3 = Has("Progressive Seduction Rank", 3) # B
    seduction_4 = Has("Progressive Seduction Rank", 4) # A
    seduction_5 = Has("Progressive Seduction Rank", 5) # S

    oral_1 = Has("Progressive Oral Rank", 1) # D
    oral_2 = Has("Progressive Oral Rank", 2) # C
    oral_3 = Has("Progressive Oral Rank", 3) # B
    oral_4 = Has("Progressive Oral Rank", 4) # A
    oral_5 = Has("Progressive Oral Rank", 5) # S

    chest_1 = Has("Progressive Chest Rank", 1) # D
    chest_2 = Has("Progressive Chest Rank", 2) # C
    chest_3 = Has("Progressive Chest Rank", 3) # B
    chest_4 = Has("Progressive Chest Rank", 4) # A
    chest_5 = Has("Progressive Chest Rank", 5) # S

    hands_1 = Has("Progressive Hands Rank", 1) # D
    hands_2 = Has("Progressive Hands Rank", 2) # C
    hands_3 = Has("Progressive Hands Rank", 3) # B
    hands_4 = Has("Progressive Hands Rank", 4) # A
    hands_5 = Has("Progressive Hands Rank", 5) # S

    buttocks_1 = Has("Progressive Buttocks Rank", 1) # D
    buttocks_2 = Has("Progressive Buttocks Rank", 2) # C
    buttocks_3 = Has("Progressive Buttocks Rank", 3) # B
    buttocks_4 = Has("Progressive Buttocks Rank", 4) # A
    buttocks_5 = Has("Progressive Buttocks Rank", 5) # S

    privates_1 = Has("Progressive Penile/Vaginal Rank", 1) # D
    privates_2 = Has("Progressive Penile/Vaginal Rank", 2) # C
    privates_3 = Has("Progressive Penile/Vaginal Rank", 3) # B
    privates_4 = Has("Progressive Penile/Vaginal Rank", 4) # A
    privates_5 = Has("Progressive Penile/Vaginal Rank", 5) # S

    anal_1 = Has("Progressive Anal Rank", 1) # D
    anal_2 = Has("Progressive Anal Rank", 2) # C
    anal_3 = Has("Progressive Anal Rank", 3) # B
    anal_4 = Has("Progressive Anal Rank", 4) # A
    anal_5 = Has("Progressive Anal Rank", 5) # S

    thighs_1 = Has("Progressive Thighs Rank", 1) # D
    thighs_2 = Has("Progressive Thighs Rank", 2) # C
    thighs_3 = Has("Progressive Thighs Rank", 3) # B
    thighs_4 = Has("Progressive Thighs Rank", 4) # A
    thighs_5 = Has("Progressive Thighs Rank", 5) # S

    feet_1 = Has("Progressive Feet Rank", 1) # D
    feet_2 = Has("Progressive Feet Rank", 2) # C
    feet_3 = Has("Progressive Feet Rank", 3) # B
    feet_4 = Has("Progressive Feet Rank", 4) # A
    feet_5 = Has("Progressive Feet Rank", 5) # S

    science_1 = Has("Progressive Science Rank", 1) # D : 0
    science_1 = Has("Progressive Science Rank", 2) # C : 1
    science_1 = Has("Progressive Science Rank", 3) # B : 2
    science_1 = Has("Progressive Science Rank", 4) # A : 3
    science_1 = Has("Progressive Science Rank", 5) # A* : 4

    math_1 = Has("Progressive Math Rank", 1) # D : 0
    math_2 = Has("Progressive Math Rank", 2) # C : 1
    math_3 = Has("Progressive Math Rank", 3) # B : 2
    math_4 = Has("Progressive Math Rank", 4) # A : 3
    math_5 = Has("Progressive Math Rank", 5) # A* : 4

    english_1 = Has("Progressive English Rank", 1) # D : 0
    english_2 = Has("Progressive English Rank", 2) # C : 1
    english_3 = Has("Progressive English Rank", 3) # B : 2
    english_4 = Has("Progressive English Rank", 4) # A : 3
    english_5 = Has("Progressive English Rank", 5) # A* : 4

    history_1 = Has("Progressive History Rank", 1) # D : 0
    history_2 = Has("Progressive History Rank", 2) # C : 1
    history_3 = Has("Progressive History Rank", 3) # B : 2
    history_4 = Has("Progressive History Rank", 4) # A : 3
    history_5 = Has("Progressive History Rank", 5) # A* : 4

    willpower_1 = Has("Progressive Willpower Rank", 1) # fainthearted
    willpower_2 = Has("Progressive Willpower Rank", 2) # mindful
    willpower_3 = Has("Progressive Willpower Rank", 3) # resolved
    willpower_4 = Has("Progressive Willpower Rank", 4) # determined
    willpower_5 = Has("Progressive Willpower Rank", 5) # tenacious
    willpower_6 = Has("Progressive Willpower Rank", 6) # iron

    physique_1 = Has("Progressive Physique Rank", 1) # skinny
    physique_2 = Has("Progressive Physique Rank", 2) # slender
    physique_3 = Has("Progressive Physique Rank", 3) # slim
    physique_4 = Has("Progressive Physique Rank", 4) # athletic
    physique_5 = Has("Progressive Physique Rank", 5) # firm
    physique_6 = Has("Progressive Physique Rank", 6) # powerful

    promiscuity_1 = Has("Progressive Promiscuity Rank", 1) # prudish
    promiscuity_2 = Has("Progressive Promiscuity Rank", 2) # curious
    promiscuity_3 = Has("Progressive Promiscuity Rank", 3) # excited
    promiscuity_4 = Has("Progressive Promiscuity Rank", 4) # crave
    promiscuity_5 = Has("Progressive Promiscuity Rank", 5) # slut
    promiscuity_6 = Has("Progressive Promiscuity Rank", 6) # insatiable

    exhibitionism_1 = Has("Progressive Exhibitionism Rank", 1) # shy
    exhibitionism_2 = Has("Progressive Exhibitionism Rank", 2) # like
    exhibitionism_3 = Has("Progressive Exhibitionism Rank", 3) # enjoy
    exhibitionism_4 = Has("Progressive Exhibitionism Rank", 4) # excites
    exhibitionism_5 = Has("Progressive Exhibitionism Rank", 5) # shameless
    exhibitionism_6 = Has("Progressive Exhibitionism Rank", 6) # wild

    deviancy_1 = Has("Progressive Deviancy Rank", 1) # conventional
    deviancy_2 = Has("Progressive Deviancy Rank", 2) # strange
    deviancy_3 = Has("Progressive Deviancy Rank", 3) # shocking
    deviancy_4 = Has("Progressive Deviancy Rank", 4) # scandalous
    deviancy_5 = Has("Progressive Deviancy Rank", 5) # crave
    deviancy_6 = Has("Progressive Deviancy Rank", 6) # lust

    fakeid = Has("Fake ID")

    # if needed later add weapon skills here too

    # Game Options:
    multipleruns_toggle = OptionFilter(MultipleRuns)
    rng_toggle = OptionFilter(DontRestrictRNG)

    # World Options:
    anal_toggle = OptionFilter(Anal)
    tentacles_toggle = OptionFilter(Tentacles)
    lactation_toggle = OptionFilter(Lactation)
    softvore_toggle = OptionFilter(SoftVore)
    beastiality_toggle = OptionFilter(Beastiality)
    parasites_toggle = OptionFilter(Parasites)
    # swarms_toggle = OptionFilter(Swarms)
    bodywriting_toggle = OptionFilter(Bodywriting)

    pregnancy_toggle = OptionFilter(Pregnancy)
    parasiticpregnancy_toggle = OptionFilter(ParasiticPregnancy)

    animal_transformation_toggle = OptionFilter(AnimalTransformations)
    divine_transformation_toggle = OptionFilter(DivineTransformations)


    # Transformations:
    randomize_transformations = OptionFilter(RandomizeTransformations)
    wolf_tf = Rule(Has("Wolf Transformation") & randomize_transformations & animal_transformation_toggle)

    flight = Rule(Has("Flight"))

    # Sexual Traits
    bitch_trait = Rule(beastiality_toggle)
    prey_trait = Rule(tentacles_toggle)
    tasty_trait = Rule(softvore_toggle)
    milkaddict_trait = Rule(lactation_toggle)

    # Area Rulings:
    tentacle_plains = Rule(tentacles_toggle & deviancy_6) # TODO: check this devi rank
    tentacle_forest = Rule(tentacles_toggle)

    # avery_mansion_score = Rule(housekeeping_4) # replace with adoption papers check

    # Feat Rulings:
    # no_control = Rule(beastiality_toggle) # "beastiality or monster people"? so doesn't require any toggle?
    # equinerescue_feat = Rule(beastiality_toggle) # TODO: double check that this requires beastiality, I dobut it
    # headpack_feat = Rule(beastiality_toggle) # TODO: double check that this requires beastiality, I dobut it
    # foodchain_feat = Rule(beastiality_toggle) # TODO: double check that this requires beastiality, I dobut it
    knot_feat = Rule(beastiality_toggle)

    sexspecialist_feat = Rule(anal_toggle)
    pridefarm_feat = Rule(lactation_toggle)
    crimmostfowl_feat = Rule(bodywriting_toggle) # sydney will write on you unless you have bodywriting **off**

    animal_transformation_feat = Rule(animal_transformation_toggle) # all feats that require an animal tf
    angel_feat = Rule(divine_transformation_toggle & multipleruns_toggle)
    fallenangel_feat = Rule(divine_transformation_toggle & multipleruns_toggle)
    demon_feat = Rule(divine_transformation_toggle)
    
    specialtraitcollector_feat = Rule(bitch_trait & prey_trait & tasty_trait & milkaddict_trait)
    
    broodmother_feat = Rule(parasiticpregnancy_toggle & tentacles_toggle & beastiality_toggle)
    # zoologist also here ^
    earslime_feat = Rule(parasites_toggle & parasiticpregnancy_toggle) # change if I ever swap parasitic preg toggle
    # ear slime amalgam also here ^
    giantslug_feat = Rule(parasiticpregnancy_toggle) # change if I ever swap parasitic preg toggle
    redemption_feat = Rule(divine_transformation_toggle)
    
    getpregnant_feat = Rule(pregnancy_toggle)
    fatherhood_feat = Rule(pregnancy_toggle)
    mpreg_feat = Rule(pregnancy_toggle & parasites_toggle)
    hailmary_feat = Rule(pregnancy_toggle & multipleruns_toggle)







    

def set_all_rules(world: DoLWorld) -> None:
    set_all_entrance_rules(world)
    set_all_location_rules(world)
    set_completion_condition(world)

def set_all_entrance_rules(world: DoLWorld) -> None:
    print("do rules") # TODO: entrance rules

def set_all_location_rules(world: DoLWorld) -> None:
    print("do rules") # TODO: location rules

def set_completion_condition(world: DoLWorld) -> None:
    print("do rules") # TODO: completion conditions