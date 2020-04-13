import time
import board
import busio
import digitalio
import adafruit_vl53l0x
from picamera import PiCamera

led = digitalio.DigitalInOut(board.D17)
led.direction = digitalio.Direction.OUTPUT

i2c = busio.I2C(board.SCL, board.SDA)
lidar = adafruit_vl53l0x.VL53L0X(i2c)
lidar.measurement_timing_budget = 200000

trigger = True
alarm = False

timestamp = time.strftime('%b-%d-%Y_%H:%M', time.localtime())

def stream_camera():
	camera.start_preview()
	camera.start_recording(f'/recordings/{timestamp}.h264')
	sleep(10)
	camera.stop_recording()
	camera.stop_preview
	
def play_sound():
	return

def activate_alarm():
	print('alarm activated!')
	for _ in range(10):
		led.value = True
		time.sleep(0.5)
		led.value = False
		time.sleep(0.5)
		

while trigger:
	dist = lidar.range
	if (dist < 300) and (dist != 0):
		activate_alarm()
	time.sleep(0.2)

print('end!')
