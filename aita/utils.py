import random
import sys

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

class Console:
    def __init__(self): 
        try:
            import termios
            self.tcflush = termios.tcflush
            self.TCIFLUSH = termios.TCIFLUSH
            self.os = 'nix'
        except:
            import msvcrt
            self.msvcrt = msvcrt
            self.os = 'win'
            
    def flush(self):
        if self.os == 'win':
            while self.msvcrt.kbhit():
                self.msvcrt.getch()
        else:
            self.tcflush(sys.stdin, self.TCIFLUSH)
