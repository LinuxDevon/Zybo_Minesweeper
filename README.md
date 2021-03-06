# Zybo_Minesweeper
This is a project for class ECE 530 Introduction to Microprocessors. This is the final project for the class that I choose. It is going to be on the Zybo FPGA/Arm board using Xilinux for the OS. 

Tile Images From:
https://github.com/JordanMontgomery/Minesweeper

# Setup
## Installing Xillinux
I  started by installing Xillinux with the given instructions from Dr. Song. There is a copy of them in the Resources folder.

Setup SD card by moving the approptiate files in the instructions. If you don't have Vivado I included the boot.bin, devicetree.dtb, and 
xillydemo.bit in the Resource folder. The Uimage file is excluded due to the size. You have to go to http://www.xillybus.com/xillinux to 
retrieve that file.

## Start the desktop on startup
https://wiki.archlinux.org/index.php/Xinit#Autostart_X_at_login
Run startx on startup:

Put this at the end of ~/.bash_profile
```
if [[ ! $DISPLAY && $XDG_VTNR -eq 1 ]]; then
  exec startx
fi
```

## Testing the SSH connection for internet
1. Connect ethernet from the Zybo to the laptop. Set the laptop to share wifi through properites of the WIFI connection.
2. Set IP to 192.168.137.2 on Zybo.
3. Set IP to 192.168.137.1 on the Laptop.
4. Ping 8.8.8.8 and google.com to confirm working internet.
	- `ping 8.8.8.8`

## installing the libraries
Install the libraries by running the script: `install.sh` in the Scripts folder

# Running the game
Start the game by typing `./main.py`.

To get an idea of the options type `./main.py -h`
