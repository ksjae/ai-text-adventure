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

    def generate(self, prompt="You throw my pants at the monster, temporarily blinding it.", length=50):
        # encode context the generation is conditioned on
        input_ids = self.tokenizer.encode(prompt, return_tensors='tf')

        sample_outputs = self.model.generate(
            input_ids,
            do_sample=True, 
            max_length=length, 
            top_k=50, 
            top_p=0.95, 
            num_return_sequences=1
        )

        return str(self.tokenizer.decode(sample_outputs[0], skip_special_tokens=True))