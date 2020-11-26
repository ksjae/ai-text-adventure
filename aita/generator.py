import sys
import os
import argparse
import json
import re
import keyboard

from aita.customclass import *
from aita.constants import *
from aita.translation import Translation
from aita.utils import Console

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
    def __init__(self, model_path=HF_MODEL_PATH):
        from transformers import TFGPT2LMHeadModel, GPT2Tokenizer
        self.tokenizer = GPT2Tokenizer.from_pretrained(model_path)
        self.model = TFGPT2LMHeadModel.from_pretrained(model_path, pad_token_id=self.tokenizer.eos_token_id)
    def from_prompt(self, prompt="...", length=50, remove_prompt=False):
        if prompt is None:
            prompt = '. '
        input_ids = self.tokenizer.encode(prompt, return_tensors='tf')
        if input_ids is None:
            return ""
        sample_outputs = self.model.generate(
            input_ids,
            do_sample=True, 
            min_length=length, 
            max_length=min(2*length, 200),
            top_k=TOP_K, 
            top_p=TOP_P, 
            num_return_sequences=1,
            temperature=TEMPERATURE,
            repetition_penalty=10.0
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
        self.__choices.append(content)

    def add_choices_list(self, lst):
        self.__choices.extend(lst)

    def remove_choice_by_id(self, _id):
        try:
            self.__choices.pop(_id)
        except:
            raise NonExistent

    def remove_choice_by_name(self, name):
        try:
            self.__choices.remove(name)
        except:
            raise NonExistent

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
        console = Console()
        while True:
            self.print_choices(choice_num, skip_newline=skip_newline)
            console.flush()
            keyboard.read_key()
            if keyboard.is_pressed('down'):
                choice_num += 1
                if choice_num >= len(self.choices):
                    choice_num = len(self.choices) - 1
            elif keyboard.is_pressed('up'):
                choice_num -= 1
                if choice_num < 0:
                    choice_num = 0
            for i, _ in enumerate(self.choices):
                if keyboard.is_pressed(str(i+1)):
                    choice_num = i
                    if return_choice_id:
                        return choice_num
                    return self.choices[choice_num]
            for _ in self.choices:
                sys.stdout.write(CURSOR_UP_ONE) 
                sys.stdout.write(ERASE_LINE)
            if keyboard.is_pressed('enter'):
                break
        sys.stdout.flush()
        if return_choice_id:
            return choice_num
        return self.choices[choice_num]

class FightSceneGen(ChoiceGenerator):
    '''
    Inspired from Filip Hracek's method of fight render.
    '''
    def __init__(self, translation: Translation):
        super().__init__()
        self.translation = translation
        self.weapon_chooser = ChoiceGenerator()
        self.target_chooser = ChoiceGenerator()
        self.binary_chooser = ChoiceGenerator()
        part = ANATOMY
        self.target_chooser.add_choices_list([part.arm,part.leg,part.torso,part.head])
        self.binary_chooser.add_choices_list([self.translation.yes, self.translation.no])

    def find_weapon(self, item_list: list, attack_type: AttackType):
        weapons_avail = item_list
        for item in weapons_avail:
            if item.item_type == attack_type:
                weapons_avail.remove(item)
        return weapons_avail

    def get_physical_choice(self, actor: Actor):
        print(self.translation.attack_with)
        self.weapon_chooser.add_choices_list(self.find_weapon(actor.items, AttackType.melee))
        weapon = self.weapon_chooser.get_choice()

        print(self.translation.attack_where)
        target = self.target_chooser.get_choice()

        return weapon, target
    
    def get_magical_choice(self, actor: Actor):
        print(self.translation.which_magic)
        self.weapon_chooser.add_choices_list(self.find_weapon(actor.items, AttackType.magical))
        weapon = self.weapon_chooser.get_choice()
        if weapon.affetcs_area:
            target = '*'
        else:
            print(self.translation.attack_where)
            target = self.target_chooser.get_choice()

        return weapon, target

    def get_bow_choice(self, actor: Actor):
        print(self.translation.which_bow)
        self.weapon_chooser.add_choices_list(self.find_weapon(actor.items, AttackType.ranged))
        weapon = self.weapon_chooser.get_choice()

        print(self.translation.which_part)
        target = self.target_chooser.get_choice()

        return weapon, target

    def get_fight_choice(self, actor: Actor):
        chooser = ChoiceGenerator()
        chooser.add_choices_list(self.translation.fight_choice)
        choice = chooser.get_choice(return_choice_id=True)
        if choice == 1:
            return self.get_physical_choice(actor)
        elif choice == 2:
            return self.get_bow_choice(actor)
        elif choice == 3:
            return self.get_magical_choice(actor)
        else:
            return None, None
    
    def generate_action(self, actor: Actor, detail_level=0):
        '''
        Limelight-ish actor action description generator
        detail level 0 : ignore
        detail level 1 : 'swings knife'
        detail level 2 : 'stabs the rabbit in the eye'
        detail level 3 : 'stabs the rabbit in the eye. It tries to move, but hits a tree.'
        '''
        pass

class QuestSceneGen(ChoiceGenerator):
    '''
    Takes care of events after initiating talk from character to generating & adding quests
    '''
    def __init__(self):
        super().__init__()

    def get_choice(self):
        pass

class MerchantSceneGen(ChoiceGenerator):
    pass


class NPCGen():
    '''
    Generates NPCs.
    NPC: *All* default in-game character
    '''
    def __init__(self, **defaults):
        '''
        Initialize a NPC making factory - such as police, etc.
        '''
        pass
    def generate(self):
        return Actor()