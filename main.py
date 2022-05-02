

def objectFilter():
    pass


def boundingBoxToError(frames):
    """
    We need to make this a separate function from alignment since we should smooth over any gaps. 
    The models doesn't have any object permanece so we have to make an approximation 
    Input:  
        frames: frames to wait after the object dissapears. 
    """


def alignment(xError, yError):
    """    
    Goal: Adjust the motor speed as the x and y error converges
    Inputs:
        xError: float
        yError: float
    """

    return speedX, speedY


def PID(Kp, Ki, Kd, MV_bar=0):
    """
    From: https://jckantor.github.io/CBE30338/04.01-Implementing_PID_Control_with_Python_Yield_Statement.html
    Output: setpoint
    """

    # initialize stored data
    e_prev = 0
    t_prev = -100
    I = 0
    
    # initial control
    MV = MV_bar
    
    while True:
        # yield MV, wait for new t, PV, SP
        t, PV, SP = yield MV
        
        # PID calculations
        e = SP - PV
        
        P = Kp*e
        I = I + Ki*e*(t - t_prev)
        D = Kd*(e - e_prev)/(t - t_prev)
        
        MV = MV_bar + P + I + D
        
        # update stored data for next iteration
        e_prev = e
        t_prev = t    