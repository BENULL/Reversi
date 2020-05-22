#!/usr/bin/python 
# -*- coding: utf-8 -*-

class Board():
    def __init__(self, n):
        self.n = n
        self.board = self.generateBoard()
        self.chess = {0: '.', 1: 'O', 2: 'X'}

    def generateBoard(self):
        # 0 empty 1 white 2 black
        i = int(self.n / 2)
        board = [[0] * self.n for _ in range(self.n)]
        board[i][i]=board[i-1][i-1] = 1
        board[i][i-1]=board[i-1][i] = 2
        return board

    def draw(self):
        index = 'abcdefghijklmnopqrstuvwxyz'
        print(' ',*index[:self.n])
        for h,row in zip(index,self.board):
            print(h,*map('.OX'.__getitem__,row))
        print()