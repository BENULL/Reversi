#!/usr/bin/python 
# -*- coding: utf-8 -*-

from board import Board
import itertools
import operator
import collections
from functools import reduce
from constant import Status
import time
import csv

class Reversi():

    _DIRECTIONS = [(1,0),(1,1),(1,-1),(-1,0),(-1,1),(-1,-1),(0,1),(0,-1)]

    def __init__(self, n, turn):
        self.n = n                                              # board dimension
        self.b = Board(n)                                       # board
        self.turn = 0 if turn == 'X' or turn == 'x' else 1      # player turn
        self.step = 1                                           # game step
        self.status = Status.WAIT                               # game status

    def isValidPosition(self,x,y):
        """检查位置的有效性
        Args:
            x:int
                行坐标
            y:int
                列坐标
        Returns:
            bool:  
        """

        return 0 <= x < self.n and 0 <= y < self.n
    
    def nextPosition(self,direction,x,y):
        """得到这个方向下一步坐标

        Args:
            direction:Tuple(int,int)
                移动的方向
            r:int
                行坐标
            c:int
                列坐标
        Returns:
            int,int:
                下一个位置的行坐标和列坐标
        """

        return x+direction[0],y+direction[1]
    
    def score(self,r,c):
        """得到落子在r,c处时需翻转的棋子坐标的集合
       
        Args:
            r:int
                行坐标
            c:int
                列坐标
        Returns:
            List(Tuple(int,int)):
                落子在r,c处时需翻转的棋子坐标的集合
        """

        return list(itertools.chain.from_iterable([self.scoreDirection(r+m[0],c+m[1],m,self.step%2+1,[]) for m in Reversi._DIRECTIONS]))

    def scoreDirection(self,x,y,direction,color,turn):
        """得到需要翻转的棋子坐标
       
        Args:
            x:int
                行坐标
            y:int
                列坐标
            direction:List(Tuple(int,int))
                移动的方向
            color:int
                落子的棋子颜色
            turn:List(Tuple(int,int))
                需翻转的棋子坐标的集合
        Returns:
            List(Tuple(int,int)):
                需翻转的棋子坐标的集合
        """

        if not self.isValidPosition(x,y) or self.b.board[x][y]==0 :
            return []
        if self.b.board[x][y]!=color:
            turn+=[(x,y)]
            return self.scoreDirection(*self.nextPosition(direction,x,y),direction,color,turn)
        else:
            return turn

    def checkPut(self, pos):
        """检查人落子是否有效
        Args:
            pos:Tuple(int,int)       
        Returns:
        Raises:
            AssertionError: 落子位置无效
        """

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
        """检查游戏状态
        Args:
        Returns:
        """
       
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
        """比较

        Args:
            a:List(Tuple(int,int),List(Tuple(int,int)))
            b:List(Tuple(int,int),List(Tuple(int,int)))
        Returns:
            返回List[1]长度大的，相等则返回行坐标小的，行坐标相等时返回列坐标小的
        """

        if len(a[1])>len(b[1]):
            return a 
        elif len(a[1])==len(b[1]) and a[0]<=b[0]:
            return a
        else:
            return b
          
    def aiPut(self):
        """得到电脑得落子位置和待翻转的棋子坐标集合

        有位置可下时返回最佳落子位置
        没有位置可以下时返回(),[]
        
        Args:
        Returns:
           Tuple(int,int)
            落子位置
           List(Tuple(int,int))
            待翻转的棋子坐标集合
        """

        allPos = filter(lambda pos : self.b.board[pos[0]][pos[1]]==0,itertools.product(range(self.n),repeat=2))
        allScoreForPos  = map(lambda pos: [pos,self.score(pos[0],pos[1])],allPos)
        maxScorePos = reduce(self.cmp,allScoreForPos,[(),[]])
        return maxScorePos[0],maxScorePos[1]

    def aiPlay(self):
        """
        电脑落子逻辑

        Args:
        Returns:
        """

        pos,turnList = self.aiPut()
        if turnList:
            print('Computer places {} at {}'.format(self.b.chess[self.step % 2+1],chr(pos[0]+97)+chr(pos[1]+97)))
            for x,y in turnList+[pos]:
                self.b.board[x][y] = self.step % 2+1
            reversi.b.draw()
            self.step += 1
            self.turn += 1

    def pPlay(self):
        """
        人落子逻辑

        Args:
        Returns:
        """

        pos = input('Enter move for {} (RowCol):'.format(self.b.chess[self.step % 2+1]))
        if self.checkPut(pos):
            reversi.b.draw()
            self.step += 1
            self.turn += 1
        else:
            print('Invalid move')

    def play(self):
        """
        控制游戏进程

        Args:
        Returns:
        """
        
        self.status = Status.ONGOING
        plays = [self.aiPlay,self.pPlay]
        while self.status == Status.ONGOING:
            plays[self.turn % len(plays)]()
            self.checkGame()
        else:
            print('Game over. {}'.format(Status(self.status)))

    def saveGameToCsv(self,startTime,endTime,turn,filename='Reversi.csv'):
        """
        记录游戏信息保存到csv文件

        Args:
            startTime:float
                游戏开始时间
            endTime:float
                游戏结束时间
            turn:str
                电脑执黑或白
        """
        
        start= time.strftime('%Y%m%d %H:%M:%S',time.localtime(startTime))
        duration = int(endTime - startTime)
        size = f'{self.n}*{self.n}'
        xPlayer,oPlayer = ('Computer','Human') if turn.lower() == 'x' else  ('Human','Computer')
        score = '{} to {}'.format(*operator.itemgetter(2,1)(collections.Counter(itertools.chain.from_iterable(self.b.board))))
        info = [start,duration,size,xPlayer,oPlayer,score]
        with open(f'./{filename}', 'a') as f:
            writer = csv.writer(f)
            writer.writerow(info)
        print(f'history has been saved to {filename}')



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
    startTime = time.time()
    reversi = Reversi(n, turn)
    # draw board
    reversi.b.draw()
    reversi.play()
    endTime = time.time()
    # save game info
    reversi.saveGameToCsv(startTime,endTime,turn)
    input('Enter to quit')