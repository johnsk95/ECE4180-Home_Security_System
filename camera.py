
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

frame_lock = threading.Lock()
class Camera(object):
    thread = None  # background thread that reads frames from camera
    write_thread = None
    write_to_file = False
    frame = None  # current frame is stored here by background thread
    last_access = 0  # time of last client access to the camera
    out = None

    def __init__(self, output_file_name):
        fourcc = cv2.VideoWriter_fourcc('M','J','P','G')
        self.out = cv2.VideoWriter(output_file_name, fourcc, 10, (640,480))

    def initialize(self):
        if Camera.thread is None:
            # start background frame thread
            Camera.thread = threading.Thread(target=self._thread)
            Camera.thread.start()

            # wait until frames start to be available
            while self.frame is None:
                time.sleep(0)
                
            self.write_to_file = True
            Camera.write_thread  = threading.Thread(target=self._write_thread)
            Camera.write_thread.start()

    def get_frame(self):
        Camera.last_access = time.time()
        self.initialize()
        frame_lock.acquire()
        new_frame = copy.deepcopy(self.frame)
        frame_lock.release()
        return new_frame
    
    def write_frame(self, frame):
        #write to output file
        arr = np.frombuffer(frame, np.uint8)
        image = cv2.imdecode(arr, cv2.IMREAD_COLOR)
        image = cv2.resize(image, (640,480))
        self.out.write(image)
    
    def shut_down_write(self):
        self.write_to_file = False

    def _write_thread(self):
        while(self.write_to_file):
            frame = self.get_frame()
            self.write_frame(frame)
        self.write_thread = None

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

                frame_lock.acquire()
                cls.frame = stream.read()
                frame_lock.release()

                # reset stream for next frame
                stream.seek(0)
                stream.truncate()

                # if there hasn't been any clients asking for frames in
                # the last 10 seconds stop the thread
                if time.time() - cls.last_access > 10:
                    break
                
        cls.thread = None
        cls.write_to_file = False
