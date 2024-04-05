import time 
from Hardware import MotorControl 

motor = MotorControl()

if not motor.connect():
    print('could not connect') 
    exit()

motor.move((0,0)) 
time.sleep(1) 

for i in range(5):
    motor.move((1000, 1000))
    time.sleep(0.2)
    motor.move((-1000,-1000))
    time.sleep(0.2) 

motor.move((0,0)) 