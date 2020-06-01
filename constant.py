
#!/usr/bin/python 
# -*- coding: utf-8 -*-

from enum import Enum


class Status(Enum):

    WAIT = 0
    ONGOING = 1
    FOUL = 2
    XWIN = 3
    OWIN = 4
    DRAW = 5

    def __str__(self):
        return str(_STATUS[self.value])

_STATUS = {Status.WAIT.value: 'wait the game to start',
           Status.ONGOING.value: 'in the game',
           Status.FOUL.value: 'someone fouls in the game',
           Status.XWIN.value: 'X player wins!',
           Status.OWIN.value: 'O player wins!',
           Status.DRAW.value: 'DRAW!'}