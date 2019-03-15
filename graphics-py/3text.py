#!/usr/bin/env python3

from graphics import *

# DEFINE
WIDTH       = 1280
HEIGHT      = 720

def main():
    # Start of program
    win = GraphWin("Capra", WIDTH, HEIGHT, autoflush=False)
    win.setBackground(color_rgb(200, 200, 200))

    # Logic of program
    txt = Text(Point(250, 250), "Howdy folks!")
    txt.setTextColor('black')
    txt.setSize(30)
    txt.setFace('helvetica')
    txt.draw(win)

    # End of program
    win.getMouse()
    win.close()

if __name__ == '__main__': main()