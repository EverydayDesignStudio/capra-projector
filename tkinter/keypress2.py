#!/usr/bin/env python3 

from tkinter import *
import sys

main = Tk()

def leftKey(event):
    sys.stdout.flush()
    print("Left key pressed")
    sys.stdout.flush()

def rightKey(event):
    sys.stdout.flush()
    print("Right key pressed")
    sys.stdout.flush()

frame = Frame(main, width=100, height=100)
main.bind('<Left>', leftKey)
main.bind('<Right>', rightKey)
frame.pack()
main.mainloop()

main.bind('45')
main.bind('45')
main.bind('45')
main.bind('45')
main.bind('45')
main.bind('45')
main.bind('45')
main.bind('45')
main.bind('45')
main.bind('45')
main.bind('45')
main.bind('45')
main.bind('45')
main.bind('45')
main.bind('45')