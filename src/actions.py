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
    Returns True if action is successfully finished.
    """
    # You attack the zombie's neck. The head is dangling down. The zombie is still moving.
    dice = DiceRoll()
    attack_modifier = source.advantage_score - source.disadvantage_score - 1 if target.has_cover else 0
    attack_damage = dice.raw + attack_modifier
    if dice.crit_miss:
        attack_damage = 0
    if attack_damage > target.armor or dice.crit_hit: #attack hits
        print("Dealt attack")
        if attack_damage > 0:
            getattr(target.anatomy, part).health.use(attack_damage)
    return True

def defend(source: Actor,
           part: str,
           attack_type:AttackType,
           ):
    """
    A function applying defence strategy to Actor.
    Returns True if action is successfully finished.
    """
    # You raise your arm and guard from the enemy's attack.
    source.anatomy.pose = Pose().defending
    getattr(source.anatomy, part).defending = True
    return True

def undefend(source: Actor,
             part: str,
             attack_type:AttackType,
             ):
    """
    A function canceling defence strategy from Actor.
    Returns True if action is successfully finished.
    """
    # You raise your arm and guard from the enemy's attack.
    source.anatomy.pose = Pose().defending
    
    return True

def heal(source: Actor, 
         target: Actor, 
         part: str,
         amount=-1,
         max_amount=1000
         ):
    if amount == -1: # Random
        dice = DiceRoll(max_amount)
        amount = dice.raw
    getattr(target.anatomy, part).health.restore(amount)
    pass