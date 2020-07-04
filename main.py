from spew import Text
from logic import *
from customclass import *


print("LOADING...")
#generator = Text()
print("THE GAME IS ON.")
#prompt = "You entered the dungeon. You killed monsters. The monsters poisoned you. You see a locked door. You go in the door."
#print('prompt:', prompt)
#print(generator.generate(prompt, 200, remove_prompt=True))
print("SKIPPING SETUP.")

player = Player(
        Stat(1,2,3,4,5,6),
        [Item("knife",{'visible': True, 'magical': False})],
        "Cave Johnson")
player.set_skill({'name':"", 'max_damage':0, 'min_damage':0, 'tendency':0, 'expression':"", 'verb':['']})
print("You, as "+player.name+", will now experience a unique adventure.")
print("To start adventure, type a short summary of what happened.")
print("For instance, \""+player.name+" was being chased by an army of robots. The robot uprising had begun. With only a knife in his hands, he did not know what to do.\"")
print('='*40)
