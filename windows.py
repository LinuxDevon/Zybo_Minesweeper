#!/usr/bin/python3

import tkinter as tk
from button import *
from random import *
from time import sleep

# -- DEFINES -- #
PAD = 5
RESET_COUNT = "000"
RESET_WIDTH = 25
RESET_HEIGHT = 25

# This creates the window that holds the time, Reset button, flag count, and grid of mines
# The Window itself is a frame.
# INPUTS:
#     parent : the root window
#     numOfRows : the number of rows of tiles
#     numOfCols : the number of cols of tiles
#     numOfBombs: the total bombs to place under the tiles
#     mode      : the mode value to activate cheater mode (true/false)
class Window(tk.Frame):
   def __init__(self, parent , numOfRows, numOfCols, numOfBombs, mode):
      tk.Frame.__init__(self,parent) # create the frame to attach to the root
      self.root = parent

      # variables for the board
      self.gameOver = False
      self.row = numOfRows
      self.col = numOfCols
      self.startingBombCount = numOfBombs
      self.mode = mode

      # images
      self.deadSmiley = tk.PhotoImage(file="Tiles/deadsmiley.png")
      self.smiley = tk.PhotoImage(file="Tiles/smiley.png")
      self.sunglassesSmiley = tk.PhotoImage(file="Tiles/sunglasses.png")

      self.timeCount = "000"
      self.flagCount = str(self.startingBombCount).zfill(3)   # fill with leading zeros

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

      self.ResetButton = tk.Button(self, image=self.smiley, width=RESET_WIDTH, height=RESET_HEIGHT, command=self.Reset)
      self.ResetButton.grid(row=0, column=1, sticky="n")

      self.FlagCount = tk.Label(self, textvariable=self.flags, font=('times', '20', 'bold'))
      self.FlagCount.grid(row=0, column=2, sticky="w", padx=15)
      
      # configure the right and left column to be far left and right
      self.grid_columnconfigure(1, weight=2)

      self.MineFrame = tk.Frame(self)

      # make the buttons
      rowNum = 0;

      # create all the tiles and insert them into the two arrays.
      # the one is 2d array for the ripple algorithm to look like the grid
      # and the 1d is forsearching easier
      for colNum in range(self.row*self.col):
         tile = Tile(self.MineFrame, self, rowNum, colNum%self.col, self.mode)
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
      if(time < 999):
         time = time + 1
      
      # convert back to a string and add leading zeros
      self.timeCount = str(time).zfill(3) # fill 3 spaces with zeros
      self.time.set(self.timeCount)

      # call the timer again after one second
      if(not self.gameOver):
         self.after(1000, self.updateTime)

   # Called when a bomb is clicked to set as game over
   def GameOver(self):
      self.gameOver = True

      self.ResetButton.config(image=self.deadSmiley)

      # show the bombs at the end
      for tile in self.tileArray:
         tile.showBomb()

   # called when a tile is pressed. It is the algorithm to 
   # open up the appropriate tiles based on the click
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
               # if there was a tile that was a zero next to a pressed one it was set as
               # needs updated in the checkTiles() function. This looping creates the 
               # ripple effect when clicking on a zero tile and exposing the appropriate tiles
               if(tileToCheck.toUpdate):  # check if the tile needs updated
                  self.checkTiles(tileToCheck)  # update the tile
                  numOfTilesToUpdate += 1

            if(numOfTilesToUpdate == 0): # no more tiles break
               toUpdate = False

            numOfTilesToUpdate = 0

      self.checkForWin()

   # increases the flag count by one
   def incrementFlag(self):
      self.flagCount = str(int(self.flagCount) + 1).zfill(3)
      self.flags.set(self.flagCount)

   # decreases the flag count by one
   def decrementFlag(self):
      self.flagCount = str(int(self.flagCount) - 1).zfill(3)
      self.flags.set(self.flagCount)

   # looks to see if there are only bomb tiles left and tells the game is over
   # if there is a win
   def checkForWin(self):
      numOfTilesNotPressed = 0

      # check for a win!
      for tileToCheck in self.tileArray:
         # if there is no pressed tile and all of them are bombs is a win
         if(not tileToCheck.isPressed() and not tileToCheck.isBomb()):
            numOfTilesNotPressed += 1

      # no tiles that are pressed meaning the left over are bombs
      if(numOfTilesNotPressed == 0):
         self.gameOver = True
         self.ResetButton.config(image=self.sunglassesSmiley)
         print("GAME WON!!!!!!!!!!")
         print("Congratulations!")

   def checkTiles(self, tile):
      # the row and col of the tile that needs checked
      row = tile.row
      col = tile.col

      tile.updateState()   # update the surrounding 8 tiles 

      # bounds check the rows and columns. If there is a zero mark that it still needs updated.
      # if there is just number then it doesn't need check so just show the tile
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
     
   # Reset the gameboard
   def Reset(self):
      print("Game reset...")

      # reset the reset button and disable until it is done resetting
      self.ResetButton.config(image=self.smiley, state=tk.DISABLED)

      # reset the game flag count and timer
      self.timeCount = RESET_COUNT
      self.time.set(self.timeCount)

      self.flagCount = str(self.startingBombCount).zfill(3)
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

      self.ResetButton.config(state=tk.NORMAL) # enable the button to be pressed now that it is reset

   # This loops through and add bombs
   # Then it increases the tile count to the appropriate count
   def RandomizeBombs(self):
      # pick the bombs at random
      bombs = sample(self.tileArray, self.startingBombCount)

      # set the tiles as bombs that are bombs
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