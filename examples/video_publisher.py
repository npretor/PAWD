import sys 
sys.path.append('..') 
from turret import StreamingServer 

streamer = StreamingServer() 
streamer.start(fps=30) 