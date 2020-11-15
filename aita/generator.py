import sys
import os
import argparse
import json
import re

from aita.customclass import *
from aita.constants import *


TOP_P = 0.9
TOP_K = 0 # 0 sets to greedy mode.
TEMPERATURE = 0.6
HF_MODEL_PATH = os.path.join(SCRIPT_PATH, '..','model')

class Generator:
    def from_prompt(self, prompt, length=20):
        '''
        The function taking care of actual text generation
        '''
        pass

class TFGenerator(Generator):
    def __init__(self):
        import tensorflow.compat.v1 as tf
        import numpy as np

        from .train.modeling import GroverModel, GroverConfig, sample
        from .tokenization import tokenization
        self.tokenizer = tokenization.FullTokenizer(vocab_file=os.path.join(SCRIPT_PATH, 'kotok'), do_lower_case=True)
        self.news_config = GroverConfig.from_json_file(os.path.join(SCRIPT_PATH, 'config','xl.json'))

        batch_size = 8
        max_batch_size = 4

        # factorize batch_size = (num_chunks * batch_size_per_chunk) s.t. batch_size_per_chunk < max_batch_size
        num_chunks = int(np.ceil(batch_size / max_batch_size))
        self.batch_size_per_chunk = int(np.ceil(batch_size / num_chunks))

        self.top_p = np.ones((num_chunks, batch_size_per_chunk), dtype=np.float32) * TOP_P

        tf_config = tf.ConfigProto(allow_soft_placement=True)
        self.tf_config.gpu_options.allow_growth = True

    def extract_generated_target(output_tokens, tokenizer):
        """
        Given some tokens that were generated, extract the target
        :param output_tokens: [num_tokens] thing that was generated
        :param encoder: how they were encoded
        :param target: the piece of metadata we wanted to generate!
        :return:
        """
        # Filter out first instance of start token
        assert output_tokens.ndim == 1

        start_ind = 0
        end_ind = output_tokens.shape[0]

        return tokenization.printable_text(tokenizer.convert_ids_to_tokens(output_tokens))
    
    def from_prompt(self, prompt, length=20):
        with tf.device('/device:XLA_GPU:0'):
            with tf.Session(config=tf_config, graph=tf.Graph()) as sess:
                initial_context = tf.placeholder(tf.int32, [self.batch_size_per_chunk, None])
                p_for_topp = tf.placeholder(tf.float32, [self.batch_size_per_chunk])
                eos_token = tf.placeholder(tf.int32, [])
                min_len = tf.placeholder(tf.int32, [])
                tokens, probs = sample(news_config=self.news_config, initial_context=initial_context,
                                    eos_token=eos_token, min_len=min_len, ignore_ids=None, p_for_topp=p_for_topp,
                                    do_topk=False)

                saver = tf.train.Saver()
                saver.restore(sess, tf.train.latest_checkpoint(tf.train.latest_checkpoint(os.path.join(SCRIPT_PATH, 'model'))))
                line = tokenization.convert_to_unicode(prompt)
                encoded = self.tokenizer.tokenize(line)
                context_formatted = []
                context_formatted.extend(encoded)
                # Format context end

                gens = []
                gens_raw = []
                gen_probs = []

                for chunk_i in range(self.num_chunks):
                    tokens_out, probs_out = sess.run([tokens, probs],
                                                    feed_dict={initial_context: [context_formatted] * self.batch_size_per_chunk,
                                                                eos_token: 50256, min_len: length,
                                                                p_for_topp: self.top_p[chunk_i]})

                    for t_i, p_i in zip(tokens_out, probs_out):
                        gens.append(extract_generated_target(output_tokens=t_i, tokenizer=self.tokenizer))

                l = re.findall('.{1,70}', gens[0].replace('<|endoftext|>', '').replace('|>', ''))
            return " ".join(l)
        return None

class HFGenerator:
    def __init__(self):
        from transformers import GPT2LMHeadModel, GPT2Tokenizer
        self.tokenizer = GPT2Tokenizer.from_pretrained(os.path.join(SCRIPT_PATH, 'kotok'))
        # add the EOS token as PAD token to avoid warnings
        self.model = GPT2LMHeadModel.from_pretrained(HF_MODEL_PATH, pad_token_id=self.tokenizer.eos_token_id)
    def generate(self, prompt="...", length=50, remove_prompt=False):
        # encode context the generation is conditioned on
        input_ids = self.tokenizer.encode(prompt, return_tensors='tf')
        sample_outputs = self.model.generate(
            input_ids,
            do_sample=True, 
            min_length=length, 
            max_length=min(2*length, 800),
            top_k=TOP_K, 
            top_p=TOP_P, 
            num_return_sequences=1,
            temperature=TEMPERATURE,
            repetition_penalty=10
        )
        output_text = str(self.tokenizer.decode(sample_outputs[0], skip_special_tokens=True))
        output_text = output_text.split('.')[:-1]
        output_text = '.'.join(output_text) + '.'
        return output_text

class ChoiceGenerator:
    '''
    Class for creating interface contents
    '''
    def __init__(self):
        self.__choices = []

    def add_choice(self, content):
        pass

    def remove_choice_by_id(self, id):
        pass

    def remove_choice_by_name(self, name):
        pass

    @property
    def choices(self):
        return self.__choices

    def print_choices(self, choice_num, skip_newline=False):
        for i, choice in enumerate(self.choices):
            if i == choice_num:
                print(f" ⇨ {i+1}. {choice}", end='')
            else:
                print(f"   {i+1}. {choice}", end='')
            if not skip_newline:
                print('')

    def get_choice(self, skip_newline=False, return_choice_id = False):
        choice_num = 0
        while True:
            self.print_choices(choice_num, skip_newline=skip_newline)
            rawinput = click.getchar()
            if rawinput == '\x0D':
                break
            if rawinput == KEY_DOWN:
                choice_num += 1
                if choice_num >= len(self.choices):
                    choice_num = len(self.choices) - 1
            elif rawinput == KEY_UP:
                choice_num -= 1
                if choice_num < 0:
                    choice_num = 0
            for _ in choices:
                sys.stdout.write(CURSOR_UP_ONE) 
                sys.stdout.write(ERASE_LINE) 
        if return_choice_id:
            return choice_num
        return self.choices[choice_num]

class FightSceneGen(ChoiceGenerator):
    '''
    Inspired from Filip Hracek's method of fight render.
    '''
    pass

class QuestSceneGen(ChoiceGenerator):
    '''
    Takes care of events after initiating talk from character to generating & adding quests
    '''
    pass

class MerchantSceneGen(ChoiceGenerator):
    pass