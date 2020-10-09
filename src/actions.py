from .customclass import *
from .utils import *

def attack(source: Actor, 
           target: Actor, 
           part: str,
           attack_type:AttackType,
           current_weapon:Damage
           ):
    """
    A function executing the action.
    Returns effectiveness of the action, from 0 to 1.
    """
    # You attack the zombie's neck. The head is dangling down. The zombie is still moving.
    target.has_cover
    dice = DiceRoll()
    attack_modifier = source.advantage_score - source.disadvantage_score
    attack_damage = dice.raw + attack_modifier
    if dice.crit_miss:
        attack_damage = 0
    if attack_damage > target.armor or dice.crit_hit: #attack hits
        print("Dealt attack")
        if attack_damage > 0:
            getattr(target.anatomy, part).wear -= attack_damage
    return True