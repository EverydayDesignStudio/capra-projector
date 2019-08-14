#!/usr/bin/env python3

is_RPi = True

if is_RPi:
    DB = '/home/pi/Pictures/capra-projector.db'
    PATH = '/home/pi/Pictures'
else:
    DB = '/Volumes/Capra/capra-projector.db'
    PATH = '/Volumes/Capra'
blank_path = '{p}/blank.png'.format(p=PATH)

# Imports
from capra_data_types import Picture, Hike
from sql_controller import SQLController
from sql_statements import SQLStatements
from PIL import ImageTk, Image          # Pillow image functions
from tkinter import Tk, Canvas, Label   # Tkinter, GUI framework in use
import time
from time import sleep
import datetime
if is_RPi:
    from gpiozero import Button         # Rotary encoder, detected as button
    from RPi import GPIO                # GPIO pin detection for Raspberry Pi

# GPIO BCM PINS
ROTARY_ENCODER_CLOCKWISE = 23
ROTARY_ENCODER_COUNTER = 24
ROTARY_ENCODER_BUTTON = 25

BUTTON_PLAY_PAUSE = 5
BUTTON_NEXT = 6
BUTTON_PREVIOUS = 12

# ADC - MCP 3008 Channels
ACCELEROMETER_X = 7
ACCELEROMETER_Y = 6
ACCELEROMETER_Z = 5

BUTTON_MODE = 2

SLIDER_SWITCH_MODE_1 = 2
SLIDER_SWITCH_MODE_2 = 1
SLIDER_SWITCH_MODE_3 = 0


