from spew import Text
from logic import Tagger
import spacy

#generator = Text()
#prompt = "You entered the dungeon. You killed monsters. The monsters poisoned you. You see a locked door. You go in the door. You see"
#print('prompt:', prompt)

sentence_count = 5
nlp = spacy.load("en_core_web_sm")
#nlp.add_pipe(nlp.create_pipe('sentencizer'))
while True:
    prompt = input()
    doc = nlp(prompt)
    #sentence_len = len(list(doc.sents))
    delta = ""
    for token in doc:
        print(token.text, token.dep_, token.pos_, token.head.text, token.lemma_)
'''
while True:
    created = generator.generate(prompt + delta, len(prompt + delta) + 50)
    #print(created)
    #EXTRACT 1 SENTENCE - . and ! and ?
    doc = nlp(created.replace(prompt, '', 1))
    doc = list(doc.sents)[:1]
    delta += ' '.join(map(str,doc))
    doc = nlp(delta)
    print(delta)
'''



#tagger = Tagger()
#print(tagger.tag("My friend shoots a bullet as I throw myself at him."))