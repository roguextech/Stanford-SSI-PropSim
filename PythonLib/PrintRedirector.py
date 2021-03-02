'''
PrintRedirector:

A ScrolledText object (limited to display a maximum number of lines before scrolling off)
that can be used to handle print() messages instead of sending them to the terminal. 

Setting sys.stdout = PrintRedirector() will cause all print statements to be written to this object.

__enter__ and __exit__ allow this object to be called using a with... as... : framework, and ensures the logfile is closed 
when the program ends.
'''

import tkinter as tk
from tkinter import scrolledtext as stxt
from io import StringIO as StringIO

NUM_LINES = 150

class PrintRedirector(stxt.ScrolledText):
    def __init__(self, master):
        super().__init__(master=master, wrap='word', font = ('Courier New',11), foreground='black', background='white',relief='sunken',height=1)
        self['state'] = 'disabled'

    def check_range(self):
        if float(self.index("end-1c")) == NUM_LINES+2:
            self.delete("1.0", "1.end + 1 char")

    def write(self, msg):
        self['state'] = 'normal'
        if msg == 'clc' or isinstance(msg, int):
            self.delete("1.0", "end+1c") # clear on these cues
        else:
            self.insert(tk.END, msg)
            self.see(tk.END)
            self.check_range()
        self['state'] = 'disabled'
    
    def flush(self):
        print()

    def __enter__(self):
        return self

    def __exit__(self, *args):
        pass
