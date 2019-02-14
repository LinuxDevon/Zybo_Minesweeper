#!/usr/bin/python3

import tkinter as tk
from enum import Enum

# -- DEFINES -- #

# enum for the State of the tiles
class State(Enum):
	PRESSED = 0
	START = 1
	BOMB = 2
	FLAG = 3
	QUESTIONABLE = 4

# The class is a tile that contains a number or bomb
# The tile itself is a button.
# INPUTS:
#     parent - the frame to place the buttons in
#     gameFrame - the overall frame that holds everything
#     row - the row the button is being placed in
#     col - the column the button is being placed in
#     mode - tells the button if cheater mode is on or not (true/false)
#            If it is true then the bomb is displayed
class Tile(tk.Button):
   def __init__(self, parent, gameFrame, row, col, mode):
      # buttons specific variables
      self.gameFrame = gameFrame
      self.root = parent
      self.width = 15
      self.height = 15
      self.isCheatMode = mode

      self.toUpdate = False

      self.row = row
      self.col = col

      self.state = State.START
      self.count = 0
      self.bomb = False

      self.loadImages() # the the appropriate images from the Tiles folder

      # initialize the button
      tk.Button.__init__(self, parent, width=self.width, height=self.height, image=self.coveredTile)

      # attach functions for each button click
      self.enableButtons()

   # reads all the tile images that will be used for the buttons
   # these are the bomb tiles, number tiles, question tile, flag tile, and the default hidden tile
   def loadImages(self):
      self.bombTile = tk.PhotoImage(file="Tiles/greymine.png")
      self.explodeBombTile = tk.PhotoImage(file="Tiles/mine.png")
      self.noBombTile = tk.PhotoImage(file="Tiles/nomine.png")

      self.numbers = [0] * 9

      self.numbers[0] = tk.PhotoImage(file="Tiles/blank.png")
      self.numbers[1] = tk.PhotoImage(file="Tiles/one.png")
      self.numbers[2] = tk.PhotoImage(file="Tiles/two.png")
      self.numbers[3] = tk.PhotoImage(file="Tiles/three.png")
      self.numbers[4] = tk.PhotoImage(file="Tiles/four.png")
      self.numbers[5] = tk.PhotoImage(file="Tiles/five.png")
      self.numbers[6] = tk.PhotoImage(file="Tiles/six.png")
      self.numbers[7] = tk.PhotoImage(file="Tiles/seven.png")
      self.numbers[8] = tk.PhotoImage(file="Tiles/eight.png")

      self.coveredTile = tk.PhotoImage(file="Tiles/covered.png")

      self.questionTile = tk.PhotoImage(file="Tiles/question.png")
      self.flagTile = tk.PhotoImage(file="Tiles/flagged.png")

   # This is changes the appropriate state based on the button click
   def leftButtonClick(self, event):
      # if it is in the start state that means that it was just pressed
      if(self.state == State.START):
         self.state = State.PRESSED

         # display the tile number
         self.config(image=self.numbers[self.count])
         self.disableButtons()   # don't allow the button to be pressed anymore

         if(self.count == 0): # only update other tiles if it is a zero
            self.gameFrame.UpdateTiles(self)
         else: # might be a win if it is a number need to check though
            self.gameFrame.checkForWin() 

      # if i was a bomb that means the game is over
      elif(self.state == State.BOMB):
         if(self.bomb):
            print("Game Over......     :(")
            self.gameFrame.GameOver()
            self.config(image=self.explodeBombTile)

   # This is changes the appropriate state based on the button click
   def rightButtonClick(self, event):
      # change to the flag and show it after first click
      if(self.state == State.START):
         self.state = State.FLAG
         self.config(image=self.flagTile)
         self.gameFrame.decrementFlag()
      elif(self.state == State.BOMB):
         self.state = State.FLAG
         self.config(image=self.flagTile)
         self.gameFrame.decrementFlag()

      # next click means it is a question mark
      elif(self.state == State.FLAG):
         self.state = State.QUESTIONABLE
         self.config(image=self.questionTile)
         self.gameFrame.incrementFlag()

      # go back to original state on next click
      elif(self.state == State.QUESTIONABLE):
         if(self.bomb):
            self.state = State.BOMB
         else:
            self.state = State.START
         self.config(image=self.coveredTile)

   # used to display the appropirate tile when checking
   # and updating the tiles after being pressed. 
   def updateState(self):
      if(self.state == State.PRESSED):
         self.toUpdate = False
      elif(self.state == State.START):
         if(not self.bomb):
            self.state = State.PRESSED
            self.config(image=self.numbers[self.count])
            self.disableButtons()
      elif(self.state == State.BOMB):
         self.toUpdate = False
      elif(self.state == State.FLAG):
         self.toUpdate = False
      elif(self.state == State.QUESTIONABLE):
         self.toUpdate = False

   # Set tile to need to update to update later
   def needUpdate(self):
      if(not self.bomb):
         self.toUpdate = True

   # makes the state of the tile a bomb
   def setBombTile(self):
      self.state = State.BOMB
      self.bomb = True

      # display bomb when cheat mode is on
      if(self.isCheatMode):
         self.config(image=self.bombTile)

   # used to increase the count when looping over the bombs
   def increaseTileCount(self):
      # increase count based on the last value
      if(not self.isBomb()):	# only increment count if it isn't a bomb
         self.count += 1

   # check the tile and show bomb if it is a bomb
   # if there was a flag and no bomb then display the no bomb tile
   def showBomb(self):
      self.disableButtons()
      if(self.state == State.FLAG  and not self.bomb):
         self.config(image=self.noBombTile) 
      elif(self.bomb):
         self.config(image=self.bombTile)

   # returns true if the tile is a bomb false otherwise
   def isBomb(self):
   	  return self.bomb

   # returns true if the button is pressed otherwise false
   def isPressed(self):
      if(self.state == State.PRESSED):
         return True
      else:
         return False

   # enable button presses by binding the appropriate functions the 
   # appropriate buttons
   def enableButtons(self):
      self.bind('<Button-1>', self.leftButtonClick)
      self.bind('<Button-3>', self.rightButtonClick)

   # disable button presses by binding the appropriate functions the 
   # appropriate buttons
   def disableButtons(self):
      self.unbind('<Button-1>')
      self.unbind('<Button-3>')

   # resets the button value to the defaults
   # enables clicks again and show the covered tile 
   def reset(self):
      self.state = State.START
      self.count = 0
      self.bomb = False
      self.toUpdate = False
      self.config(image=self.coveredTile)
      self.enableButtons()