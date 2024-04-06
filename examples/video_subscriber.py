"""
Start as many of these as needed. Run these first, then start video_publisher.py
"""

import imagezmq 

image_hub = imagezmq.ImageHub(open_port='tcp://192.168.4.52:5555', REQ_REP=False)

while True: 
    name, image = image_hub.recv_image() 
    print(image.shape) 