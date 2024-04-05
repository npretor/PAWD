"""
Options worth trying: 
    Image streaming with OpenCV and Flask: https://maker.pro/nvidia-jetson/tutorial/streaming-real-time-video-from-rpi-camera-to-browser-on-jetson-nano-with-flask
    (This one worked)
"""

import flask
from flask import Flask, request, render_template, jsonify, redirect, send_file, Response
from flask.views import View, MethodView
import cv2 as cv

import nanocamera 
import sys, time 
from PIL import Image
from io import BytesIO 


import logging
logging.basicConfig(level=logging.INFO)

app = Flask(__name__)


try:
    cam = nanocamera.Camera()
except:
    logging.error("could not connect to camera")
    cam = None 

def gen_frames():
    while cam.isReady():
        frame = cam.read()
        ret, buffer = cv.imencode('.jpg', frame) 
        frame = buffer.tobytes()
        yield (b'--frame\r\n'
            b'Content-Type: image/jpeg\r\n\r\n' + frame + b'\r\n') 



@app.route("/", methods={"GET", "POST"}) 
def home():
    if request.method == "POST":
        return redirect("/")
    else:
        return render_template('home.html')


@app.route("/cam_image")
def cam_image():
    """This method is from the voltera camera example, and is not working""" 
    frame = cam.read() 
    byte_io = BytesIO()
    # Image.fromarray(frame).save(byte_io, format="PNG")
    # key, encoded_frame = cv.imencode(".png", frame)

    # import ipdb; ipdb.set_trace()
    return send_file(encoded_frame, mimetype='image/png')


@app.route("/fire")
def fire():
    """
    Fires for a set amount of time 
    """
    logging.debug('Firing')
    return json.dumps({'success':True}), 200, {'ContentType':'application/json'} 


@app.route('/video_feed') 
def video_feed():
    """
    https://towardsdatascience.com/video-streaming-in-web-browsers-with-opencv-flask-93a38846fe00
    This creates the problem of the camera not being able to stop 
    """
    return Response(gen_frames(), mimetype='multipart/x-mixed-replace; boundary=frame')

if __name__ == "__main__":
    app.run(host='0.0.0.0', port=5000, debug=False)        