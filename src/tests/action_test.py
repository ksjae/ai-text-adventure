from ..customclass import *
from ..actions import *

def test_attack(target, anatomy_part):
    character1 = Actor()
    character2 = Actor()
    attack(character1, character2, 'arm')

