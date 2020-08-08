import spacy
# import en_core_web_md # Install with python3 -m spacy download en_core_web_sm
from spacy.symbols import nsubj, VERB
from spew import Text
from customclass import *
import random
import neuralcoref

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
        neuralcoref.add_to_pipe(self.nlp)
        merge_nps = self.nlp.create_pipe("merge_noun_chunks")
        self.nlp.add_pipe(merge_nps)
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
                tokens_with_pos.append(token)
        return tokens_with_pos

    def pick_subj(self, sentence):
        subjects = []
        for token in self.extract(sentence):
            #print(token.text)
            if token.dep == nsubj:
                subjects.append(token.text)
        return subjects

    def entity(self, name, scope: Scope, certainty=0.4):
        """
        Returns an entity(a Character class) best matching from current scope
        plain(a tree), named($PLAYER_NAME), or related(dragon)

        For plain items, a 'suitable' character with 0 attributes will be returned.

        *Greedily searches word with closest similarity*
        """
        x = self.nlp(name)
        score = {i: self.nlp(i.name).similarity(x) for i in scope.characters}
        score.update({
            i: self.nlp(i.name).similarity(x) for player in scope.players for i in [player.name] + player.alt_names})
        score.update({i: self.nlp(i.name).similarity(x) for i in scope.objects})
        probable_item = max(score.items(), key=lambda x: x[1])
        print('Chose', str(probable_item[0]), probable_item[1])
        if probable_item[1] < certainty:
            print('Not certain @ ',score)
            result_character = Character(name=name)
            return result_character
        return probable_item[0]


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

if __name__ == "__main__":
    """
    TEST CODE
    """
    tag_test = Tagger()
    scope_test = Scope()
    scope_test.characters.append(Character(name="the wizard"))
    scope_test.characters.append(Character(name="King Jorg the third"))
    scope_test.characters.append(Player(name="You"))
    while True:
        i = input()
        print(str(tag_test.entity(name=i, scope=scope_test)))
