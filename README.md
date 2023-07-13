# PAWD: Precision Animal Watering Device

![./docs/images/IMG_3072.jpeg](PAWD and son of PAWD) 

### Startup 
Root priviledges are required for serial commands to the Arduino. 
1. Clone the repository
```
git clone git@github.com:npretor/PAWD.git && cd PAWD
```
2. Flash the Arduino with the provided serial motor control sketch under ./Arduino/MultiStepperSerialControl
3. Hookup the CSI camera to port 0
4. Start the script on the Jetson
    sudo ./main.py 

### Hookup and assembly 
This repo runs on a Jetson Nano with a CSI camera. Selectable tracking targets are based on detectnet classes: 
* Cat - Class 18 
* Dog - Class 19 
* Person - Class 1
