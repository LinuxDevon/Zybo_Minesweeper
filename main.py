#!/usr/bin/python3

# -- INLCUDES -- #
import tkinter as tk
from windows import *

# -- DEFINES -- #
TITLE = "The Best Minesweeper"

# function is used to create the main root frame
# everything is attached to this window.
def startApplication():
   root = tk.Tk()
   root.title(TITLE)
   print("Root window created")

   window = Window(root)
   window.pack(fill=tk.BOTH)
   # print("Starting the mine window")
   # mineWindow = MineWindow(root)
   # mineWindow.pack(side=tk.BOTTOM)

   # print("Starting the top window")
   # topWindow = TopWindow(root)
   # topWindow.pack(fill=tk.X, side=tk.TOP)

   print("Running main loop... the game loop")
   root.mainloop()

# start code for the game
if __name__ == "__main__":
   print("==========================================")
   print("Starting Application")

   startApplication()
   
   print("Application closed")
   print("=========================================")
