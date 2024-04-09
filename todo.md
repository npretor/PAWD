


Two modes: Monitor and Active  
    Monitor 
        - waits for a PID input signal, then records video with a timestamp for 10 seconds (for now). If the PID is detected during the recording, 10 seconds is added. 
        - (later) When a PID signal is detected, video is processed for 30 seconds and if an animal is detected, mode is switched to active. Recording should still be streaming to a file, just now also a server and the processing input 
    Active 
        - Powers up the stepper motors 
        - (later) Raises the rain protection 


Active settings: 
    auto-tracking
    auto-firing 
    firing duration and pause time 

3 simultaneous possible streaming locations, always at least 2 
 - log file location 
 - ML model for processing 
 - webserver (possible) 