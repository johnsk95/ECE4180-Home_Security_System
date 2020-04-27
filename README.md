# ECE4180 Project Spring 2020 - Home Security System
Home Security System using Raspberry Pi  
Team members: Rachel Tierney, John Seon Keun Yi  

## Introduction
The Home Security System is designed and built for the final project of Embedded Systems Design (ECE4180) at Georgia Tech.  
This system uses a Raspberry Pi 3B and a ToF distance sensor to detect an approaching object (person) and trigger an alarm.  
One stand-out feature of this project is that every function of the system such as camera stream and alarm status is observable and controllable via a website connected to the Pi. 

Demo:  
Presentation: 

## Getting Started
The instructions below will help you set up the components needed for this system. 

### Parts Used
- [Raspberry Pi 3B+](https://www.raspberrypi.org/products/raspberry-pi-3-model-b-plus/)
- [Pi Camera](https://www.raspberrypi.org/products/camera-module-v2/)
- [Pi Cobbler](https://thepihut.com/products/adafruit-assembled-pi-t-cobbler-plus-gpio-breakout-pi-a-b-pi-2-pi-3-zero)
- [Adafruit VL53L0X ToF sensor](https://www.adafruit.com/product/3317)
- [Basic LED](https://www.sparkfun.com/products/9590) (A resistor around 330 Ohms is also needed!)
- Bluetooth Speaker, or any wired speaker that connects to the Pi
- Miscellaneous HW: breadboard, jumper wires

### Software
- Python 3
- flask
- ...

## Assembling the Hardware
![alt text](https://i.imgur.com/Xv41inH.jpg "hw_assembly")
For this project you need a Raspberry Pi with its GPIO pins linked to a breadboard using a Pi Cobbler.  
We used a Raspberry Pi 3B+ model for our implementation.  

1. Connect the Pi Camera to the Pi as seen [here](https://projects.raspberrypi.org/en/projects/getting-started-with-picamera). Use the link to enable and test the camera
2. Connect the ribbon cable to the GRIO pins on the Pi and the Pi cobbler
3. Insert the Pi cobbler to a breadboard
4. Connect the LED to the GPIO pin #17
The wiring table is as follows:

5. Connect the ToF sensor to the Pi
The wiring table is as follows:

The overall wiring diagram is as follows:


## Setting up the software environment
Everything is done inside the Raspberry Pi. You may access the Pi using peripherals directly connected to it or use a remote access such as [VNC Viewer](https://www.realvnc.com/en/connect/download/viewer/0)  

### Installing libraries

