#!/usr/bin/python3

import tkinter as tk
from enum import Enum

# -- DEFINES -- #
STARTING_COLOR = "light gray"
PRESSED_COLOR = "gray"
BOMB_COLOR	= "blue"
FLAG_COLOR 	= "red"
QUESTION_COLOR = "yellow"

class State(Enum):
	PRESSED = 0
	START = 1
	BOMB = 2
	FLAG = 3
	QUESTIONABLE = 4

class Tile(tk.Button):
   def __init__(self, parent, gameFrame, row, col, mode):
      # buttons specific variables
      self.gameFrame = gameFrame
      self.root = parent
      self.width = 15
      self.height = 15
      self.isCheatMode = mode

      self.row = row
      self.col = col

      self.state = State.START
      self.count = 0
      self.bomb = False

      self.loadImages()

      self.toUpdate = False

      # initialize the button
      # tk.Button.__init__(self, parent, width=self.width, height=self.height, command=self.leftButtonClick, bg=STARTING_COLOR, textvariable=self.count, font=('times', '10', 'bold'))
      # tk.Button.__init__(self, parent, width=self.width, height=self.height, font=('times', '10', 'bold'), bg=STARTING_COLOR)
      tk.Button.__init__(self, parent, width=self.width, height=self.height, image=self.coveredTile)

      # attach functions for each button click
      self.enableButtons()

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

   def leftButtonClick(self, event):
      if(self.state == State.PRESSED):
         None
      elif(self.state == State.START):
         self.state = State.PRESSED
         self.config(image=self.numbers[self.count])
         self.disableButtons()
         if(self.count == 0):
            self.gameFrame.UpdateTiles(self)
         else:
            self.gameFrame.checkForWin() 
      elif(self.state == State.BOMB):
         if(self.bomb):
            print("Game Over......     :(")
            self.gameFrame.GameOver()
            self.config(image=self.explodeBombTile)
      elif(self.state == State.FLAG):
         None
      elif(self.state == State.QUESTIONABLE):
         None

   def rightButtonClick(self, event):
         if(self.state == State.PRESSED):
            None
         elif(self.state == State.START):
            self.state = State.FLAG
            self.config(image=self.flagTile)
            self.gameFrame.decrementFlag()
         elif(self.state == State.BOMB):
            self.state = State.FLAG
            self.config(image=self.flagTile)
            self.gameFrame.decrementFlag()
         elif(self.state == State.FLAG):
            self.state = State.QUESTIONABLE
            self.config(image=self.questionTile)
            self.gameFrame.incrementFlag()
         elif(self.state == State.QUESTIONABLE):
            if(self.bomb):
   	  	      self.state = State.BOMB
            else:
   	  	      self.state = State.START
            self.config(image=self.coveredTile)

   def updateState(self):
         if(self.state == State.PRESSED):
            self.toUpdate = False
            # None
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

   def needUpdate(self):
      if(not self.bomb):
         self.toUpdate = True

   # makes the state of the tile a bomb
   def setBombTile(self):
      self.state = State.BOMB
      self.bomb = True
      if(self.isCheatMode):
         self.config(image=self.bombTile)

   # used to increase the count when looping over the bombs
   def increaseTileCount(self):
      # increase count based on the last value
      if(not self.isBomb()):	# only increment count if it isn't a bomb
         self.count += 1

   def showBomb(self):
      self.disableButtons()
      if(self.state == State.FLAG  and not self.bomb):
         self.config(image=self.noBombTile) 
      elif(self.bomb):
         self.config(image=self.bombTile)

   # returns true if the tile is a bomb false otherwise
   def isBomb(self):
   	  return self.bomb

   # returns the state of the button
   def isPressed(self):
      if(self.state == State.PRESSED):
         return True
      else:
         return False

   def enableButtons(self):
      self.bind('<Button-1>', self.leftButtonClick)
      self.bind('<Button-3>', self.rightButtonClick)

   def disableButtons(self):
      self.unbind('<Button-1>')
      self.unbind('<Button-3>')

   def reset(self):
      self.state = State.START
      self.count = 0
      self.bomb = False
      self.toUpdate = False
      self.config(image=self.coveredTile)
      self.enableButtons()