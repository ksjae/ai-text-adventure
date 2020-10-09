'''
import sys
import os
import argparse
import json
import re

import tensorflow.compat.v1 as tf
import numpy as np

from .train.modeling import GroverModel, GroverConfig, sample
from .tokenization import tokenization
from .customclass import *

##### ignore tf deprecated warning temporarily
os.environ['TF_CPP_MIN_LOG_LEVEL'] = '3'
tf.logging.set_verbosity(tf.logging.DEBUG)
from tensorflow.python.util import deprecation
deprecation._PRINT_DEPRECATION_WARNINGS = False
try:
    from tensorflow.python.util import module_wrapper as deprecation
except ImportError:
    from tensorflow.python.util import deprecation_wrapper as deprecation
deprecation._PER_MODULE_WARNING_LIMIT = 0
#####

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

proj_root_path = os.path.dirname(os.path.dirname(os.path.realpath(__file__)))
tokenizer = tokenization.FullTokenizer(vocab_file=os.path.join(proj_root_path, 'kotok'), do_lower_case=True)
news_config = GroverConfig.from_json_file(os.path.join(proj_root_path, 'config','xl.json'))

batch_size = 8
max_batch_size = 4

# factorize batch_size = (num_chunks * batch_size_per_chunk) s.t. batch_size_per_chunk < max_batch_size
num_chunks = int(np.ceil(batch_size / max_batch_size))
batch_size_per_chunk = int(np.ceil(batch_size / num_chunks))

top_p = 0.9
top_p = np.ones((num_chunks, batch_size_per_chunk), dtype=np.float32) * top_p

tf_config = tf.ConfigProto(allow_soft_placement=True)
tf_config.gpu_options.allow_growth = True

class Generator:
    def from_prompt(prompt, length=20):
        with tf.device('/device:XLA_GPU:0'):
            with tf.Session(config=tf_config, graph=tf.Graph()) as sess:
                initial_context = tf.placeholder(tf.int32, [batch_size_per_chunk, None])
                p_for_topp = tf.placeholder(tf.float32, [batch_size_per_chunk])
                eos_token = tf.placeholder(tf.int32, [])
                min_len = tf.placeholder(tf.int32, [])
                tokens, probs = sample(news_config=news_config, initial_context=initial_context,
                                    eos_token=eos_token, min_len=min_len, ignore_ids=None, p_for_topp=p_for_topp,
                                    do_topk=False)

                saver = tf.train.Saver()
                saver.restore(sess, tf.train.latest_checkpoint(tf.train.latest_checkpoint(os.path.join(proj_root_path, 'model'))))
                line = tokenization.convert_to_unicode(prompt)
                encoded = tokenizer.tokenize(line)
                context_formatted = []
                context_formatted.extend(encoded)
                # Format context end

                gens = []
                gens_raw = []
                gen_probs = []

                for chunk_i in range(num_chunks):
                    tokens_out, probs_out = sess.run([tokens, probs],
                                                    feed_dict={initial_context: [context_formatted] * batch_size_per_chunk,
                                                                eos_token: 50256, min_len: length,
                                                                p_for_topp: top_p[chunk_i]})

                    for t_i, p_i in zip(tokens_out, probs_out):
                        extraction = extract_generated_target(output_tokens=t_i, tokenizer=tokenizer)
                        gens.append(extraction['extraction'])

                l = re.findall('.{1,70}', gens[0].replace('<|endoftext|>', '').replace('|>', ''))
            return " ".join(l)
        return None
    def fight_prompt(opponent):
        return None
        
'''