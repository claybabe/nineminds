#9 men's morris - validation and discussion of simulated rules
#copyright - clayton thomas baber 2018

#this validate a model's ability to progress the gamestate by an action

from tkinter import *
import time
import random
import torch
import numpy as np
import tkinter as tk
from tkinter import filedialog

cHeight=444
cellSize=cHeight/9

tk = Tk()
tk.aspect(1,1,1,1)
canvas = Canvas(tk, width=cHeight, height=cHeight, bg="dark green")
canvas.pack(fill=BOTH, expand=1)

positions = (1,1),(4,1),(7,1),(2,2),(4,2),(6,2),(3,3),(4,3),(5,3),(1,4),(2,4),(3,4),(5,4),(6,4),(7,4),(3,5),(4,5),(5,5),(2,6),(4,6),(6,6),(1,7),(4,7),(7,7),(0,0),(0,1),(0,2),(0,3),(0,4),(0,5),(0,6),(0,7),(0,8),(8,0),(8,1),(8,2),(8,3),(8,4),(8,5),(8,6),(8,7),(8,8)
lines = (0,1),(1,2),(3,4),(4,5),(6,7),(7,8),(9,10),(10,11),(12,13),(13,14),(15,16),(16,17),(18,19),(19,20),(21,22),(22,23),(0,9),(1,4),(2,14),(3,10),(4,7),(5,13),(6,11),(8,12),(9,21),(10,18),(11,15),(12,17),(13,20),(14,23),(16,19),(19,22)
pixels = [(0,0,0,0)] * 75
pixels[74] = 24, 33, 42, 1

state = [1,1,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,1,1,1,1,1,1,1,1,1,-1,-1,-1,-1,-1,-1,-1,-1,-1,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0]#,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0]

def calculate_pixels(event):
    global cHeight, cellSize
    cHeight=min(event.width, event.height)
    cellSize = cHeight / 9

    for i in range(0,42):
        pixels[i] = (positions[i][0]*cellSize+cellSize/4, positions[i][1]*cellSize+cellSize/4, (positions[i][0]+1)*cellSize-cellSize/4, (positions[i][1]+1)*cellSize-cellSize/4)
    for i in range(0,16):
        pixels[i+42] = (positions[lines[i][0]][0]*cellSize+3*cellSize/4, positions[lines[i][0]][1]*cellSize+cellSize/2,positions[lines[i][1]][0]*cellSize+cellSize/4, positions[lines[i][1]][1]*cellSize+cellSize/2)
    for i in range(16,32):
        pixels[i+42] = (positions[lines[i][0]][0]*cellSize+cellSize/2, positions[lines[i][0]][1]*cellSize+3*cellSize/4,positions[lines[i][1]][0]*cellSize+cellSize/2, positions[lines[i][1]][1]*cellSize+cellSize/4)
    pixels[74] = 24, 33, 42, cellSize/4

    draw()

drawing = True

#this function will draw the current gamestate on the canvas.
def draw():
    if not drawing: return
    
    #wipe the canvas clean
    canvas.delete(ALL)

    color = "dark green", "green", "dark red", "red"    
    base = 0
    if(state[1:5].count(1)!=1):
        base = 2
    canvas.configure(background=color[base])
        
    #draw each of the board positions
    for i in pixels[:24]:
        canvas.create_oval(i[0], i[1], i[2], i[3], outline=color[base+1], width=pixels[74][3])
        
    #draw the horizontal connecting lines
    for i in pixels[42:58]:
        canvas.create_line(i[0], i[1], i[2], i[3], fill=color[base+1], width=pixels[74][3])
    
    #draw the vertical connecting lines
    for i in pixels[58:74]:    
        canvas.create_line(i[0], i[1], i[2], i[3], fill=color[base+1], width=pixels[74][3])
    
    #draw a player piece on the position it is occupying
    occupations = state[5:47]

    for i in range(0,42):
        if occupations[i]==0: continue
        if occupations[i]==1: player="white"
        else: player="black"
        canvas.create_oval(pixels[i][0], pixels[i][1], pixels[i][2], pixels[i][3], fill=player, outline=player)
    
    #outline a position if it is selected
    selected = state[47:71]#89]
    if 1 in selected:
        if state[0] == 1:
            color = "black"
        else:
            color = "white"
        selected_position = selected.index(1)
        canvas.create_oval(pixels[selected_position][0], pixels[selected_position][1], pixels[selected_position][2], pixels[selected_position][3], outline=color, width=5)
    #update the canvas holder
    tk.update()
    
    #maybe slow down the animation to a visually pleasing speed
    time.sleep(0.1)
################################
#loop through the positions and see if mouse click was on a board position
def click(event):
    #only check the board positions, as we don't care if a click was on a starting position
    for i in range(0, 24):
        if event.x > pixels[i][0] and event.x < pixels[i][2] and event.y > pixels[i][1] and event.y < pixels[i][3]:
            #clicked registered on the i'th position, process it
            action = [0] * 24
            action[i] = 1            
            clicked(action)
            break

def clicked(action):
    global state

    #imagine a difference
    requested_reality = state + action

    #change the world
    state = np.round(model(torch.tensor(np.array(requested_reality, dtype=np.float32))).detach().numpy()).astype(np.int32).tolist()

    #we've made changes to the gamestate, so lets update board view
    draw()
    

#
#this will set the gamestate back to start
def right_click(event):
    clear_board()
    
def clear_board():
    global state
    state[:] = [1,1,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,1,1,1,1,1,1,1,1,1,-1,-1,-1,-1,-1,-1,-1,-1,-1,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0]#,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0]
    draw()

#fire click when left click
canvas.bind("<Button-1>", click)
#fire clear_board when right click
canvas.bind("<Button-3>", right_click)

#we need to recalculate the pixels list anytime the window is resized
tk.bind("<Configure>", calculate_pixels)
################################


#initialize board
draw()


rules_model_path = filedialog.askopenfilename()
model = torch.load(rules_model_path, map_location='cpu')



#so the window stays open, waiting for clickput
tk.mainloop()
