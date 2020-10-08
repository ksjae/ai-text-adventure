class Damage:
    cleaving: int
    slashing: int
    thrusting: int
    tearing: int

class Stat:
    attack: Damage
    defence: Damage
    vitality: int
    intelligence: int
    constitution: int
    dexterity: int
    stamina: int

    def __init__(self, atk, defence, vit=1, con=0, dex=0, sta=0, intel=0):
        self.attack = atk
        self.defence = defence
        self.vitality = vit
        self.constitution = con
        self.dexterity = dex
        self.stamina = sta
        self.intelligence = intel
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
    stat_portion = Stat(0,0,10)
    def __init__(self):
        is_vital = True
        name="머리"
class Torso(Bodypart):
    stat_portion = Stat(0,0,10)
    def __init__(self):
        is_vital = True
        name="가슴"
class Stomach(Torso):
    stat_portion = Stat(0,1,5)
    def __init__(self):
        is_vital = True
        name="배"
class Waist(Torso):
    stat_portion = Stat(0,2,0)
    def __init__(self):
        is_vital = False
        name="허리"
class Arm(Bodypart):
    stat_portion = Stat(10,10,1)
    def __init__(self):
        is_vital = False
        name="팔"
class Leg(Bodypart):
    stat_portion = Stat(5,5,1)
    def __init__(self):
        is_vital = False
        name="다리"
class Pose:
    standing = 0
    defending = 1
    off_balance = 2
    on_ground = 3
    extended = 4
    def __init__(self):
        self.pose = "서"
    def __str__(self):
        return str(self.pose)
        
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
    anatomy: Anatomy
    pose: Pose
    stat: Stat
    def __init__(self):
        pass