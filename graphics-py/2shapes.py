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
        pt = Point(250, 250)
        cir = Circle(pt, 50)
        cir.setFill(color_rgb(0, 0, 0))
        cir.draw(win)
        
        # Point
        pt2 = Point(250, 250)
        pt2.setOutline('white')
        pt2.draw(win)
        
        # Line
        pt3 = Point(0, 0)
        pt4 = Point(WIDTH, HEIGHT)
        ln = Line(pt3, pt4)
        ln.setOutline('purple')
        ln.draw(win)
        
        # Rectangle
        rect = Rectangle(Point(500, 500), Point(700, 700))
        rect.setOutline(color_rgb(0, 255, 255))
        rect.setFill(color_rgb(0, 255, 0))
        rect.draw(win)
        
        # Circle
        cir = Circle(Point(700, 700), 50)
        cir.setOutline(color_rgb(0, 255, 255))
        cir.setFill(color_rgb(255, 255, 255))
        cir.draw(win)
        
        # Polygon
        poly = Polygon(Point(100, 40), Point(100, 100), Point(40, 100))
        poly.setFill('blue')
        poly.draw(win)
        
        # End of program
        win.getMouse()
        win.close()
    
if __name__ == '__main__': main()