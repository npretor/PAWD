import time
import Jetson.GPIO as GPIO

# https://github.com/NVIDIA/jetson-gpio

# I'm seeing a ton of noise, for example from my macbook touchpad. Need a better power supply and shielding

Z_MOTOR_STEP =  21      # HEADER PIN 21 
Z_MOTOR_DIR =   22      # HEADER PIN 22 
Y_MOTOR_STEP =  23      # HEADER PIN 23 
Y_MOTOR_DIR =   24      # HEADER PIN 24 

delay = 0.001
steps = 100

# Set the numberings to be the same as the PCB board label numbers
GPIO.setwarnings(True)
GPIO.setmode(GPIO.BOARD)

# Set pin modes
GPIO.setup(Z_MOTOR_STEP, GPIO.OUT, initial=GPIO.LOW) 
GPIO.setup(Y_MOTOR_STEP, GPIO.OUT, initial=GPIO.LOW) 

GPIO.setup(Z_MOTOR_DIR, GPIO.OUT, initial=GPIO.LOW) 
GPIO.setup(Y_MOTOR_DIR, GPIO.OUT, initial=GPIO.LOW) 



for step in range(0, steps):
    time.sleep(delay)
    GPIO.output(Z_MOTOR_STEP, GPIO.HIGH)
    GPIO.output(Y_MOTOR_STEP, GPIO.HIGH)
    time.sleep(delay)
    GPIO.output(Z_MOTOR_STEP, GPIO.LOW)
    GPIO.output(Y_MOTOR_STEP, GPIO.LOW)    

time.sleep(1)
GPIO.output(Z_MOTOR_DIR, GPIO.HIGH) 
GPIO.output(Y_MOTOR_DIR, GPIO.HIGH) 

for step in range(0, steps):
    time.sleep(delay)
    GPIO.output(Z_MOTOR_STEP, GPIO.HIGH)
    GPIO.output(Y_MOTOR_STEP, GPIO.HIGH)
    time.sleep(delay)
    GPIO.output(Z_MOTOR_STEP, GPIO.LOW)
    GPIO.output(Y_MOTOR_STEP, GPIO.LOW)    


GPIO.cleanup([Z_MOTOR_DIR, Z_MOTOR_STEP, Y_MOTOR_DIR, Y_MOTOR_STEP])



class motorControl:
    def __init__(self, MOTOR_STEP_PIN, MOTOR_DIR_PIN, step_angle_deg=1.8, micro_steps=.125):
        self.step_pin = STEP_PIN 
        self.dir_pin = DIR_PIN 
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
            GPIO.output(Z_MOTOR_STEP, GPIO.HIGH)
            GPIO.output(Y_MOTOR_STEP, GPIO.HIGH)
            time.sleep(delay)
            GPIO.output(Z_MOTOR_STEP, GPIO.LOW)
            GPIO.output(Y_MOTOR_STEP, GPIO.LOW)   
            time.sleep(delay)

    def close(self):
        GPIO.cleanup([MOTOR_STEP_PIN, MOTOR_DIR_PIN])
