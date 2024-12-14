# -*- coding: utf-8 -*-
"""
The Game of Life (GoL) module named in honour of John Conway

This module defines the classes required for the GoL simulation.

Created on Tue Jan 15 12:21:17 2019

@author: shakes
"""
import numpy as np
from scipy import signal
import rle

class GameOfLife:
    '''
    Object for computing Conway's Game of Life (GoL) cellular machine/automata
    '''
    def __init__(self, N=256, finite=False, fastMode=True):
        self.N = N
        self.grid = np.zeros((N,N), np.int64)
        self.neighborhood = np.ones((3,3), np.int64) # 8 connected kernel
        self.neighborhood[1,1] = 0 #do not count centre pixel
        self.finite = finite
        self.fastMode = fastMode
        self.aliveValue = 1
        self.deadValue = 0
        
    def getStates(self):
        '''
        Returns the current states of the cells
        '''
        return self.grid
    
    def getGrid(self):
        '''
        Same as getStates()
        '''
        return self.getStates()
               
    def _liveNeighbors(self, row, col):
        '''
        Private helper part A, finds the number of live neighbors for a cell at position (row, col)
        '''
        count = 0

        #note that rows and columns range from 0 to N-1 in values (zero indexing)
        #uses max and min to take boundaries into consideration
        upperRow = max(row - 1, 0) #if row = 0, we use 0 instead of -1 (out of bounds)
        lowerRow = min(row + 1, self.N - 1) #if row = N-1, we use that instead of N (out of bounds)
        leftCol = max(col - 1, 0) #if col = 0, we use 0 instead of -1 (out of bounds)
        rightCol = min(col + 1, self.N - 1) #if col = N-1, we use that instead of N (out of bounds)


        for r in range(upperRow, lowerRow+1): #upperRow has lower index
            for c in range(leftCol, rightCol+1):
                if (r != row or c!= col) and self.grid[r, c] == 1: #do not count cell being operated on
                    count += 1

        return count


    def evolve(self):
        '''
        Given the current states of the cells, apply the GoL rules:
        - Any live cell with fewer than two live neighbors dies, as if by underpopulation.
        - Any live cell with two or three live neighbors lives on to the next generation.
        - Any live cell with more than three live neighbors dies, as if by overpopulation.
        - Any dead cell with exactly three live neighbors becomes a live cell, as if by reproduction
        '''
        newGrid = np.zeros((self.N, self.N), np.int64) #blank grid which will change to evolution


        #get weighted sum of neighbors
        if (self.fastMode == True): #PART E
            #we use mode='same' to ensure output has same dimensions as input grid
            #if we used mode='full' then we get larger dimensions as full multiplication is done
            #if we used mode='valid' then the output would be trimmed to only include valid positions

            #we use boundary='wrap' to ensure figures wrap from one edge to another on an infinite plane
            #if we used boundary='symm' then we get incorrect symmetry different to our actual self.grid
            #if we used boundary='fill' then we get incorrect cells in corners
            sums = signal.convolve2d(self.grid, self.neighborhood, mode='same', boundary='wrap')

            for row in range(self.N):
                for col in range(self.N):
                    cellState = self.grid[row, col] #whether current cell is dead or alive
                    liveNeighbors = sums[row, col]

                    #dont need to set to states 0 as this is default in newGrid
                    if (cellState == 1) and (liveNeighbors == 2 or liveNeighbors == 3):
                        newGrid[row, col] = self.aliveValue #cell lives on to next evolution
                    elif (cellState == 0) and (liveNeighbors == 3):
                        newGrid[row, col] = self.aliveValue #dead cell reproduces in next evolution
            
        else: #if fastMode == False, we use the brute force search (PART A)
            #implement the GoL rules by thresholding the weights
            #iterate through each cell position
            for row in range(self.N):
                for col in range(self.N):
                    cellState = self.grid[row, col] #whether current cell is dead or alive
                    liveNeighbors = self._liveNeighbors(row, col)

                    #dont need to set to states 0 as this is default in newGrid
                    if (cellState == 1) and (liveNeighbors == 2 or liveNeighbors == 3):
                        newGrid[row, col] = self.aliveValue #cell lives on to next evolution
                    elif (cellState == 0) and (liveNeighbors == 3):
                        newGrid[row, col] = self.aliveValue #dead cell reproduces in next evolution
        
        
        #update the grid
        self.grid = newGrid
    
    def insertBlinker(self, index=(0,0)):
        '''
        Insert a blinker oscillator construct at the index position
        '''
        self.grid[index[0], index[1]+1] = self.aliveValue
        self.grid[index[0]+1, index[1]+1] = self.aliveValue
        self.grid[index[0]+2, index[1]+1] = self.aliveValue
        
    def insertGlider(self, index=(0,0)):
        '''
        Insert a glider construct at the index position
        '''
        self.grid[index[0], index[1]+1] = self.aliveValue
        self.grid[index[0]+1, index[1]+2] = self.aliveValue
        self.grid[index[0]+2, index[1]] = self.aliveValue
        self.grid[index[0]+2, index[1]+1] = self.aliveValue
        self.grid[index[0]+2, index[1]+2] = self.aliveValue
        
    def insertGliderGun(self, index=(0,0)):
        '''
        Insert a glider construct at the index position
        '''
        self.grid[index[0]+1, index[1]+25] = self.aliveValue
        
        self.grid[index[0]+2, index[1]+23] = self.aliveValue
        self.grid[index[0]+2, index[1]+25] = self.aliveValue
        
        self.grid[index[0]+3, index[1]+13] = self.aliveValue
        self.grid[index[0]+3, index[1]+14] = self.aliveValue
        self.grid[index[0]+3, index[1]+21] = self.aliveValue
        self.grid[index[0]+3, index[1]+22] = self.aliveValue
        self.grid[index[0]+3, index[1]+35] = self.aliveValue
        self.grid[index[0]+3, index[1]+36] = self.aliveValue
        
        self.grid[index[0]+4, index[1]+12] = self.aliveValue
        self.grid[index[0]+4, index[1]+16] = self.aliveValue
        self.grid[index[0]+4, index[1]+21] = self.aliveValue
        self.grid[index[0]+4, index[1]+22] = self.aliveValue
        self.grid[index[0]+4, index[1]+35] = self.aliveValue
        self.grid[index[0]+4, index[1]+36] = self.aliveValue
        
        self.grid[index[0]+5, index[1]+1] = self.aliveValue
        self.grid[index[0]+5, index[1]+2] = self.aliveValue
        self.grid[index[0]+5, index[1]+11] = self.aliveValue
        self.grid[index[0]+5, index[1]+17] = self.aliveValue
        self.grid[index[0]+5, index[1]+21] = self.aliveValue
        self.grid[index[0]+5, index[1]+22] = self.aliveValue
        
        self.grid[index[0]+6, index[1]+1] = self.aliveValue
        self.grid[index[0]+6, index[1]+2] = self.aliveValue
        self.grid[index[0]+6, index[1]+11] = self.aliveValue
        self.grid[index[0]+6, index[1]+15] = self.aliveValue
        self.grid[index[0]+6, index[1]+17] = self.aliveValue
        self.grid[index[0]+6, index[1]+18] = self.aliveValue #changed to 18 based on comparing to glidergun
        self.grid[index[0]+6, index[1]+23] = self.aliveValue
        self.grid[index[0]+6, index[1]+25] = self.aliveValue
        
        self.grid[index[0]+7, index[1]+11] = self.aliveValue
        self.grid[index[0]+7, index[1]+17] = self.aliveValue
        self.grid[index[0]+7, index[1]+25] = self.aliveValue
        
        self.grid[index[0]+8, index[1]+12] = self.aliveValue
        self.grid[index[0]+8, index[1]+16] = self.aliveValue
        
        self.grid[index[0]+9, index[1]+13] = self.aliveValue
        self.grid[index[0]+9, index[1]+14] = self.aliveValue

    def _fileReaderTxt(self, filename):
        '''
        Reads a plaintext file for GoL pattern and outputs a string txtString containing file contents
        '''
        txtString = ''
        file = open(filename, 'r')
        for line in file:
            if (line[0] != '!'): #removing comment lines starting with '!' or '#'
                txtString += line

        file.close()
        return txtString
    

    def insertFromPlainText(self, txtString, pad=0):
        '''
        Assumes txtString contains the entire pattern as a human readable pattern without comments
        '''
        strippedTxtString = txtString.strip()
        splitString = strippedTxtString.split('\n') #split at each line
        rows = len(splitString) #number of rows patterns takes up
        cols = len(splitString[0]) #number of columns patterns takes up

        #we must ensure that our pattern goes to the middle of our grid otherwise will be out of bounds
        firstRow = (self.N - rows) // 2
        firstCol = (self.N - cols) // 2

        for r in range(rows):
            for c in range(cols):
                if splitString[r][c] == 'O':
                    self.grid[r + firstRow, c + firstCol] = self.aliveValue


    def _fileReaderRle(self, filename):
        '''
        Reads an rle file for GoL pattern and outputs a string rleString containing file contents
        '''
        rleString = ''
        file = open(filename, 'r')
        for line in file:
            if (line[0] != '!'): #removing comment lines starting with '!' or '#'
                 rleString += line

        file.close()
        return rleString

    def insertFromRLE(self, rleString, pad=0):
        '''
        Given string loaded from RLE file, populate the game grid
        '''
        parser = rle.RunLengthEncodedParser(rleString) #use parser from rle.py
        # pattern = parser.pattern_2d_array

        pattern = parser.human_friendly_pattern

        strippedTxtString = pattern.strip()
        splitString = strippedTxtString.split('\n') #split at each line
        rows = len(splitString) #number of rows patterns takes up
        cols = len(splitString[0]) #number of columns patterns takes up

        #we must ensure that our pattern goes to the middle of our grid otherwise will be out of bounds
        firstRow = (self.N - rows) // 2
        firstCol = (self.N - cols) // 2

        for r in range(rows):
            for c in range(cols):
                if splitString[r][c] == 'o':
                    self.grid[r + firstRow, c + firstCol] = self.aliveValue

