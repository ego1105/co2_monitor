#!/usr/bin/python3
# -*- coding:utf-8 -*-

import RPi.GPIO as GPIO

# BCM pins
Prot   = 21
Pgruen = 16
Pgelb  = 20
RGG = ( Prot, Pgruen, Pgelb)

def init( pins):
    # initialize pins
    GPIO.setmode(GPIO.BCM)
    GPIO.setwarnings(False)
    for pin in pins:
        GPIO.setup( pin, GPIO.OUT)
        GPIO.output( pin, 0)

def set( pins, values):
    for pin, value in zip( pins, values):
        GPIO.output( pin, int(value))


try:
    #data file name
    file_co2 = 'data_last_co2.txt'

    # get last value or default
    try:
        with open( file_co2, 'r') as f:
            co2 = float( f.readline() )
    except:
        co2 = 400        

    # initialize leds
    init(RGG)        
    
    # switch leds
    if co2<1000:
        set( RGG, ( 0, 1, 0))
    elif co2>=1000 and co2<1500:
        set( RGG, ( 0, 0, 1))
    else:
        set( RGG, ( 1, 0, 0))


except IOError as e:
    print(e)
    
except KeyboardInterrupt:    
    print("ctrl + c:")    
    exit()

finally:  
    #GPIO.cleanup() # this ensures a clean exit, but will switch off the LEDs     
    pass
