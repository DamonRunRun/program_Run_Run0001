# -*- coding: utf-8 -*-
"""
Created on Sat Apr  9 15:59:20 2022

@author: 44741
"""

def update_map(Person_info,my_board):
    for x in range(0,len(Person_info)):
        for y in range(0,len(Person_info[x])):
            healthpoint = Person_info[x][y][2]
            if healthpoint < 256 and healthpoint > 0 :
                my_board[x,y] = [healthpoint,0,0]
            elif healthpoint < 1:
                my_board[x,y] = [255,255,255]
            if Person_info[x][y][5] == True and healthpoint >255:
                my_board[x,y] = [0,0,255]    