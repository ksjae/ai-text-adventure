from spew import Text
from logic import *
from customclass import *
from spacy.symbols import NOUN, VERB
import os, sys
import collections

'''
FUNCTIONS
'''
def saveProgress(filename="game.save"):
    return True

def loadProgress(filename="game.save"):
    return {}

# Load stuff
print("LOADING...")
#generator = Text()
tagger = Tagger()
savefile = loadProgress()
print("THE GAME IS ON.")

# Setup world, player

print("TEST MODE - SKIPPING SETUP")

prompt = "You entered the dungeon. You killed monsters. The monsters poisoned you. You see a locked door. You go in the door."
print('prompt:', prompt)
#print(generator.generate(prompt, 200, remove_prompt=True))
if 'player' not in savefile.keys():
    player = Player(
            Stat(1,2,3,4,5,6),
            [Item("knife",{'visible': True, 'magical': False})],
            "Cave Johnson")
    player.set_skill({'name':"", 'max_damage':0, 'min_damage':0, 'tendency':0, 'expression':"", 'verb':['']})
else :
    player = savefile['player']

'''
print("You, as "+player.name+", will now experience a unique adventure.")
print("To start adventure, type a short summary of what happened. *Newline(Enter key) will terminate input*")
print("For instance, \""+player.name+" was being chased by an army of robots. The robot uprising had begun. With only a knife in his hands, he did not know what to do.\"")
print('='*40)
'''

# Loop forever

print('remember to put a period at the end.')
backlog_sentence_count=7
backlog = []

while True:
    try:
        print('> ', end='')
        action = input()
        backlog = backlog[-backlog_sentence_count:]
        backlog.append(action)
        string = tagger.nlp(action)
        '''
        for chunk in string.noun_chunks:
            if chunk.root.head.pos == VERB:
                if chunk.root.dep_ == 'nsubj':
                    print(chunk.root.text+'('+chunk.text+')','has',chunk.root.head.lemma)
                elif chunk.root.dep_ == 'dobj':
                    print('action |',chunk.root.head.text,'| applied to |', chunk.root.text+'('+chunk.text+')')
                elif chunk.root.dep_ == 'nsubjpass':
                    print('action |',chunk.root.head.text,'| applied to |', chunk.root.text+'('+chunk.text+')')
        '''
        events = Events()
        for token in string:
            if token.pos == VERB:
                #EXTRACT SUBJ, OBJ(ex weapon), NSUBJPASS, ...
                if token.text not in events:
                    event = Event(action=token.text)
                    for child in token.children:
                        text = child.text
                        if child.text == 'it': # special treatment

                        if 'subj' in child.dep_:
                            event.source = text
                        elif child.dep_ == 'dobj':
                            event.destination = text
                        elif child.dep_ == 'prep':
                            event.destination = text
                            
                    print(event)
                    events.append(event)
        print('\n','='*40)
        print(events,'happened.')
        print('='*40)
        #generated = str(generator.generateFiltered(' '.join(backlog), 2))
        #backlog.append(generated)
        #print(generated)
    except KeyboardInterrupt:
        print('\nSaving & Exiting...\n')
        saveProgress()
        try:
            sys.exit(0)
        except SystemExit:
            os._exit(0)

