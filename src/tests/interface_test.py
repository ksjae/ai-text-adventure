from ..interface import *

def test_initial_random_prompt():
    assert get_random_initial_prompt() is not None