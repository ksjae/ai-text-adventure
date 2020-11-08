from aita.customclass import *
from aita.generator import *
from aita.constants import *
import os
import random
import sys
import time

DATA_PATH = os.path.join(SCRIPT_PATH,'data')
LANG = 'ko' # TODO: Lang selection

def print_welcome():
    print('-'*80)
    print("AI Text Adventure PROTOTYPE A")

def print_choices(choices, skip_newline = False):
    while True:
        for i, choice in enumerate(choices):
            print(f"{i}. {choice}", end='')
            if not skip_newline:
                print('')
        rawinput = input()
        try:
            input_num = int(rawinput)
            rawinput = choices[input_num]
        except:
            if rawinput in choices:
                pass
            else:
                print("잘못된 선택입니다.")
        return rawinput

def get_random_initial_prompt():
    plot = open(os.path.join(DATA_PATH,LANG,'plot')).read().split('\n')
    protagonist_explanation = open(os.path.join(DATA_PATH,LANG,'protagonist_explanation')).read().split('\n')
    protagonist_type = open(os.path.join(DATA_PATH,LANG,'protagonist_type')).read().split('\n')
    story_about = open(os.path.join(DATA_PATH,LANG,'story_about')).read().split('\n')
    story_begin = open(os.path.join(DATA_PATH,LANG,'story_begin')).read().split('\n')
    
    actor_string = f"이 이야기는 {random.choice(protagonist_explanation)}한 {random.choice(protagonist_type)}와 "
    actor_string += f"{random.choice(protagonist_explanation)}한 {random.choice(protagonist_type)}의 이야기이다.\n"
    story_start_string = f"{random.choice(story_about)}에 대해 {random.choice(plot)} {random.choice(story_begin)}(으)로 시작한다."

    return actor_string + story_start_string

def run_adventure():
    # Initial config
    print("1) 수동으로 새 게임 만들기\n2) 자동으로 새 게임 만들기\n3) 불러오기")
    
    supported_fantasy_types = ["영웅","역사","중세","소드 앤 소서리","코믹","서사시","다크","디스토피아","현실주의적"]
    
    print("원하는 판타지 종류를 선택해 주세요:")
    print_choices(supported_fantasy_types)

    print('이야기를 시작합니다.')
    print(get_random_initial_prompt())
    
    # Loop
    while True:
        user_input = input('> ')
        print("Placeholder for data generated from prompt", user_input)

def main(flags):
    print_welcome()
    try:
        run_adventure()
    except KeyboardInterrupt:
        print("\nBye.")
        sys.exit()