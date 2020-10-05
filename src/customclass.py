class Stat:
    constitution: int
    dexterity: int
    stamina: int
    intelligence: int

class Damage:
    cleaving: int
    slashing: int
    thrusting: int
    tearing: int

class Item:
    _id: int
    delta_stat: Stat
    raw_price: int
    wear: int
    damage: Damage

class Bodypart:
    is_vital: bool
    stat_portion: Stat
    name: str
    valid_damage: Damage
class Head(Bodypart):
    def __init__():
        is_vital = True
        name="머리"
class Torso(Bodypart):
    def __init__():
        is_vital = True
        name="가슴"
class Stomach(Torso):
    def __init__():
        is_vital = True
        name="배"
class Waist(Torso):
    def __init__():
        is_vital = False
        name="허리"
class Arm(Bodypart):
    def __init__():
        is_vital = False
        name="팔"
class Leg(Bodypart):
    def __init__():
        is_vital = False
        name="다리"
class Pose:
    standing = 0
    defending = 1
    off_balance = 2
    on_ground = 3
    extended = 4
class Anatomy:
    def __init__(self,
                head: Head,
                torso: Torso,
                arm: Arm,
                leg: Leg):

        self.pose = Pose.standing
        self.head = head
        self.torso = torso
        self.arm = arm
        self.leg = leg

class Actor:
    def __init__(self,
                 body=
                 )