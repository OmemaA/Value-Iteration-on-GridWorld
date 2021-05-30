import numpy as np
import matplotlib.pyplot as plt
from matplotlib import colors as c
import copy
from tkinter import *
from pprint import pprint


size = 10
reward = [[-1,-1,-1,-1,-1,-1,-1,-1,-1,-1],
        [-1,-1,-100,-1,-1,-1,-1,-1,-1,-1],
        [-1,-1,-1,-1,-100,-1,-1,-1,-1,-100],
        [100,-1,-1,-1,-100,-100,-1,-1,-1,-1],
        [-1,-100,-1,-1,-1,-1,-1,-1,-1,-1],
        [-1,-1,-1,-100,-1,-1,-100,-1,-1,-1],
        [-1,-1,-1,-1,-1,-1,-1,-1,-1,-1],
        [-1,-100,-1,-100,-1,-1,-100,-100,-100,-1],
        [-1,-1,100,-1,-1,-1,-1,-1,-1,-1],
        [-1,-1,-1,-1,-1,-1,-1,-1,-1,-1]]
        

def value_iteration(dicounted_rate, theta):
    converged = False
    old_grid = copy.deepcopy(reward)
    while(not converged):
        V, delta = copy.deepcopy(reward), 0
        for i in range(size):
            for j in range(size):
                if reward[i][j] not in (-100, 100):
                    values = []
                    for next_v in possible_actions(old_grid,i,j).values():
                        values.append(reward[i][j] + dicounted_rate* next_v)
                    V[i][j] = round(max(values),2)
                    delta = max(delta, abs(max(values) - old_grid[i][j]))
                    converged = True if delta < theta else False
        old_grid = V
    return old_grid


def possible_actions(grid,i,j):
    actions = dict()
    if (j-1) >=0: actions['L'] = (grid[i][j-1])
    else: actions['L'] = (grid[i][j])

    if (i-1) >=0: actions['U'] = (grid[i-1][j])
    else: actions['U'] = (grid[i][j])

    if (j+1) < size: actions['R'] = (grid[i][j+1])
    else: actions['R'] = (grid[i][j])

    if (i+1) < size: actions['D'] = (grid[i+1][j])
    else: actions['D'] = (grid[i][j])

    return actions
    

def plotGraph(data):
    master = Tk()
    canvas = Canvas(master, width=500, height=500, borderwidth=0, highlightthickness=0)
    cellwidth = 50
    cellheight = 50
    for row in range(10):
        for column in range(10):
            if reward[row][column] == 100: color = 'green'
            elif reward[row][column] == -100: color = 'red'
            else: color = 'white'

            x1 = column*cellwidth
            y1 = row * cellheight
            x2 = x1 + cellwidth
            y2 = y1 + cellheight

            canvas.create_rectangle(x1,y1,x2,y2, fill=color, tags="rect")

            if reward[row][column] not in (100, -100):
                actions = possible_actions(data, row, column)
                direction = max(actions, key=actions.get)

                x1 = column*cellwidth + 25 #middle
                y1 = row * cellheight + 25 #middle

                if direction == 'R': 
                    x2, y2 = x1 + 25, y1
                elif direction == 'L': 
                    x2, y2 = x1 - 25,  y1
                elif direction == 'U': 
                    x2, y2 = x1, y1 - 25
                elif direction == 'D': 
                    x2, y2 = x1, y1 + 25
                canvas.create_line(x1,y1,x2,y2, arrow=LAST)

    canvas.pack()
    master.mainloop()



policy = value_iteration(0.8,0.1)
pprint(policy)
plotGraph(policy)