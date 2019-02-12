#!/usr/bin/python3

import tkinter as tk
from button import *
from random import *
from time import sleep

# -- DEFINES -- #
PAD = 5
ROW = 10
COL = 10
RESET_COUNT = "000"
TOTAL_BOMBS = 10

class Window(tk.Frame):
   def __init__(self, parent):
      tk.Frame.__init__(self,parent) # create the frame to attach to the root
      self.root = parent

      # variables for the board
      self.gameOver = False
      self.row = ROW
      self.col = COL
      self.timeCount = "000"
      self.flagCount = str(TOTAL_BOMBS).zfill(3)   # fill with leading zeros

      # timer setup
      self.time = tk.StringVar()       # make the time a variable
      self.time.set(self.timeCount)    # set to zero

      # The number of flags available to check on the board
      self.flags = tk.StringVar()      # number of flags available
      self.flags.set(self.flagCount) 

      # double array for the board tiles
      self.tiles = [[0 for i in range(self.col)] for j in range(self.row)]
      self.tileArray = [0 for i in range(self.col*self.row)]

      self.Widgets()

   # attach the widgets that are apart of the frame
   def Widgets(self):
      self.Timer = tk.Label(self, textvariable=self.time, font=('times', '20', 'bold'))
      self.Timer.grid(row=0, column=0, sticky="e", padx=15)

      self.ResetButton = tk.Button(self, text="R", command=self.Reset)
      self.ResetButton.grid(row=0, column=1, sticky="n")

      self.FlagCount = tk.Label(self, textvariable=self.flags, font=('times', '20', 'bold'))
      self.FlagCount.grid(row=0, column=2, sticky="w", padx=15)
      
      # configure the right and left column to be far left and right
      self.grid_columnconfigure(1, weight=2)

      self.MineFrame = tk.Frame(self)

      # make the buttons
      rowNum = 0;

      for colNum in range(self.row*self.col):
         tile = Tile(self.MineFrame, self, rowNum, colNum%self.col)
         self.tiles[rowNum][colNum%self.col] = tile
         self.tileArray[colNum] = tile
         tile.grid(row=rowNum, column=colNum%self.col)

         if(colNum%self.col == self.col-1):
            rowNum += 1

      self.RandomizeBombs()

      self.MineFrame.grid(row=1, column=0, columnspan=3)

      print("Timer starting for everyone second...")
      self.updateTime()

   # update time value
   def updateTime(self):
      # convert time to an int to add
      time = int(self.timeCount)
      time = time + 1
      
      # convert back to a string and add leading zeros
      self.timeCount = str(time).zfill(3) # fill 3 spaces with zeros
      self.time.set(self.timeCount)

      # call the timer again after one second
      if(not self.gameOver):
         self.after(1000, self.updateTime)

   def GameOver(self):
      self.gameOver = True

      for tile in self.tileArray:
         tile.showBomb()

   def UpdateTiles(self, tile):
      numOfTilesToUpdate = 0
      toUpdate = True

      # if it is a number don't check surrounding tiles
      if(tile.count > 0):
         tile.updateState()
      else:
         self.checkTiles(tile)  # start the algorithm by checking the tile clicked

         # update all the tiles based on the one you clicked
         while(toUpdate):
            # check if tiles still need updated
            for tileToCheck in self.tileArray:
               if(tileToCheck.toUpdate):
                  self.checkTiles(tileToCheck)  # update the tile
                  numOfTilesToUpdate += 1

            if(numOfTilesToUpdate == 0): # no more tiles break
               toUpdate = False

            numOfTilesToUpdate = 0

      self.checkForWin()

   def incrementFlag(self):
      self.flagCount = str(int(self.flagCount) + 1).zfill(3)
      self.flags.set(self.flagCount)

   def decrementFlag(self):
      self.flagCount = str(int(self.flagCount) - 1).zfill(3)
      self.flags.set(self.flagCount)

   def checkForWin(self):
      numOfTilesNotPressed = 0

      # check for a win!
      for tileToCheck in self.tileArray:
         if(not tileToCheck.isPressed() and not tileToCheck.isBomb()):
            numOfTilesNotPressed += 1

      print(numOfTilesNotPressed)
      if(numOfTilesNotPressed == 0):
         self.gameOver = True
         print("GAME WON!!!!!!!!!!")
         print("Congradulations!")

   def checkTiles(self, tile):
      row = tile.row
      col = tile.col

      tile.updateState()

      if(row-1 >= 0):   # below
         if(self.tiles[row-1][col].count == 0 and not self.tiles[row-1][col].isPressed()):
            self.tiles[row-1][col].needUpdate()
         elif(self.tiles[row-1][col].count > 0):
            self.tiles[row-1][col].updateState()

      if(row-1 >= 0 and col-1 >= 0): # bottom left
         if(self.tiles[row-1][col-1].count == 0 and not self.tiles[row-1][col-1].isPressed()):
            self.tiles[row-1][col-1].needUpdate()
         elif(self.tiles[row-1][col-1].count > 0):
            self.tiles[row-1][col-1].updateState()

      if(row-1 >= 0 and col+1 < self.col): # bottom right
         if(self.tiles[row-1][col+1].count == 0 and not self.tiles[row-1][col+1].isPressed()):
            self.tiles[row-1][col+1].needUpdate()
         elif(self.tiles[row-1][col+1].count > 0):
            self.tiles[row-1][col+1].updateState()

      if(row+1 < self.row): # above
         if(self.tiles[row+1][col].count == 0 and not self.tiles[row+1][col].isPressed()):
            self.tiles[row+1][col].needUpdate()
         elif(self.tiles[row+1][col].count > 0):
            self.tiles[row+1][col].updateState()

      if(row+1 < self.row and col-1 >= 0): # top left
         if(self.tiles[row+1][col-1].count == 0 and not self.tiles[row+1][col-1].isPressed()):
            self.tiles[row+1][col-1].needUpdate()
         elif(self.tiles[row+1][col-1].count > 0):
            self.tiles[row+1][col-1].updateState()

      if(row+1 < self.row and col+1 < self.col): # bottom right
         if(self.tiles[row+1][col+1].count == 0 and not self.tiles[row+1][col+1].isPressed()):
            self.tiles[row+1][col+1].needUpdate()
         elif(self.tiles[row+1][col+1].count > 0):
            self.tiles[row+1][col+1].updateState()

      if(col+1 < self.col):   # to the right
         if(self.tiles[row][col+1].count== 0 and not self.tiles[row][col+1].isPressed()):
            self.tiles[row][col+1].needUpdate()
         elif(self.tiles[row][col+1].count > 0):
            self.tiles[row][col+1].updateState()

      if(col-1 >= 0):   # to the left
         if(self.tiles[row][col-1].count == 0 and not self.tiles[row][col-1].isPressed()):
            self.tiles[row][col-1].needUpdate()
         elif(self.tiles[row][col-1].count > 0):
            self.tiles[row][col-1].updateState()

         
   # place holder for reset function to the gameboard
   def Reset(self):
      print("Game reset...")
      # sleep(1.5)

      # reset the game flag count and timer
      self.timeCount = RESET_COUNT
      self.time.set(self.timeCount)

      self.flagCount = str(TOTAL_BOMBS).zfill(3)
      self.flags.set(self.flagCount)

      # reset every tile
      for tile in self.tileArray:
         tile.reset()

      # re randomize the bombs
      self.RandomizeBombs()

      if(self.gameOver == True):
         # restart the timer
         self.gameOver = False
         self.updateTime()
      else:
         # game is not over anymore
         self.gameOver = False


   def RandomizeBombs(self):
      # pick the bombs at random
      bombs = sample(self.tileArray, TOTAL_BOMBS)

      # set the tiles as bombs
      for tile in bombs:
         tile.setBombTile()

      # loop over the array to make the correct numbers
      for row in range(self.row):
         for col in range(self.col):
            # bounds check each 8 surrounding tiles
            if(row-1 >= 0):   # below
               if(self.tiles[row-1][col].isBomb()):
                  self.tiles[row][col].increaseTileCount()

            if(row-1 >= 0 and col-1 >= 0): # bottom left
               if(self.tiles[row-1][col-1].isBomb()):
                  self.tiles[row][col].increaseTileCount()

            if(row-1 >= 0 and col+1 < self.col): # bottom right
               if(self.tiles[row-1][col+1].isBomb()):
                  self.tiles[row][col].increaseTileCount()

            if(row+1 < self.row): # above
               if(self.tiles[row+1][col].isBomb()):
                  self.tiles[row][col].increaseTileCount()

            if(row+1 < self.row and col-1 >= 0): # top left
               if(self.tiles[row+1][col-1].isBomb()):
                  self.tiles[row][col].increaseTileCount()

            if(row+1 < self.row and col+1 < self.col): # bottom right
               if(self.tiles[row+1][col+1].isBomb()):
                  self.tiles[row][col].increaseTileCount()

            if(col+1 < self.col):   # to the right
               if(self.tiles[row][col+1].isBomb()):
                  self.tiles[row][col].increaseTileCount()

            if(col-1 >= 0):   # to the left
               if(self.tiles[row][col-1].isBomb()):
                  self.tiles[row][col].increaseTileCount()