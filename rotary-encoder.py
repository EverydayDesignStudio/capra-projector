#!/usr/bin/env python3

#!/usr/bin/python

from gpiozero import Button
from RPi import GPIO
import Queue

eventq = Queue.Queue()

pin_a = Button(17)                      # Rotary encoder pin A connected to GPIO2
pin_b = Button(18)                      # Rotary encoder pin B connected to GPIO3

def pin_a_rising():                    # Pin A event handler
    if pin_b.is_pressed: eventq.put(-1)# pin A rising while A is active is a clockwise turn

def pin_b_rising():                    # Pin B event handler
    if pin_a.is_pressed: eventq.put(1) # pin B rising while A is active is a clockwise turn

pin_a.when_pressed = pin_a_rising      # Register the event handler for pin A
pin_b.when_pressed = pin_b_rising      # Register the event handler for pin B

while True:
    message = eventq.get()
    print(message)