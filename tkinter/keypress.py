#!/usr/bin/env python3

from tkinter import Tk, Entry
import sys

root = Tk()

def click(key):
    # print the key that was pressed
    sys.stdout.flush()
    print(key.char)

entry = Entry()
entry.grid()
# Bind entry to any keypress
entry.bind("<Key>", click)

root.mainloop()