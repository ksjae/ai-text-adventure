"""
I know this is not the best way. However, gettext does NOT work well with fstrings :(
"""
import random

class Translation:
    fist: str
    bow: str
    lightning: str
    def actor_string(self, protagonist_explanation, protagoinst_type):
        return ""
    def story_start_string(self, story_begin, story_about, plot):
        return ""
class EN:
    fist = 'fist'
    bow = 'bow'
    lightning = 'lightning'
    def actor_string(self, protagonist_explanation, protagoinst_type):
        actor_string = f"이 이야기는 {random.choice(protagonist_explanation)} {random.choice(protagonist_type)}와 "
        actor_string += f"{random.choice(protagonist_explanation)} {random.choice(protagonist_type)}의 이야기이다.\n"
        return actor_string

class KO:
    fist = '주먹'
    bow = '활'
    lightning = '번개'
    def actor_string(self, protagonist_explanation, protagoinst_type):
        actor_string = f"이 이야기는 {random.choice(protagonist_explanation)} {random.choice(protagonist_type)}와 "
        actor_string += f"{random.choice(protagonist_explanation)} {random.choice(protagonist_type)}의 이야기이다.\n"
        return actor_string

def initialize_translation(lang_code):
    if lang_code == 'ko':
        return KO
    return EN