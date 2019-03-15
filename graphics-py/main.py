#!/usr/bin/env python3

from graphics import *

# DEFINE
WIDTH       = 1280
HEIGHT      = 720

def main():
        win = GraphWin("Capra", WIDTH, HEIGHT, autoflush=True)

        for i in range(1000):
                c = Circle(Point(i, 50), 10)
                c.draw(win)
                update(30)
                
        # win.plot(50, 50, "red")
        # win.setBackground('gray')
        # 
        # inputBox = Entry(Point(3,4), 100)
        #  
        # clickPoint = win.checkMouse()
        # print(clickPoint)
        # 
        # keyString = win.getKey()
        # print(keyStrings)
        # 
        # win.getMouse() # pause for click in window
        # win.close()
    
if __name__ == '__main__': main()