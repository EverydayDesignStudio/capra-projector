#!/usr/bin/env python3

from tkinter import Tk, Label, Button

root = Tk()
b = Button(text="Click to fade away", command=root.quit)
b.pack()

def quit(self):
    self.fade_away()

def fade_away(self):
    alpha = self.parent.attributes("-alpha")
    if alpha > 0:
        alpha -= .001
        root.attributes('-alpha', alpha)
        root.after(1, self.fade_away)
    else:
        self.parent.destroy()

root = Tk()
# root.pack(fill="both", expand=True)
root.mainloop()
