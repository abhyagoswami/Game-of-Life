# -*- coding: utf-8 -*-
"""
Game of life script with animated evolution

Created on Tue Jan 15 12:37:52 2019

@author: shakes
"""
import conway

N=1050

padding = 10

#read RLE file
# with open("gosperglidergun.rle", "r") as text_file:

# with open("onionrings.rle", "r") as text_file: #This is 96x96
# with open("sawtooth.rle", "r") as text_file: #This is 128x173
# with open("reflector.rle", "r") as text_file: #This is 22x23
        
with open("breeder1.rle", "r") as text_file: #PART E, this is 749x338

# with open("turingmachine.rle", "r") as text_file: #PART G
        rleString = text_file.read()

#create the game of life object
life = conway.GameOfLife(N, fastMode=True)
life.insertFromRLE(rleString, padding)
cells = life.getStates() #initial state

#-------------------------------
#plot cells
import matplotlib.pyplot as plt
import matplotlib.animation as animation

fig = plt.figure()

plt.gray()

img = plt.imshow(cells, animated=True)

def animate(i):
    """perform animation step"""
    global life
    
    life.evolve()
    cellsUpdated = life.getStates()
    
    img.set_array(cellsUpdated)
    
    return img,

interval = 50 #ms

#animate 24 frames with interval between them calling animate function at each frame
ani = animation.FuncAnimation(fig, animate, frames=24, interval=interval, blit=True)
#~ animate(0)

plt.show()
