#!/usr/bin/python3

# -- INLCUDES -- #
import tkinter as tk
import sys, getopt
from windows import *

# -- DEFINES -- #
TITLE = "The Best Minesweeper"
ROW = 10
COL = 10
TOTAL_BOMBS = 10
NO_CHEAT = False

# function is used to create the main root frame
# everything is attached to this window.
def startApplication(totalRows, totalCols, totalBombs, mode):
   root = tk.Tk()
   root.title(TITLE)
   print("Root window created")

   window = Window(root, totalRows, totalCols, totalBombs, mode)
   window.pack(fill=tk.BOTH)

   print("Running main loop... the game loop")
   root.mainloop()

# start code for the game
def main(argv):
   rows = ROW
   cols = COL
   bombs = TOTAL_BOMBS
   mode = NO_CHEAT
   try:
      opts, args = getopt.getopt(argv,"hr:c:b:m",["rows=","columns=","bombs="])
   except getopt.GetoptError:
      print("INPUT ERROR...")
      print('./main.py -h for help...')
      sys.exit(2)
   for opt, arg in opts:
      if opt == '-h':
         print("The options are:")
         print('./main.py -r <number of rows> -c <number of columns> -b <total bombs> -m')
         print()
         print(" <number of rows> - must be greater than 1")
         print(" <number of columns> - must be greater than 1")
         print(" <total bombs> - number of bombs in the game. Has to be fewer than rows*columns")
         print()
         print(" -m is to activate cheater mode: default is off")
         print()
         print("./main.py with no args defaults to rows=10, columns=10, total bombs=10")
         print
         sys.exit()
      elif opt in ("-r", "--ifile"): # row number
         rows = arg
      elif opt in ("-c", "--ifile"): # column number
         cols = arg
      elif opt in ("-b", "--ifile"): # bomb number
         bombs = arg
      elif opt == '-m': # cheater mode
         mode = True

   rows = int(rows)
   cols = int(cols)
   bombs = int(bombs)

   if(bombs > rows*cols):
      printf("INPUT ERROR: Number of bombs exceeds the rows and columns!")
      sys.exit(2)

   if(rows < 1 or cols < 1):
      printf("INPUT ERROR: Too few rows or columns. They must be greater than 1.")
      sys.exit(2)

   print("These are the settings for this game:")
   
   # print out the settings being used for the game
   print()
   print("Number of rows:    " + str(rows))
   print("Number of columns: " + str(cols))
   print("Number of bombs:   " + str(bombs))
   print("Cheater mode is:   " + str(mode))
   print()

   print("==========================================")
   print("Starting Application")

   startApplication(rows, cols, bombs, mode)

if __name__ == "__main__":

   main(sys.argv[1:]) # send the command line arguments
   
   print("Application closed")
   print("==========================================")
