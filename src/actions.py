from .customclass import *
from .utils import *

def attack(source: Actor, 
           target: Actor, 
           **kwargs
           ):
    """
    A function executing the action.
    Returns True if action is successfully finished.
    """
    part = kwargs['part']
    attack_type = kwargs['attack_type']
    current_weapon = kwargs['current_weapon']
    
    # You attack the zombie's neck. The head is dangling down. The zombie is still moving.
    dice = DiceRoll()
    attack_modifier = source.advantage_score - source.disadvantage_score
    attack_modifier -= 1 if target.has_cover else 0
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
         **kwargs
         ):

    if 'amount' not in kwargs.keys(): # Heal to max
        amount = 999999999
    else:
        amount = kwargs['amount']

    if 'part' in kwargs.keys():
        if kwargs['part'] == 'all' :
            parts = ['head','torso','arm','leg']
            for part in parts:
                getattr(target.anatomy, part).health.restore(amount)
        else:
            getattr(target.anatomy, kwargs['part']).health.restore(amount)
    else:
        parts = ['head','torso','arm','leg']
        for part in parts:
            getattr(target.anatomy, part).health.restore(amount)

def exchange(source: Actor,
             target: Actor, 
             thing: Item,):
    source.remove_items(thing)
    target.items(thing)

def buy(source: Actor,
        target: Actor, 
        thing: Item,
        price: Gold):
    source.addgold(price)
    target.removegold(price)

    source.remove_items(thing)
    target.items(thing)

def get(target: Actor,
        thing: Item):
    target.items(thing)

def get_gold(target: Actor,
             amount: Gold):
    target.addgold(amount)