from flask import Flask, render_template, Response, request
# Raspberry Pi camera module (requires picamera package, developed by Miguel Grinberg)
from camera import Camera
import cv2

app = Flask(__name__)
armed = False
live_stream = False
play_audio = False
@app.route('/', methods=['GET', 'POST'])
def index():
    #print(request.form)
    if request.method == 'POST':
        if "Arm" in request.form:
            armed = True
            print("Armed")
            pass
        elif "Start Camera" in request.form:
            live_stream = True
            print("Live streaming")
            pass
        elif "Send Audio" in request.form:
            play_audio = True
            print("Sending audio")
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
        if(camera_works):
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
    return Response(gen(Camera()),
                    mimetype='multipart/x-mixed-replace; boundary=frame')

if __name__ == '__main__':
    camera_works = False
    fourcc = cv2.VideoWriter_fourcc(*'XVID')
    out = cv2.VideoWriter('output.avi',fourcc, 20.0, (640,480))
    try:
        #TODO: need better way to test if camera is attached
        with picamera.PiCamera(resolution='640x480', framerate=24) as camera:
            print("Camera attached")
            camera_works = True
    except:
        camera_works = False
        cap = cv2.VideoCapture('dolce_faster.mp4')

    app.run(host='192.168.88.213', port =8000, debug=True, threaded=True)
