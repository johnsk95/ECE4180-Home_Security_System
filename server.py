from flask import Flask, render_template, Response, request
# Raspberry Pi camera module (requires picamera package, developed by Miguel Grinberg)
from camera import Camera
import cv2
import picamera
import time
import board
import busio

armed = True
live_stream = False
play_audio = False
camera = None
cap = cv2.VideoCapture('dolce_faster.mp4')
app = Flask('__main__')

@app.route('/', methods=['GET', 'POST'])
def index():
    global armed
    global live_stream
    global play_audio
    if request.method == 'POST':
        if "Arm" in request.form:
            armed = True
            print("Armed")
            pass
        elif "Disarm" in request.form:
            armed = False
            print("Disarmed")
            pass
        elif "Start Camera" in request.form:
            if live_stream:
                live_stream = False
            else:
                live_stream = True
            pass
        elif "Send Audio" in request.form:
            play_audio = True
            pass
    if request.method == 'GET':
        print("No get methods")
    """Video streaming home page."""
    return render_template('index.html')

def gen():
    """Video streaming generator function."""
    while True:
        frame = None
        frame_ready = False
        if(camera is not None):
            frame = camera.get_frame()
            frame_ready = True
        else:
            if(cap.isOpened()):
                ret, image = cap.read()
                image = cv2.resize(image, (640,480))
                _, frame = cv2.imencode('.JPEG', image)
                frame = frame.tostring()
                frame_ready = True
        if(frame_ready):       
            yield (b'--frame\r\n'
                b'Content-Type: image/jpeg\r\n\r\n' + frame + b'\r\n')
@app.route('/video_feed')
def video_feed():
    """Video streaming route. Put this in the src attribute of an img tag."""
    return Response(gen(),
                    mimetype='multipart/x-mixed-replace; boundary=frame')

def start_server():
    app.run(host='0.0.0.0', port =8000, debug=False, threaded=True)

def attach_camera(cam):
    camera = cam

