import time 
from Hardware import MotorControl 

motor = MotorControl()

if not motor.connect():
    print('could not connect') 
    exit()

motor.move((0,0)) 
time.sleep(1) 

# for i in range(5):
#     # Anything above 1000 with an abrupt change the rotation can't handle 
#     motor.move((100, 100))
#     time.sleep(0.2)
#     motor.move((-100,-100))
#     time.sleep(0.2) 

t = 0.025

# Experiment with
#    Move values from 5 to 50


for i in range(5):
    for i in range(25):
        motor.move((20,20)) 
        time.sleep(t)
    
    time.sleep(1)
    
    for i in range(25):
        motor.move((-20,-20))
        time.sleep(t)
    
    time.sleep(1)

motor.move((0,0)) 