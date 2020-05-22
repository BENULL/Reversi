
#!/usr/bin/python 
# -*- coding: utf-8 -*-

from enum import Enum

_STATUS = {0: 'wait the game to start',
           1: 'in the game',
           2: 'someone fouls in the game',
           3: 'X player wins!',
           4: 'O player wins!',
           5: 'DRAW!'}

class Status(Enum):

    WAIT = 0
    ONGOING = 1
    FOUL = 2
    XWIN = 3
    OWIN = 4
    DRAW = 5

    def __str__(self):
        return str(_STATUS[self.value])
