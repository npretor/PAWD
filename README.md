# PAWD: Precision Animal Watering Device

The goal of this project was to make a water turret to keep our dogs away from certain areas in the yard. It uses a Jetson Nano for inference, and an Arduino for low level motor control. 

![PAWD and son of PAWD](./docs/images/IMG_3231.jpeg) 

### Startup 
Root priviledges are required for serial commands to the Arduino. 
1. Clone the repository
```
git clone git@github.com:npretor/PAWD.git && cd PAWD
```
2. Flash the Arduino with the provided serial motor control sketch under ./Arduino/MultiStepperSerialControl
3. Hookup the CSI camera to port 0
4. Start the script on the Jetson
```   
    sudo ./main.py 
```

### Hookup and assembly 
This repo runs on a Jetson Nano with a CSI camera. Selectable tracking targets are based on detectnet classes: 
* Cat - Class 18 
* Dog - Class 19 
* Person - Class 1

## Develop mode 
```
sudo docker run --runtime nvidia -it --privileged --rm --network=host -v /tmp/argus_socket:/tmp/argus_socket -v ~/github/PAWD/:/home/PAWD/ -v /dev/ttyUSB0:/dev/ttyUSB0 dustynv/opencv:r32.7.1

cd home/PAWD 
pip3 install Flask nanocamera ipdb Pillow pyserial imagezmq telemetrix-aio
cd flask 
python3 app.py 
```

## Build container 
```
docker build -t turretapp:v1 .
```

## Start the server 
```
sudo docker run --runtime nvidia -it --privileged --rm --network=host -v /tmp/argus_socket:/tmp/argus_socket -v ~/github/PAWD/:/home/PAWD/ turretapp:v1 
python3 app.py
```


### Install local cert 
```
cd ~/github/PAWD
sudo apt-get install openssl
openssl genrsa -out server.key 2048
openssl req -new -key server.key -out server.csr
openssl x509 -req -days 365 -in server.csr -signkey server.key -out server.crt
```


### Install arduino cli 
```

mkdir ~/local && mkdir ~/local/bin
curl -fsSL https://raw.githubusercontent.com/arduino/arduino-cli/master/install.sh | BINDIR=~/local/bin sh
PATH=$PATH:/home/dlinano/local/bin

arduino-cli core update-index --additional-urls https://files.seeedstudio.com/arduino/package_seeeduino_boards_index.json
arduino-cli core update-index --additional-urls https://raw.githubusercontent.com/espressif/arduino-esp32/gh-pages/package_esp32_index.json
```

### Use arduino cli 