from flask import current_app, Flask, render_template, Response, request, session, jsonify
from flask_session import Session
# Raspberry Pi camera module (requires picamera package, developed by Miguel Grinberg)
from camera import Camera
import cv2
import picamera
import time
import board
import busio
import sys
import threading
import os
from flask_socketio import SocketIO, emit
import numpy as np

app = Flask("app")
socketio = SocketIO(app)
   
@socketio.on('alarmoff')
def on_off(msg):
    alarm_off()

@app.route('/', methods=['GET'])
def index():
    return refresh_page()

@app.route('/receive_message', methods=['POST'])
def receive_message():
    message = request.form.get('message')
    app.config['message'] = message
    return '', 204

def alarm_off():
    app.config['stop_alarm'] = True
    time.sleep(2)
    app.config['stop_alarm'] = False
    return refresh_page()

@app.route('/update_display_record')
def update_record():
    value = ""
    status = ""
    record = not app.config['record']
    app.config['record'] = record
    camera = config['camera']
    if record and (camera is not None):
        value = "Stop"
        status = "Camera Status: Recording"
        start_recording_camera()
    else:
        value = "Record"
        status = "Camera Status: Not Recording"
        stop_recording_camera() 
    
    print(record)
    return jsonify(value=value, status=status)

@app.route('/display_record')
def display_record():
    value = ""
    status = ""
    record = app.config['record']
    if record:
        value = "Stop"
        status = "Camera Status: Recording"
    else:
        value = "Record"
        status = "Camera Status: Not Recording"
    return jsonify(value=value, status=status)

@app.route('/arm')
def arm():
    armed = app.config['armed']
    status = ""
    value = ""
    if armed:
        value = "Arm"
        status = "Alarm Status: Disarmed"
        app.config['armed'] = False
    else:
        value = "Disarm"
        status = "Alarm Status: Armed"
        app.config['armed'] = True
    return jsonify(value=value, status=status)

def gen(camera):
    """Video streaming generator function."""
    while True:
        frame = None
        frame_ready = False
        if(camera is not None):
            frame = camera.get_frame()
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

def display_alarm_active():
    with app.app_context():
        socketio.emit('alarm status', {'data': 'Alarm triggered'}) 

def get_video_dir_path():
    absFilePath = os.path.dirname(__file__)
    return absFilePath+"/static/videos"

def get_video_filenames():
    video_path = get_video_dir_path()
    f = list()
    if not os.listdir(video_path):
        print("Directory is empty")
    else:
        for filename in os.listdir(video_path):
            f.append(filename)
    return f


def refresh_page():
    with app.app_context():
        record = ""
        rec_status = ""
        if(app.config['record']):
            record = "Stop"
            rec_status = "Recording"
        else:
            record = "Record"
            rec_status = "Not Recording"
        armed = ""
        arm_status = ""
        if(app.config['armed']):
            armed = "Disarm"
            arm_status = "Armed"
        else:
            armed = "Arm"
            arm_status = "Not Armed"
        return render_template('index.html', record_value=record,
         armed_value = armed, record_status=rec_status, armed_status= arm_status, 
         videos = get_video_filenames())

def test_camera():
    try:
        with picamera.PiCamera() as test_cam:
            print("camera attached")
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
        ready = True,
        stop_alarm = False,
        message = ""
    )
    app.run(host='0.0.0.0', port=8000, debug=False, threaded=True)
    
def start_camera(camera):
    camera.initialize()
    camera.set_output_current_time()
    camera.start_record()

def start_recording_camera():
    with app.app_context():
        config = app.config
        camera = config['camera']
        if(camera is not None):
            with app.app_context():
                socketio.emit('record', 1) 
                app.config['record'] = True
            start_camera(camera)

def stop_recording_camera():
    with app.app_context():
        config = app.config
        camera = config['camera']
        if(camera is not None):
            with app.app_context():
                socketio.emit('record', 0) 
                app.config['record'] = False
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

def get_message():
    with app.app_context():
        config = app.config
        return config['message']


def get_stop_alarm():
    with app.app_context():
        config = app.config
        return config['stop_alarm']


def shutdown_server():
    sys.exit(0)
