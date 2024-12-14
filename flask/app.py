"""
Options worth trying: 
    Image streaming with OpenCV and Flask: https://maker.pro/nvidia-jetson/tutorial/streaming-real-time-video-from-rpi-camera-to-browser-on-jetson-nano-with-flask
    (This one worked)
"""

import flask
from flask import Flask, request, render_template, jsonify, redirect, send_file, Response
from flask.views import View, MethodView
import cv2 as cv
import serial 
import threading 

import signal

import nanocamera 
import sys, time 
from PIL import Image
from io import BytesIO 
import imagezmq 
import json
import numpy as np

from video_utilities import gstreamer_pipeline
from utilities import FiringTimer, map_x_range, map_y_range

import logging
logging.basicConfig(level=logging.INFO)

app = Flask(__name__)


x, y, = 1500, 1500 
fire = False 
firing_active = False 
serial_active = True 
video_active = True

timer = FiringTimer()

ser = serial.Serial(port='/dev/ttyUSB0', baudrate=115200) 


def motion_control():
    global x, y, fire, serial_active, video_active, firing_active
    while serial_active:
        firing_active = timer.firing_status
        ser.write(f'<{x}, {y}, {firing_active}>'.encode())
        time.sleep(0.0500)


thread = threading.Thread(target=motion_control, daemon=True)
camera = cv.VideoCapture(gstreamer_pipeline(), cv.CAP_GSTREAMER)

def generate_frames():
    global video_active

    while video_active:
        success, frame = camera.read()
        if not success:
            break
        else:
            ret, buffer = cv.imencode('.jpg', frame)  # Encode frame as JPEG
            frame = buffer.tobytes()
            yield (b'--frame\r\n'
                   b'Content-Type: image/jpeg\r\n\r\n' + frame + b'\r\n')


def shutdown_server():
    """Function to release the camera and cleanup resources"""
    print("Shutting down server and releasing resources...")
    global x, y, fire, serial_active, video_active
    serial_active = False 
    video_active = False

    time.sleep(1)
    
    thread.join()
    camera.release()
    time.sleep(3)
    sys.exit(0)  


def signal_handler(sig, frame):
    """Signal handler to catch SIGINT (Ctrl+C) and SIGTERM (termination signal)"""
    print('Received signal to terminate the server.')
    shutdown_server()  

signal.signal(signal.SIGINT, signal_handler)  # For Ctrl+C
signal.signal(signal.SIGTERM, signal_handler)  # For termination signal



@app.route("/", methods={"GET", "POST"}) 
def home():
    if request.method == "POST":
        return redirect("/")
    else:
        return render_template('home_joystick_only.html') # Use home2 for tilt controls

# @app.route('/tilt', methods=['POST'])
# def receive_tilt():
#     """
#     Execution time from start to finish seems to be 0.002, so quite short. Unsure where the slowdown is coming from 
#     Expects: 
    
#     """
#     global x, y, fire, serial_active

#     data = request.json
#     tiltLR = data.get('tiltLR')
#     tiltFB = data.get('tiltFB')
#     # direction = data.get('direction')

#     # Put all this in another function that updates separately 
#     x = int(map_x_range(tiltFB))
#     y = int(map_y_range(tiltLR))
    
#     ser.write(f'<{x}, {y}, 0>'.encode())

#     # print("x: ", x, "  y: ",y)
#     return jsonify({"status": "success"}), 200


# @app.route('/show_tilt')
# def show_tilt():
#     return render_template('tilt.html')    

@app.route('/joystick', methods=["POST"])
def receive_joystick():
    """
    Expects json: 
    {
        x: -100 to 100,
        y: -100 to 100
    }
    """

    global x, y, fire, serial_active

    data = request.json 
    lr = data.get('x')
    ud = data.get('y')

    x = int(map_x_range(-int(lr), old_min=-100, old_max=100))
    y = int(map_y_range(int(ud), old_min=-100, old_max=100))

    return jsonify({'status': "success"}), 200


@app.route("/fire", methods={"GET", "POST"})
def fire():
    """
    Fires for a set amount of time 
    """
    global firing_active
    print('Firing')
    timer.fire()
    return jsonify({'success': True}), 200

@app.route('/video_feed')
def video_feed():
    return Response(generate_frames(),
                    mimetype='multipart/x-mixed-replace; boundary=frame')


if __name__ == "__main__":
    try:
        thread.start()
        app.run(host='0.0.0.0', port=5000, debug=False, ssl_context=('../server.crt', '../server.key')) 
        
    except Exception as e:
        print(f"Error: {e}")
          
    finally:
        shutdown_server()