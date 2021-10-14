#!/usr/bin/env python3
import os, sys, time, string
import RPi.GPIO as GPIO

class Button:
    def __init__(self, channel, parent):
        self.parent = parent
        self.channel = channel
        self.state = 0
        
    def button_rise_callback(self, channel):
        self.parent.n = self.parent.n + 1
        
        val = GPIO.input(channel)

        if self.state == val: return
        self.state = val

        if val == 0:
            print("%s Button was released: %s" % (self.parent.n, channel))
        else:
            print("%s Button was pushed: %s" % (self.parent.n, channel))

class Buttons:
    def __init__(self):
        self.n = 0
        self.buttons = {}
    
    def add(self, button):
        self.buttons[button.channel] = button

def setup():
    GPIO.setwarnings(False)
    GPIO.setmode(GPIO.BCM)

    buttons = Buttons()

    for pin in (12, 13, 23, 27):
        b = Button(pin, buttons)
        buttons.add(b)
        GPIO.setup(pin, GPIO.IN, pull_up_down=GPIO.PUD_DOWN)
        GPIO.add_event_detect(pin, GPIO.BOTH, callback=b.button_rise_callback)

    return buttons


def start():
    setup()
    message = input("Press enter to quit\n\n")
    GPIO.cleanup() # Clean up

if __name__ == "__main__" :
    start()
