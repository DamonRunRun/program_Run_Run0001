# -*- coding: utf-8 -*-
"""
Created on Wed Mar 30 23:30:41 2022

@author: nicko
"""

from numpy.random import random, randint
import numpy as np
healthpoint = 0

#Person_info is used to record the patient's coordinates, healthpoint, remaining incubation days, whether it has been infected or not, and the spread range; the array is a two-dimensional array, which is easy to understand
#The program finally judges that all points are blue (0, 0, 255) or black (0, 0, 0), green (0, 255, 0) to end
#Initialize the map
def init_map():
    my_board = np.zeros((50, 50, 3), np.uint8)
    Person_info = []
    for i in range(50):
        my_line =[]
        for j in range(50):
            #for k in range(3):
                my_board[i,j] = [0,255,0]
                healthpoint = randint(256,300)
                my_line.append([i,j,healthpoint,10,10,False])
        Person_info.append(my_line)
        
    return my_board,Person_info

#caculate the remaining incubation days
def person_information(x,y,healthpoint,has_record):
    #for x in range(0,len(Person_info)):
        #for y in range(0,len(Person_info[x])):
             # 180 is the base，the difference between the standard and the health point divide by 10, the quotient is the incubation days
             #Person_info[x][y] = [x,y,healthpoint,0,0]             
             #healthpoint = Person_info[x][y][2]
             if healthpoint > 0:
                 incubation= (healthpoint-180)//10
             else:
                 incubation = 0
                 
             # 扩散范围           
             if healthpoint < 256 and healthpoint > 0:
                 area = healthpoint // 50
                 has_record = True
             else:                 
                 area = 0
             Person_info[x][y] = [Person_info[x][y][0],Person_info[x][y][1],healthpoint,incubation,area,has_record]
                      
             return Person_info
