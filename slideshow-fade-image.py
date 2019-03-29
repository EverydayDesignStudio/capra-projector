#!/usr/bin/env python3

# Imports
#import queue                       # Queue functions for threading
import sys                          # System functions
from gpiozero import Button       # Rotary encoder, detected as button
from PIL import ImageTk, Image      # Pillow image functions
from RPi import GPIO                # GPIO pin detection for Raspberry Pi
from time import sleep              # sleeping functions
from tkinter import Tk, Label       # Tkinter, GUI framework in use

# Setup GPIO
clk = 17
cnt = 18
GPIO.setmode(GPIO.BCM)
GPIO.setup(clk, GPIO.IN, pull_up_down=GPIO.PUD_DOWN)
GPIO.setup(cnt, GPIO.IN, pull_up_down=GPIO.PUD_DOWN)


# Slideshow class which is the main class that runs and is listening for events
class Slideshow:
    # Setup for the batch of images
    # TODO - this will be changed when connected with database
    _EXTENSION = '.jpg'
    _DIRECTORY = 'hike4/'
    _PICTURE = 1
    _LIMIT = 240
    _CURRENT_RAW_PATH = 'hike4/1.jpg'
    _NEXT_RAW_PATH = 'hike4/2.jpg'

    # Initialization for rotary encoder
    clkLastState = GPIO.input(clk)


    def __init__(self, win):
        # Setup the window
        self.window = win
        self.window.title("Capra")
        self.window.geometry("1280x720")
        self.window.configure(background='red')

        # Bind to events in which to listen
        self.window.bind('<Left>', self.leftKey)
        self.window.bind('<Right>', self.rightKey)
        self.window.bind(GPIO.add_event_detect(clk, GPIO.BOTH, callback=self.detectedRotaryChange))
        
        # Initialization for images and associated properties
        self.alpha = 0
        self.current_raw = Image.open(self._CURRENT_RAW_PATH, 'r')
        self.next_raw = Image.open(self._NEXT_RAW_PATH, 'r')
        
        # Display the first image to the screen
        self.display_photo_image = ImageTk.PhotoImage(self.current_raw)
        self.image_label = Label(master=root, image=self.display_photo_image)
        self.image_label.pack(side='bottom', fil='both', expand='yes')

        # Start continual fading function, will loop for life of the class
        root.after(100, func=self.fade_image)


    # Updates the pointer to the NEXT image
    # command could be a '+' or '-' move in the database
    def update_raw_images(self, command):
        if command == '+':
            if self._PICTURE + 1 > self._LIMIT:
                self._PICTURE = 1

            self._NEXT_RAW_PATH = self._DIRECTORY + str(self._PICTURE + 1) + self._EXTENSION
            self.next_raw = Image.open(self._NEXT_RAW_PATH, 'r')
            self._PICTURE += 1

        elif command == '-':
            if self._PICTURE < 2:
                self._PICTURE = self._LIMIT

            self._NEXT_RAW_PATH = self._DIRECTORY + str(self._PICTURE - 1) + self._EXTENSION
            self.next_raw = Image.open(self._NEXT_RAW_PATH, 'r')
            self._PICTURE -= 1
        
        else:
            raise Exception('command should be either '+' or '-'')


    # Loops for the life of the program, fading between the current image
    # and the NEXT image
    def fade_image(self):
        print('Fading the image at alpha of: ', self.alpha)
        if self.alpha < 1.0:
            self.current_raw = Image.blend(self.current_raw, self.next_raw, self.alpha)
            self.display_photo_image = ImageTk.PhotoImage(self.current_raw)
            self.image_label.configure(image=self.display_photo_image)

            self.alpha = self.alpha + 0.1
        root.after(100, self.fade_image)


    # Detects right key press
    def rightKey(self, event):
        print('increment the count')
        self.update_raw_images('+')
        # Sets amount of fade between pictures
        self.alpha = .2


    # Detects left key press
    def leftKey(self, event):
        print("decrement the count")
        self.update_raw_images('-')
        # Sets amount of fade between pictures
        self.alpha = .2


    # Detects rotary encoder change
    def detectedRotaryChange(self, event):
        print("Rotary changed")
        clkState = GPIO.input(clk)
        cntState = GPIO.input(cnt)
        if clkState != self.clkLastState:
            # Increment
            if cntState != clkState:    
                self.update_raw_images('+')
                # Sets amount of fade between pictures
                self.alpha = .2
            # Decrement
            else:                       
                self.update_raw_images('-')
                # Sets amount of fade between pictures
                self.alpha = .2
        self.clkLastState = clkState
        # sleep(0.1)


# Create the root window
root = Tk()
slide_show = Slideshow(root)
root.mainloop()
