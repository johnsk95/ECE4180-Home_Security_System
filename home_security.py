from guizero import App, Text, PushButton, TextBox
from gpiozero import LED
from time import sleep
import time
from picamera import PiCamera

led = LED(17)
camera = PiCamera()

timestamp = time.strftime('%b-%d-%Y_%H:%M', time.localtime())

def toggle_alarm():
	# toggle led and sound, start recording
	while True:
		led.on()
		sleep(0.5)
		led.off()
		sleef(0.5)
		
def start():
    start_button.disable()
    stop_button.enable()

def stop():
    start_button.enable()
    stop_button.disable()
    
def toggle_camera():
    camera.start_preview()
    camera.start_recording(f'/home/pi/pivids/{timestamp}.h264')
    sleep(5)
    camera.stop_recording()
    camera.stop_preview()
    
def toggle_mic():
    return
	
		
app = App(title='Home Security System')
appName = Text(app, text='Home Security System', width='fill', align='top')

start_button = PushButton(app, command=start)
stop_button = PushButton(app, command=stop, text="DISARM", enabled=False)

camera_button = PushButton(app, command=toggle_camera, text='Camera')
speak_button = PushButton(app, command=toggle_mic, text='Speak')

app.display()
