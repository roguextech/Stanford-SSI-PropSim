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

class PrintRedirector(StringIO):
    def __init__(self, master):
        super().__init__()
        self.widget = stxt.ScrolledText(master=master, wrap='word', font = ('TkDefaultFont', 9), foreground='white', background='black',relief='sunken',height=1)

    def check_range(self):
        if float(self.widget.index("end-1c")) == NUM_LINES+2:
            self.widget.delete("1.0", "1.end + 1 char")

    def write(self, msg):
            msg += self.getvalue()
            self.widget['state'] = 'normal'
            self.widget.insert(tk.END, msg)
            self.widget.see(tk.END)
            self.check_range()
            self.widget['state'] = 'disabled'
    
    def flush(self):
        pass

    def __enter__(self):
        return self

    def __exit__(self, *args):
        pass
