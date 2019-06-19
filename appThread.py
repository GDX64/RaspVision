#!/usr/bin/env python
from importlib import import_module
import os
from flask import Flask, render_template, Response
import threading
import queue
import cv2
import time

class appThread(threading.Thread):
    def __init__(self, threadID, name, fila=queue.Queue()):
        threading.Thread.__init__(self)
        self.threadID = threadID
        self.name = name
        self.fila=fila
        
    def run(self):
        print("Starting " + self.name)
        self.video_streaming()
        
        
    def video_streaming(self):
        app = Flask(__name__)

        @app.route('/')
        def index():
            """Video streaming home page."""
            return render_template('index.html')


        def gen():
            """Video streaming generator function."""
            while True:
                frame = self.fila.get()
                yield (b'--frame\r\n'
                       b'Content-Type: image/jpeg\r\n\r\n' + frame + b'\r\n')


        @app.route('/video_feed')
        def video_feed():
            """Video streaming route. Put this in the src attribute of an img tag."""
            return Response(gen(),
                            mimetype='multipart/x-mixed-replace; boundary=frame')
                            
        app.run(host='0.0.0.0', port='5000', threaded=True)



