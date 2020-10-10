from ..utils import *

def test_dice():
    dice = DiceRoll(10)
    assert dice.raw <= 10
    if dice.raw != 10:
        assert dice.crit_hit == False
    elif dice.raw != 1:
        assert dice.crit_miss == False