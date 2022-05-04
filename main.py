#!/usr/bin/python3

from cv2 import HOGDESCRIPTOR_DESCR_FORMAT_ROW_BY_ROW
import jetson.inference
import jetson.utils

import argparse
import sys
import numpy as np
from simple_pid import PID

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





def boundingBoxToError(center, imageSize):
    """
    We need to make this a separate function from alignment since we should smooth over any gaps. 
    The models doesn't have any object permanece so we have to make an approximation 
    Input:  
        frames: (tuple) frames to wait after the object dissapears. 
    """

    imageCenter = (int(imageSize[0]/2), int(imageSize[1]/2)) 

    return error 


# load the object detection network
net = jetson.inference.detectNet(opt.network, sys.argv, opt.threshold)
# create video sources
input = jetson.utils.videoSource(opt.input_URI, argv=sys.argv)


while True:
    # capture the next image
    img = input.Capture()     # img.shape (height, width) 
    imgx = img.shape[1] 
    imgy = img.shape[0] 

    # detect objects in the image (with overlay)
    detections = net.Detect(img, overlay=opt.overlay)
    # print the detections
    print("detected {:d} objects in image".format(len(detections)))

    #print("Class ID:   ",detection[0].ClassID, "    Type: ",detections[0].Center)
    #for i in detections:
    #	print("Classid:  ",detections[i].ClassID)
        # ID 18 is a cat, ID 19 is a dog
    if len(detections) >= 1:
        if detections[0].ClassID == 18:
            print('Cat found')
        elif detections[0].ClassID == 19:
            print('Dog found')
            #boundingBoxToError(detections[0].Center, imgx, imgy) 
        else:
            print('Detections:    ', detections[0].ClassID, 'Center:    ', detections[0].Center)



    print('======================================================================')
    # render the image
    #output.Render(img)

    # update the title bar
    #output.SetStatus("{:s} | Network {:.0f} FPS".format(opt.network, net.GetNetworkFPS()))#

    # print out performance info
    #net.PrintProfilerTimes()

    # exit on input/output EOS
    #if not input.IsStreaming() or not output.IsStreaming():
    #    break



def objectFilter():
    pass





def alignment(xError, yError):
    """    
    Goal: Adjust the motor speed as the x and y error converges
    Inputs:
        xError: float
        yError: float
    """

    return speedX, speedY


 
    
