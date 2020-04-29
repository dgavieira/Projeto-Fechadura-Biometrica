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
    acendeLed(LED_RED)
    apagaLed(LED_RED)
    acendeLed(LED_RED)
    apagaLed(LED_RED)
    time.sleep(5)
    exit(1)

def acendeLed(pino_led):
    gpio.output(pino_led, 1)
    return


def apagaLed(pino_led):
    gpio.output(pino_led, 0)
    return


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
        apagaLed(LED_BLUE)
        acendeLed(LED_RED)
        apagaLed(LED_RED)
        acendeLed(LED_RED)
        apagaLed(LED_RED)
        print('Template already exists at position #' + str(positionNumber))
        time.sleep(5)
        exit(0)

    print('Remove finger...')
    apagaLed(LED_BLUE)
    acendeLed(LED_GREEN)
    apagaLed(LED_GREEN)
    acendeLed(LED_GREEN)
    apagaLed(LED_GREEN)
    acendeLed(LED_BLUE)
    time.sleep(2)

    print('Waiting for same finger again...')

    ## Wait that finger is read again
    while ( f.readImage() == False ):
        pass

    ## Converts read image to characteristics and stores it in charbuffer 2
    f.convertImage(0x02)

    ## Compares the charbuffers
    if ( f.compareCharacteristics() == 0 ):
        apagaLed(LED_BLUE)
        acendeLed(LED_RED)
        apagaLed(LED_RED)
        acendeLed(LED_RED)
        apagaLed(LED_RED)
        raise Exception('Fingers do not match')

    ## Creates a template
    f.createTemplate()

    ## Saves template at new position number
    positionNumber = f.storeTemplate()
    print('Finger enrolled successfully!')
    print('New template position #' + str(positionNumber))
    #alterado
    print(positionNumber)
    #alterado
    apagaLed(LED_BLUE)
    acendeLed(LED_GREEN)
    apagaLed(LED_GREEN)
    acendeLed(LED_GREEN)
    apagaLed(LED_GREEN)
    gpio.cleanup()

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
    apagaLed(LED_BLUE)
    time.sleep(5)
    exit(1)
