from spew import Text
from logic import *
from customclass import *
from spacy.symbols import NOUN, VERB


print("LOADING...")
generator = Text()
tagger = Tagger()
print("THE GAME IS ON.")
prompt = "You entered the dungeon. You killed monsters. The monsters poisoned you. You see a locked door. You go in the door."
print('prompt:', prompt)
print(generator.generate(prompt, 200, remove_prompt=True))
print("TEST MODE - SKIPPING SETUP")

player = Player(
        Stat(1,2,3,4,5,6),
        [Item("knife",{'visible': True, 'magical': False})],
        "Cave Johnson")
player.set_skill({'name':"", 'max_damage':0, 'min_damage':0, 'tendency':0, 'expression':"", 'verb':['']})

'''
print("You, as "+player.name+", will now experience a unique adventure.")
print("To start adventure, type a short summary of what happened. *Newline(Enter key) will terminate input*")
print("For instance, \""+player.name+" was being chased by an army of robots. The robot uprising had begun. With only a knife in his hands, he did not know what to do.\"")
print('='*40)
'''
print('remember to put a period at the end.')
backlog_sentence_count=7
backlog = []
while True:
    print('> ', end='')
    action = input()
    backlog = backlog[-backlog_sentence_count:]
    backlog.append(action)
    #print('You choose to do')
    '''
    for i in tagger.pick_pos(NOUN, action):
        print(i, end=' ')
    print('')
    for i in tagger.pick_pos(VERB, action):
        print(i, end=' ')
    print('')
    '''
    generated = str(generator.generateFiltered(' '.join(backlog), 2))
    backlog.append(generated)
    print(generated)

    