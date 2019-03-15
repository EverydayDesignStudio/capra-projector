#!/usr/bin/env python3
# https://python-textbok.readthedocs.io/en/1.0/Introduction_to_GUI_Programming.html

from tkinter import Tk, Label, Button, Entry, IntVar, END, W, E

class Calculator:
    def __init__(self, win):
        self.window = win
        self.window.title("Calculator")

        self.total = 0
        self.entered_number = 0

        self.total_label_text = IntVar()
        self.total_label_text.set(self.total)

        self.total_label = Label(master=self.window, textvariable=self.total_label_text)
        self.label = Label(master=self.window, text="Total:")

        vcmd = self.window.register(self.validate)
        self.entry = Entry(master=self.window, validate='key', validatecommand=(vcmd, '%P'))

        self.add_button = Button(master=self.window, text='+', highlightbackground='#333', command=lambda: self.update('add'))
        self.subtract_button = Button(master=self.window, text='-', highlightbackground='#333', command=lambda: self.update('subtract'))
        self.reset_button = Button(master=self.window, text='Reset', highlightbackground='#333', command=lambda: self.update('reset'))

        #Layout
        self.label.grid(row=0, column=0, sticky=W)
        self.total_label.grid(row=0, column=1, columnspan=2, sticky=E)
        self.entry.grid(row=1, column=0, columnspan=3, sticky=W+E)

        self.add_button.grid(row=2, column=0)
        self.subtract_button.grid(row=2, column=1)
        self.reset_button.grid(row=2, column=2, sticky=W+E)

    def validate(self, new_text):
        if not new_text: # the textfield is being cleared
            self.entered_number = 0
            return True

        try:
            self.entered_number = int(new_text)
            return True
        except ValueError:
            return False

    def update(self, method):
        if method == 'add':
            self.total += self.entered_number
        elif method == 'subtract':
            self.total -= self.entered_number
        else: # reset
            self.total = 0

        self.total_label_text.set(self.total)
        self.entry.delete(0, END)

# This creates the root window
root = Tk()
calc = Calculator(root)
root.mainloop()