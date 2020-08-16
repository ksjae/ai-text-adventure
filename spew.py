import tensorflow as tf
from transformers import GPT2LMHeadModel, GPT2Tokenizer, CTRLLMHeadModel, CTRLTokenizer
from spacy.lang.en import English
import torch
import random
import requests
from tqdm import trange

class Text():
    tokenizer = None
    model = None
    nlp = None
    sentencizer = None
    model_type = "GPT2"
    top_p = 0.9
    top_k = 5
    repetition_penalty = 1.7
    temperature=0.6

    def __init__(self, model_name="model", seed=42): # use HF model name
        if model_name == "ctrl":
            self.tokenizer = CTRLTokenizer.from_pretrained("ctrl")
            # add the EOS token as PAD token to avoid warnings
            self.model = CTRLLMHeadModel.from_pretrained("ctrl", pad_token_id=self.tokenizer.eos_token_id)
            self.model_type = 'CTRL'
        else:
            self.tokenizer = GPT2Tokenizer.from_pretrained(model_name)
            # add the EOS token as PAD token to avoid warnings
            self.model = GPT2LMHeadModel.from_pretrained(model_name, pad_token_id=self.tokenizer.eos_token_id)
        torch.manual_seed(seed)
        torch.cuda.manual_seed_all(seed)
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
        try:
            gen_text = req.json()[0]['generated_text']
        except KeyError:
            print(req.json())
            return "ERROR"
        return gen_text

    def generate(self, prompt="You throw pants at the monster, temporarily blinding it. The monster tries to attack you, but misses.", length=50, remove_prompt=False):
        # encode context the generation is conditioned on
        context = torch.tensor(self.tokenizer.encode(prompt), dtype=torch.long, device=torch.device("cuda" if torch.cuda.is_available() and not no_cuda else "cpu"))
        t = context.unsqueeze(0).repeat(1, 1)
        with torch.no_grad():
            for _ in trange(length):

                inputs = {'input_ids': t}
                outputs = self.model(**inputs)  # Note: we could also use 'past' with GPT-2/Transfo-XL/XLNet/CTRL (cached hidden-states)
                next_token_logits = outputs[0][:, -1, :] / (self.temperature if self.temperature > 0 else 1.)

                # repetition penalty from CTRL (https://arxiv.org/abs/1909.05858)
                for i in range(1):
                    for _ in set(t[i].tolist()):
                        next_token_logits[i, _] /= self.repetition_penalty

                if self.top_k > 0:
                    # Remove all tokens with a probability less than the last token of the top-k
                    indices_to_remove = next_token_logits < torch.topk(next_token_logits, self.top_k)[0][..., -1, None]
                    next_token_logits[indices_to_remove] = -float('Inf')

                if self.top_p > 0.0:
                    sorted_logits, sorted_indices = torch.sort(next_token_logits, descending=True)
                    cumulative_probs = torch.cumsum(torch.nn.functional.softmax(sorted_logits, dim=-1), dim=-1)

                    # Remove tokens with cumulative probability above the threshold
                    sorted_indices_to_remove = cumulative_probs > self.top_p
                    # Shift the indices to the right to keep also the first token above the threshold
                    sorted_indices_to_remove[..., 1:] = sorted_indices_to_remove[..., :-1].clone()
                    sorted_indices_to_remove[..., 0] = 0

                    # scatter sorted tensors to original indexing
                    indices_to_remove = sorted_indices_to_remove.scatter(dim=1, index=sorted_indices, src=sorted_indices_to_remove)
                    next_token_logits[indices_to_remove] = -float('Inf')
                next_token = torch.multinomial(torch.nn.functional.softmax(next_token_logits, dim=-1), num_samples=1)
                t = torch.cat((t, next_token), dim=1)
        t = t[:, len(t):].tolist()
        for o in t:
            text = self.tokenizer.decode(o, clean_up_tokenization_spaces=True)
            text = text[: None]
        
        if remove_prompt:
            text.replace(prompt, '', 1)
        return text

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