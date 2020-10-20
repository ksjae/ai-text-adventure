from ..interface import *

def test_initial_random_prompt():
    assert len(get_random_initial_prompt()) > 20