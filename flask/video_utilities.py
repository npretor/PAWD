def gen_frames():
    while cam.isReady():
        frame = cam.read()
        ret, buffer = cv.imencode('.jpg', frame) 

        frame = buffer.tobytes()
        yield (b'--frame\r\n'
            b'Content-Type: image/jpeg\r\n\r\n' + frame + b'\r\n') 

def gen_frames2():
    while True:
        try:
            name, frame = image_hub.recv_image() 
            ret, buffer = cv.imencode('.jpg', frame) 
            frame = buffer.tobytes()
        except:
            return None 
        
        yield (b'--frame\r\n'
            b'Content-Type: image/jpeg\r\n\r\n' + frame + b'\r\n') 


def start_video(start=False):
    if start:
        try:
            cam = nanocamera.Camera()
            return cam
        except:
            logging.error("could not connect to camera")
            return None


# image_hub = imagezmq.ImageHub(open_port='tcp://192.168.4.119:5555', REQ_REP=False)

# image_hub = imagezmq.ImageHub(open_port='tcp://127.0.0.1:5555', REQ_REP=False)            

# cam = start_video(False)