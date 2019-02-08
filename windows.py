#!/usr/bin/python3

import tkinter as tk
from button import *

# -- DEFINES -- #
PAD = 5

class TopWindow(tk.Frame):
   def __init__(self, parent):
      tk.Frame.__init__(self,parent) # create the frame to attach to the root
      self.root = parent

      # timer setup
      self.time = tk.StringVar() # make the time a variable
      self.time.set("000")        # set to zero

      # The number of flags available to check on the board
      self.flags = tk.StringVar() # number of flags available
      self.flags.set("004") 

      self.Widgets()
      

   # attach the widgets that are apart of the frame
   def Widgets(self):
      self.Timer = tk.Label(self, textvariable=self.time)
      # self.Timer.pack(side=tk.LEFT, fill=tk.X, padx=PAD, ipadx=PAD, ipady=PAD, pady=PAD)
      self.Timer.grid(row=0, column=0, sticky="e")

      self.ResetButton = tk.Button(self, text="R", command=self.Reset)
      # self.ResetButton.pack(side=tk.LEFT, fill=tk.X)
      self.ResetButton.grid(row=0, column=1, sticky="n")

      self.FlagCount = tk.Label(self, textvariable=self.flags)
      # self.FlagCount.pack(side=tk.LEFT, fill=tk.X, padx=PAD, ipadx=PAD, ipady=PAD, pady=PAD)
      self.FlagCount.grid(row=0, column=2, sticky="w")

   # place holder for reset function to the gameboard
   def Reset(self):
      print("game reset")

# The main window that holds the board 
class MineWindow(tk.Frame):
   def __init__(self, parent):
      tk.Frame.__init__(self,parent) # create a frame to attach to the root
      self.root = parent
      self.height = 1
      self.width = 1

      self.tiles = [[],[]]

      self.Widgets()

   # attach the widgets that are apart of the frame
   def Widgets(self):
      row = 0;
      for n in range(9):
         button = tk.Button(self, width=self.width, height=self.height)
         button.grid(row=row, column=n%3)

         if(n%3 == 2):
            row += 1

class Window(tk.Frame):
   def __init__(self, parent):
      tk.Frame.__init__(self,parent) # create the frame to attach to the root
      self.root = parent

      # timer setup
      self.time = tk.StringVar() # make the time a variable
      self.time.set("000")        # set to zero

      # The number of flags available to check on the board
      self.flags = tk.StringVar() # number of flags available
      self.flags.set("004") 

      self.root = parent
      self.height = 1
      self.width = 1

      self.tiles = [[],[]]

      self.Widgets()

   # attach the widgets that are apart of the frame
   def Widgets(self):
      self.Timer = tk.Label(self, textvariable=self.time)
      # self.Timer.pack(side=tk.LEFT, fill=tk.X, padx=PAD, ipadx=PAD, ipady=PAD, pady=PAD)
      self.Timer.grid(row=0, column=0, sticky="e", padx=15)

      self.ResetButton = tk.Button(self, text="R", command=self.Reset)
      # self.ResetButton.pack(side=tk.LEFT, fill=tk.X)
      self.ResetButton.grid(row=0, column=1, sticky="n")

      self.FlagCount = tk.Label(self, textvariable=self.flags)
      # self.FlagCount.pack(side=tk.LEFT, fill=tk.X, padx=PAD, ipadx=PAD, ipady=PAD, pady=PAD)
      self.FlagCount.grid(row=0, column=2, sticky="w", padx=15)
      
      # configure the right and left column
      self.grid_columnconfigure(1, weight=2)
      #self.grid_columnconfigure(2, weight=2)

      self.MineFrame = tk.Frame(self)

      row = 0;
      for n in range(100):
         button = tk.Button(self.MineFrame, width=self.width, height=self.height)
         button.grid(row=row, column=n%10)

         if(n%10 == 9):
            row += 1

      self.MineFrame.grid(row=1, column=0, columnspan=3)

   # place holder for reset function to the gameboard
   def Reset(self):
      print("game reset")