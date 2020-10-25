import random

class DiceRoll:
    def __init__(self, dicetype=20):
        self.raw = random.randint(1,dicetype)
        self.crit_miss = False
        self.crit_hit = False
        if self.raw == 1:
            self.crit_miss = True
        elif self.raw == 20:
            self.crit_hit = True
    def __call__(self, dicetype=20):
        self.raw = random.randint(1,dicetype)
        self.crit_miss = False
        self.crit_hit = False
        if self.raw == 1:
            self.crit_miss = True
        elif self.raw == 20:
            self.crit_hit = True