#!/usr/bin/python3
import time
from cv2 import HOGDESCRIPTOR_DESCR_FORMAT_ROW_BY_ROW
import jetson.inference
import jetson.utils
import threading

import argparse
import sys
import numpy as np
from simple_pid import PID
#from motorControl import MotorController
import serial
import pdb

# parse the command line
parser = argparse.ArgumentParser(description="Locate objects in a live camera stream using an object detection DNN.", 
                                 formatter_class=argparse.RawTextHelpFormatter, epilog=jetson.inference.detectNet.Usage() +
                                 jetson.utils.videoSource.Usage() + jetson.utils.videoOutput.Usage() + jetson.utils.logUsage())
parser.add_argument("input_URI", type=str, default="", nargs='?', help="URI of the input stream")
parser.add_argument("output_URI", type=str, default="", nargs='?', help="URI of the output stream")
parser.add_argument("--network", type=str, default="ssd-mobilenet-v2", help="pre-trained model to load (see below for options)")
parser.add_argument("--overlay", type=str, default="box,labels,conf", help="detection overlay flags (e.g. --overlay=box,labels,conf)\nvalid combinations are:  'box', 'labels', 'conf', 'none'")
parser.add_argument("--threshold", type=float, default=0.5, help="minimum detection threshold to use") 
is_headless = ["--headless"] if sys.argv[0].find('console.py') != -1 else [""]

try:
	opt = parser.parse_known_args()[0]

except:
	print("")
	parser.print_help()
	sys.exit(0) 


# - - - - - - - Initialization - - - - - - - #
pidx = PID(1.5, 0.1, 0.05, setpoint=0)
pidy = PID(1.5, 0.1, 0.05, setpoint=0)


ser = serial.Serial(port='/dev/ttyACM0', baudrate=115200)

class ObjectTracker:
    """
    Get the detection results
    See if there is a desired object in view
    Get the location of the desired object 
    """
    def __init__(self, object_type="person", bbox_size=50):
        self.object_type = object_type     
        self.object_detected = False 

        self.detections = {
            'person': 1,
            'cat': 18, 
            'dog': 19
        } 

        # Update these 
        self.object_center = None
        self.object_
     

    def errorFromCenter(self, bbox_center, image_size):
        """
        We need to make this a separate function from alignment since we should smooth over any gaps and interpolate for n frames. 
        The model doesn't have any object permenance so we have to make an approximation 
        Input:  
            frames: (tuple) frames to wait after the object dissapears. 
        """
        
        imageCenter = (int(image_size[0]/2), int(image_size[1]/2)) 
        error = (bbox_center[0] - imageCenter[0], bbox_center[1] -  imageCenter[1]) 
        return error 

    def objectDetected(self, detections):
        if len(detections) > 0:
            for detection in detections:
                if self.detections[self.object_type] == detection.ClassID:
                    self.object_center = detection.Center
                    self.object_detected = True
                    return True
            self.object_detected = True
            return False
        else:
            self.object_detected = True
            return False


    def processDetections(self, detections):
        """
        ID 1 is a person 
        ID 18 is a cat 
        ID 19 is a dog 
        """
        bbox_center = (imgx/2, imgy/2) 
        if len(detections) >= 1:
            for detection in detections:
                if detection.ClassID == 1:
                    print('person found')
                    return detection.Center
        return bbox_center


output = jetson.utils.videoOutput(opt.output_URI, argv=sys.argv+is_headless)

# load the object detection network
net = jetson.inference.detectNet(opt.network, sys.argv, opt.threshold)
# create video sources
input = jetson.utils.videoSource(opt.input_URI, argv=sys.argv)

threshold = 50
previousError = (1,1)

tracker = ObjectTracker()

with serial.Serial(port='/dev/ttyACM0', baudrate=115200) as ser:
    while True:
        # capture the next image
        img = input.Capture()     # img.shape (height, width) 
        imgx = img.shape[1] 
        imgy = img.shape[0] 
        bbox_center = (imgx/2, imgy/2)

        # detect objects in the image (with overlay)
        detections = net.Detect(img, overlay=opt.overlay) 
        print("detected {:d} objects in image".format(len(detections))) 

        output.Render(img)
        output.SetStatus("{:s} | Network {:.0f} FPS".format(opt.network, net.GetNetworkFPS()))

        # Sort detections for desired object
        if not tracker.objectDetected(detections):
            # Don't move 
            # Don't fire 
            ser.write(b'<0,0,0,0,0>')
            continue
        else:
            # Calulate the error relative to the center of the image, leaving a center buffer zone 
            error = tracker.errorFromCenter(bbox_center, image_size=(imgx, imgy))
            print('Error: ', error)

            if abs(error[0]) > threshold:
                if error[0] > 0:
                    print('Moving right') 
                    ser.write(b'<0, -100, 0, 0, 0>') 
                    time.sleep(0.01) 
                elif error[0] < 0:
                    print('Moving left')
                    ser.write(b'<0, 100, 0, 0, 0>') 
                    time.sleep(0.01) 
                previousError = error
            else:
                print('object on target, firing') 
                ser.write(b'<0, 0, 0, 0, 1>') 

            # PID calculation
            controlx = pidx(error[0]) 
            controly = pidy(error[1]) 

            print('======================================================================') 

            if not input.IsStreaming() or not output.IsStreaming():
                ser.write(b'<0,0,0,0, 0>')
                print("writing zeroes") 
                break


