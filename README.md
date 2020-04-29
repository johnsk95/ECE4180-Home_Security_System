# ECE4180 Project Spring 2020 - Home Security System
Home Security System using Raspberry Pi  
__Team members__: Rachel Tierney, John Seon Keun Yi  

## Introduction
The Home Security System is designed and built for the final project of Embedded Systems Design (ECE4180) at Georgia Tech.  
This system uses a Raspberry Pi 3B and a ToF distance sensor to detect an approaching object (person) and trigger an alarm.
We also use an mbed board connected to an LCD to display a message sent from the website.   
One stand-out feature of this project is that every function of the system such as camera stream and alarm status is observable and controllable via a website connected to the Pi. 

[Demo video link](https://www.youtube.com/watch?v=90K8kdUWc1k)  
[Presentation link](https://www.dropbox.com/s/lmhxl2stzh04p3s/ECE4180_presentation_Tierney_Yi.ppsx?dl=0) (Same file also uploaded on repo)

## Getting Started
The instructions below will help you set up the components needed for this system. 

### Parts Used
- [Raspberry Pi 3B+](https://www.raspberrypi.org/products/raspberry-pi-3-model-b-plus/)
- [Pi Camera](https://www.raspberrypi.org/products/camera-module-v2/)
- [Pi Cobbler](https://thepihut.com/products/adafruit-assembled-pi-t-cobbler-plus-gpio-breakout-pi-a-b-pi-2-pi-3-zero)
- [Adafruit VL53L0X ToF sensor](https://www.adafruit.com/product/3317)
- [Basic LED](https://www.sparkfun.com/products/9590) (A resistor around 330 Ohms is also needed!)
- [mbed LPC1768](https://os.mbed.com/platforms/mbed-LPC1768/)
- [uLCD-144-G2 LCD module](https://4dsystems.com.au/ulcd-144-g2)
- Bluetooth Speaker, or any wired speaker that connects to the Pi
- Miscellaneous HW: breadboard, jumper wires

### Software
- Python 3
- flask
- socketio
- OpenCV
- AJAX
- Javascript
- C++

## Part 1. Assembling the Hardware
### Raspberry Pi
![assembly](https://i.imgur.com/Rb73GCd.jpg|width=100)
For this project you need a Raspberry Pi with its GPIO pins linked to a breadboard using a Pi Cobbler.  
We used a Raspberry Pi 3B+ model for our implementation.  
1. Connect the Pi Camera to the Pi as seen [here](https://projects.raspberrypi.org/en/projects/getting-started-with-picamera). Use the link to enable and test the camera
2. Connect the ribbon cable to the GRIO pins on the Pi and the Pi cobbler
3. Insert the Pi cobbler to a breadboard
4. Connect the LED to the GPIO pin #17
The wiring table is as follows:  

| Pi | LED |
| --- | --- |
| GPIO17 | + |
| GND | - * |  

\* Note that the - pin of the LED has to go through a resistor (100-330Ohms) before going into GND  

5. Connect the ToF sensor to the Pi
The wiring table is as follows: 

| Pi | Sensor |
| --- | --- |
| 3V3 | VIN |
| GND | GND |
| SCL | SCL |
| SDA | SDA |  

### Mbed 
The Mbed board is used to receive a message sent from the home secucity web server and display it on an LCD.  
Insert the mbed into a breadboard. Then connect the LCD to the mbed.  
The wiring table is as follows:    

| Pi | Mbed | uLCD |
| --- | --- | --- |
| 5v* |  | +5V |
|  | p27 |  TX  |
|  | p28 |  RX  |
|  | GND |  GND  |
|  | p30 |  RES  |

\* The LCD needs 5V power to run. Connect the 5V on the lcd to the 5V output pin on the Pi. 

The overall wiring schamatic is as follows:  
![schematic](https://i.imgur.com/bKOOpgh.png)

## Part 2. Setting up the software environment  
### Compiling text receiving code to mbed
Connect the mbed with a PC. Download the code to receive messages sent from the pi web server and display on the LCD [here](https://os.mbed.com/users/jyi62/code/serialtoLCD/)  
Compile and insert the code on the mbed board.  
Disconnect from the PC. Connect the usb cord from the mbed to one of the usb ports on the Pi.  
To see if the mbed is connected to the Pi, enter below line on the terminal  
``` ls /dev/ttyACM ```  

You should see something like `/dev/ttyACM0`. If you do, the mbed is successfully connected to the Pi.  

### Setting up the Pi 
Everything else is done inside the Raspberry Pi. You may access the Pi using peripherals directly connected to it or use a remote access such as [VNC Viewer](https://www.realvnc.com/en/connect/download/viewer/0)  
Make sure the Raspbian OS is installed in your Pi. Specific instructions are on the raspi webpage.  
Connect a speaker to the raspi. You can either connect a wired speaker through the audio jack on the Pi, or connect a bluetooth speaker. Instructions to connect a bluetooth speaker is [here](https://github.com/binnes/tobyjnr/wiki/Getting-Sound-to-work-on-the-Raspberry-Pi)  
If you haven't, connect the Pi to the same wireless network as your host computer/device. You need to be on the same network to access the pi server.  

### Setting up the server
Clone this repository using command:
```git clone https://github.com/johnsk95/ECE4180-Home_Security_System.git```  
Navigate to the repo using:
```cd ECE4180-Home_Security_System```

Install python required libraries using the command  
```sudo pip3 install picamera opencv-python numpy flask flask_session flask-socketio RPI.GPIO digitalio adafruit-blinka adafruit-circuitpython-vl53l0x serial```

Run this command to look up the Pi's IP
```ifconfig```
Since we are connecting through wifi, look in the part labeled 'wlan'  
![ipaddr](https://i.imgur.com/ELT4o66.png)  

In this example, the if we will use is `192.168.88.213`  

The main code for this project is comprised of three parts.  
`home_security.py` Main execution code. Links and activates the hardware. (LED, ToF, sound, camera) This is where the system monitors the distance with the ToF sensor and triggers the alarm.  
`camera.py` Controls the camera. Deals with recording videos and streaming the camera feed to the server.  Also records stream on command.
`server.py` Broadcasts the website and transmits messages to and from between the pi and the website.  

You need to enter your Pi's IP address in `server.py`.  
Go to `start_server()`, and in line 181  
![server_ip](https://i.imgur.com/BuOFfkr.png)  

Change `'0.0.0.0'` to the IP address you found out above.  The home seciruty website will be broadcasted to this address.  

### Adjusting trigger distance
This system triggers an alarm if an object comes within a set distance. This is done by periodically monitoring the distance using the ToF distance sensor.  
This is controlled in line 73 in `home_security.py`.   
![distance](https://i.imgur.com/dHfyXkK.png)  
The default distance is set to 40cm (400mm) You can change the distance if you want. 

## Part 3. Running the System
Run this command to activate the home security system
```python3 home_security.py```
In the terminal you will see something like this:  
![running](https://i.imgur.com/ZFX34Q1.png)  
The camera and server needs a couple seconds to activate.  
Now the security system is online and the server is active!  
To access the website, go the the address in the command line using a device connected to the same network as the Pi.  
For example, if your Pi's IP address is `192.168.88.213`, type in `http://192.168.88.213:8000` in a web browser.  

This is the website to control and monitor the security system. 

![w1](https://i.imgur.com/Wmfke8C.png)
![w2](https://i.imgur.com/ARpwagC.png)

The website shows a live feed from the Pi camera.  
When someone approaches within a set distance, the alarm is triggered. The LED flashed and a siren is played through the speaker for 10 seconds. The host is notified through the website through a warning popup.

![warning](https://i.imgur.com/3toJMxC.png)  

A popup will appear on the webpage when the alarm is triggered. You can stop the alarm midway by pressing the Stop Alarm button on this popup. 
When the alarm is triggered, the Pi records and saves a video of the camera feed. This is saved locally in `/static/videos` You can select and play the recorded videos using the drop down menu on the website.  

You can also arm/disarm the alarm or manually record the camera feed through the Record and Arm buttons on the top. The recording and arm status is also displayed on the top of the webpage.  

Lastly, you can send a message from the website to be viewed on the lcd attached to the mbed.  

![msg](https://i.imgur.com/thZ0Bjr.png)
![lcd](https://i.imgur.com/TFQStrw.jpg|height=200)

A detailed overview of the functions of the Home Security System is described on the demo video. Follow the link on the top of this page to see the demo.  