from ..customclass import *
from ..actions import *

def test_attack():
    character1 = Actor()
    character2 = Actor()
    attack(character1, character2, 'arm', AttackType.melee, Damage.cleaving)

