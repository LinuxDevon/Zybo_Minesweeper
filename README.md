# Zybo_Minesweeper
This is a project for class ECE 530 Introduction to Microprocessors. This is the final project for the class that I choose. It is going to be on the Zybo FPGA/Arm board using Xilinux for the OS. 

Tile Images From:
https://github.com/pvinis/Distributed-Minesweeper

# Setup
I  started by installing Xillinux with the instructions Dr. Song given.

Setup SD card. couldn't run the project... had to have him give me the binary.

https://wiki.archlinux.org/index.php/Xinit#Autostart_X_at_login
Run startx on startup:

put this at the end of ~/.bash_profile
```
if [[ ! $DISPLAY && $XDG_VTNR -eq 1 ]]; then
  exec startx
fi
```
connect ethernet and set my laptop to share wifi.
Set IP to 192.168.137.2 on Zybo
Set IP to 192.168.137.1 on Zybo
ping 8.8.8.8 and google.com to confirm working internet.
install libraries:
sudo apt-get install python3 python3-dev python3-dbg python3-tk