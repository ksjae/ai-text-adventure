from aita.customclass import *
from aita.actions import *

def test_attack():
    character1 = Actor()
    character2 = Actor()
    attack(character1, character2, 
            part='arm', 
            attack_type=AttackType.melee,
            current_weapon=Damage.cleaving
            )

def test_defence():
    character1 = Actor()
    armor_prev = character1.armor
    defend(character1, part='arm', attack_type=AttackType.melee)
    assert character1.anatomy.pose == Pose().defending
    assert character1.armor > armor_prev

def test_heal():
    character1 = Actor()
    character2 = Actor()
    attack(character1, character2, 
            part='arm', 
            attack_type=AttackType.melee,
            current_weapon=Damage.cleaving
            )
    hp_prev = character2.hp
    heal(character1,character2,
        part='arm',
        amount=10
    )
    assert character2.hp > hp_prev

def test_commit_events():
    character1 = Actor()
    event_queue = EventQueue()
    attack(character1, character1, 
            part='arm', 
            attack_type=AttackType.melee,
            current_weapon=Damage.cleaving
            )
    hp_prev = character1.hp
    event_queue.put(heal, character1, character1)
    event_queue.commit()
    assert character1.hp > hp_prev
    
def test_purchase():
    amount = 5
    character1 = Actor()
    character2 = Actor()

    get_gold(character1, 10)
    thing = Item()
    character2.add_items(thing)

    buy(character2, character1, Item, 10)

    assert character1.gold == 0
    assert thing in character1.items
    assert character2.gold == 10