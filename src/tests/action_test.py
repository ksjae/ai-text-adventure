from ..customclass import *
from ..actions import *

def test_attack():
    character1 = Actor()
    character2 = Actor()
    attack(character1, character2, 'arm', AttackType.melee, Damage.cleaving)

def test_defence():
    character1 = Actor()
    armor_prev = character1.armor
    defend(character1, part='arm', attack_type=AttackType.melee)
    assert character1.anatomy.pose == Pose().defending
    assert character1.armor > armor_prev

def test_heal():
    character1 = Actor()
    character2 = Actor()
    attack(character1,character2,'arm',AttackType.melee, Damage.cleaving)
    hp_prev = character2.hp
    heal(character1,character2,'arm',10)
    assert character2.hp > hp_prev

def commit_events():
    character1 = Actor()
    hp_prev = character1.hp
    event_queue = EventQueue()
    event_queue.put(character1,character1,heal)
    event_queue.commit()
    assert character1.hp > hp_prev
    