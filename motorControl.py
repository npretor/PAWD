"""

Vertical(camera y axis) motor geartrain
    Stepper is 1.8 degrees per step
    Gear 1 is 16 teeth
    Gear 2 is 160 teeth
"""

import time
import Jetson.GPIO as GPIO
import threading 
import time


class MotorController:
    def __init__(self, MOTOR_STEP_PIN, MOTOR_DIR_PIN, step_angle_deg=1.8, micro_steps=.125):
        self.motorSpeed = 0
        self.step_pin = MOTOR_STEP_PIN 
        self.dir_pin = MOTOR_DIR_PIN 
        self.state = 'idle'
        GPIO.setwarnings(True)
        GPIO.setmode(GPIO.BOARD)
        GPIO.setup(MOTOR_STEP_PIN, GPIO.OUT, initial=GPIO.LOW) 
        GPIO.setup(MOTOR_DIR_PIN, GPIO.OUT, initial=GPIO.LOW) 
        self.step_angle_deg = step_angle_deg
        self.micro_steps = micro_steps 

    def moveAngle(self, move_angle, speed, angle='degrees'):
        """
        Speed is in degrees per second
        """
        steps = int(round((move_angle / self.step_angle_deg) * self.micro_steps, 0))
        delay = speed   # Degrees per second. Steps per degree
        # move_time = delay * 2 * steps
        for step in range(0, steps):
            GPIO.output(self.step_pin, GPIO.HIGH)
            time.sleep(delay)
            GPIO.output(self.dir_pin, GPIO.LOW)
            time.sleep(delay)

    def moveTime(self, moveduration, direction, speed):
        """
        Time: (seconds)
        Speed: (steps/second) 
        Direction: left, right
        """
        if direction == 'left':
            GPIO.output(self.dir_pin, GPIO.LOW)
        elif direction == 'right':
            GPIO.output(self.dir_pin, GPIO.HIGH)
        else:
            print('direction invalid')
            exit(0)

        endtime = moveduration + time.time()
        print(endtime,time.time(),endtime-time.time())  
        if speed == 0:
            time.sleep(moveduration)
            return 0
        else:
            delay = 1 / (speed*2)
        print('delay',delay)
        while time.time() <= endtime:
            GPIO.output(self.step_pin, GPIO.HIGH)
            time.sleep(delay)
            GPIO.output(self.step_pin, GPIO.LOW)
            time.sleep(delay)
        return 0

    def _moveLive(self):
        """
        Primary function that handles the motion pulses
        Speed: steps / second
        """

        while self.state == 'running':
            if self.motorSpeed == 0:
                # sleep instead of moving for a constant time
                time.sleep(0.001) 
            else:
                # Direction
                if self.motorSpeed > 0:
                    GPIO.output(self.dir_pin, GPIO.LOW)
                elif self.motorSpeed < 0:
                    GPIO.output(self.dir_pin, GPIO.HIGH)
                                
                delay = ((1/(abs(self.motorSpeed))) / 2 )
                print('delay:   ', delay)
                GPIO.output(self.step_pin, GPIO.HIGH)
                time.sleep(delay) 
                GPIO.output(self.step_pin, GPIO.LOW)
                time.sleep(delay) 

    def moveLiveStart(self):
        """
        Starts the thread
        """
        self.state = 'running'
        self.t = threading.Thread(target=self._moveLive)
        self.t.start()

    def moveLiveSetSpeed(self, speed):
        self.motorSpeed = speed

    def moveLiveEnd(self):
        self.state = 'idle'
        self.t.join()

    def close(self):
        GPIO.cleanup([self.step_pin, self.dir_pin]) 


def simpleTest():
    m = MotorController(21,22)

    locations = [(-100, 10),(100, -10) , (-5, -5)]
    threshold = 10

    for x,y in locations:
        print("processing: ",x,y)
        # Is the value within +_threshold range
        if abs(x) <= threshold:
            time.sleep(.5)

        else:
            speed = 1000
            # If it's outside, determine the direction to move
            if x > 0: 
                direction = 'right'
            else: 
                direction = 'left'
        
            m.moveTime(1, direction, speed)
            time.sleep(1)
    m.close()

#simpleTest() 


def test():
    m = MotorController(21, 22)
    m.moveLiveStart()

    # Counterclockwise
    m.moveLiveSetSpeed(2000)

    print('sleeping')
    time.sleep(1)

    print('awake, changing speed')
    # Clockwise
    m.moveLiveSetSpeed(-2000)

    time.sleep(1)

    print('closing')
    m.moveLiveEnd()
    m.close()

#test()