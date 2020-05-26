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
        '''check the positions 

        Args:
            x:int
                the row index
            y:int
                the col index
        Returns:
            bool:
                the position valid or invalid
        '''
        return 0 <= x < self.n and 0 <= y < self.n
    
    def nextPosition(self,direction,x,y):
        '''the next positions to move

        Args:
            direction:[(int,int),]
                the directions to move
            r:int
                the row index
            c:int
                the col index
        Returns:
            int,int:
                the position's row index and col index
        '''
        return x+direction[0],y+direction[1]
    
    def score(self,r,c):
        '''get the positions to be flipped when put in r,c
       
        Args:
            r:int
                the row index
            c:int
                the col index
        Returns:
            List:
                the list has the position of the pieces to be flipped if put the chess in r,c
        '''

        return list(itertools.chain.from_iterable([self.scoreDirection(r+m[0],c+m[1],m,self.step%2+1,[]) for m in Reversi._DIRECTIONS]))

    def scoreDirection(self,x,y,direction,color,turn):
        '''find the positions to flipped
       
        Args:
            x:int
                the row index
            y:int
                the col index
            direction:[(int,int),]
                eight directions to move
            color:int
                the color of chess to put
            turn:[(int,int),]
                the positions to flipped
        Returns:
            [(int,int),]:
                the positions to flipped
        '''

        if not self.isValidPosition(x,y) or self.b.board[x][y]==0 :
            return []
        if self.b.board[x][y]!=color:
            turn+=[(x,y)]
            return self.scoreDirection(*self.nextPosition(direction,x,y),direction,color,turn)
        else:
            return turn

    def checkPut(self, pos):
        '''check person's put

        Args:
            pos:(int,int)
                check the position where person put 
        Returns:
        Raises:
            AssertionError: move position disable
        '''

        assert len(pos)>=2 , 'move position disable'
        r = ord(pos[0]) - 97
        c = ord(pos[1]) - 97
        assert 0 <= r < self.n and 0 <= c < self.n, 'move position disable'
        turnList = self.score(r, c)
        if turnList:
            for x,y in turnList+[(r,c)]:
                self.b.board[x][y] = self.step % 2+1
            return True
        else:
            return False

    def checkGame(self):
        '''check game status
        check the game to set status
        Args:
        Returns:
        '''
       
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
        '''compare a and b 

        Args:
            a:[(int,int),[(int,int),]]
            b:[(int,int),[(int,int),]]
        Returns:

        '''
        if len(a[1])>len(b[1]):
            return a 
        elif len(a[1])==len(b[1]) and a[0]<b[0]:
            return a
        else:
            return b
            
    def aiPut(self):
        '''get the location of the computer's put and the location of the pieces to be filpped

        If there's no place to put return (),[]
        else return the best pos to put

        Args:
        Returns:
           a: (int,int)
            the position to put
           b:[(int,int),]
            the position of the pieces to be flipped
        '''
        allPos = filter(lambda pos : self.b.board[pos[0]][pos[1]]==0,itertools.product(range(self.n),repeat=2))
        allScoreForPos  = map(lambda pos: [pos,self.score(pos[0],pos[1])],allPos)
        maxScorePos = reduce(self.cmp,allScoreForPos,[(),[]])
        return maxScorePos[0],maxScorePos[1]

    def aiPlay(self):
        '''
        the computer's turn to play chess

        Args:
        Returns:
        '''
        pos,turnList = self.aiPut()
        if turnList:
            print('Computer places {} at {}'.format(self.b.chess[self.step % 2+1],chr(pos[0]+97)+chr(pos[1]+97)))
            for x,y in turnList+[pos]:
                self.b.board[x][y] = self.step % 2+1
            reversi.b.draw()
            self.step += 1
            self.turn += 1

    def pPlay(self):
        '''
        the person's turn to play chess

        Args:
        Returns:
        '''
        pos = input('Enter move for {} (RowCol):'.format(self.b.chess[self.step % 2+1]))
        if self.checkPut(pos):
            reversi.b.draw()
            self.step += 1
            self.turn += 1
        else:
            print('Invalid move')

    def play(self):
        '''
        control the game progress

        Args:
        Returns:
        '''
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