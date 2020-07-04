import tensorflow as tf
from transformers import TFGPT2LMHeadModel, GPT2Tokenizer

class Text():
    tokenizer = None
    model = None
    def __init__(self, seed=42):
        self.tokenizer = GPT2Tokenizer.from_pretrained("gpt2-xl")
        # add the EOS token as PAD token to avoid warnings
        self.model = TFGPT2LMHeadModel.from_pretrained("gpt2-xl", pad_token_id=self.tokenizer.eos_token_id)
        tf.random.set_seed(42)

    def generate(self, prompt="You throw my pants at the monster, temporarily blinding it.", length=50, remove_prompt=False):
        # encode context the generation is conditioned on
        input_ids = self.tokenizer.encode(prompt, return_tensors='tf')

        sample_outputs = self.model.generate(
            input_ids,
            do_sample=True, 
            min_length=length, 
            max_length=min(2*length, 800),
            top_k=20, 
            top_p=0.95, 
            num_return_sequences=1,
            temperature=0.3,
            repetition_penalty=10
        )
        t = str(self.tokenizer.decode(sample_outputs[0], skip_special_tokens=True))
        if remove_prompt:
            t.replace(prompt, '', 1)
        return t