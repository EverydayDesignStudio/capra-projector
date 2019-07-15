#!/usr/bin/env python3

is_RPi = True
DB = '/home/pi/Pictures/capra-projector.db'
PATH = '/home/pi/Pictures'
# DB = '/Volumes/Capra/capra-projector.db'
# PATH = '/Volumes/Capra'
blank_path = '{p}/blank.png'.format(p=PATH)

# Imports
from capra_data_types import Picture, Hike
from sql_controller import SQLController
from sql_statements import SQLStatements
from PIL import ImageTk, Image      # Pillow image functions
from tkinter import Tk, Label       # Tkinter, GUI framework in use
import time
if is_RPi:
    from gpiozero import Button         # Rotary encoder, detected as button
    from RPi import GPIO                # GPIO pin detection for Raspberry Pi
    from time import sleep


# Setup GPIO
if is_RPi:
    GPIO.setmode(GPIO.BCM)

    # Rotary encoder
    clk = 21
    cnt = 20
    rotary_button = 16
    GPIO.setup(clk, GPIO.IN, pull_up_down=GPIO.PUD_DOWN)
    GPIO.setup(cnt, GPIO.IN, pull_up_down=GPIO.PUD_DOWN)
    GPIO.setup(rotary_button, GPIO.IN, pull_up_down=GPIO.PUD_UP)

    # Rotary switch
    mode1 = 13
    mode2 = 19
    mode3 = 26
    GPIO.setup(mode1, GPIO.IN, pull_up_down=GPIO.PUD_UP)
    GPIO.setup(mode2, GPIO.IN, pull_up_down=GPIO.PUD_UP)
    GPIO.setup(mode3, GPIO.IN, pull_up_down=GPIO.PUD_UP)

    # Play / Pause button
    play_pause_button = 5
    GPIO.setup(play_pause_button, GPIO.IN, pull_up_down=GPIO.PUD_UP)


