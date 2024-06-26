import time, os
import logging 
import threading 
from collections import deque
import imagezmq
import nanocamera 
from Hardware import MotorControl 

ctime = time.ctime().replace(':',"_")
# FIXME 
logging.basicConfig(
    filename=f"logs/{ctime}.log", 
    level=logging.INFO,
    format='%(asctime)s %(message)s',
)


class Turret:
    """
    Axes are relative to self, outward from the camera. 
        X is left->right            (-, +)
        Y is down-> up              (-, +)
        Z is in->out from center    (-, +)
    """
    def __init__(self):
        self.status_options = {'offline', 'online', 'monitoring','hunting'} 
        self.status = 'offline' 
        self.engagement_mode={
            "passive",              # just record when an animal is recognized 
            "auto_with_handoff",    # track, but leave firing to user 
            "full_irobot"           # track and fire, full autonomy 
            }
        self.motion = MotorControl() 
        
        self.trigger = None 
        self.motion_enable = None 
        self.motion_detected = False
        self.sleep_interval = 1 # seconds
        self.record_interval = 10 # seconds
        self.streamer = None 

    def startup(self):
        self.motion.connect()  
        self.motion.calibrate() 
        self.status = 'monitoring' 

    def start_streaming(self):
        self.streamer = StreamingServer() 
        logging.info('Streaming started')
        self.streamer.start(fps=30) 

    def stop_streaming(self):
        logging.info('Streaming stopped')
        self.streamer.stop() 


    def start_flask(self):
        pass 
    
    def stop_flask(self):
        pass 

    def run(self):
        while active():

            if motion_detected():
                timer_complete = time.time() + self.record_interval 
                """
                Broadcast video on a zmq socket, but vary the framerate? 
                """
                # Start video recording and save to the log 
                # Stream video to classifier 
                # Start server 
                
                # Send notification 
                
                # Turn on the motion system 
                self.motion_enable = True 
                
                if motion_detected():
                    timer_complete = time.time() + self.record_interval 
                else:
                    pass 

            time.sleep(sleep_interval)

    def motion_detected(self):
        # Check GPIO 
        return False 


class Classifier:
    """
    This class is in charge of getting frames from the streamer and performing classifications on them 
    """
    def __init__(self):
        self.frames = deque(maxlen=25) 



class StreamingServer:
    """
    Start threading
    """
    def __init__(self):
        self.video_thread = None 
        self.fps = '0' # {0, 1, 30} 
        self.camera = None 

    def init_camera(self, cam_number=0):
        """
        Verify there is a camera at /dev/video0 
        Verify the camera is ready 
        """
        cam_device = f'/dev/video{cam_number}'
        try:
            os.path.exists(cam_device) 
        except Exception as e:
            logging.error(f"No camera: {e}") 
        
        self.camera = nanocamera.Camera(source=cam_device) 
        logging.info('camera is initialized:') 
         
    def start(self, fps):
        """Start thread""" 
        self.fps = fps
        print('starting thread ')
        self.video_thread = threading.Thread(target=self._stream_video, args=[fps])
        self.video_thread.start()

    def stop(self):
        """Stop thread""" 
        self.state = '0'
        self.streaming = False
        self.video_thread.join()
        self.camera.release() 


    def _stream_video(self, fps=30):
        """ Stream using pub-sub """ 

        print('initializing camera')
        if self.camera == None:
            self.init_camera() # Does the camera also need to run in the thread? 

        print('starting imagezmq')
        # Accept connections on all tcp addresses, port 5555 
        sender = imagezmq.ImageSender(connect_to='tcp://*:5555', REQ_REP=False) 

        print('sending images now') 
        i = 0 
        self.streaming = True 
        while self.streaming == True:
            frame = self.camera.read() 
            sender.send_image('image', frame) 
            print('sent image', i) 
            i+=1 


if __name__ == "__main__":
    turret = Turret()    
    turret.start_streaming()
    time.sleep(10) 
    turret.stop_streaming()
