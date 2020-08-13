import tensorflow as tf
from transformers import TFGPT2LMHeadModel, GPT2Tokenizer, CTRLLMHeadModel, CTRLTokenizer
from spacy.lang.en import English
import torch
import random
import requests

class Text():
    tokenizer = None
    model = None
    nlp = None
    sentencizer = None
    model_type = "GPT2"
    def __init__(self, model_name="gpt2-large", seed=42): # use HF model name
        if model_name == "ctrl":
            self.tokenizer = CTRLTokenizer.from_pretrained("ctrl")
            # add the EOS token as PAD token to avoid warnings
            self.model = CTRLLMHeadModel.from_pretrained("ctrl", pad_token_id=self.tokenizer.eos_token_id)
            self.model_type = 'CTRL'
        else:
            self.tokenizer = GPT2Tokenizer.from_pretrained(model_name)
            # add the EOS token as PAD token to avoid warnings
            self.model = TFGPT2LMHeadModel.from_pretrained(model_name, pad_token_id=self.tokenizer.eos_token_id)
        tf.random.set_seed(seed)
        self.nlp = English()
        self.nlp.add_pipe(self.nlp.create_pipe('sentencizer'))

    def sentences(self, string):
        '''
        Divide string into a array of str(sentence)
        '''
        doc = self.nlp(string)
        return list(map(str,list(doc.sents)))

    def generate_from_api(self, prompt, url="https://api-inference.huggingface.co/models/gpt2-large"):
        req = requests.post(url, data=f'"{prompt}"') #Needs double quotes
        gen_text = req.json()['generated_text']
        return gen_text

    def generate(self, prompt="You throw pants at the monster, temporarily blinding it. The monster tries to attack you, but misses.", length=50, remove_prompt=False):
        # encode context the generation is conditioned on
        input_ids = self.tokenizer.encode(prompt, return_tensors='tf')
        if self.model_type is 'GPT2':
            sample_outputs = self.model.generate(
                input_ids,
                do_sample=True, 
                min_length=length, 
                max_length=max(2*length, 100),
                top_k=0, 
                top_p=0.9, 
                num_return_sequences=1,
                temperature=0.6,
                repetition_penalty=3
            )
            t = str(self.tokenizer.decode(sample_outputs[0], skip_special_tokens=True))
        elif self.model_type == 'CTRL':
            input_ids = torch.tensor(self.tokenizer.encode("Links "+prompt, add_special_tokens=True)).unsqueeze(0)  # Batch size 1
            sample_outputs = self.model(input_ids, labels=input_ids)
            #print(sample_outputs)
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

class Dice():
    def __init__(self, seed=2837):
        random.seed(seed)
    def lean_roll(self, min_value, max_value, lean):
        if lean < 0.5:
            beta=5
            alpha=9*lean+0.5
        else:
            alpha=5
            beta=9*lean+0.5
        p = random.betavariate(alpha, beta)
        return min_value * (1-p) + max_value*p
    def roll(self, min_value, max_value):
        return random.choice([i for i in range(min_value, max_value+1)])