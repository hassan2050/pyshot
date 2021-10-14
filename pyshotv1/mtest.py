#!/usr/bin/env python3
import os, sys, time, string
import RPi.GPIO as GPIO

def button_rise_callback(channel):
  val = GPIO.input(channel)
  a1 = GPIO.input(17)
  a2 = GPIO.input(18)

  if val:
    print (channel, val, a1, a2)
  

def setup():
    GPIO.setwarnings(False)
    GPIO.setmode(GPIO.BCM)

    GPIO.setup(17, GPIO.OUT)
    GPIO.setup(18, GPIO.OUT)
    
    GPIO.setup(23, GPIO.IN, pull_up_down=GPIO.PUD_DOWN)
    GPIO.setup(27, GPIO.IN, pull_up_down=GPIO.PUD_DOWN)

    GPIO.add_event_detect(23, GPIO.BOTH, callback=button_rise_callback)
    GPIO.add_event_detect(27, GPIO.BOTH, callback=button_rise_callback)

    GPIO.output(17, GPIO.LOW)
    GPIO.output(18, GPIO.LOW)
    
    while 1:
      GPIO.output(17, GPIO.LOW)
      GPIO.output(18, GPIO.HIGH)
      time.sleep(.05)
      GPIO.output(17, GPIO.HIGH)
      GPIO.output(18, GPIO.LOW)
      time.sleep(.05)



def start():
    setup()
    message = input("Press enter to quit\n\n")
    GPIO.cleanup() # Clean up

if __name__ == "__main__" :
    start()
