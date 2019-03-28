#!/usr/bin/env python3

# Imports
import sys
from PIL import ImageTk, Image
from RPi import GPIO
from gpiozero import Button
from time import sleep
from tkinter import Tk, Label
import queue

# Setup for GPIO
clk = 17
cnt = 18

GPIO.setmode(GPIO.BCM)
GPIO.setup(clk, GPIO.IN, pull_up_down=GPIO.PUD_DOWN)
GPIO.setup(cnt, GPIO.IN, pull_up_down=GPIO.PUD_DOWN)


# Slideshow class which is the main class that runs and is listening for events
class Slideshow:
    _DIRECTORY = 'hike4/'
    # _DIRECTORY = 'hike4-tiny/'
    _EXTENSION = '.jpg'
    # FILE_PATH = ''
    FILE_PATH = 'hike4-tiny/2.jpg'
    COUNT = 0
    _LIMIT = 241
    
    ROTARY_COUNTER = 1
    clkLastState = GPIO.input(clk)

    # pin_a = Button(17)  # Rotary encoder pin A connected to GPI17
    # pin_b = Button(18)  # Rotary encoder pin B connected to GPI18

    def __init__(self, win):
        self.window = win
        self.window.title("Capra")
        self.window.geometry("1280x720")
        self.window.configure(background='black')

        self.moveFilePointer('+')
        self.img = ImageTk.PhotoImage(Image.open(self.FILE_PATH, 'r'))
        self.picture_label = Label(master=self.window, image=self.img)
        self.picture_label.pack(side="bottom", fill="both", expand="yes")

        self.window.bind('<Left>', self.leftKey)
        self.window.bind('<Right>', self.rightKey)
        
        self.window.bind(GPIO.add_event_detect(clk, GPIO.BOTH, callback=self.detectedRotaryChange))

        # Register the event handler for pin A
        # self.pin_a.when_pressed = self.pin_a_rising
        # Register the event handler for pin B
        # self.pin_b.when_pressed = self.pin_b_rising

        # self.the_queue = queue.Queue()
        # root.after(100, self.listen_for_results())

        root.after(10, self.update_picture())

    # Pin A event handler
    def pin_a_rising(self):
        if self.pin_b.is_pressed:
            self.moveFilePointer('+')
            self.showImage()

            # print('-1')
            # eventq.put(-1) # pin A rising while B is active is a counter-clockwise turn

    # Pin B event handler
    def pin_b_rising(self):
        if self.pin_a.is_pressed:
            self.moveFilePointer('-')
            self.showImage()

            # print('1')
            # eventq.put(1) # pin B rising while A is active is a clockwise turn
    
    def detectedRotaryChange(self, event):
        print("Rotary changed")
        clkState = GPIO.input(clk)
        cntState = GPIO.input(cnt)
        if clkState != self.clkLastState:
            if cntState != clkState:
                self.ROTARY_COUNTER += 1
                # self.the_queue.put('plus one')
            else:
                self.ROTARY_COUNTER -= 1
                # self.the_queue.put('minus one')
        self.clkLastState = clkState
        # sleep(0.1)
        
        self.buildFilePointer()
        # self.showImage()
    
    def showImage(self):
        self.img = ImageTk.PhotoImage(Image.open(self.FILE_PATH, 'r'))
        self.picture_label.configure(image=self.img)
        
    def buildFilePointer(self):
        if self.ROTARY_COUNTER > self._LIMIT:
            self.ROTARY_COUNTER = 1
        elif self.ROTARY_COUNTER < 1:
            self.ROTARY_COUNTER = self._LIMIT
        sys.stdout.flush()
        print(self.ROTARY_COUNTER)
        sys.stdout.flush()

        self.FILE_PATH = self._DIRECTORY + str(self.ROTARY_COUNTER) + self._EXTENSION
        sys.stdout.flush()
        print(self.FILE_PATH)
        sys.stdout.flush()

    def moveFilePointer(self, command):
        if command == '+':
            self.COUNT += 1
            if self.COUNT > self._LIMIT:
                self.COUNT = 1
        elif command == '-':
            self.COUNT -= 1
            if self.COUNT < 1:
                self.COUNT = self._LIMIT
        else:
            raise Exception('command should be either '+' or '-'')

        self.FILE_PATH = self._DIRECTORY + str(self.COUNT) + self._EXTENSION
        sys.stdout.flush()
        print(self.FILE_PATH)
        sys.stdout.flush()

    def update_picture(self):
        print('hello')
        self.showImage()
        root.after(1, self.update_picture)

    def rightKey(self, event):
        print("Increment the count")
        self.moveFilePointer('+')
        # self.showImage()

    def leftKey(self, event):
        print("Decrement the count")
        self.moveFilePointer('-')
        # self.showImage()

    def listen_for_results(self):
        print('Listening for results: ')
        try:
            message = self.the_queue.get()
            print(message)
            # root.after(100, self.listen_for_results())
        except queue.Empty:
            root.after(100, self.listen_for_results())

    
# Create the root window
root = Tk()
slide_show = Slideshow(root)
root.mainloop()