# Slideshow class which is the main class that runs and is listening for events
class Slideshow:
    # Setup for the batch of images
    TRANSITION_DELAY = 2000     # time between pictures in milliseconds
    IS_TRANSITION_FORWARD = True

    # Initialization for rotary encoder
    if is_RPi:
        clkLastState = GPIO.input(clk)
        ROTARY_COUNT = 0                # Used exclusively for testing

    def __init__(self, win):
        # Setup the window
        self.window = win
        self.window.title("Capra Slideshow")
        self.window.geometry("1280x720")
        self.window.configure(background='purple')

        # Bind to events in which to listen
        self.window.bind('<Left>', self.leftKey)
        self.window.bind('<Right>', self.rightKey)
        self.window.bind('<space>', self.space_key)

        if is_RPi:
            self.window.bind(GPIO.add_event_detect(clk, GPIO.BOTH, callback=self.detected_rotary_change))
            self.window.bind(GPIO.add_event_detect(rotary_button, GPIO.RISING, callback=self.rotary_button_pressed))
            # self.rotary_button_pressed = GPIO.input(rotary_button)        # not sure if this is correct

        # Initialization for database implementation
        self.sql_controller = SQLController(database=DB)
        self.picture_starter = self.sql_controller.get_first_time_picture_in_hike(13)
        self.picture = self.sql_controller.next_altitude_picture_across_hikes(self.picture_starter)
        self.picture_starter.print_obj()
        self.picture.print_obj()

        # Initialization for images and associated properties
        self.alpha = 0
        self.is_across_hikes = False

        # Initialize current and next images
        self.current_raw_top = Image.open(self._build_filename(self.picture_starter.camera1), 'r')
        self.next_raw_top = Image.open(self._build_filename(self.picture.camera1), 'r')
        self.current_raw_mid = Image.open(self._build_filename(self.picture_starter.camera2), 'r')
        self.next_raw_mid = Image.open(self._build_filename(self.picture.camera2), 'r')
        self.current_raw_bot = Image.open(blank_path, 'r')
        self.next_raw_bot = Image.open(blank_path, 'r')

        # Display the first 3 images to the screen
        self.display_photo_image_top = ImageTk.PhotoImage(self.current_raw_top)
        self.image_label_top = Label(master=root, image=self.display_photo_image_top)
        self.image_label_top.pack(side='right', fill='both', expand='yes')

        self.display_photo_image_mid = ImageTk.PhotoImage(self.current_raw_mid)
        self.image_label_mid = Label(master=root, image=self.display_photo_image_mid)
        self.image_label_mid.pack(side='right', fill='both', expand='yes')

        self.display_photo_image_bot = ImageTk.PhotoImage(self.current_raw_bot)
        self.image_label_bot = Label(master=root, image=self.display_photo_image_bot)
        self.image_label_bot.pack(side='right', fill='both', expand='yes')

        # Start continual fading function, will loop for life of the class
        root.after(0, func=self.fade_image)
        # root.after(self.TRANSITION_DELAY, func=self.auto_increment_slideshow)

    def _build_next_raw_images(self, next_picture: Picture):
        print('build images')
        self.next_raw_top = Image.open(self._build_filename(next_picture.camera1), 'r')
        self.next_raw_mid = Image.open(self._build_filename(next_picture.camera2), 'r')
        # self.next_raw_bot = Image.open(blank_path, 'r')

    def _build_filename(self, end_of_path: str) -> str:
        return '{p}{e}'.format(p=PATH, e=end_of_path)

    # Loops for the life of the program, fading between the current image and the NEXT image
    def fade_image(self):
        print('Fading the image at alpha of: ', self.alpha)
        print(time.time())
        if self.alpha < 1.0:
            # Top image
            self.current_raw_top = Image.blend(self.current_raw_top, self.next_raw_top, self.alpha)
            # self.current_raw_top = self.next_raw_top
            self.display_photo_image_top = ImageTk.PhotoImage(self.current_raw_top)
            self.image_label_top.configure(image=self.display_photo_image_top)

            # Middle image
            # self.current_raw_mid = Image.blend(self.current_raw_mid, self.next_raw_mid, self.alpha)
            self.current_raw_mid = self.next_raw_mid
            self.display_photo_image_mid = ImageTk.PhotoImage(self.current_raw_mid)
            self.image_label_mid.configure(image=self.display_photo_image_mid)

            # Bottom image
            self.current_raw_bot = Image.blend(self.current_raw_bot, self.next_raw_bot, self.alpha)
            # self.current_raw_bot = self.next_raw_bot
            self.display_photo_image_bot = ImageTk.PhotoImage(self.current_raw_bot)
            self.image_label_bot.configure(image=self.display_photo_image_bot)

            self.alpha = self.alpha + 0.0417
        root.after(83, self.fade_image)

    def auto_increment_slideshow(self):
        # print('Auto incremented slideshow')
        if self.IS_TRANSITION_FORWARD:
            self.picture = self.sql_controller.next_altitude_picture_across_hikes(self.picture)
            self.picture.print_obj()
            self._build_next_raw_images(self.picture)
            self.alpha = .2
        else:
            self.picture = self.sql_controller.previous_altitude_picture_across_hikes(self.picture)
            self.picture.print_obj()
            self._build_next_raw_images(self.picture)
            self.alpha = .2

        root.after(self.TRANSITION_DELAY, self.auto_increment_slideshow)

    # KEYBOARD KEYS
    def rightKey(self, event):
        print('increment the count')
        self.IS_TRANSITION_FORWARD = True
        self.picture = self.sql_controller.next_altitude_picture_across_hikes(self.picture)
        self.picture.print_obj()
        self._build_next_raw_images(self.picture)
        self.alpha = .2     # Resets amount of fade between pictures

    def leftKey(self, event):
        print("decrement the count")
        self.IS_TRANSITION_FORWARD = False
        self.picture = self.sql_controller.previous_altitude_picture_across_hikes(self.picture)
        self.picture.print_obj()
        self._build_next_raw_images(self.picture)
        self.alpha = .2     # Resets amount of fade between pictures

    def space_key(self, event):
        print('space key pressed')

    # HARDWARE CONTROLS
    def detected_rotary_change(self, event):
        clkState = GPIO.input(clk)
        cntState = GPIO.input(cnt)
        if clkState != self.clkLastState:
            # Increment
            if cntState != clkState:
                self.ROTARY_COUNT += 1
                print("Rotary +: ", self.ROTARY_COUNT)

                self.IS_TRANSITION_FORWARD = True   # For auto slideshow
                self.picture = self.sql_controller.next_time_picture_in_hike(self.picture)
                self.picture.print_obj()
                self._build_next_raw_images(self.picture)
                self.alpha = .2     # Resets amount of fade between pictures
            # Decrement
            else:
                self.ROTARY_COUNT -= 1
                print("Rotary -: ", self.ROTARY_COUNT)

                self.IS_TRANSITION_FORWARD = False  # For auto slideshow
                self.picture = self.sql_controller.previous_time_picture_in_hike(self.picture)
                self.picture.print_obj()
                self._build_next_raw_images(self.picture)
                self.alpha = .2     # Resets amount of fade between pictures
        self.clkLastState = clkState
        # sleep(0.1)

    def rotary_button_pressed(self, event):
        print('rotary pressed')
        # self.is_across_hikes = True

# Create the root window
root = Tk()
root.attributes("-fullscreen", True)
root.bind("<Escape>", exit)
slide_show = Slideshow(root)
root.mainloop()
