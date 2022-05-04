import time
import Jetson.GPIO as GPIO

class motorControl:
    def __init__(self, MOTOR_STEP_PIN, MOTOR_DIR_PIN, step_angle_deg=1.8, micro_steps=.125):
        self.step_pin = MOTOR_STEP_PIN 
        self.dir_pin = MOTOR_DIR_PIN 
        GPIO.setwarnings(True)
        GPIO.setmode(GPIO.BOARD)
        GPIO.setup(MOTOR_STEP_PIN, GPIO.OUT, initial=GPIO.LOW) 
        GPIO.setup(MOTOR_DIR_PIN, GPIO.OUT, initial=GPIO.LOW) 
        self.step_angle_deg = step_angle_deg
        self.micro_steps = micro_steps
    
    def move(self, move_angle, speed, angle='degrees'):
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

    def close(self):
        GPIO.cleanup([self.step_pin, self.dir_pin]) 