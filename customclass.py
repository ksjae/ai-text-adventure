class Event():
    who = None
    what = "dies"
    explanation = "by hunger"
    def __init__(self, character, event, explanation):
        self.who = character
        self.what = event
        self.explanation = explanation
    def get_prompt(self):
        return str(self.who) + self.what + self.explanation

class Status():

    mode = {'NONE': True, 'BATTLE': False, 'TRADE': False, 'QUEST': False}
    recent_events = []
    world_prompt=""
    current_situation_prompt=""
    characters = []
    players = []
    future_events = []

    def in_battle(self):
        return self.mode['BATTLE']
    def in_trade(self):
        return self.mode['TRADE']
    def in_quest(self):
        return self.mode['QUEST']

class Quest():
    def generate(self, status: Status()):
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
    stats = (0,0,0,0,0,0)
    items = []
    quests = []
    name = ""
    modifier = ""
    skill = {'name':"", 'max_damage':0, 'min_damage':0, 'tendency':0, 'expression':"", 'verb':['']} #tendency : 쏠리는 비율 - 1에 가까우면 크리티컬 잘 터짐
    def __init__(self, stats, items):
        self.stats = stats
        self.items = items
    def set_skill(self, skill):
        self.skill = skill
    def __str__(self):
        return self.name

class Player(Character):

    def __init__(self, stats, items, name):
        self.stats = stats
        self.items = items
        self.name = name
    def __str__(self):
        return "You"


class Item():
    name = ""
    spec = {'visible': False, 'magical': False}
    def __init__(self, name, spec):
        self.name = name
        self.spec = spec

class Stat():
    strength, dexterity, constitution, intelligence, wisdom, charisma = (0,0,0,0,0,0)
    def __init__(self, strength, dexterity, constitution, intelligence, wisdom, charisma):
        self.strength, self.dexterity, self.constitution, self.intelligence, self.wisdom, self.charisma = strength, dexterity, constitution, intelligence, wisdom, charisma