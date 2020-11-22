from aita.customclass import *
from aita.generator import *
from aita.constants import *
from aita.translation import *
from termios import tcflush, TCIOFLUSH
import os
import random
import sys
import time
import click

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
        tcflush(sys.stdin, TCIFLUSH)
        rawinput = click.getchar()
        if rawinput == '\x0D':
            break
        if rawinput == KEY_DOWN:
            choice_num += 1
            if choice_num >= len(choices):
                choice_num = len(choices) - 1
        elif rawinput == KEY_UP:
            choice_num -= 1
            if choice_num < 0:
                choice_num = 0
        for _ in choices:
            sys.stdout.write(CURSOR_UP_ONE) 
            sys.stdout.write(ERASE_LINE) 
    if return_choice_id:
        return choice_num
    for _ in choices:
            sys.stdout.write(CURSOR_UP_ONE) 
            sys.stdout.write(ERASE_LINE)
    sys.stdout.flush()
    return choices[choice_num]

def get_random_initial_prompt(LANG='ko'):
    plot = open(os.path.join(DATA_PATH,LANG,'plot')).read().split('\n')
    protagonist_explanation = open(os.path.join(DATA_PATH,LANG,'protagonist_explanation')).read().split('\n')
    protagonist_type = open(os.path.join(DATA_PATH,LANG,'protagonist_type')).read().split('\n')
    story_about = open(os.path.join(DATA_PATH,LANG,'story_about')).read().split('\n')
    story_begin = open(os.path.join(DATA_PATH,LANG,'story_begin')).read().split('\n')
    
    if LANG == 'ko':
        actor_string = f"이 이야기는 {random.choice(protagonist_explanation)} {random.choice(protagonist_type)}와 "
        actor_string += f"{random.choice(protagonist_explanation)} {random.choice(protagonist_type)}의 이야기이다.\n"
        story_start_string = f"{random.choice(story_begin)} {random.choice(plot)} {random.choice(story_about)} 이야기가 시작된다."

    elif LANG == 'en':
        actor_string = f"The story is about {random.choice(protagonist_type)} who {random.choice(protagonist_explanation)} and "
        actor_string += f"{random.choice(protagonist_type)} who {random.choice(protagonist_explanation)}\n"
        story_start_string = f"It is a story about {random.choice(story_about)} The story begins {random.choice(story_begin)} {random.choice(plot)}"

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
    if input("불러오려면 load를 입력해 주세요(건너뛰려면 Enter):") == 'load':
        history = load_save()
    else:
        supported_fantasy_types = ["영웅","역사","중세","소드 앤 소서리","코믹","서사시","다크","디스토피아","현실주의적"]
        
        print("원하는 판타지 종류를 선택해 주세요:")
        story_type = get_choice(supported_fantasy_types)

        print(story_type, '이야기를 시작합니다.')
        print('-'*80,'\n')

        init_prompt = get_random_initial_prompt(LANG)
        print(init_prompt)
        print("\n\n이제 당신은 이야기의 주인공이자 해설자, 진행자 입니다.")
        print("무슨 이야기가 이루어질지, 써내려 가면서 즐겨보세요.\n\n")
    
    print("※ 저장은 save를 입력하시면 됩니다. 프로그램 종료 시에도 저장됩니다.")

    print("선택지를 제공해드릴까요?")
    flags.simple_mode = True if get_choice([YES,NO]) == YES else False
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

        fight_gen = FightSceneGen()

        while True:
            mode = get_choice([MOVE_MODE,FIGHT_MODE,TALK_MODE])
            if mode == MOVE_MODE:
                available_ways = ['동','서','남','북']
                choice = f"나는 {get_choice(available_ways)}쪽으로 이동했다."
            elif mode == FIGHT_MODE:
                weapon, target = fight_gen.get_fight_choice(player)
                if target == '*':
                    choice = f"나는 {weapon}으로 공격했다."
                elif target is not None:
                    choice = f"나는 {weapon}으로 {target}을 공격했다."
            elif mode == TALK_MODE:
                choice = f"\"{input('> ')}\""
            output = generator.from_prompt(choice)
            print(output)
            if output is not None:
                history.append(output + '\n')
        
    else:
        while True:
            user_input = input('> ')
            if user_input == 'save':
                save()
                print('\n저장됨.\n')
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
        print("\n저장 중...")
        save()
        sys.exit()