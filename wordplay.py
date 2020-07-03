import spacy
import en_core_web_sm
from spacy.symbols import nsubj, VERB

nlp = en_core_web_sm.load()

battle_trigger_word = ['fight', 'slit', 'cut']
battle_purpose_verb = ['throw', 'use', 'cure', 'shoot']
battle_trigger_obj = ['damage']
battle_word = battle_purpose_verb+battle_trigger_obj+battle_trigger_word

trade_trigger_word = ['trade', 'give', 'exchange']
trade_purpose_verb = ['find', 'take', 'search']

quest_trigger_word = ['talk', 'ask', '"']
quest_purpose_verb = []

tokenized = nlp("My friend shoots a bullet as I throw myself at him.")

trigger_mode = {'NONE': True, 'BATTLE': False, 'TRADE': False, 'QUEST': False}

def set_trigger_mode(name = 'NONE'):
    trigger_mode = {'NONE': False, 'BATTLE': False, 'TRADE': False, 'QUEST': False}
    trigger_mode[name] = True

for token in tokenized:
    if token.dep == nsubj and token.head.pos == VERB:
        print(token.text)
        for ancestor in token.ancestors:
            if ancestor.lemma_ in battle_word:
                print("↑ [BATTLE]")
                trigger_mode = {'NONE': False, 'BATTLE': False, 'TRADE': False, 'QUEST': False}
                trigger_mode['BATTLE'] = True

print(trigger_mode)
