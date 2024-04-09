"""when video breaks: sudo systemctl restart nvargus-daemon.service """

import nanocamera as nano 

cam = nano.Camera()

frame = cam.read() 
print(frame.shape) 

cam.release() 
del cam