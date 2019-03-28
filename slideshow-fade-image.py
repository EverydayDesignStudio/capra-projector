#!/usr/bin/env python3

# Imports
import sys
from PIL import ImageTk, Image
from time import sleep
from tkinter import Tk, Label
import queue


# Slideshow class which is the main class that runs and is listening for events
class Slideshow:
    _EXTENSION = '.jpg'
    _DIRECTORY = 'hike4/'
    _PICTURE = 58
    _LIMIT = 241

    def __init__(self, win):
        self.window = win
        self.window.title("Capra")
        self.window.geometry("1280x720")
        self.window.configure(background='red')

        self.alpha = 0

        # self.moveFilePointer('+')
        # self.img = ImageTk.PhotoImage(Image.open(self.FILE_PATH, 'r'))
        # self.picture_label = Label(master=self.window, image=self.img)
        # self.picture_label.pack(side="bottom", fill="both", expand="yes")

        

        self.window.bind('<Left>', self.leftKey)
        self.window.bind('<Right>', self.rightKey)

        # self.the_queue = queue.Queue()
        # root.after(100, self.listen_for_results())

        # root.after(10, self.update_picture())

        self.current_raw = Image.open('hike4/1.jpg', 'r')
        self.next_raw = Image.open('hike4/58.jpg', 'r')
        self.new_img_raw = Image.open('hike4/1.jpg', 'r')
        
        self.display_photo_image = ImageTk.PhotoImage(self.current_raw)
        self.image_label = Label(master=root, image=self.display_photo_image)
        self.image_label.pack(side='bottom', fil='both', expand='yes')

        root.after(0, func=self.fade_image)
        

    def moveFilePointer(self, command):
        if command == '+':
            self._PICTURE += 1
            if self._PICTURE > self._LIMIT:
                self._PICTURE = 1
        elif command == '-':
            self._PICTURE -= 1
            if self._PICTURE < 1:
                self._PICTURE = self._LIMIT
        else:
            raise Exception('command should be either '+' or '-'')

        self.FILE_PATH = self._DIRECTORY + str(self._PICTURE) + self._EXTENSION
        sys.stdout.flush()
        print(self.FILE_PATH)
        sys.stdout.flush()


    def fade_image(self):
        print('Fading the image at alpha of: ', self.alpha)
        if self.alpha < 1.0:
            self.new_img_raw = Image.blend(self.current_raw, self.next_raw, self.alpha)
            self.display_photo_image = ImageTk.PhotoImage(self.new_img_raw)
            self.image_label.configure(image=self.display_photo_image)

            self.alpha = self.alpha + 0.04
            root.after(1, self.fade_image)


    # def showImage(self):
    #     self.img = ImageTk.PhotoImage(Image.open(self.FILE_PATH, 'r'))
    #     self.picture_label.configure(image=self.img)


    def rightKey(self, event):
        print("Increment the count")
        # self.moveFilePointer('+')
        # self.showImage()


    def leftKey(self, event):
        print("Decrement the count")
        # self.moveFilePointer('-')
        # self.showImage()


    # Loops
    # def update_picture(self):
    #     print('checking for new image')
    #     self.showImage()
    #     root.after(10, self.update_picture)


    # def listen_for_results(self):
    #     print('Listening for results: ')
    #     try:
    #         message = self.the_queue.get()
    #         print(message)
    #         # root.after(100, self.listen_for_results())
    #     except queue.Empty:
    #         root.after(100, self.listen_for_results())
    

# Create the root window
root = Tk()
slide_show = Slideshow(root)
root.mainloop()
