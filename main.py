#!/usr/bin/python3

# -- INLCUDES -- #
import tkinter as tk
import sys, getopt
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

   print("Running main loop... the game loop")
   root.mainloop()

# start code for the game
def main(argv):
   startApplication()
   # try:
   #    opts, args = getopt.getopt(argv,"hr:c",["ifile=","columns="])
   # except getopt.GetoptError:
   #    print 'main.py -i <inputfile> -o <outputfile>'
   #    sys.exit(2)
   # for opt, arg in opts:
   #    if opt == '-h':
   #       print 'test.py -i <inputfile> -o <outputfile>'
   #       sys.exit()
   #    elif opt in ("-i", "--ifile"):
   #       inputfile = arg
   #    elif opt in ("-o", "--ofile"):
   #       outputfile = arg

if __name__ == "__main__":
   print("==========================================")
   print("Starting Application")

   main(sys.argv[1:]) # send the command line arguments
   
   print("Application closed")
   print("=========================================")
