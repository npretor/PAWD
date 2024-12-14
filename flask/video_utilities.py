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

# image_hub = imagezmq.ImageHub(open_port='tcp://192.168.4.119:5555', REQ_REP=False)

# image_hub = imagezmq.ImageHub(open_port='tcp://127.0.0.1:5555', REQ_REP=False)            

# cam = start_video(False)