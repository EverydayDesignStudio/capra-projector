#!/usr/bin/env python3
# https://python-textbok.readthedocs.io/en/1.0/Introduction_to_GUI_Programming.html

from tkinter import Tk, Label, Button, LEFT, RIGHT, StringVar

class MyFirstGUI:
    LABEL_TEXT = [
        'This is our first GUI!',
        'Actually, this is our second GUI.',
        'We made it better now you see :)',
        'by making this interactive',
        'Go on, click again'
    ]

    def __init__(self, win):
        self.window = win
        self.window.title("A simple GUI")

        self.label_index = 0
        self.label_text = StringVar()
        self.label_text.set(self.LABEL_TEXT[self.label_index])
        self.label = Label(master=win, textvariable=self.label_text)
        # self.label = Label(master=win, text="This is our first GUI!")
        self.label.bind('<Button-1>', self.cycle_label_text)
        self.label.pack()

        # Method calls do not have parenthesis
        self.greet_button = Button(master=win, text="Greet", highlightbackground='#3E4149', command=self.greet)
        self.greet_button.pack(side=LEFT)

        self.close_button = Button(master=win, text="Close", highlightbackground='#3E4149', command=self.quit)
        self.close_button.pack(side=RIGHT)

    def cycle_label_text(self, event):
        self.label_index += 1
        self.label_index %= len(self.LABEL_TEXT) #wrap around
        self.label_text.set(self.LABEL_TEXT[self.label_index])

    def greet(self):
        print("Greetings!")
    
    def quit(self):
        print("STOP!")
        self.window.quit()

# This creates the root window
root = Tk()
my_gui = MyFirstGUI(root)
root.mainloop()