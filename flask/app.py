"""
Options worth trying: 
    Image streaming with OpenCV and Flask: https://maker.pro/nvidia-jetson/tutorial/streaming-real-time-video-from-rpi-camera-to-browser-on-jetson-nano-with-flask
    (This one worked)
"""

import flask
from flask import Flask, request, render_template, jsonify, redirect, send_file, Response
from flask.views import View, MethodView
import cv2 as cv

import signal

import nanocamera 
import sys, time 
from PIL import Image
from io import BytesIO 
import imagezmq 

import logging
logging.basicConfig(level=logging.INFO)

app = Flask(__name__)


def gstreamer_pipeline(
        capture_width=640,
        capture_height=480,
        display_width=640,
        display_height=480,
        framerate=30,
        flip_method=0):
    return (
        f'nvarguscamerasrc ! video/x-raw(memory:NVMM), '
        f'width=(int){capture_width}, height=(int){capture_height}, '
        f'framerate=(fraction){framerate}/1 ! nvvidconv flip-method={flip_method} ! '
        f'video/x-raw, width=(int){display_width}, height=(int){display_height}, format=(string)BGRx ! '
        f'videoconvert ! video/x-raw, format=(string)BGR ! appsink'
    )

camera = cv.VideoCapture(gstreamer_pipeline(), cv.CAP_GSTREAMER)

def generate_frames():
    while True:
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
    camera.release()
    time.sleep
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
        return render_template('home2.html')


@app.route("/cam_image", methods={"GET", "POST"})
def cam_image():
    """This method is from the voltera camera example, and is not working""" 
    
    frame = cam.read() 
    byte_io = BytesIO()
    return send_file(encoded_frame, mimetype='image/png')
        
    # Image.fromarray(frame).save(byte_io, format="PNG")
    # key, encoded_frame = cv.imencode(".png", frame)


@app.route('/tilt', methods=['POST'])
def receive_tilt():
    data = request.json
    tiltLR = data.get('tiltLR')
    tiltFB = data.get('tiltFB')
    direction = data.get('direction')

    print(f"Tilt Left/Right: {tiltLR}, Tilt Front/Back: {tiltFB}, Direction: {direction}")

    return jsonify({"status": "success", "message": "Tilt data received"}), 200



@app.route("/fire", methods={"GET", "POST"})
def fire():
    """
    Fires for a set amount of time 
    """
    logging.debug('Firing')
    return json.dumps({'success':True}), 200, {'ContentType':'application/json'} 


# @app.route('/video_feed', methods={"GET", "POST"}) 
# def video_feed():
#     """
#     https://towardsdatascience.com/video-streaming-in-web-browsers-with-opencv-flask-93a38846fe00
#     This creates the problem of the camera not being able to stop 
#     """
#     return Response(gen_frames2(), mimetype='multipart/x-mixed-replace; boundary=frame')

@app.route('/video_feed')
def video_feed():
    return Response(generate_frames(),
                    mimetype='multipart/x-mixed-replace; boundary=frame')



if __name__ == "__main__":
    try:
        app.run(host='0.0.0.0', port=5000, debug=False, ssl_context=('../server.crt', '../server.key')) 
    except Exception as e:
        print(f"Error: {e}")
        shutdown_server()        