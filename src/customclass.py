from enum import Enum

class Damage(Enum):
    cleaving = 1
    slashing = 2
    thrusting = 3
    tearing = 4

class AttackType(Enum):
    melee = 1
    ranged = 2
    magical = 3

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
    def __init__(self):
        wear=10
class Bodypart(Item):
    is_vital: bool
    stat_portion: Stat
    name: str
    valid_damage: Damage
    def __init__(self):
        super().__init__()
class Head(Bodypart):
    stat_portion = Stat(0,0,10)
    def __init__(self):
        super().__init__()
        is_vital = True
        name="머리"
class Torso(Bodypart):
    stat_portion = Stat(0,0,10)
    def __init__(self):
        super().__init__()
        is_vital = True
        name="가슴"
class Stomach(Torso):
    stat_portion = Stat(0,1,5)
    def __init__(self):
        super().__init__()
        is_vital = True
        name="배"
class Waist(Torso):
    stat_portion = Stat(0,2,0)
    def __init__(self):
        super().__init__()
        is_vital = False
        name="허리"
class Arm(Bodypart):
    stat_portion = Stat(10,10,1)
    def __init__(self):
        super().__init__()
        is_vital = False
        name="팔"
class Leg(Bodypart):
    stat_portion = Stat(5,5,1)
    def __init__(self):
        super().__init__()
        is_vital = False
        name="다리"
class Pose:
    def __init__(self):
        self.standing = True
        self.defending = False
        self.off_balance = False
        self.on_ground = False
        self.extended = False
    def __str__(self):
        return str(self.pose)

    @property
    def pose(self):
        if self.defending:
            return '방어'
        elif self.off_balance:
            return '균형이 무너진'
        elif self.on_ground:
            return '엎어진'
        elif self.extended:
            return '뻗은'
        else:
            return '서있는'

    @pose.setter
    def pose(self, new_pose):
        self.standing = False
        self.defending = False
        self.off_balance = False
        self.on_ground = False
        self.extended = False
        if new_pose == 'defending':
            self.defending = True
        elif new_pose == 'off balance':
            self.off_balance = True
        elif new_pose == 'on ground':
            self.on_ground = True
        elif new_pose == 'extended':
            self.extended = True
        else:
            self.standing = True
        
class Anatomy:
    def __init__(self,
                head: Head,
                torso: Torso,
                arm: Arm,
                leg: Leg):

        self.pose = Pose().pose
        self.head = head
        self.torso = torso
        self.arm = arm
        self.leg = leg

class Actor:
    anatomy: Anatomy
    pose: Pose
    stat: Stat
    __under_cover: bool
    
    def __init__(self):
        self.__items = []
        self.__under_cover = False
        head = Head()
        torso = Torso()
        arm = Arm()
        leg = Leg()
        self.anatomy = Anatomy(head=head,
                        torso=torso,
                        arm=arm,
                        leg=leg,)
        self.anatomy.pose = Pose().pose
        self.stat = Stat(0,0)
    
    @property
    def items(self):
        return self.__items

    @items.setter
    def items(self, item:Item):
        self.__items.append(item)

    @property
    def spellAblilty(self):
        return 0

    @property
    def armor(self):
        armor_total = 0
        for item in self.items:
            armor_total += item.delta_stat.defence
        armor_total += self.stat.defence
        return armor_total

    @property
    def has_cover(self):
        return self.__under_cover

    def get_attack_type_modifier(self, attack_type):
        if attack_type == AttackType.melee:
            return self.stat.attack
        elif attack_type == AttackType.ranged:
            return self.stat.dexterity
        elif attack_type == AttackType.magical:
            return self.spellAbility
        else:
            return 0

    @property
    def advantage_score(self, ):
        return 0

    @property
    def disadvantage_score(self, ):
        return 0

    