# Reggaeton Be Gone
sends packets to disable BT speakers (hopefully)

#install

```ssh
pip install RPi.GPIO
pip3 install Adafruit_GPIO
sudo apt install git
pip install picamera
sudo apt install python3-opencv
sudo apt-get install libatlas-base-dev libportaudio0 libportaudio2 libportaudiocpp0 portaudio19-dev
git clone https://github.com/edgeimpulse/linux-sdk-python
sudo python3 -m pip install edge_impulse_linux -i https://pypi.python.org/simple
sudo python3 -m pip install numpy
sudo python3 -m pip install pyaudio
```

# Parts 
Raspberry Pi 3 \

DFRobot Oled 128x32 \

Push button \

BT Audio Receiver 5.0 (to test with your own BT) \

Jumper cables

# Connections
Oled SDA ->  Rpi GPIO 2
Oled SCL -> Rpi GPIO 3
Oled VCC -> Rpi VCC
Oled GND -> Rpi GND

Button pin 1 -> GPIO26
Button pin 2 -> GND

Power supply: 5V 3A

# Oled screen font
Font: White Rabbit, Created By: Matthew Welch

# Originally created by
Roni Bandini, @RoniBandini
