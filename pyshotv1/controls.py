#!/usr/bin/env python3
import os, sys, time, string, logging
import RPi.GPIO as GPIO
import pygame
import threading

class Button:
    def __init__(self, channel, key, parent):
        self.parent = parent
        self.channel = channel
        self.key = key
        self.state = 0
        self.lastpressed = 0
        
    def button_rise_callback(self, channel):
        self.parent.n = self.parent.n + 1
        
        val = GPIO.input(channel)

        dt = time.time() - self.lastpressed
        
        if self.state == val: return
        
        logging.debug("%s: button_rise: val:%s state:%s" % (self.channel, val, self.state))

        if 0:
          if dt < .50:
            logging.debug("%s: dt=%s" % (self.channel, dt))
            return
        
        self.state = val
        
        if val == 1:
          self.released(self.key)
        else:
          self.lastpressed = time.time()
          self.pressed(self.key)
          
            
    def pressed(self, key):
      pygame.event.post(pygame.event.Event(pygame.KEYDOWN, key=key))
      logging.debug("%s: Button was pushed: (%s)" % (self.channel, key))

    def released(self, key):
      pygame.event.post(pygame.event.Event(pygame.KEYUP, key=key))
      logging.debug("%s: Button was released: (%s)" % (self.channel, key))
            

class Button2:
    def __init__(self, channel, keys, parent):
        self.parent = parent
        self.channel = channel
        self.keys = keys

        self.state = 0

    def wait(self, line):
      val = GPIO.input(self.channel)
      if val:
        while 1:
          val = GPIO.input(self.channel)
          if not val: break
          time.sleep(.05)
        self.released(self.keys[line])
      self.state = val

    def button_rise_callback(self, line):
        self.parent.n = self.parent.n + 1
        
        val = GPIO.input(self.channel)
        if self.state == val: return
        
        logging.debug("%s: button_rise: val:%s state:%s" % (self.channel, val, self.state))
        self.state = val

        if val == 0:
          self.released(self.keys[line])
        else:
          self.pressed(self.keys[line])

    def pressed(self, key):
      pygame.event.post(pygame.event.Event(pygame.KEYDOWN, key=key))
      logging.debug("%s: Button was pushed: (%s)" % (self.channel, key))

    def released(self, key):
      pygame.event.post(pygame.event.Event(pygame.KEYUP, key=key))
      logging.debug("%s: Button was released: (%s)" % (self.channel, key))
            
class Buttons:
    def __init__(self):
        self.n = 0
        self.buttons = {}
    
    def add(self, button):
        self.buttons[button.channel] = button

class Keypad(threading.Thread):
  def __init__(self, lines, buttons):
    super().__init__()
    
    self.buttons = buttons
    self.lines = lines

    self.setDaemon(True)
    
  def run(self):
    while 1:
      for n,line in enumerate(self.lines):
        GPIO.output(line, GPIO.HIGH)

        for b in self.buttons:
          val = GPIO.input(b.channel)
          if val:
            b.button_rise_callback(n)
            b.wait(n)

        GPIO.output(line, GPIO.LOW)
        time.sleep(.1)
    
def setupButtons():
    GPIO.setwarnings(False)
    GPIO.setmode(GPIO.BCM)

    buttons = Buttons()

    for (pin, key) in ((12, 'z'), (13, 'x')):
    #for (pin, key) in ((5, 'z'), (6, 'x')):
        b = Button(pin, ord(key), buttons)
        buttons.add(b)
        GPIO.setup(pin, GPIO.IN, pull_up_down=GPIO.PUD_UP)
        GPIO.add_event_detect(pin, GPIO.BOTH,
                              callback=b.button_rise_callback, bouncetime=100)

    lines = (18, 17)
    for line in lines:
      GPIO.setup(line, GPIO.OUT)
      GPIO.output(line, GPIO.LOW)

    for (pin, keys) in ((23, (ord('\r'), ord('v'))), (27, (ord('a'), ord('m')))):
        b = Button2(pin, keys, buttons)
        buttons.add(b)
        GPIO.setup(pin, GPIO.IN, pull_up_down=GPIO.PUD_DOWN)
        
    time.sleep(.5)

    keypad = Keypad(lines, (buttons.buttons[23], buttons.buttons[27]))
    buttons.keypad = keypad
    keypad.start()

    return buttons

    
def start():
  buttons = setupButtons()
  message = input("Press enter to quit\n\n")
  
  GPIO.cleanup() # Clean up

if __name__ == "__main__" :
    start()
