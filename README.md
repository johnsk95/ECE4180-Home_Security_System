# ECE4180 Project Spring 2020 - Home Security System
Home Security System using Raspberry Pi  
Team members: Rachel Tierney, John Seon Keun Yi  

## Introduction
The Home Security System is designed and built for the final project of Embedded Systems Design (ECE4180) at Georgia Tech.  
This system uses a Raspberry Pi 3B and a ToF distance sensor to detect an approaching object (person) and trigger an alarm.
We also use an mbed board connected to an LCD to display a message sent from the website.   
One stand-out feature of this project is that every function of the system such as camera stream and alarm status is observable and controllable via a website connected to the Pi. 

Demo:  
Presentation: 

## Getting Started
The instructions below will help you set up the components needed for this system. 

### Parts Used
- [Raspberry Pi 3B+](https://www.raspberrypi.org/products/raspberry-pi-3-model-b-plus/)
- [Pi Camera](https://www.raspberrypi.org/products/camera-module-v2/)
- [Pi Cobbler](https://thepihut.com/products/adafruit-assembled-pi-t-cobbler-plus-gpio-breakout-pi-a-b-pi-2-pi-3-zero)
- [mbed LPC1768](https://os.mbed.com/platforms/mbed-LPC1768/)
- [Adafruit VL53L0X ToF sensor](https://www.adafruit.com/product/3317)
- [uLCD-144-G2 LCD module](https://4dsystems.com.au/ulcd-144-g2)
- [Basic LED](https://www.sparkfun.com/products/9590) (A resistor around 330 Ohms is also needed!)
- Bluetooth Speaker, or any wired speaker that connects to the Pi
- Miscellaneous HW: breadboard, jumper wires

### Software
- Python 3
- flask
- ...

## Assembling the Hardware
### Raspberry Pi
![assembly](https://i.imgur.com/Rb73GCd.jpg)
For this project you need a Raspberry Pi with its GPIO pins linked to a breadboard using a Pi Cobbler.  
We used a Raspberry Pi 3B+ model for our implementation.  
1. Connect the Pi Camera to the Pi as seen [here](https://projects.raspberrypi.org/en/projects/getting-started-with-picamera). Use the link to enable and test the camera
2. Connect the ribbon cable to the GRIO pins on the Pi and the Pi cobbler
3. Insert the Pi cobbler to a breadboard
4. Connect the LED to the GPIO pin #17
The wiring table is as follows:
| Pi        | LED           |
| ------------- |:------------:|
| GPIO17 | + |
| GND | - |
* Note that the - pin of the LED has to go through a resistor (100-330Ohms) before going into GND  

5. Connect the ToF sensor to the Pi
The wiring table is as follows:
| Pi        | Sensor           |
| ------------- |:------------:|
| 3V3 | VIN |
| GND | GND |
| SCL | SCL |
| SDA | SDA |


### Mbed 
The Mbed board is used to receive a message sent from the home secucity web server and display it on an LCD.  
Insert the mbed into a breadboard. Then connect the LCD to the mbed.  
The wiring table is as follows:  
| Pi        | Mbed           | uLCD  |
| ------------- |:-------------:| -----:|
|   5v   |  | +5V |
|  | p27      |  TX  |
|  | p28      |  RX  |
|  | GND      |  GND  |
|  | p30      |  RES  |

* The LCD needs 5V power to run. Connect the 5V on the lcd to the 5V output pin on the Pi. 

The overall wiring schamatic is as follows:
![schamatic](https://i.imgur.com/uHkqsJr.png)

## Setting up the software environment
### Compiling text receiving code to mbed
Connect the mbed with a PC. Download the code to receive messages sent from the pi web server and display on the LCD [here](https://os.mbed.com/users/jyi62/code/serialtoLCD/)  
Compile and insert the code on the mbed board.  
Disconnect from the PC. Connect the usb cord from the mbed to one of the usb ports on the Pi.  
To see if the mbed is connected to the Pi, enter below line on the terminal
``` ls /dev/ttyACM ```  
You should see something like `/dev/ttyACM0`. If you do, the mbed is successfully connected to the Pi.  

### Setting up the Pi web server
Everything else is done inside the Raspberry Pi. You may access the Pi using peripherals directly connected to it or use a remote access such as [VNC Viewer](https://www.realvnc.com/en/connect/download/viewer/0)  
Clone this repository using command:  
```git clone https://github.com/johnsk95/ECE4180-Home_Security_System.git```  

### Installing libraries

