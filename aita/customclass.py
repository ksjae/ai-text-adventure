from enum import Enum
from python_console_menu import AbstractMenu
import random

from aita.errors import *

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

class Health:
    wear: int
    _health: int
    def __init__(self, health):
        self._health = health
        self.wear = 0
    
    def __index__(self):
        return self._health - self.wear

    def __int__(self):
        return self._health - self.wear

    def restore(self, amount):
        self.wear -= amount
        if self.wear < 0:
            self.wear = 0

    def use(self, amount):
        if int(self) < 0:
            raise NoLongerUsable
        self.wear += amount

class Item:
    delta_stat: Stat
    raw_price: int
    health: Health
    damage: Damage
    iid: int
    def __init__(self):
        self.wear=10
        self.iid = ''.join([str(random.randint(0, 9)) for i in range(10)])  # This ain't crpyto, it'll do
class Gold(Item):
    count: int
    unit: str
    def __init__(self, count, unit='G'):
        super().__init__()
        self.unit = unit
        self.count = count

    def __str__(self):
        return f"{self.count} {self.unit}"

    def __index__(self):
        return self.count

    def __int__(self):
        return self.count

class Bodypart(Item):
    vital: bool
    _stat_portion: Stat
    name: str
    valid_damage: Damage
    defending: bool
    def __init__(self):
        super().__init__()
        self.defending = False
class Head(Bodypart):
    _stat_portion = Stat(0,0)
    def __init__(self):
        super().__init__()
        self.vital = True
        self.name="머리"
        self.health = Health(10)
class Torso(Bodypart):
    _stat_portion = Stat(0,0)
    def __init__(self):
        super().__init__()
        self.vital = True
        self.name="가슴"
        self.health = Health(10)
class Stomach(Torso):
    _stat_portion = Stat(0,1)
    def __init__(self):
        super().__init__()
        self.vital = True
        self.name="배"
        self.health = Health(5)
class Waist(Torso):
    _stat_portion = Stat(0,2)
    def __init__(self):
        super().__init__()
        self.vital = False
        self.name="허리"
        self.health = Health(1)
class Arm(Bodypart):
    _stat_portion = Stat(10,10)
    def __init__(self):
        super().__init__()
        self.vital = False
        self.name="팔"
        self.health = Health(2)
class Leg(Bodypart):
    _stat_portion = Stat(5,5)
    def __init__(self):
        super().__init__()
        self.vital = False
        self.name="다리"
        self.health = Health(2)
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
    stat: Stat
    __under_cover: bool
    age: int
    height: bool
    weight: bool
    skin_tone: str
    hair_color: str
    eye_color: str
    religion: str
    _gold: Gold
    
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
        self._gold = 0
    
    @property
    def items(self):
        return self.__items

    def add_items(self, item:Item):
        self.__items.append(item)

    def remove_items(self, item: Item):
        for i, owned_item in enumerate(self.__items):
            if owned_item.iid == item.iid:
                return self.__items.pop(i)
        raise NonExistent

    @property
    def spellAblilty(self):
        return 0

    @property
    def armor(self):
        armor_total = 0
        for item in self.items:
            armor_total += item.delta_stat.defence
        armor_total += self.stat.defence
        if self.anatomy.pose == Pose().defending:
            armor_total += 1
        return armor_total

    @property
    def hp(self):
        bodyparts = [self.anatomy.head, self.anatomy.torso, self.anatomy.arm, self.anatomy.leg]
        sum = 0
        for part in bodyparts:
            sum += int(part.health)
        return sum

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
        return 1

    @property
    def disadvantage_score(self, ):
        return 0

    @property
    def gold(self, ):
        return self._gold

    def addgold(self, amount):
        self._gold += amount

    def removegold(self, amount):
        self._gold -= amount

class Event:
    source: Actor
    target: Actor
    action: None # Function
    kwargs: None
    def __init__(self, **kwargs):
        def empty():
            pass
        self.action = empty
        self.source = None
        self.target = None
        self.kwargs = kwargs
    
    def process(self):
        self.action(self.source, self.target, self.kwargs)

class EventQueue:
    def __init__(self):
        self._queue = []
    
    def get(self):
        if len(self._queue) > 0:
            return self._queue.pop(0)
        raise ValueError    # Queue Empty, Dumbass
    
    def put(self, item, source, target, turn=0, kwargs={}): # Put Event/item at Nth turn
        while len(self._queue) <= turn:
            self._queue.append([]) # Append list of events
        self._queue[turn].append(
            (item,source,target,kwargs))

    def commit(self):
        events = self.get()
        for event in events:
            item, source, target, kwargs = event
            if kwargs == {}:
                item(source, target)
            else:
                item(source, target, **kwargs)
                
class AppFlags:
    user_id = None
    model_path = ''
    model_type = None
    is_using_online_api = False
    is_dev = False
    LANG = 'ko'
    simple_mode = True

    @property
    def is_authenticated(self):
        return user_id is not None
    