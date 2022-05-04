# -*- coding: utf-8 -*-
"""
Created on Tue Mar 22 14:45:15 2022

@author: nicko
"""

import matplotlib.pyplot as plt
import numpy as np
from numpy.random import randint
import pygal
import imageio
import os

#healthpoint = 0

#Person_info records the patient's coordinates, healthpoint, remaining incubation days, whether they have been infected or not, and the spread range
#the array is a two-dimensional array, which is easy to understand
#The program finally judges that all points are blue（0，0，255）or white（255,255,255），green（0，255，0）to finish
#initialize the map
def init_map():
    Length = 64
    Width = 64    
    my_board = np.zeros((Length, Width, 3), np.uint8)
    Person_info = []
    for i in range(Length):
        my_line =[]
        for j in range(Width):
                my_board[i,j] = [0,255,0]
                healthpoint = randint(256,300)
                my_line.append([i,j,healthpoint,0,0,False])
        Person_info.append(my_line)
        
    return my_board,Person_info

        
#Randomly generate two infector
def rand_infector(my_board,Person_info,area_divider):
    for i in range(0,2):
        x_axis = randint(0,len(Person_info))
        y_axis = randint(0,len(Person_info[x_axis]))
        healthpoint = randint(200,230)
        #has_record = True
        my_board[x_axis,y_axis] = [healthpoint,0,0]       
        Person_info[x_axis][y_axis] = [x_axis,y_axis,healthpoint,(healthpoint-180)//10,healthpoint // area_divider,True]
    return my_board,Person_info
        
#virus spread
def spread (Person_info,area_divider):
    for X in Person_info:
        for Y in X:             
            if Y[2] < 256 and Y[2] > 0 and Y[5] == True :
                x_axis = Y[0]
                y_axis = Y[1]
                healthpoint = Y[2]
                incubation = Y[3]
                area = Y[4]
                has_record = Y[5]
                if incubation > 0:
                    incubation -= 1                   
                    Person_info[x_axis][y_axis] = [x_axis,y_axis,healthpoint,incubation,area,has_record]
                    Person_info = infect_near_by(x_axis,y_axis,healthpoint,area,Person_info,area_divider)
                else:
                    #Judge whether to increase or decrease the healthpoint, infect nearby
                    my_dies = randint(1,11)
                    if my_dies < 3:
                        healthpoint -= 100
                    elif my_dies > 5:
                        healthpoint += 100
                    area = healthpoint // area_divider
                    #Prevent reinfection in recovered patients
                    if healthpoint > 255 and has_record == True:
                        healthpoint += 600
                    Person_info[x_axis][y_axis] = [x_axis,y_axis,healthpoint,incubation,area,has_record]
                    if healthpoint > 0 and healthpoint< 256 and has_record == True:
                        Person_info = infect_near_by(x_axis,y_axis,healthpoint,area,Person_info,area_divider)
    #People who are infected on the day cannot spread 
    for x in range(0,len(Person_info)):
        for y in range(0,len(Person_info[x])):
            if Person_info[x][y][2] > 0 and Person_info[x][y][2] < 256:
                Person_info[x][y][5] = True
            
    return Person_info
                
def infect_near_by (x_axis,y_axis,healthpoint,area,Person_info,area_divider):
    #prevent overflow/out of bound
    for x in range( max(0, x_axis - area) , min(len(Person_info), x_axis + area+1) ):
        for y in range( max(0, y_axis - area) , min(len(Person_info[x]), y_axis + area+1) ):
            has_record = Person_info[x][y][5] 
            if has_record == False:                
                my_divider = 0
                for i in range(1,area+1):
                    if abs(x-x_axis)<=i and abs(y-y_axis)<=i:
                        my_divider = i
                        break
                base_rate = 30/my_divider
                
                rate_infected = (Person_info[x][y][2] - healthpoint) /6.5 + base_rate 
                my_dies = randint(1,101)
                if my_dies < rate_infected:
                    healthpoint = randint(200,230)
                    Person_info[x][y] = [x,y,healthpoint,(healthpoint-180)//10,healthpoint//area_divider,has_record]
    return Person_info
                
                
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

def plot_my_diagram(Person_info,days,my_board,My_days):
    plt.figure(num=3, figsize=(24, 15))
    plt.subplot(1, 2, 1)  
    My_map = plt.imshow(my_board)
    plt.title('Infection Status',fontsize=35)
    plt.subplot(1, 2, 2) 
    Line_chart (My_days)   
    plt.savefig('D:/Bristol/FCP/Project/pictures/'+str(days)+'.jpeg') 
    return days

def  loop_end_no_infection(days,Person_info):
    no_infection = False
    if days > 1:
        infection_count = 0
        for x in Person_info:
            for y in x:
                 if y[2] >0 and y[2] < 256:
                    infection_count += 1
        if infection_count == 0: 
            no_infection = True 
        else:
            no_infection = False
    return no_infection

def plot_my_svg(My_days,days):
    line_chart = pygal.StackedBar()
    line_chart.title = 'Infection Data statistic (in %)'
    line_chart.x_labels = map(str, range(0,days))
    line_chart.add('susceptible', My_days[0])
    line_chart.add('mild infected',  My_days[1])
    line_chart.add('infected', My_days[2])
    line_chart.add('seriously infected',  My_days[3])
    line_chart.add('recorvered',  My_days[4])
    line_chart.add('death',  My_days[5])
    line_chart.show_y_guides = True    # Display gridlines for the Y-axis
    line_chart.render_to_file('bar_chart.svg')

#Main program 
My_days = [[100],[0],[0],[0],[0],[0],[0]]#susceptible,mild infected,infected,seriously infected,recorved,death,days
no_infection = False
days = 0 
area_divider = 120
while no_infection==False and days < 365:
    if days == 0:
       my_board_and_Person_info=init_map()
       my_board = my_board_and_Person_info[0]
       Person_info = my_board_and_Person_info[1]

    if days == 1:
        my_board_and_Person_info = rand_infector(my_board,Person_info,area_divider)
        my_board = my_board_and_Person_info[0]
        Person_info = my_board_and_Person_info[1]
    else:       
        Person_info = spread (Person_info,area_divider) 
        
    My_days = Data_statistic(Person_info,My_days)
    update_map(Person_info, my_board)
    
    count = 0
    for x in range(0,len(Person_info)):
        for y in range(0,len(Person_info[x])):
            if Person_info[x][y][2]>0 and Person_info[x][y][2]<256 :
                count = count +1
                
    no_infection = loop_end_no_infection(days, Person_info)
    
#draw the diagram      
    days = plot_my_diagram(Person_info, days,my_board,My_days)
    days += 1 
    

gif_images = []
for i in range(0, days):
    gif_images.append(imageio.imread('D:/Bristol/FCP/Project/pictures/'+str(i)+'.jpeg'))   # read all the pictures saved in the folder
imageio.mimsave("test.gif", gif_images, fps=3)   # turn pictures into gif

plot_my_svg(My_days, days)
#open gif
os.system(r'start test.gif')

