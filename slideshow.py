#!/usr/bin/env python3

import sys
# from tkinter import *
from tkinter import Tk, Label
from PIL import ImageTk, Image

class Slideshow:
    FILE_PATH = '4.jpg'
    EXTENSION = 'jpg'

    def __init__(self, win):
        self.window = win
        self.window.title("Capra")
        self.window.geometry("1280x720")
        self.window.configure(background='black')

        self.img = ImageTk.PhotoImage(Image.open(self.FILE_PATH))
        self.picture = Label(self.window, image=self.img)
        self.picture.pack(side="bottom", fill="both", expand="yes")

        self.window.bind('<Left>', self.leftKey)
        self.window.bind('<Right>', self.rightKey)

    def showImage(self):
        #Creates a Tkinter-compatible photo image, which can be used everywhere Tkinter expects an image object.
        img = ImageTk.PhotoImage(Image.open(self.FILE_PATH))
        #The Label widget is a standard Tkinter widget used to display a text or image on the screen.
        picture = Tk.Label(self.window, image = img)
        #The Pack geometry manager packs widgets in rows or columns.
        picture.pack(side="bottom", fill="both", expand="yes")

    def leftKey(self, event):
        sys.stdout.flush()
        print("Decrement the count")
        sys.stdout.flush()

    def rightKey(self, event):
        sys.stdout.flush()
        print("Increment the count")
        sys.stdout.flush()

# This creates the root window
root = Tk()
slide_show = Slideshow(root)
root.mainloop()