import time
import board
import busio
import digitalio
import adafruit_vl53l0x
import server 
from camera import Camera
from signal import signal, SIGINT
from sys import exit

led = digitalio.DigitalInOut(board.D17)
led.direction = digitalio.Direction.OUTPUT

i2c = busio.I2C(board.SCL, board.SDA)
lidar = adafruit_vl53l0x.VL53L0X(i2c)
lidar.measurement_timing_budget = 200000

trigger = True
alarm = False
recording = False
timestamp = time.strftime('%b-%d-%Y_%H:%M', time.localtime())
#camera = PiCamera()

def stream_camera():
	camera.start_preview()
	camera.start_recording(f'/home/pi/recordings/{timestamp}.h264')
	sleep(10)
	camera.stop_recording()
	camera.stop_preview
	
def play_sound():
	return

def activate_alarm(camera):
	if(camera is not None):
		print('alarm activated!')
		camera.start_preview()
		camera.start_recording(f'/home/pi/recordings/{timestamp}.h264')
		for _ in range(10):
			led.value = True
			time.sleep(0.5)
			led.value = False
			time.sleep(0.5)
		camera.stop_recording()
		camera.stop_preview

def start_camera(camera):
	if(not recording):
		try:
			#TODO: need better way to test if camera is attached
			with picamera.PiCamera() as test_cam:
				print("Camera attached")
				test_cam.close()

			cam = Camera()
			cam.initialize()
			cam.set_output("output")
			cam.start_record()
			server.attach_camera(cam)
		except:
			print('camera not detected!')

def handler(signal_received, frame):
    # Handle any cleanup here
    print('SIGINT or CTRL-C detected. Exiting gracefully')
	server.shutdown_server()
    exit(0)
		
if __name__ == '__main__':

	server.start_server()
	cam = None

	server.attach_camera(cam)
	start_camera(cam)

	while True:
		print("testing lidar")
		dist = lidar.range
		if (dist < 400) and (dist != 0) and server.armed:
			activate_alarm(cam)
		if (server.live_stream and streaming_video):
			start_camera(cam)
			print("Live streaming")
			#Add code here to start camera
		if (server.play_audio):
			print("streaming audio")
		time.sleep(0.2)



print('end!')
