from flask import current_app, Flask, render_template, Response, request, session
from flask_session import Session
# Raspberry Pi camera module (requires picamera package, developed by Miguel Grinberg)
from camera import Camera
import cv2
import picamera
import time
import board
import busio
import sys

cap = cv2.VideoCapture('dolce_faster.mp4')
app = Flask("app")


@app.route('/', methods=['GET', 'POST'])
def index():
    if request.method == 'POST':
        if "Arm" in request.form:
            app.config['armed'] = True
            print("Armed")
            pass
        elif "Disarm" in request.form:
            app.config['armed'] = False
            print("Disarmed")
            pass
        elif "Record" in request.form:
            print("Record")
            record = app.config['record']
            if record:
                app.config['record'] = False
            else:
                app.config['record'] = True
            pass
    if request.method == 'GET':
        print("No get methods")
    """Video streaming home page."""
    return render_template('index.html')

def gen(camera):
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
    config = app.config
    camera = config['camera']
    return Response(gen(camera),
                    mimetype='multipart/x-mixed-replace; boundary=frame')
 

def test_camera():
    try:
        with picamera.PiCamera() as test_cam:
            print("Camera attached")
            test_cam.close()
        return True
    except:
        print('camera not detected!')
        return False
    return False

def start_server():
    cam = None
    if(test_camera()):
        cam = Camera()
        print("initialize camera")
        cam.initialize()

    app.config.update(
        camera = cam,
        armed = True,
        record = False,
        stream_audio = False,
        ready = True
    )
    app.run(host='192.168.88.213', port =8000, debug=False, threaded=True)
    
def start_camera(camera):
    camera.initialize()
    camera.set_output_current_time()
    camera.start_record()

def start_recording_camera():
    with app.app_context():
        config = app.config
        camera = config['camera']
        if(camera is not None):
            start_camera(camera)

def stop_recording_camera():
    with app.app_context():
        config = app.config
        camera = config['camera']
        if(camera is not None):
            camera.stop_record()

def get_ready():
    with app.app_context():
        config = app.config
        if('ready' not in config):
            return False
        else:
            return config['ready']

def get_armed():
    with app.app_context():
        config = app.config
        return config['armed']

def get_record():
    with app.app_context():
        config = app.config
        return config['record']

def get_streaming_audio():
    with app.app_context():
        config = app.config
        return config['stream_audio']

def shutdown_server():
    sys.exit(0)
