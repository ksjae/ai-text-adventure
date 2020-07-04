import spacy
import en_core_web_sm # Install with python3 -m spacy download en_core_web_sm
from spacy.symbols import nsubj, VERB
from spew import Text
from customclass import *
import random

class Tagger():
    battle_trigger = ['fight', 'slit', 'cut']
    battle_verb = ['throw', 'use', 'cure', 'shoot']
    battle_word = battle_verb+battle_trigger

    trade_trigger = ['trade', 'give', 'exchange']
    trade_verb = ['find', 'take', 'search']

    quest_trigger = ['talk', 'ask', '"']
    quest_verb = []

    nlp = None

    def __init__(self):
        self.nlp = spacy.load('en_core_web_sm')

        f = open('data/battle_trigger.txt', 'r+')
        self.battle_trigger = [line for line in f.readlines()]
        f.close()

    def tag(self, sentence = "My friend shoots a bullet as I throw myself at him."):
        tokenized = self.nlp(sentence)

        trigger_mode = {'NONE': True, 'BATTLE': False, 'TRADE': False, 'QUEST': False}

        def set_mode(name = 'NONE'):
            trigger_mode = {'NONE': False, 'BATTLE': False, 'TRADE': False, 'QUEST': False}
            trigger_mode[name] = True

        for token in tokenized:
            if token.dep == nsubj and token.head.pos == VERB:
                print(token.text)
                for ancestor in token.ancestors:
                    if ancestor.lemma_ in self.battle_trigger:
                        print("↑ [BATTLE]")
                        trigger_mode = {'NONE': False, 'BATTLE': False, 'TRADE': False, 'QUEST': False}
                        trigger_mode['BATTLE'] = True

        return trigger_mode

    def generate_prompt(self, generator: Text, tag, status: Status, length=300):
        prompt = ""
        generator.generate(prompt, length)