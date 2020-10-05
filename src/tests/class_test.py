from ..customclass import *

def test_anatomy_creation():
    head = Head()
    torso = Torso()
    arm = Arm()
    leg = Leg()
    anatomy = Anatomy(head=head,
                      torso=torso,
                      arm=arm,
                      leg=leg,)
    anatomy.pose = Pose.standing
    assert anatomy.head == head
    assert anatomy.torso == torso
    assert anatomy.arm == arm
    assert anatomy.leg == leg

def test_character_generation():
    pass