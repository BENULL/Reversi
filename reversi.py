#!/usr/bin/python 
# -*- coding: utf-8 -*-

from board import Board
import itertools
import operator
import collections
from functools import reduce
from constant import Status

class Reversi():

    _DIRECTIONS = [(1,0),(1,1),(1,-1),(-1,0),(-1,1),(-1,-1),(0,1),(0,-1)]

    def __init__(self, n, turn):
        self.n = n                                              # board dimension
        self.b = Board(n)                                       # board
        self.turn = 0 if turn == 'X' or turn == 'x' else 1      # player turn
        self.step = 1                                           # game step
        self.status = Status.WAIT                               # game status

    def isValidPosition(self,x,y):
        return 0 <= x < self.n and 0 <= y < self.n
    
    def nextPosition(self,direction,x,y):
        x+=direction[0]
        y+=direction[1]
        return x,y
    
    def score(self,r,c):
        return list(itertools.chain.from_iterable([self.scoreDirection(r+m[0],c+m[1],m,self.step%2+1,[]) for m in Reversi._DIRECTIONS]))

    def scoreDirection(self,x,y,direction,color,turn):
        if not self.isValidPosition(x,y) or self.b.board[x][y]==0 :
            return []
        if self.b.board[x][y]!=color:
            turn+=[(x,y)]
            return self.scoreDirection(*self.nextPosition(direction,x,y),direction,color,turn)
        else:
            return turn

    def checkPut(self, pos):
        # check person put
        assert len(pos)>=2 , 'move position disable'
        r = ord(pos[0]) - 97
        c = ord(pos[1]) - 97
        assert 0 <= r < self.n and 0 <= c < self.n, 'move position disable'
        turnList = self.score(r, c)
        if turnList:
            # turn chess
            for x,y in turnList+[(r,c)]:
                self.b.board[x][y] = self.step % 2+1
            return True
        else:
            return False

    def checkGame(self):
        # check game status
        empty,oNum,xNum = operator.itemgetter(0,1,2)(collections.Counter(itertools.chain.from_iterable(self.b.board)))
        hasPut = True
        pos,turnList = self.aiPut()
        if not turnList:
            self.step += 1
            posNext,turnListNext = self.aiPut()
            if not turnListNext:
                hasPut = False
            else:
                self.step -= 1
                print('{} player has no valid move'.format(self.b.chess[self.step % 2+1]))
                self.step -= 1
                self.turn -= 1
                print('{} player go on'.format(self.b.chess[self.step % 2+1]))
        if empty ==0 or oNum==0 or xNum == 0 or not hasPut:
            self.status = [Status.DRAW.value,Status.OWIN.value,Status.XWIN.value][(oNum > xNum)-(oNum<xNum)]
    
    def cmp(self,a,b):
        if len(a[1])>len(b[1]):
            return a 
        elif len(a[1])==len(b[1]) and a[0]<b[0]:
            return a
        else:
            return b
            
    def aiPut(self):
        # computer put
        allPos = filter(lambda pos : self.b.board[pos[0]][pos[1]]==0,itertools.product(range(self.n),repeat=2))
        allScoreForPos  = map(lambda pos: [pos,self.score(pos[0],pos[1])],allPos)
        maxScorePos = reduce(self.cmp,allScoreForPos,[(),[]])
        return maxScorePos[0],maxScorePos[1]

    def aiPlay(self):
        pos,turnList = self.aiPut()
        if turnList:
            print('Computer places {} at {}'.format(self.b.chess[self.step % 2+1],chr(pos[0]+97)+chr(pos[1]+97)))
            for x,y in turnList+[pos]:
                self.b.board[x][y] = self.step % 2+1
            reversi.b.draw()
            self.step += 1
            self.turn += 1

    def pPlay(self):
        pos = input('Enter move for {} (RowCol):'.format(self.b.chess[self.step % 2+1]))
        if self.checkPut(pos):
            reversi.b.draw()
            self.step += 1
            self.turn += 1
        else:
            print('Invalid move')

    def play(self):
        self.status = Status.ONGOING
        plays = [self.aiPlay,self.pPlay]
        while self.status == Status.ONGOING:
            plays[self.turn % len(plays)]()
            self.checkGame()
        else:
            print('Game over. {}'.format(Status(self.status)))

if __name__ == "__main__":
    print('Enter the board dimension:')
    try:
        n = int(input())
    except Exception as e:
        print('the board dimension is invalid, start game with default dimension = 4')
        n = 4
    assert 4 <= n <= 26 and n % 2 == 0, 'the board dimension is disable'
    print('Computer plays (X/O):')
    turn = input()
    assert turn in ['X','x','O', 'o'], 'the symbol of computer is disable'
    # generate game
    reversi = Reversi(n, turn)
    # draw board
    reversi.b.draw()
    reversi.play()
    input('Enter to quit')