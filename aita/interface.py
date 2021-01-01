from aita.customclass import *
from aita.generator import *
from aita.constants import *
from aita.translation import *
from aita.utils import Console
import os
import random
import sys
import time
import keyboard

console = Console()

def print_welcome():
    print('-'*80)
    print("AI Text Adventure PROTOTYPE A")

def get_choice(choices, skip_newline = False, return_choice_id = False):
    choice_num = 0
    while True:
        for i, choice in enumerate(choices):
            if i == choice_num:
                print(f" ⇨ {i+1}. {choice}", end='')
            else:
                print(f"   {i+1}. {choice}", end='')
            if not skip_newline:
                print('')
        console.flush()
        key = keyboard.read_key()
        keyboard.read_key()
        if key == 'down':
            choice_num += 1
            if choice_num == len(choices):
                choice_num = len(choices) - 1
        elif key == 'up':
            choice_num -= 1
            if choice_num < 0:
                choice_num = 0
        for _ in choices:
            sys.stdout.write(CURSOR_UP_ONE) 
            sys.stdout.write(ERASE_LINE)
        if key == 'enter':
            break
        try:
            choice_num = int(key) - 1
            break
        except:
            pass
    if return_choice_id:
        return choice_num
    sys.stdout.flush()
    return choices[choice_num]

def get_random_initial_prompt(LANG, translation: Translation):
    plot = open(os.path.join(DATA_PATH,LANG,'plot'),'r',encoding="utf-8").read().split('\n')
    protagonist_explanation = open(os.path.join(DATA_PATH,LANG,'protagonist_explanation'),'r',encoding="utf-8").read().split('\n')
    protagonist_type = open(os.path.join(DATA_PATH,LANG,'protagonist_type'),'r',encoding="utf-8").read().split('\n')
    story_about = open(os.path.join(DATA_PATH,LANG,'story_about'),'r',encoding="utf-8").read().split('\n')
    story_begin = open(os.path.join(DATA_PATH,LANG,'story_begin'),'r',encoding="utf-8").read().split('\n')

    actor_string = translation.actor_string(protagonist_explanation, protagonist_type)
    story_start_string = translation.story_start_string(story_begin, story_about, plot)

    return actor_string + story_start_string

def save():
    savefile = os.path.join(DATA_PATH,'savefile')
    with open(savefile,'w') as f:
        f.writelines(history)
    return

def load_save():
    savefile = os.path.join(DATA_PATH,'savefile')
    with open(savefile,'r') as f:
        history = f.readlines()
    return history

def run_adventure(flags, generator: Generator, translation: Translation):
    # Initial config
    global history
    history = []
    if input(translation.load) == 'load':
        history = load_save()
    else:
        supported_fantasy_types = translation.supported_fantasy_types
        
        print(translation.select_fantasy_type)
        story_type = get_choice(supported_fantasy_types)

        print(*translation.story_start(story_type))
        print('-'*80,'\n')

        init_prompt = get_random_initial_prompt(LANG, translation)
        print(init_prompt)
        print(translation.hello_msg)
    
    print(translation.save_howto)

    print(translation.simple_mode_prompt)
    flags.simple_mode = True if get_choice([translation.yes, translation.no]) == translation.yes else False
    sys.stdout.write(CURSOR_UP_ONE) 
    sys.stdout.write(ERASE_LINE)

    sys.stdout.flush()

    # INIT
    player = Actor()
    fist = Item()
    fist.give_name(translation.fist)
    fist.set_type(AttackType.melee)
    fist.delta_stat = Stat(1,1)
    player.add_item(fist)
    bow = Item()
    bow.give_name(translation.bow)
    bow.set_type(AttackType.ranged)
    bow.delta_stat = Stat(1,0,0)
    player.add_item(bow)
    lightning = Item()
    lightning.give_name(translation.bow)
    lightning.set_type(AttackType.magical)
    lightning.delta_stat = Stat(1,0,0)
    player.add_item(lightning)

    # Loop
    if flags.simple_mode:
        '''
        MOVE_MODE
        FIGHT_MODE
        TALK_MODE
        3가지로 나누어 구현
        '''

        fight_gen = FightSceneGen(translation)

        while True:
            mode = get_choice([translation.MOVE_MODE,translation.FIGHT_MODE,translation.TALK_MODE])
            if mode == translation.MOVE_MODE:
                choice = translation.move_string(get_choice(translation.bearing))
            elif mode == translation.FIGHT_MODE:
                weapon, target = fight_gen.get_fight_choice(player)
                choice = translation.attack_string(weapon, target)
            elif mode == translation.TALK_MODE:
                choice = f"\"{input('> ')}\""
            output = generator.from_prompt(choice)
            print(output)
            if output is not None:
                history.append(output + '\n')
        
    else:
        while True:
            keyboard.read_key()
            user_input = input('> ')
            if user_input == 'save':
                save()
                print('\n'+translation.saved+'\n')
                continue
            sys.stdout.write(CURSOR_UP_ONE) 
            sys.stdout.write(ERASE_LINE)
            output = generator.from_prompt(user_input,length=20)
            print(output)
            if output is not None:
                history.append(output + '\n')

def main(flags, generator=None):
    global LANG
    LANG = flags.LANG
    translation = initialize_translation(flags.LANG)
    print_welcome()
    try:
        run_adventure(flags, generator, translation)
    except KeyboardInterrupt:
        print(translation.saving)
        save()
        sys.exit()