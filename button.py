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
   def __init__(self, parent, gameFrame, row, col):
      # buttons specific variables
      self.gameFrame = gameFrame
      self.root = parent
      self.width = 1
      self.height = 1

      self.row = row
      self.col = col

      self.state = State.START
      self.count = 0
      self.bomb = False

      self.toUpdate = False

      # initialize the button
      # tk.Button.__init__(self, parent, width=self.width, height=self.height, command=self.leftButtonClick, bg=STARTING_COLOR, textvariable=self.count, font=('times', '10', 'bold'))
      tk.Button.__init__(self, parent, width=self.width, height=self.height, font=('times', '10', 'bold'), bg=STARTING_COLOR)
      
      # attach functions for each button click
      self.bind('<Button-1>', self.leftButtonClick)
      self.bind('<Button-3>', self.rightButtonClick)

   def leftButtonClick(self, event):
   	  if(self.state == State.PRESSED):
   	     None
   	  elif(self.state == State.START):
   	     self.state = State.PRESSED
   	     self.config(background=PRESSED_COLOR, state=tk.DISABLED, text=str(self.count))
   	     if(self.count == 0):
   	     	self.gameFrame.UpdateTiles(self)
   	  elif(self.state == State.BOMB):
   	     if(self.bomb):
   	     	print("Game Over......     :(")
   	     	self.gameFrame.GameOver()
   	  elif(self.state == State.FLAG):
   	     None
   	  elif(self.state == State.QUESTIONABLE):
   	     None

   def rightButtonClick(self, event):
   	  if(self.state == State.PRESSED):
   	  	None
   	  elif(self.state == State.START):
   	  	self.state = State.FLAG
   	  	self.config(background=FLAG_COLOR, state=tk.DISABLED)
   	  elif(self.state == State.BOMB):
   	  	self.state = State.FLAG
   	  	self.config(background=FLAG_COLOR, state=tk.DISABLED)
   	  elif(self.state == State.FLAG):
   	  	self.state = State.QUESTIONABLE
   	  	self.config(background=QUESTION_COLOR, state=tk.DISABLED)
   	  elif(self.state == State.QUESTIONABLE):
   	  	if(self.bomb):
   	  	   self.state = State.BOMB
   	  	else:
   	  	   self.state = State.START
   	  	self.config(background=STARTING_COLOR, state=tk.NORMAL)

   def updateState(self):
         if(self.state == State.PRESSED):
            None
         elif(self.state == State.START):
            if(not self.bomb):
               self.state = State.PRESSED
               self.config(background=PRESSED_COLOR, state=tk.DISABLED, text=str(self.count))
         elif(self.state == State.BOMB):
            None
         elif(self.state == State.FLAG):
            None
         elif(self.state == State.QUESTIONABLE):
            None
         self.toUpdate = False

   def needUpdate(self):
      self.toUpdate = True

   # makes the state of the tile a bomb
   def setBombTile(self):
      self.state = State.BOMB
      # self.config(bg=BOMB_COLOR)
      self.bomb = True

   # used to increase the count when looping over the bombs
   def increaseTileCount(self):
      # increase count based on the last value
      if(not self.isBomb()):	# only increment count if it isn't a bomb
         self.count += 1

   def showBomb(self):
   	  if(self.bomb):
   	  	self.config(bg=BOMB_COLOR)

   # returns true if the tile is a bomb false otherwise
   def isBomb(self):
   	  if(self.state == State.BOMB):
   	  	return True
   	  else:
   	  	return False

   # returns the state of the button
   def isPressed(self):
      if(self.state == State.PRESSED):
         return True
      else:
         return False

   def reset(self):
   	  self.state = State.START
   	  self.count = 0
   	  self.bomb = False
   	  self.config(state=tk.NORMAL, bg=STARTING_COLOR, width=self.width, height=self.height, text="")