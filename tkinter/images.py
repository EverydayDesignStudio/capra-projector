#!/usr/bin/env python3



# In this file, I've left the different ways I tried to use Tkinter and Pillow to display an image
# on screen. The version at the bottom actually works. Hopefully it is helfpul.



# import tkinter
# import cv2
# from PIL import Image
# from PIL import ImageTk
# # import PIL.image, PIL.ImageTk
# 
# def main():
#     window = tkinter.Tk()
#     # photo = tkinter.PhotoImage(file="sike.gif")
#     
#     # Load an image using OpenCV
#     cv_img = cv2.imread("sike.gif")
#     # Get the image dimensions (OpenCV stores image data as NumPy ndarray)
#     height, width, no_channels = cv_img.shape
#     
#     # Create a canvas that can fit the above image
#     canvas = tkinter.Canvas(window, width = width, height = height)
#     canvas.pack()
#     
#     # Use PIL (Pillow) to convert the NumPy ndarray to a PhotoImage
#     photo = PIL.ImageTk.PhotoImage(image = PIL.Image.fromarray(cv_img))
#     
#     # Add a PhotoImage to the Canvas
#     canvas.create_image(0, 0, image=photo, anchor=tkinter.NW)
#     
#     window.mainloop()
#     
# if __name__ == '__main__': main()



# import tkinter
# import cv2
# import PIL.Image, PIL.ImageTk
# 
# # Create a window
# window = tkinter.Tk()
# window.title("OpenCV and Tkinter")
# 
# # Load an image using OpenCV
# cv_img = cv2.cvtColor(cv2.imread("sike.gif"), cv2.COLOR_BGR2RGB)
# 
# # Get the image dimensions (OpenCV stores image data as NumPy ndarray)
# height, width, no_channels = cv_img.shape
# 
# # Create a canvas that can fit the above image
# canvas = tkinter.Canvas(window, width = width, height = height)
# canvas.pack()
# 
# # Use PIL (Pillow) to convert the NumPy ndarray to a PhotoImage
# photo = PIL.ImageTk.PhotoImage(image = PIL.Image.fromarray(cv_img))
# 
# # Add a PhotoImage to the Canvas
# canvas.create_image(0, 0, image=photo, anchor=tkinter.NW)
# 
# # Run the window loop
# window.mainloop()



# from tkinter import *
# 
# canvas_width = 300
# canvas_height =300
# 
# master = Tk()
# 
# canvas = Canvas(master, 
#            width=canvas_width, 
#            height=canvas_height)
# canvas.pack()
# 
# img = PhotoImage(file="4.jpg")
# canvas.create_image(20,20, anchor=NW, image=img)
# 
# mainloop()



# Shout out to the following thread for finally showing me how to do this
# https://stackoverflow.com/questions/23901168/how-do-i-insert-a-jpeg-image-into-a-python-tkinter-window
import tkinter as tk
from PIL import ImageTk, Image

def main():
    #This creates the main window of an application
    window = tk.Tk()
    window.title("Capra")
    window.geometry("1280x720")
    window.configure(background='grey')
    
    path = "4.jpg"
    
    #Creates a Tkinter-compatible photo image, which can be used everywhere Tkinter expects an image object.
    img = ImageTk.PhotoImage(Image.open(path))
    
    #The Label widget is a standard Tkinter widget used to display a text or image on the screen.
    panel = tk.Label(window, image = img)
    
    #The Pack geometry manager packs widgets in rows or columns.
    panel.pack(side = "bottom", fill = "both", expand = "yes")
    
    #Start the GUI
    window.mainloop()

if __name__ == '__main__': main()