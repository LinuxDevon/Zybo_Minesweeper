#!/usr/bin/python3

# -- INLCUDES -- #
import tkinter as tk

# -- DEFINES -- #
TITLE = "The Best Minesweeper"
PAD = 5

class TopWindow(tk.Frame):
   def __init__(self, parent):
      tk.Frame.__init__(self,parent) # create the frame to attach to the root
      self.root = parent

      # timer setup
      self.time = tk.StringVar() # make the time a variable
      self.time.set("000")        # set to zero

      self.flags = tk.StringVar() # number of flags available
      self.flags.set("004") 

      self.Widgets()
      

   # attach the widgets that are apart of the frame
   def Widgets(self):
      self.Timer = tk.Label(self, textvariable=self.time)
      self.Timer.pack(side=tk.LEFT, fill=tk.X, padx=PAD, ipadx=PAD, ipady=PAD, pady=PAD)

      self.ResetButton = tk.Button(self, text="R", command=self.Reset)
      self.ResetButton.pack(side=tk.LEFT, fill=tk.X)

      self.FlagCount = tk.Label(self, textvariable=self.flags)
      self.FlagCount.pack(side=tk.LEFT, fill=tk.X, padx=PAD, ipadx=PAD, ipady=PAD, pady=PAD)

   def Reset(self):
      print("game reset")

# The main window that holds the board 
class MineWindow(tk.Frame):
   def __init__(self, parent):
      tk.Frame.__init__(self,parent) # create a frame to attach to the root
      self.root = parent
      self.height = 5
      self.width = 5

      
      

   def Widgets(self):
      for n in range(10):
         

# function is used to create the main root frame
# everything is attached to this window.
def startApplication():
   root = tk.Tk()
   root.title(TITLE)
   print("Root window created")

   print("Starting the mine window")
   mineWindow = MineWindow(root)
   mineWindow.pack(fill=tk.BOTH, side=tk.BOTTOM)

   print("Starting the top window")
   topWindow = TopWindow(root)
   topWindow.pack(fill=tk.BOTH, side=tk.TOP)

   print("Running main loop... the game loop")
   root.mainloop()

# start code for the game
if __name__ == "__main__":
   print("==========================================")
   print("Starting Application")

   startApplication()
   
   print("Application closed")
   print("=========================================")
