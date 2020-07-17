import tensorflow as tf
from transformers import TFGPT2LMHeadModel, GPT2Tokenizer
from spacy.lang.en import English

class Text():
    tokenizer = None
    model = None
    nlp = None
    sentencizer = None
    def __init__(self, seed=42, model_name="ctrl"): # use HF model name
        self.tokenizer = GPT2Tokenizer.from_pretrained("ctrl")
        # add the EOS token as PAD token to avoid warnings
        self.model = TFGPT2LMHeadModel.from_pretrained("ctrl", pad_token_id=self.tokenizer.eos_token_id)
        tf.random.set_seed(42)
        self.nlp = English()
        self.nlp.add_pipe(self.nlp.create_pipe('sentencizer'))

    def sentences(self, string):
        '''
        Divide string into a array of str(sentence)
        '''
        doc = self.nlp(string)
        return list(map(str,list(doc.sents)))


    def generate(self, prompt="You throw my pants at the monster, temporarily blinding it.", length=50, remove_prompt=False):
        # encode context the generation is conditioned on
        input_ids = self.tokenizer.encode(prompt, return_tensors='tf')

        sample_outputs = self.model.generate(
            input_ids,
            do_sample=True, 
            min_length=length, 
            max_length=min(2*length, 800),
            top_k=20, 
            top_p=0.92, 
            num_return_sequences=1,
            temperature=0.6,
            repetition_penalty=10
        )
        t = str(self.tokenizer.decode(sample_outputs[0], skip_special_tokens=True))
        if remove_prompt:
            t.replace(prompt, '', 1)
        return t

    def generateFiltered(self, prompt, sentence_count):
        doc = self.nlp(prompt)
        sentence_len = len(list(doc.sents))
        delta = ""
        while True:
            created = self.generate(prompt + delta, len(prompt + delta) + 50)
            doc = self.nlp(created.replace(prompt, '', 1))
            doc = self.sentences(created.replace(prompt, '', 1))[:1]  #EXTRACT 1 SENTENCE
            delta += ' '.join(map(str,doc))
            doc = self.nlp(delta)
            print(delta)
            if(len(list(doc.sents)) >= sentence_count):
                break
        return delta

    def generateResponse(self, prompt):
        return self.generateFiltered(prompt, 1)