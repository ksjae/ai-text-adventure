"""
I know this is not the best way. However, gettext does NOT work well with fstrings :(

Simply Copy-paste EN or Translation class and edit the inner contents to translate!
When translated, head over to github and give me a pull request.
If you don't know what github or pull requests are, just email the code to webmaster [at) ksjit.com
"""
import random

class Translation:
    fist: str
    bow: str
    lightning: str
    load: str
    supported_fantasy_types: list
    select_fantasy_type: str
    hello_msg: str
    save_howto: str
    simple_mode_prompt: str
    yes: str
    no: str
    bearing: list
    saving: str
    saved: str
    attack_with: str
    attack_where: str
    which_magic: str
    which_bow: str
    which_part: str
    fight_choice: list

    MOVE_MODE: str
    FIGHT_MODE: str
    TALK_MODE: str
    def actor_string(protagonist_explanation, protagonist_type):
        actor_string = f"이 이야기는 {random.choice(protagonist_explanation)} {random.choice(protagonist_type)}와 "
        actor_string += f"{random.choice(protagonist_explanation)} {random.choice(protagonist_type)}의 이야기이다.\n"
        return actor_string
    def story_start_string(story_begin, story_about, plot):
        return f"{random.choice(story_begin)} {random.choice(plot)} {random.choice(story_about)} 이야기가 시작된다."
    def story_start(story_type):
        return story_type, '이야기를 시작합니다.'
    def move_string(direction):
        return f"나는 {direction}쪽으로 이동했다."
    def attack_string(weapon, target='*'):
        choice = ""
        if target == '*':
            choice = f"나는 {weapon}으로 공격했다."
        elif target is not None:
            choice = f"나는 {weapon}으로 {target}을 공격했다."
        return choice
class EN(Translation):
    fist = 'fist'
    bow = 'bow'
    lightning = 'lightning'
    load = "Enter 'load'(without quotes) to load from save file(Press Enter to skip):"
    supported_fantasy_types = ["heroic","historical","medieval","sword & sorcery","comic","epic","dark","dystopian","realistic"]
    select_fantasy_type = 'Select the (fantasy) type you want:'
    hello_msg = "\n\nYou are now the main character, the narrator, the curator of the story. Enjoy and write down the story.\n\n"
    save_howto = "* Enter 'save'(without quotes) to save. Save on Exit is enabled."
    simple_mode_prompt = "Activate Simple Mode?"
    yes = "Yes"
    no = "No"
    bearing = ['north','south','east','west']
    fight_choice = ['Charge at enemy', 'Draw bow', 'Prepare magic', 'Ignore']
    saving = 'Saving...'
    saved = 'Saved.'
    attack_with='What will you attack with?'
    attack_where='Where would you attack?'
    which_magic='Which magic will you use?'
    which_bow='Which bow will you attack?'
    which_part='Aim where?'

    MOVE_MODE = "Move"
    FIGHT_MODE = "Fight"
    TALK_MODE = "Talk"


    def actor_string(protagonist_explanation, protagonist_type):
        actor_string = f"This story is about {random.choice(protagonist_type)} who {random.choice(protagonist_explanation)} and "
        actor_string += f"{random.choice(protagonist_type)} who {random.choice(protagonist_explanation)}\n"
        return actor_string
    def story_start_string(story_begin, story_about, plot):
        return f"It is a story about {random.choice(story_about)} The story begins {random.choice(story_begin)} with {random.choice(plot)}"
    def story_start(story_type):
        return 'Starting a', story_type, 'story.'
    def move_string(direction):
        return f"I moved {direction}"
    def attack_string(weapon, target='*'):
        choice = ""
        if target == '*':
            choice = f"I attacked with {weapon}"
        elif target is not None:
            choice = f"I attacked {target} with {weapon}"

class KO(Translation):
    fist = '주먹'
    bow = '활'
    lightning = '번개'
    load = '불러오려면 load를 입력해 주세요(건너뛰려면 Enter):'
    supported_fantasy_types = ["영웅","역사","중세","소드 앤 소서리","코믹","서사시","다크","디스토피아","현실주의적"]
    select_fantasy_type = '원하는 판타지 종류를 선택해 주세요:'
    hello_msg = "\n\n이제 당신은 이야기의 주인공이자 해설자, 진행자 입니다. 무슨 이야기가 이루어질지, 써내려 가면서 즐겨보세요.\n\n"
    save_howto = "※ 저장은 save를 입력하시면 됩니다. 프로그램 종료 시에도 저장됩니다."
    simple_mode_prompt = "선택지를 제공해드릴까요?"
    yes = "네"
    no = "아니오"
    bearing = ['동','서','남','북']
    fight_choice = ['달려들기','활 꺼내기','마법 준비하기','무시']
    saving = '저장 중...'
    saved = '[저장됨]'
    attack_with='무엇으로 공격하시겠습니까?'
    attack_where='어딜 공격하시겠습니까?'
    which_magic='어떤 마법을 이용하시겠습니까?'
    which_bow='무슨 활로 공격하시겠습니까?'
    which_part='무슨 부위를 공격하시겠습니까?'

    MOVE_MODE = "이동"
    FIGHT_MODE = "전투"
    TALK_MODE = "대화"

def initialize_translation(lang_code):
    if lang_code == 'ko':
        return KO
    return EN