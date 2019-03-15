#!/usr/bin/env python3

from graphics import *

# DEFINE
WIDTH       = 1280
HEIGHT      = 720

def main():
        # Start of program
        win = GraphWin("Capra", WIDTH, HEIGHT, autoflush=False)
        win.setBackground(color_rgb(255, 0, 0))
        
        # Logic of program
        pt = Point(250, 250)
        cir = Circle(pt, 50)
        cir.setFill(color_rgb(0, 0, 0))
        cir.draw(win)
        
        # End of program
        win.getMouse()
        win.close()
    
if __name__ == '__main__': main()