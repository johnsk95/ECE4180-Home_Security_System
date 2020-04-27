import os, sys
import time
import board
import busio
import digitalio
import adafruit_vl53l0x
import server 
from camera import Camera
from signal import signal, SIGINT
import threading

led = digitalio.DigitalInOut(board.D17)
led.direction = digitalio.Direction.OUTPUT

i2c = busio.I2C(board.SCL, board.SDA)
lidar = adafruit_vl53l0x.VL53L0X(i2c)
lidar.measurement_timing_budget = 200000
	
def play_sound():
	#print('playing sound!')
	for _ in range(3):
		os.system('mpg321 siren.mp3')
		time.sleep(0.2)
		if server.get_stop_alarm():
			print("stop sound")
			break

def flash_led():
	for _ in range(10):
		led.value = True
		time.sleep(0.5)
		led.value = False
		time.sleep(0.5)
		if server.get_stop_alarm():
			print("stopped led")
			break
		
def activate_alarm():
	sound_thread = threading.Thread(target=play_sound)
	led_thread = threading.Thread(target=flash_led)
	server.start_recording_camera()
	sound_thread.start()
	led_thread.start()
	led_thread.join()
	sound_thread.join()
	time.sleep(10)
	server.stop_recording_camera()


def handler(signal_received, frame):
	# Handle any cleanup here
	print('SIGINT or CTRL-C detected. Exiting')
	server.shutdown_server()
	sys.exit(0)

		
if __name__ == '__main__':
	signal(SIGINT, handler)
	server_thread = threading.Thread(target= server.start_server)
	server_thread.start()
	
	while not server.get_ready():
		print("not ready")
		time.sleep(0.2)
	print('system on! Press CTRL-C to exit')
	while True:
		dist = lidar.range
		print(dist)
		if (dist < 400) and (dist != 0) and server.get_armed():
			server.display_alarm_active()
			activate_alarm()
		time.sleep(0.2)
