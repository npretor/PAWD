import time 

class FiringTimer:
    def __init__(self, firing_time=5):
        self.firing_time = firing_time
        self.firing_active = False
        self.t_stop = time.time()

    def fire(self):
        self.t_stop = time.time() + self.firing_time

    def update_firing_status(self):
        if time.time() >= self.t_stop:
            self.firing_active = False 
        else:
            self.firing_active = True

    @property
    def firing_status(self):
        self.update_firing_status()
        return self.firing_active


def map_x_range(values, old_min=0, old_max=90, new_min=1200, new_max=1800):
    return np.clip( ((values - old_min) / (old_max - old_min)) * (new_max - new_min) + new_min, a_min=new_min, a_max=new_max)

def map_y_range(values, old_min=-45, old_max=45, new_min=1200, new_max=1800):
    return np.clip( ((values - old_min) / (old_max - old_min)) * (new_max - new_min) + new_min, a_min=new_min, a_max=new_max)
