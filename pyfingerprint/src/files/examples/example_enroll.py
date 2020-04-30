#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
PyFingerprint
Copyright (C) 2015 Bastian Raschke <bastian.raschke@posteo.de>
All rights reserved.

"""

import time
from pyfingerprint.pyfingerprint import PyFingerprint
#alterado
import sqlite3
import RPi.GPIO as gpio

LED_RED = 40
LED_GREEN = 38
LED_BLUE = 36

## Enrolls new finger
##

def configura_GPIO():
    gpio.setmode(gpio.BOARD)
    gpio.setup(LED_BLUE, gpio.OUT)
    gpio.setup(LED_GREEN, gpio.OUT)
    gpio.setup(LED_RED, gpio.OUT)

## Tries to initialize the sensor
try:
    f = PyFingerprint('/dev/ttyUSB0', 57600, 0xFFFFFFFF, 0x00000000)

    if ( f.verifyPassword() == False ):
        raise ValueError('The given fingerprint sensor password is wrong!')

    configura_GPIO()

except Exception as e:
    print('The fingerprint sensor could not be initialized!')
    print('Exception message: ' + str(e))
    #if there is some communication sensor failure in this point the red led will blink once
    piscaLed(LED_RED, 1)
    time.sleep(5)
    exit(1)

def acendeLed(pino_led):
    gpio.output(pino_led, 1)
    return


def apagaLed(pino_led):
    gpio.output(pino_led, 0)
    return

#Turn off Blue Led and does the pin (another led color) blinks 'qtd' times 
def piscaLed(pin, qtd):
    apagaLed(LED_BLUE)
    for i in range(qtd):
        acendeLed(pin)
        time.sleep(0.5)
        apagaLed(pin)
        time.sleep(0.5)


## Gets some sensor information
print('Currently used templates: ' + str(f.getTemplateCount()) +'/'+ str(f.getStorageCapacity()))

## Tries to enroll new finger
try:
    print('Waiting for finger...')
    acendeLed(LED_BLUE)

    ## Wait that finger is read
    while ( f.readImage() == False ):
        pass

    ## Converts read image to characteristics and stores it in charbuffer 1
    f.convertImage(0x01)

    ## Checks if finger is already enrolled
    result = f.searchTemplate()
    positionNumber = result[0]

    if ( positionNumber >= 0 ):
        print('Template already exists at position #' + str(positionNumber))
        #if the fingerprint already exists in the sensor memory the red led will blinks twice
        piscaLed(LED_RED, 2)
        time.sleep(5)
        exit(0)

    print('Remove finger...')
    apagaLed(LED_BLUE)
    time.sleep(2)

    print('Waiting for same finger again...')
    acendeLed(LED_BLUE)
    ## Wait that finger is read again
    while ( f.readImage() == False ):
        pass

    ## Converts read image to characteristics and stores it in charbuffer 2
    f.convertImage(0x02)

    ## Compares the charbuffers
    if ( f.compareCharacteristics() == 0 ):
        #if the first and second read don't match the red led will blinks three times
        piscaLed(LED_RED, 3)
        raise Exception('Fingers do not match')

    ## Creates a template
    f.createTemplate()

    ## Saves template at new position number
    positionNumber = f.storeTemplate()
    #if the fingerprint enrolled successfully the green will brinks twice
    piscaLed(LED_GREEN, 2)
    print('Finger enrolled successfully!')
    print('New template position #' + str(positionNumber))
    #alterado
    print(positionNumber)
    #alterado

    #metodo de atualizar banco
    url = '/home/pi/github/Projeto-Fechadura-Biometrica/User-Interface/optima.db'
    conn = sqlite3.connect(url)
    cursor = conn.cursor()
    try:
        cursor.execute("""
            ALTER TABLE optima
            ADD COLUMN pos_number INTEGER
            """)
        print("position number column created")
        cursor.execute("""
            UPDATE optima
            SET pos_number = (?)
            WHERE pos_number IS NULL
            """, (positionNumber,)
                       )
        print("data successfully updated")
        conn.commit()
        conn.close()
        
    except:
        print("column already exists")
        cursor.execute("""
        UPDATE optima
        SET pos_number = (?)
        WHERE pos_number IS NULL
        """, (positionNumber,))
        print("data successfully updated")
        conn.commit()
        conn.close()
        
    time.sleep(5)

except Exception as e:
    print('Operation failed!')
    print('Exception message: ' + str(e))
    time.sleep(5)
    exit(1)
