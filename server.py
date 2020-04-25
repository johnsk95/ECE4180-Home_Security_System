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
import threading
import os
from flask_socketio import SocketIO, emit

cv_lock = threading.Lock()
cap = cv2.VideoCapture('dolce_faster.mp4')
app = Flask("app")
socketio = SocketIO(app)
   

@app.route('/', methods=['GET'])
def index():
    return refresh_page()


@app.route('/record', methods=['POST'])
def record():
    record = app.config['record']
    if record:
        app.config['record'] = False
    else:
        app.config['record'] = True
    return refresh_page()

@app.route('/arm', methods=['POST'])
def arm():
    armed = app.config['armed']
    if armed:
        app.config['armed'] = False
    else:
        app.config['armed'] = True
    return refresh_page()

@app.route('/selectvideo', methods=['POST'])
def update_video():
    print('update video')
    filename = request.form.get('videos_select')
    total_path = get_video_dir_path()+'/'+filename
    print(total_path)
    video_cap = cv2.VideoCapture(total_path)
    app.config['play_video'] = video_cap
    app.config['current_video']='video/'+filename
    return refresh_page()

def gen(camera):
    """Video streaming generator function."""
    while True:
        frame = None
        frame_ready = False
        if(camera is not None):
            frame = camera.get_frame()
            frame_ready = True
        else:
            with cv_lock:
                if(cap.isOpened()):
                    ret, image = cap.read()
                    image = cv2.resize(image, (640,480))
                    _, frame = cv2.imencode('.JPEG', image)
                    frame = frame.tostring()
                    frame_ready = True
        if(frame_ready):       
            yield (b'--frame\r\n'
                b'Content-Type: image/jpeg\r\n\r\n' + frame + b'\r\n')
def play_video():
    while True:
        frame_ready = False
        if(app.config['play_video'] is not None):
            with cv_lock:
                video = app.config['play_video']
                ret, image = video.read()
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
@app.route('/recorded_video')
def recorded_video():
    return Response(play_video(),
                    mimetype='multipart/x-mixed-replace; boundary=frame')

def display_alarm_active():
    with app.app_context():
        socketio.emit('alarm status', {'data': 'Alarm triggered'}) 

def get_video_dir_path():
    absFilePath = os.path.dirname(__file__)
    return absFilePath+"/videos"

def get_video_filenames():
    video_path = get_video_dir_path()
    f = list()
    for filename in os.listdir(video_path):
        print(filename)
        f.append(filename)
    return f
def refresh_page():
    with app.app_context():
        record = ""
        rec_status = ""
        if(app.config['record']):
            record = "Record"
            rec_status = "Not Recording"
        else:
            record = "Stop"
            rec_status = "Recording"
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
         videos = get_video_filenames(), current_video=get_current_video())

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
        ready = True,
        play_video = None,
        current_video = None
    )
    app.run(host='0.0.0.0', port =8000, debug=False, threaded=True)
    
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

def get_current_video():
    with app.app_context():
        config = app.config
        return config['current_video']


def shutdown_server():
    sys.exit(0)
