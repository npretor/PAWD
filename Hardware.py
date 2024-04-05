"""
1. Find the effective refresh rate. That becomes t 
distance(t) = p_k*e(t) * p_i*e(t) * D(t)  

What variable am I altering? 
    t is fixed 
    speed and step count can be fixed, but above a certain step count I lose steps 
    Find the max step count by doing a test: move left at 1x speed, move right at 0.5x speed. 



"""
import time 
import serial
import logging 

class MotorControl:
    def __init__(self):
        self.x_angle = 0.0 
        self.y_angle = 0.0 
        self.x_limit = (-100, 100)
        self.y_limit = (-100, 100)
        self.device = None 

    def connect(self, port='/dev/ttyACM0'):
        try:
            self.device = serial.Serial(port=port, baudrate=115200) 
            time.sleep(1)
            return True
        except Exception as e:
            print(e)
            return False

    def calibrate(self):
        """
        1. Move until tilt at zero 
        2. Move right for half of the limit, might left for half of the limit 
        """
        pass 

    def move(self, distance):
        x, y = distance
        message = f"<{x}, {y}, 0, 0>"
        self.device.write( message.encode())  


class GPIO:
    def __init__(self, pin, mode):
        self.pin=pin 
        self.mode = mode     # input, output, pwm 

    def on(self):
        if self.mode == 'input' or self.mode == 'pwm':
            pass 

    def off(self):
        if self.mode == 'input' or self.mode == 'pwm':
            pass 
