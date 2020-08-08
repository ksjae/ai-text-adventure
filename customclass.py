import collections
import random

class Action():
    who = None
    what = "dies"
    explanation = "by hunger"
    def __init__(self, character, event, explanation):
        self.who = character
        self.what = event
        self.explanation = explanation
    def get_prompt(self):
        return str(self.who) + self.what + self.explanation

class Scope():
    """
    A vague representation of current events. Has the following - 
    1. TIME, LOCATION
    2. CURRENT PLAYERS(multiplayer-proof)
    3. CURRENT CHARACTERS(incl. enemy)
    4. EXPLICIT OBJECTS(ex. cup(in a bar))
    """
    Relativetime = collections.namedtuple("Relativetime","year month day hour minute second")
    location = ""
    time =  Relativetime(1,1,1,0,0,0)
    characters = []
    players = []
    objects = []

class World(Scope):
    mode = {'NONE': True, 'BATTLE': False, 'TRADE': False, 'QUEST': False}
    recent_events = []
    world_prompt=""
    current_situation_prompt=""
    players = []
    future_events = []
    current_turn_character = None
    pc_action = ""

    def in_battle(self):
        return self.mode['BATTLE']
    def in_trade(self):
        return self.mode['TRADE']
    def in_quest(self):
        return self.mode['QUEST']

    def __init__(self, **kwargs):
        pass

class Quest():
    def generate(self, status: World):
        giver = Character(random.choice(status.characters))
        while True:
            if giver not in status.players:
                break
            giver = Character(random.choice(status.characters))

        for i in range(random.randint(2,5)):
            self.quest.append({
                'finish_condition': Event(),
                'reward': Item(),
                'giver': giver
            })
        return quest
    def check_fin(self):
        return False

class Character():
    stats = 0
    items = []
    quests = []
    name = ""
    alt_names = []
    modifier = ""
    language = ""
    character_class = {'name':"", 'proficiency':""}
    level = 1
    skill = {'name':"", 'max_damage':0, 'min_damage':0, 'tendency':0, 'expression':"", 'verb':['']} #tendency : 쏠리는 비율 - 1에 가까우면 크리티컬 잘 터짐
    valid_target_action = []
    valid_action = []

    def __init__(self, stats, items=[], name=""):
        self.stats = stats
        self.items = items
        self.name = name
    def __str__(self):
        return self.name
    def set_skill(self, skill):
        self.skill = skill
    def get_hit_point(self):
        return self.level
    def valid_target_action(self, action):
        return action in self.valid_target_action


class Item():
    name = ""
    spec = {'visible': False, 'magical': False}
    def __init__(self, name, spec):
        self.name = name
        self.spec = spec

class Event():
    """
    A simple form of event (str action, source, destination, (optional) text)
    """
    action = ""
    source = ""
    destination = ""
    _original_description = ""
    def __init__(self, **kwargs):
        self.action = kwargs.get('action', "nothing")
        self.source = kwargs.get('source', "nobody")
        self.destination = kwargs.get('destination', "")
        self._original_description = kwargs.get('text', "")
    def __contains__(self, item):
        if item == self.action:
            return True
        elif item == self.source:
            return True
        elif item == self.destination:
            return True
        return False
    def __str__(self):
        if self._original_description:
            return self._original_description
        return self.action + ' done by ' + self.source + ' to ' + self.destination

class Events():
    """
    For each turn, Events contain array of Event.
    """
    __array = []
    item_limit = 0
    def __contains__(self, item):
        for i in self.__array:
            if item in i:
                return True
        return False
    def __iter__(self):
        return iter(self.__array)
    def __str__(self):
        string = ""
        for i in self.__array:
            string += (str(i)+'\n')
        return string
    def __init__(self, **kwargs):
        if 'item_limit' in kwargs.keys:
            self.item_limit=int(kwargs['item_limit'])

    def append(self, item):
        if not isinstance(item, Event):
            raise ValueError
        self.__array.append(item)


class Modifier():
    delta_stat = 0
    
class Interactable:
    pass

class Attackable:
    attacks = []
    def get_status(self):
        return True
    def attack(self):
        dmg = 0
        return dmg

class Defendable:
    defenses = []
    def defend(self):
        return self.hp
    
class Tradeable:
    """
    Can execute/accept trade requests
    """
    cash=0

    def exchange(self, item, amount):
        pass
    def sell(self, item, cost):
        """
        Sell item at cost
        """
        self.exchange(item, -amount)
        #self.exchange(Currency(),cost)
        return True
    def buy(self, item, cost):
        """
        Buy item at cost
        """
        self.exchange(item, amount)
        #self.exchange(Currency(),-cost)
        return True

class Expendable:
    remaining=0
    maximum_amount=-1
    unit='items'
    def use(self, amount):
        if amount > self.remaining:
            return False
        self.remaining -= amount
        if self.remaining == 0:
            #Destroy Item
            pass
        return True
    def refill(self, amount):
        if amount > maximum_amount:
            raise ValueError
        self.remaining = amount
        return True
    def set_expendable(self, maximum_amount):
        self.maximum_amount =maximum_amount
        self.remaining = maximum_amount

class Movable:
    friction_coefficient = 0.1
    gravitational_acceleration = 9.8
    
    @property
    def friction(self):
        return self.mass * self.gravitational_acceleration * self.friction_coefficient

    def moves(self, force):
        if force > self.friction:
            return False
        return True

    def set_friction_coefficient(self, mu):
        self.friction_coefficient = mu

class Affects:
    #뭐에게 영향을 어떻게?
    pass

class Requires:
    needed_items = []
    needed_attributes = []
    available_time = []

    def meets_item_requirement(self, item_array):
        return True

    def meets_environmental_requirement(self, scene):
        return True

    def meets_time_requirement(self, time):
        return True

    def meets_requirement(self,item,scene,time):
        return self.meets_environmental_requirement(scene) and self.meets_item_requirement(item) and self.meets_time_requirement(time)

class Plays:
    """
    Can 'play'. that is, can make player-grade actions.
    examples include player itself & companions
    """
    decide_automatically = True
    strength, dexterity, constitution, intelligence, wisdom, charisma = (0,0,0,0,0,0)

class Thinks:
    """
    Can think logically - e.g. can be mortal enemies
    Think of an orc. Orcs can be considered 'thinking'
    """
    friend_list = []
    enemy_list = []
    friend_class = []
    enemy_class = []

    def is_enemy(self, character):
        return False
    def is_friend(self, character):
        return True

class Worth:
    """
    Is worth SOMETHING and can be traded.
    0 is possible though. Never negative.
    """

    worth = 0

    def evaluate_value(self, favor=0):
        return self.worth * (1+favor)
    
class Alive:
    """
    Responds to HP changes - a tree may brown, a bot may require fixes, ...
    """
    HealthRangeMsg = collections.namedtuple('HealthRangeMsg', 'min max msg')
    responses = [] #HRM array

    def generate_health_response(self):
        return ""

class Makes:
    """
    Can craft stuff - spider-web, human-hatchet, etc.
    """
    craftable = [] #item array
    
    def craft_item(self, item):
        if item in craftable: # needs more advanced logic
            return item
        return False
    
class Karma:
    global_karma = 0
    location_karma = {}
    global_karma_benefit = {}

    @property
    def global_benefit(self):
        return True #SHOULD RETURN A MODIFIER OBJECT