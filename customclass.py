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

class Stat():
    strength, dexterity, constitution, intelligence, wisdom, charisma = (0,0,0,0,0,0)
    def __init__(self, strength, dexterity, constitution, intelligence, wisdom, charisma):
        self.strength, self.dexterity, self.constitution, self.intelligence, self.wisdom, self.charisma = strength, dexterity, constitution, intelligence, wisdom, charisma

class Character():
    stats: Stat
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

    def __init__(self, stats=Stat(0,0,0,0,0,0), items=[], name=""):
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

class Player(Character):
    def __str__(self):
        return "You"

class Effect():
    delay: int
    amount: int
    name: str
    
    def __init__(self, delay, amount, name=""):
        self.name = name
        self.amount = amount
        self.delay = delay

class Damage():
    target: Character
    spec = None #Array of effects

class Item():
    name = ""
    spec = {'visible': False, 'magical': False}
    def __init__(self, name, spec):
        self.name = name
        self.spec = spec

class Result():
    damage: Damage
    item: Item
    item_delta: int
    new_world: None

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

class Turn():
    character: Character
    action: Action
    target: Character
    result: Result
    