# Setup GPIO
if is_RPi:
    GPIO.setmode(GPIO.BCM)

    # Rotary encoder
    clk = 23
    cnt = 24
    rotary_button = 25
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
        # self.window.geometry("720x1280")
        self.window.configure(background='purple')
        self.canvas = Canvas(root, width=1280, height=720, background="#888", highlightthickness=0)
        # self.canvas.configure(bg='#444')
        self.canvas.pack(expand='yes', fill='both')

        # Bind to events in which to listen
        self.window.bind('<Left>', self.leftKey)
        self.window.bind('<Right>', self.rightKey)
        self.window.bind('<space>', self.space_key)

        if is_RPi:
            self.window.bind(GPIO.add_event_detect(clk, GPIO.BOTH, callback=self.detected_rotary_change))
            # Using GPIO.BOTH sorta works, but is super glitchy, will probably need an after loop
            self.window.bind(GPIO.add_event_detect(rotary_button, GPIO.BOTH, callback=self.rotary_button_pressed))
            # self.rotary_button_pressed = GPIO.input(rotary_button)  # not sure if this is correct

        # Initialization for database implementation
        self.sql_controller = SQLController(database=DB)
        self.picture_starter = self.sql_controller.get_first_time_picture_in_hike(14)
        self.picture = self.sql_controller.next_time_picture_in_hike(self.picture_starter)

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
        self.image_label_top = Label(master=self.canvas, image=self.display_photo_image_top, borderwidth=0)
        self.image_label_top.pack(side='right', fill='both', expand='yes')
        # self.image_label_top.place(x=20, rely=0.0, anchor='nw')

        self.display_photo_image_mid = ImageTk.PhotoImage(self.current_raw_mid)
        self.image_label_mid = Label(master=self.canvas, image=self.display_photo_image_mid, borderwidth=0)
        self.image_label_mid.pack(side='right', fill='both', expand='yes')
        # self.image_label_mid.place(x=20, y=405, anchor='nw')

        self.display_photo_image_bot = ImageTk.PhotoImage(self.current_raw_bot)
        self.image_label_bot = Label(master=self.canvas, image=self.display_photo_image_bot, borderwidth=0)
        self.image_label_bot.pack(side='right', fill='both', expand='yes')
        # self.image_label_bot.place(x=20, y=810, anchor='nw')

        # Strip on the left
        # left_strip_raw = Image.open('images/black-strip.png', 'r')
        # self.left_strip_photo = ImageTk.PhotoImage(left_strip_raw)
        # self.left_strip_label = Label(master=self.canvas, image=self.left_strip_photo, borderwidth=0)
        # self.left_strip_label.place(relx=0.0, y=0, anchor='nw')

        # Marker
        # marker_raw = Image.open('images/marker2.png', 'r')
        # self.marker_photo = ImageTk.PhotoImage(marker_raw)
        # self.marker_label = Label(master=self.canvas, image=self.marker_photo, borderwidth=0)
        # self.marker_label.place(x=0.0, y=0.0)

        # Hike labels
        self.label_hike = Label(self.canvas, text='Hike: ')
        self.label_index = Label(self.canvas, text='Index: ')
        self.label_alt = Label(self.canvas, text='Altitude: ')
        self.label_date = Label(self.canvas, text='Date: ')
        self.label_hikesz = Label(self.canvas, text='1500')

        self.label_hike.place(relx=1.0, y=0, anchor='ne')
        self.label_index.place(relx=1.0, y=22, anchor='ne')
        self.label_alt.place(relx=1.0, y=44, anchor='ne')
        self.label_date.place(relx=1.0, y=66, anchor='ne')
        self.label_hikesz.place(relx=0.0, rely=1.0, anchor='sw')

        self.tick = self.canvas.create_rectangle(0, 0, 20, 5, outline="#fff", width=0, fill="#fff", tags=('tick'))
        self.canvas.tag_raise(self.tick)

        self.update_text()
        self.update_tick()

        # Start continual fading function, will loop for life of the class
        root.after(0, func=self.fade_image)
        # root.after(self.TRANSITION_DELAY, func=self.auto_increment_slideshow)

    def _build_next_raw_images(self, next_picture: Picture):
        # print('build images')
        self.next_raw_top = Image.open(self._build_filename(next_picture.camera1), 'r')
        self.next_raw_mid = Image.open(self._build_filename(next_picture.camera2), 'r')
        # self.next_raw_bot = Image.open(blank_path, 'r')

    def _build_filename(self, end_of_path: str) -> str:
        return '{p}{e}'.format(p=PATH, e=end_of_path)

    # Loops for the life of the program, fading between the current image and the NEXT image
    def fade_image(self):
        # print('Fading the image at alpha of: ', self.alpha)
        # print(time.time())
        if self.alpha < 1.0:
            # Top image
            self.current_raw_top = Image.blend(self.current_raw_top, self.next_raw_top, self.alpha)
            # self.current_raw_top = self.next_raw_top
            self.display_photo_image_top = ImageTk.PhotoImage(self.current_raw_top)
            self.image_label_top.configure(image=self.display_photo_image_top)

            # Middle image
            self.current_raw_mid = Image.blend(self.current_raw_mid, self.next_raw_mid, self.alpha)
            # self.current_raw_mid = self.next_raw_mid
            self.display_photo_image_mid = ImageTk.PhotoImage(self.current_raw_mid)
            self.image_label_mid.configure(image=self.display_photo_image_mid)

            # Bottom image
            self.current_raw_bot = Image.blend(self.current_raw_bot, self.next_raw_bot, self.alpha)
            # self.current_raw_bot = self.next_raw_bot
            self.display_photo_image_bot = ImageTk.PhotoImage(self.current_raw_bot)
            self.image_label_bot.configure(image=self.display_photo_image_bot)

            self.alpha = self.alpha + 0.0417
            # self.alpha = self.alpha + 0.0209
        root.after(83, self.fade_image)

    def update_text(self):
        hike = 'Hike {n}'.format(n=self.picture.hike_id)

        hike_sz = self.sql_controller.get_size_of_hike(self.picture)
        index = '{x} / {n}'.format(x=self.picture.index_in_hike, n=hike_sz)

        altitude = '{a}m'.format(a=self.picture.altitude)

        value = datetime.datetime.fromtimestamp(self.picture.time)
        date_time = value.strftime('%-I:%M:%S%p on %d %b, %Y')
        date = '{d}'.format(d=date_time)

        self.label_hike.configure(text=hike)
        self.label_index.configure(text=index)
        self.label_alt.configure(text=altitude)
        self.label_date.configure(text=date)
        self.label_hikesz.configure(text=hike_sz)

    def update_tick(self):
        hike_sz = self.sql_controller.get_size_of_hike(self.picture)
        y = (self.picture.index_in_hike / hike_sz) * 1280
        print(y)

                            # object, x1, y1, x2, y2
        self.canvas.coords(self.tick, 0, y, 30, y+8)
        # self.marker_label.place_configure(x=0.0, y=y)

        # self.canvas.itemconfig(self.tick, fill='red')
        # self.canvas.move('tick', 0, y)
        # self.tick.coords(0, 0, 100, 100)

    def auto_increment_slideshow(self):
        # print('Auto incremented slideshow')
        if self.IS_TRANSITION_FORWARD:
            self.picture = self.sql_controller.next_altitude_picture_across_hikes(self.picture)
            # self.picture.print_obj()
            self._build_next_raw_images(self.picture)
            self.alpha = .2
        else:
            self.picture = self.sql_controller.previous_altitude_picture_across_hikes(self.picture)
            # self.picture.print_obj()
            self._build_next_raw_images(self.picture)
            self.alpha = .2

        root.after(self.TRANSITION_DELAY, self.auto_increment_slideshow)

    # KEYBOARD KEYS
    def rightKey(self, event):
        # print('increment the count')
        self.IS_TRANSITION_FORWARD = True
        # self.picture = self.sql_controller.next_altitude_picture_across_hikes(self.picture)
        self.picture = self.sql_controller.next_time_picture_in_hike(self.picture)
        # self.picture.print_obj()
        self._build_next_raw_images(self.picture)
        self.alpha = .2     # Resets amount of fade between pictures
        self.update_text()
        self.update_tick()

    def leftKey(self, event):
        # print("decrement the count")
        self.IS_TRANSITION_FORWARD = False
        # self.picture = self.sql_controller.previous_altitude_picture_across_hikes(self.picture)
        self.picture = self.sql_controller.previous_time_picture_in_hike(self.picture)
        # self.picture.print_obj()
        self._build_next_raw_images(self.picture)
        self.alpha = .2     # Resets amount of fade between pictures
        self.update_text()
        self.update_tick()

    def space_key(self, event):
        print('space key pressed')

    # HARDWARE CONTROLS
    def detected_rotary_change(self, event):
        clkState = GPIO.input(clk)
        cntState = GPIO.input(cnt)
        if clkState != self.clkLastState:
            # Increment
            if cntState != clkState:
                if (self.is_across_hikes):
                    print('INCREMENT ACROSS ALL HIKES')
                    self.picture = self.sql_controller.next_time_picture_across_hikes(self.picture)
                else:
                    self.ROTARY_COUNT += 1
                    print("Rotary +: ", self.ROTARY_COUNT)

                    self.IS_TRANSITION_FORWARD = True   # For auto slideshow
                    self.picture = self.sql_controller.next_time_picture_in_hike(self.picture)
                    # self.picture.print_obj()
                    self._build_next_raw_images(self.picture)
                    self.alpha = .2     # Resets amount of fade between pictures
                    # self.update_text()
                    # self.update_tick()
            # Decrement
            else:
                if (self.is_across_hikes):
                    print('DECREMENT ACROSS ALL HIKES')
                    self.picture = self.sql_controller.next_time_picture_across_hikes(self.picture)
                else:
                    self.ROTARY_COUNT -= 1
                    print("Rotary -: ", self.ROTARY_COUNT)

                    self.IS_TRANSITION_FORWARD = False  # For auto slideshow
                    self.picture = self.sql_controller.previous_time_picture_in_hike(self.picture)
                    # self.picture.print_obj()
                    self._build_next_raw_images(self.picture)
                    self.alpha = .2     # Resets amount of fade between pictures
                    # self.update_text()
                    # self.update_tick()
        self.clkLastState = clkState
        # sleep(0.005)

    def rotary_button_pressed(self, event):
        print('rotary pressed')
        self.is_across_hikes = not self.is_across_hikes
        sleep(0.1)


# Create the root window
root = Tk()

root.attributes("-fullscreen", False)
root.bind("<Escape>", exit)
slide_show = Slideshow(root)
root.mainloop()
