"""
The jetson has issues with disconnecting from wifi and losing it's ipv4 address, 
resulting in it only having an ipv6 address and losing local network access. 
Not sure why, but restarting the wifi fixes this. 
"""
import subprocess
import socket 
import os 

mine = os.popen('ifconfig wlan0 | grep "inet 192" | cut -c 14-25')
myip = mine.read() 

if myip.startswith('192'):
    # Good to go 
    print("Connected:",myip)
    pass 
else:
    print('Not connected:',myip)
    # Option 1
    subprocess.run(["sudo", "ifconfig", "wlan0", "down", "&&", "sudo", "ifconfig", "wlan0", "up"])
    
    # Option 2 
    # subprocess.run["sudo", "systemctl", "restart", "systemd-networkd"] 



