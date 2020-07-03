from spew import Text
from logic import Tagger

#generator = Text()
#print(generator.generate("A monster was behind the door, threatening you. You throw your pants, blinding it.", 300))
tagger = Tagger()
print(tagger.tag("My friend shoots a bullet as I throw myself at him."))