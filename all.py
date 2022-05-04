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
from numpy.random import randint

healthpoint = 0

#Person_info used to record the patient's coordinates, health value,remaining incubation period days, whether they have been infected or not, and the spread range
#The program will finally determine that all points are blue（0，0，255）or balck（0，0，0），green（0，255，0）in the end.
#Initialize the board
def init_map():
    Length = 50
    Width = 50
    my_board = np.zeros((Length, Width, 3), np.uint8)
    Person_info = []
    for i in range(Length):
        my_line =[]
        for j in range(Width):
            #for k in range(3):
                my_board[i,j] = [0,255,0]
                healthpoint = randint(256,300)
                my_line.append([i,j,healthpoint,10,10,False])
        Person_info.append(my_line)
        
    return my_board,Person_info

#Calculate the incubation period and infectious range of the virus
def person_information(x,y,healthpoint,has_record):
    #for x in range(0,len(Person_info)):
        #for y in range(0,len(Person_info[x])):
             # 180 is the base value, the number obtained by subtracting the base value from the health value is divided by 10 to get the number of days of infection
             #Person_info[x][y] = [x,y,healthpoint,0,0]             
             #healthpoint = Person_info[x][y][2]
             if healthpoint > 0:
                 incubation= (healthpoint-180)//10
             else:
                 incubation = 0
                 
             # Infection range           
             if healthpoint < 256 and healthpoint > 0:
                 area = healthpoint // 100
                 has_record = True
             else:                 
                 area = 0
             Person_info[x][y] = [Person_info[x][y][0],Person_info[x][y][1],healthpoint,incubation,area,has_record]
                      
             return Person_info
         

#Randomly generate two infected
def rand_infector(my_board,Person_info):
    for i in range(0,2):
        x_axis = randint(0,len(Person_info))
        y_axis = randint(0,len(Person_info[x_axis]))
        healthpoint = randint(200,230)
        has_record = True
        my_board[x_axis,y_axis] = [healthpoint,0,0]       
        Person_info[x_axis][y_axis] = [x_axis,y_axis,healthpoint,10,0,True]
        Person_info = person_information(x_axis,y_axis,healthpoint,has_record)       
    return my_board,Person_info
        
# virus infection
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
                    #Determine whether to add or subtract health, and continue to infect the surrounding
                    my_dies = randint(1,11)
                    if my_dies < 3:
                        healthpoint -= 100
                    elif my_dies > 5:
                        healthpoint += 100
                    #prevent reinfection in people who have recovered
                    if healthpoint > 255 and has_record == True:
                        healthpoint += 600
                    Person_info = person_information(x_axis,y_axis,healthpoint,has_record)
                    Person_info = infect_near_by(x_axis,y_axis,healthpoint,area,Person_info)
    return Person_info
                
def infect_near_by (x_axis,y_axis,healthpoint,area,Person_info):
    #prevent overshooting the board boundaries
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
                
                
def update_map(Person_info,my_board):
    for x in range(0,len(Person_info)):
        for y in range(0,len(Person_info[x])):
            healthpoint = Person_info[x][y][2]
            if healthpoint < 256 and healthpoint > 1 :
                my_board[x,y] = [healthpoint,0,0]
            elif healthpoint < 1:
                my_board[x,y] = [255,255,255]
            if Person_info[x][y][5] == True and healthpoint >255:
                my_board[x,y] = [0,0,255]    

    

def Data_statistic (Person_info,My_days):

    Green = Light_red = Red = Dark_red = Blue = White = 0 
    Population = len(Person_info)*len(Person_info[0])/100   
    for x in Person_info:
        for y in x:
            healthpoint = y[2]
            if y[5] == False:
                Green += 1
            else:
                if healthpoint > 200 and healthpoint <256:
                    Light_red += 1
                elif healthpoint >100 and healthpoint < 201:
                    Red += 1
                elif healthpoint > 0 and healthpoint <101:
                    Dark_red += 1
                elif healthpoint < 1:
                    White += 1
                elif healthpoint > 255:
                    Blue += 1
    My_day_count = []                
    
    My_days[0].append(Green/Population)
    My_days[1].append(Light_red/Population)
    My_days[2].append(Red/Population)
    My_days[3].append(Dark_red/Population)
    My_days[4].append(Blue/Population)
    My_days[5].append(White/Population)
    My_days[6].append(My_days[6][-1]+1)
    #for i in range (0,len(My_days[1])):
        #My_day_count.append(i)
    #My_days.append(My_day_count)
    return My_days

def Line_chart (My_days):
    
    plt.xlim((0, 71))
    plt.ylim((0,101))      
    my_x_ticks = np.arange(0, 71, 10)
    my_y_ticks = np.arange(0, 101, 10)
    plt.xticks(my_x_ticks)
    plt.yticks(my_y_ticks)
    Line_Green=plt.plot(My_days[6],My_days[0],lw =2,c ='limegreen',label='susceptible')
    LIne_Light_Red=plt.plot(My_days[6],My_days[1],lw =2,c ='salmon',label='mild infected')
    LIne_Red=plt.plot(My_days[6],My_days[2],lw =2,c ='red',label=' infected')
    LIne_Light_Red=plt.plot(My_days[6],My_days[3],lw =2,c ='darkmagenta',label='seriously infected')
    LIne_Light_Red=plt.plot(My_days[6],My_days[4],lw =2,c ='deepskyblue',label='recorved')
    LIne_Light_Red=plt.plot(My_days[6],My_days[5],lw =2,c ='black',label='death')
    plt.title('Infection Data Statistic',fontsize=35)
    plt.xlabel('Days',fontsize=35)
    plt.ylabel('%',fontsize=35)
    plt.xticks(fontsize=35)
    plt.yticks(fontsize=35)
    if len(My_days[0]) <3:
        plt.legend(loc ='right',fontsize=15)

    
    #print(My_days[6],'  ',My_days[0])
    
    

#main program   
temp=init_map()
my_board = temp[0]
Person_info = temp[1]
temp = rand_infector(my_board,Person_info)
my_board = temp[0]
Person_info = temp[1]
My_days = [[100],[0],[0],[0],[0],[0],[0]]
no_infection = False
pic_count = 0
while no_infection==False:
   infection_count = 0
   Person_info = spread(Person_info)   
   My_days = Data_statistic(Person_info,My_days)
   update_map(Person_info, my_board)

#Mapping the virus infection  
   plt.figure(num=3, figsize=(16,10))
   plt.subplot(1, 2, 1)  
   My_map = plt.imshow(my_board)
   plt.title('Infection Status',fontsize=35)
   plt.subplot(1, 2, 2) 
   Line_chart (My_days)
   
   plt.savefig('D:/Bristol/FCP/Project/pictures/'+str(pic_count)+'.jpeg')
   plt.show() 
   pic_count += 1
   
   for x in Person_info:
       for y in x:
           if y[2] >0 and y[2] < 256:
               infection_count += 1
   if infection_count == 0: 
       no_infection = True        




import imageio

gif_images = []
for i in range(0, pic_count):
    gif_images.append(imageio.imread('D:/Bristol/FCP/Project/pictures/'+str(i)+'.jpeg'))   # 读取多张图片
imageio.mimsave("test.gif", gif_images, fps=5)   # Convert image to animated gif
#imageio.mimread("test.gif")
#test
#count =0
#for i in Person_info:
#    for k in i:
#        if k[2]<0:
#            count += 1
            #print(k)
#print(count)
#My_total = 0
#for i in My_data:
    #My_total += i
#print(My_days)
#print(My_total)
#print(Person_info)

import os
os.system(r'start test.gif')