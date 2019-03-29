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
    _LIMIT = 240

    _CURRENT_RAW_PATH = 'hike4/1.jpg'
    _NEXT_RAW_PATH = 'hike4/2.jpg'

    _IS_FADING = False

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

        

        self.current_raw = Image.open(self._CURRENT_RAW_PATH, 'r')
        self.next_raw = Image.open(self._NEXT_RAW_PATH, 'r')
        self.new_img_raw = Image.open('hike4/1.jpg', 'r')
        
        self.display_photo_image = ImageTk.PhotoImage(self.current_raw)
        self.image_label = Label(master=root, image=self.display_photo_image)
        self.image_label.pack(side='bottom', fil='both', expand='yes')

        root.after(100, func=self.fade_image)


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


    def update_raw_images(self, command):
        if command == '+':
            if self._PICTURE + 1 > self._LIMIT:
                self._PICTURE = 1
            
            # self._CURRENT_RAW_PATH = self._DIRECTORY + str(self._PICTURE) + self._EXTENSION
            self._NEXT_RAW_PATH = self._DIRECTORY + str(self._PICTURE + 1) + self._EXTENSION

            # self.current_raw = Image.open(self._CURRENT_RAW_PATH, 'r')
            self.next_raw = Image.open(self._NEXT_RAW_PATH, 'r')

            self._PICTURE += 1

        # elif command == '-':
        
        else:
            raise Exception('command should be either '+' or '-'')


    def fade_image(self):
        print('Fading the image at alpha of: ', self.alpha)
        if self.alpha < 1.0:
            # self._IS_FADING = True
            self.current_raw = Image.blend(self.current_raw, self.next_raw, self.alpha)
            self.display_photo_image = ImageTk.PhotoImage(self.current_raw)
            self.image_label.configure(image=self.display_photo_image)

            self.alpha = self.alpha + 0.01
            root.after(100, self.fade_image)
        # else:
            # self._IS_FADING = False
            # self.alpha = 0.0
        # root.after(1, self.fade_image)


    # def showImage(self):
    #     self.img = ImageTk.PhotoImage(Image.open(self.FILE_PATH, 'r'))
    #     self.picture_label.configure(image=self.img)


    def rightKey(self, event):
        print("Increment the count")
        self.update_raw_images('+')
        # self.alpha = 0                      


        # if self._IS_FADING == False:
        #     print('FADING IS FALSE')
        #     print('START FADE')
        #     self.fade_image()

        # self.moveFilePointer('+')
        # self.fade_image()
        # self.showImage()


    def leftKey(self, event):
        print("Decrement the count")
        self.moveFilePointer('-')
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
