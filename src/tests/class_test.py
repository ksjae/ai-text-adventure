from ..customclass import *
from ..utils import *

def test_anatomy_creation():
    head = Head()
    torso = Torso()
    arm = Arm()
    leg = Leg()
    anatomy = Anatomy(head=head,
                      torso=torso,
                      arm=arm,
                      leg=leg,)
    anatomy.pose = 'standing'
    assert anatomy.head == head
    assert anatomy.torso == torso
    assert anatomy.arm == arm
    assert anatomy.leg == leg

def test_character_generation():
    character = Actor()
    initial_arm_health = character.anatomy.arm

def test_armor():
    character = Actor()
    armor = Item()
    armor.delta_stat = Stat(10,10,10,1,2,3,4)
    character.items = armor
    print('Armor :', character.armor)