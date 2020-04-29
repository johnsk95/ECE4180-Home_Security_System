
#!/usr/bin/env python
# -*- coding: utf-8 -*-
#
#  camera_pi.py
#  
#  
#  
import time
import io
import threading
import picamera
import cv2
import numpy as np
import copy
from datetime import datetime

cv_lock = threading.Lock()
camera_lock = threading.Lock()
class Camera(object):
    thread = None  # background thread that reads frames from camera
    write_to_file = False
    frame = None  # current frame is stored here by background thread
    last_access = 0  # time of last client access to the camera
    out = None

    def initialize(self):
        with camera_lock:
            if Camera.thread is None:
                # start background frame thread
                Camera.thread = threading.Thread(target=self._thread)
                Camera.thread.start()

                # wait until frames start to be available
                while self.frame is None:
                    time.sleep(0)


    def get_frame(self):
        Camera.last_access = time.time()
        self.initialize()
        return self.frame
    

    @classmethod
    def start_record(cls):
        if cls.out is not None:
            cls.write_to_file = True
        else:
            print("Cannot record without setting output file\n")

    @classmethod
    def stop_record(cls):
        with cv_lock:
            cls.write_to_file = False
            if cls.out is not None:
                cls.out.release()
                cls.out = None

    @classmethod
    def set_output_current_time(cls):
        date_str = time.strftime('%b-%d-%Y_%H:%M', time.localtime())
        cls.set_output(date_str)

    @classmethod
    def set_output(cls, filename):
        with cv_lock:
            fourcc = cv2.VideoWriter_fourcc('T','H','E','O')
            cls.out = cv2.VideoWriter("static/videos/"+filename+".ogv", fourcc, 20, (640,480))
            print("create file "+filename)

    @classmethod
    def _thread(cls):
        with picamera.PiCamera() as camera:
            # camera setup
            camera.resolution = (320, 240)
            camera.hflip = True
            camera.vflip = True

            # let camera warm up
            camera.start_preview()
            time.sleep(2)

            stream = io.BytesIO()
            for foo in camera.capture_continuous(stream, 'jpeg',
                                                 use_video_port=True):
                # store frame
                stream.seek(0)

                cls.frame = stream.read()
                with cv_lock:
                    if(cls.write_to_file and cls.out is not None):
                        arr = np.frombuffer(cls.frame, np.uint8)
                        image = cv2.imdecode(arr, cv2.IMREAD_COLOR)
                        image = cv2.resize(image, (640,480))
                        cls.out.write(image)

                # reset stream for next frame
                stream.seek(0)
                stream.truncate()

                # if there hasn't been any clients asking for frames in
                # the last 10 seconds stop the thread
                if time.time() - cls.last_access > 10 and not cls.write_to_file:
                    break
                
        cls.thread = None
        cls.stop_record()
