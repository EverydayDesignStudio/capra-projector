#!/usr/bin/env python3

from graphics import *
from PIL import ImageTk

# from tkinter import *
# from PIL import ImageTk, Image

# DEFINE
WIDTH       = 1280
HEIGHT      = 720

def main():
    # Start of program
    win = GraphWin("Capra", WIDTH, HEIGHT, autoflush=False)
    win.setBackground(color_rgb(200, 200, 200))


    # Logic of program
    path = 'sike.gif'
    # path = '4.jpg'
    
    # The following works
    # img = Image(Point(120, 70), path)
    # img.draw(win)
    
    # However only GIFS are supported, not JPG, JPEG, PNG
    # img2 = Image(Point(500, 500), '4.jpg')
    # img2.draw(win)
    
    # Was trying to hack graphics.py to support other image formats
    # by wrapping it first with a ImageTk class, however the way that
    # graphic.py constructs an image is through a path
    # img = ImageTk.PhotoImage(ImageTk.Image.open(path))
    # img.draw(win)


    # End of program
    win.getMouse()
    win.close()
    
if __name__ == '__main__': main()
