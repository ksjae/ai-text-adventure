import sys
import os
import argparse
import json
import re

from .customclass import *


PROJ_ROOT = os.path.dirname(os.path.dirname(os.path.realpath(__file__)))
TOP_P = 0.9
TOP_K = 0 # 0 sets to greedy mode.
TEMPERATURE = 0.6
HF_MODEL_PATH = os.path.join(PROJ_ROOT, '..','model')

class Generator:
    def from_prompt(prompt, length=20):
        '''
        The function taking care of actual generation
        '''
        pass

class TFGenerator(Generator):
    def __init__(self):
        import tensorflow.compat.v1 as tf
        import numpy as np

        from .train.modeling import GroverModel, GroverConfig, sample
        from .tokenization import tokenization
        self.tokenizer = tokenization.FullTokenizer(vocab_file=os.path.join(PROJ_ROOT, 'kotok'), do_lower_case=True)
        self.news_config = GroverConfig.from_json_file(os.path.join(PROJ_ROOT, 'config','xl.json'))

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

        return {
            'extraction': tokenization.printable_text(tokenizer.convert_ids_to_tokens(output_tokens)),
            'start_ind': start_ind,
            'end_ind': end_ind,
        }
    
    def from_prompt(prompt, length=20):
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
                saver.restore(sess, tf.train.latest_checkpoint(tf.train.latest_checkpoint(os.path.join(PROJ_ROOT, 'model'))))
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
                        extraction = extract_generated_target(output_tokens=t_i, tokenizer=self.tokenizer)
                        gens.append(extraction['extraction'])

                l = re.findall('.{1,70}', gens[0].replace('<|endoftext|>', '').replace('|>', ''))
            return " ".join(l)
        return None

class HFGenerator:
    def __init__(self):
        from transformers import GPT2LMHeadModel, GPT2Tokenizer, CTRLLMHeadModel, CTRLTokenizer
        import torch
        self.tokenizer = GPT2Tokenizer.from_pretrained(os.path.join(PROJ_ROOT, 'kotok'))
        # add the EOS token as PAD token to avoid warnings
        self.model = GPT2LMHeadModel.from_pretrained(HF_MODEL_PATH, pad_token_id=self.tokenizer.eos_token_id)
    def generate(self, prompt="You throw my pants at the monster, temporarily blinding it.", length=50, remove_prompt=False):
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