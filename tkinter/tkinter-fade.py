#!/usr/bin/env python3

from PIL import ImageTk, Image
from tkinter import Tk, Label
import time

root = Tk()
root.title('Fading')
root.geometry('1280x720')

first_raw = Image.open('hike4/1.jpg', 'r')
first = ImageTk.PhotoImage(Image.open('hike4/1.jpg', 'r'))
second_raw = Image.open('hike4/94.jpg', 'r')
second = ImageTk.PhotoImage(Image.open('hike4/94.jpg', 'r'))

new_img = ImageTk.PhotoImage(Image.open('hike4/1.jpg', 'r'))
image_label = Label(master=root, image=new_img)
image_label.pack(side='bottom', fil='both', expand='yes')

alpha = 0
while alpha < 1.0:
    # new_img = ImageTk.PhotoImage(Image.blend(first_raw, second_raw, alpha))
    alpha = alpha + 0.01
    time.sleep(0.1)
    print(alpha)
    # image_label.update()

root.mainloop()
