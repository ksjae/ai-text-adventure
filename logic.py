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

    def extract(self, sentence):
        '''
        Extracts subject, verb & object.
        '''
        tokenized = self.nlp(sentence)
        return tokenized

    def pick_pos(self, POS, sentence):
        tokens_with_pos = []
        for token in self.extract(sentence):
            #print(token.text)
            if token.pos == POS:
                tokens_with_pos.append(token.text)
        return tokens_with_pos

    def pick_subj(self, sentence):
        subjects = []
        for token in self.extract(sentence):
            #print(token.text)
            if token.dep == nsubj:
                subjects.append(token.text)
        return subjects

    def generate_prompt(self, generator: Text, tag, status: World, length=300):
        '''
        Generates a prompt describing the current situation
        '''
        prompt = status.world_prompt
        # SUBJ[당시 턴이었던] VERB ACTION . SUBJ[Player] VERB[Result]
        prompt += status.current_situation_prompt + ". " + str(status.current_turn_character) + status.pc_action
        generator.generate(prompt, length)

    def uses_item(action):
        return False