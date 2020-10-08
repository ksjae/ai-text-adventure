from .customclass import *

def attack(source: Actor, target: Actor, part: str, damage_type:Damage):
    attack_damage = source.stat.attack