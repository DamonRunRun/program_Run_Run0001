# -*- coding: utf-8 -*-
"""
Created on Tue Mar 22 14:45:15 2022

@author: nicko
"""

#import time
#from IPython import display
import matplotlib.pyplot as plt
#import matplotlib.animation as animation
import numpy as np
from numpy.random import random, randint

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
                 
             # spread area        
             if healthpoint < 256 and healthpoint > 0:
                 area = healthpoint // 50
                 has_record = True
             else:                 
                 area = 0
             Person_info[x][y] = [Person_info[x][y][0],Person_info[x][y][1],healthpoint,incubation,area,has_record]
                      
             return Person_info
         

#Choose two random infactor
def rand_infector(my_board,Person_info):
    for i in range(0,2):
        x_axis = randint(0,50)
        y_axis = randint(0,50)
        healthpoint = randint(200,230)
        has_record = True
        my_board[x_axis,y_axis] = [healthpoint,0,0]       
        Person_info[x_axis][y_axis] = [x_axis,y_axis,healthpoint,10,0,True]
        Person_info = person_information(x_axis,y_axis,healthpoint,has_record)       
    return my_board,Person_info
        
# this part still have some problem, eg: when division of area is smaller than 100 or bigger than 125
#the infect near by also have some problem related with the change of spreading area
#the spread function is mainly done my Bowen Zhen
def spread (Person_info):
    for X in Person_info:
        for Y in X: 
            x_axis = Y[0]
            y_axis = Y[1]
            healthpoint = Y[2]
            incubation = Y[3]
            area = Y[4]
            has_record = Y[5]
            if healthpoint < 256:
                if incubation > 0:
                    incubation -= 1
                    Person_info[x_axis][y_axis] = [x_axis,y_axis,healthpoint,incubation,area,has_record]
                    #infect_near_by(x_axis,y_axis,healthpoint,area,Person_info)
                elif healthpoint>0:
                    #Judge wether to deduct healthpoint and infect the surrounding or not
                    my_dies = randint(1,11)
                    if my_dies < 3:
                        healthpoint -= 100
                    elif my_dies > 5:
                        healthpoint += 100
                    #Prevent recurrent infection of infected patients
                    if healthpoint > 255 and has_record == True:
                        healthpoint += 600
                    Person_info = person_information(x_axis,y_axis,healthpoint,has_record)
                    Person_info = infect_near_by(x_axis,y_axis,healthpoint,area,Person_info)
    return Person_info
                
def infect_near_by (x_axis,y_axis,healthpoint,area,Person_info):
    #prvent overflow
    for x in range( max(0, x_axis - area) , min(len(Person_info), x_axis + area) ):
        for y in range( max(0, y_axis - area) , min(len(Person_info), y_axis + area) ):
            has_record = Person_info[x][y][5] 
            if x!= x_axis and y!=y_axis and has_record == False:
                rate_infected = (Person_info[x_axis][y_axis][2] - healthpoint) / 3
                my_dies = randint(1,100)
                if my_dies > rate_infected:
                    healthpoint = randint(200,230)
                    Person_info = person_information(x,y,healthpoint,has_record)
    return Person_info
                
#the drawing part is mainly done my Damon Yang and Yao Feng
def update_map(Person_info,my_board):
    for x in range(0,50):
        for y in range(0,50):
            healthpoint = Person_info[x][y][2]
            if healthpoint < 256 and healthpoint > 1 :
                my_board[x,y] = [healthpoint,0,0]
            elif healthpoint < 1:
                my_board[x,y] = [255,255,255]
            if Person_info[x][y][5] == True and healthpoint >255:
                my_board[x,y] = [0,0,255]


#main program
temp=init_map()
my_board = temp[0]
Person_info = temp[1]
temp = rand_infector(my_board,Person_info)
my_board = temp[0]
Person_info = temp[1]

no_infection = False
while no_infection==False:
   infection_count = 0
   Person_info = spread(Person_info)
   update_map(Person_info, my_board)

#drawing
   im = plt.imshow(my_board)
   plt.show()
   for x in Person_info:
       for y in x:
           if y[2] >0 and y[2] < 256:
               infection_count += 1
   if infection_count == 0: 
       no_infection = True        

#test
count =0
for i in Person_info:
    for k in i:
        if k[2]<0:
            count += 1
            #print(k)
print(count)
#print(Person_info)