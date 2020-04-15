import io
import picamera
import logging
import socketserver
from threading import Condition
from http import server
import cv2
import adafruit_vl53l0x
import time
import board
import busio
import digitalio
import numpy as np

PAGE="""\
<html>
<head>
<title>picamera MJPEG streaming demo</title>
</head>
<body>
<h1>PiCamera MJPEG Streaming Demo</h1>
<img src="stream.mjpg" width="640" height="480" />
<form action="<?php echo 'test' ?>" method="post">
  <button type="submit">Submit</button>
</form>
</body>
</html>
"""


class StreamingOutput(object):
    def __init__(self):
        self.frame = None
        self.buffer = io.BytesIO()
        self.condition = Condition()

    def write(self, buf):
        if buf.startswith(b'\xff\xd8'):
            # New frame, copy the existing buffer's content and notify all
            # clients it's available
            self.buffer.truncate()
            with self.condition:
                self.frame = self.buffer.getvalue()
                self.condition.notify_all()
            self.buffer.seek(0)
        # Write the rest of the stream to disk
        #with io.open('test_output.h264', 'wb') as output:
            #output.write(self.buffer.read())
            
        return self.buffer.write(buf)

class StreamingHandler(server.BaseHTTPRequestHandler):
    def do_GET(self):
        print(self.path)
        if self.path == '/':
            self.send_response(301)
            self.send_header('Location', '/index.html')
            self.end_headers()
        elif self.path == '/index.html':
            content = PAGE.encode('utf-8')
            self.send_response(200)
            self.send_header('Content-Type', 'text/html')
            self.send_header('Content-Length', len(content))
            self.end_headers()
            self.wfile.write(content)
        elif self.path == '/stream.mjpg':
            self.send_response(200)
            self.send_header('Age', 0)
            self.send_header('Cache-Control', 'no-cache, private')
            self.send_header('Pragma', 'no-cache')
            self.send_header('Content-Type', 'multipart/x-mixed-replace; boundary=FRAME')
            self.end_headers()
            try:
                while True:
                    can_stream = True
                    if(camera_works):
                        with output.condition:
                            output.condition.wait()
                            frame = output.frame
                            arr = np.frombuffer(frame, np.uint8)
                            image = cv2.imdecode(arr, cv2.IMREAD_COLOR)
                            image = cv2.resize(image, (640,480))
                            out.write(image)
                    else:
                        if(cap.isOpened()):
                            ret, image = cap.read()
                            image = cv2.resize(image, (640,480))
                            _, frame = cv2.imencode('.JPEG', image)
                            if ret==True:
                                image = cv2.imdecode(frame, cv2.IMREAD_COLOR)
                                image = cv2.resize(image, (640,480))
                                out.write(image)
                                # write the frame
                                #out.write(image)
                        else:
                            can_stream = False
                            print("cannot stream")
                    
                    if(can_stream):
                        self.wfile.write(b'--FRAME\r\n')
                        self.send_header('Content-Type', 'image/jpeg')
                        self.send_header('Content-Length', len(frame))
                        self.end_headers()
                        self.wfile.write(frame)
                        self.wfile.write(b'\r\n')
            except Exception as e:
                logging.warning(
                    'Removed streaming client %s: %s',
                    self.client_address, str(e))
        else:
            self.send_error(404)
            self.end_headers()

    def do_POST(self):
        self.send_response(200)
        print("post");

class StreamingServer(socketserver.ThreadingMixIn, server.HTTPServer):
    allow_reuse_address = True
    daemon_threads = True
    
    
camera_works = True
fourcc = cv2.VideoWriter_fourcc(*'XVID')
out = cv2.VideoWriter('output.avi',fourcc, 20.0, (640,480))
try:
    print("start camera")
    with picamera.PiCamera(resolution='640x480', framerate=24) as camera:
        output = StreamingOutput()
        camera.start_recording(output, format='mjpeg')
        try:
            address = ('', 8000)
            server = StreamingServer(address, StreamingHandler)
            server.serve_forever()
        finally:
            if(camera_works):
                camera.stop_recording()
except:
    print("Camera not attached")
    camera_works = False
    #stream static video file instead
    cap = cv2.VideoCapture('dolce_faster.mp4')
    
    try:
        address = ('', 8000)
        server = StreamingServer(address, StreamingHandler)
        server.serve_forever()
    finally:
        cap.release()
        cv2.destroyAllWindows()
        out.release()
   
