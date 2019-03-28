#!/usr/bin/env python3

from gpiozero import Button
#from RPi import GPIO
# import Queue
from queue import *

eventq = Queue()

pin_a = Button(17)                      # Rotary encoder pin A connected to GPI17
pin_b = Button(18)                      # Rotary encoder pin B connected to GPI18


# Pin A event handler
def pin_a_rising():
    if pin_b.is_pressed:
        print('-1')
        # eventq.put(-1) # pin A rising while B is active is a counter-clockwise turn


# Pin B event handler
def pin_b_rising():
    if pin_a.is_pressed:
        print('1')
        # eventq.put(1) # pin B rising while A is active is a clockwise turn


# Register the event handler for pin A
pin_a.when_pressed = pin_a_rising
# Register the event handler for pin B
pin_b.when_pressed = pin_b_rising

while True:
    message = eventq.get()
    print(message)
