#!/usr/bin/env python3

import sys
# from tkinter import *
from tkinter import Tk, Label
from PIL import ImageTk, Image

class Slideshow:
    FILE_PATH = 'hike4/2.jpg'
    EXTENSION = 'jpg'

    def __init__(self, win):
        self.window = win
        self.window.title("Capra")
        self.window.geometry("1280x720")
        self.window.configure(background='black')

        self.img = ImageTk.PhotoImage(Image.open(self.FILE_PATH, 'r'))
        self.picture_label = Label(master=self.window, image=self.img)
        self.picture_label.pack(side="bottom", fill="both", expand="yes")

        self.window.bind('<Left>', self.leftKey)
        self.window.bind('<Right>', self.rightKey)

    def showImage(self):
        self.img = ImageTk.PhotoImage(Image.open('hike4/4.jpg', 'r'))
        self.picture_label.configure(image=self.img)

    def moveFilePointer(self):
        print('howdy')

    def rightKey(self, event):
        sys.stdout.flush()
        print("Increment the count")
        sys.stdout.flush()
        self.moveFilePointer()
        self.showImage()

    def leftKey(self, event):
        sys.stdout.flush()
        print("Decrement the count")
        sys.stdout.flush()
        self.moveFilePointer()
        self.showImage()
    
# This creates the root window
root = Tk()
slide_show = Slideshow(root)
root.mainloop()