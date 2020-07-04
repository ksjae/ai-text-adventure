from spew import Text
from logic import Tagger

generator = Text()
prompt = "You entered the dungeon. You killed monsters. The monsters poisoned you. You see a locked door. You go in the door."
print('prompt:', prompt)
print(generator.generate(prompt, 200, remove_prompt=True))
#tagger = Tagger()
#print(tagger.tag("My friend shoots a bullet as I throw myself at him.")) kd