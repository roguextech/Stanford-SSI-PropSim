import tkinter as tk
from tkinter import messagebox
from tkinter import scrolledtext 

NUM_LINES = 20

class ErrorRedirector:
    def __init__(self, master):
        self.master = master # tk root
        self.err_popup = None 
        self.stxt = None

    def stxt_init(self):
        self.err_popup = tk.Toplevel(self.master)
        self.err_popup.wm_title('Runtime Errors Encountered')
        self.err_popup.iconbitmap(default="PythonLib/ssi_logo.ico")
        self.stxt = scrolledtext.ScrolledText(master=self.err_popup, wrap='word', font = ('Courier New',11), foreground='black', background='white',relief='sunken',height=1)
        err_icon = tk.Label(self.err_popup, image = "::tk::icons::warning")
        err_icon.grid(row=0,column=0,sticky='nsew')
        self.stxt.grid(row=0,column=1,sticky='nsew')
        self.err_popup.columnconfigure(0,weight=1)
        self.err_popup.columnconfigure(1,weight=3)
        self.err_popup.rowconfigure(0,weight=1)
        self.write("Runtime Errors - Please contact PropSim support if problems persist.\n")
        self.err_popup.protocol("WM_DELETE_WINDOW", self.on_close)


    def check_range(self):
        if float(self.stxt.index("end-1c")) == NUM_LINES+2:
            self.stxt.delete("1.0", "1.end + 1 char")
    
    def write(self, msg):
        if self.err_popup == None:
            self.stxt_init()
            self.master.bell()
        err_msg = "{0}".format(msg)

        self.stxt['state'] = 'normal'
        self.stxt.insert(tk.END, err_msg)
        self.stxt.see(tk.END)
        self.check_range()
        self.stxt['state'] = 'disabled'

    def on_close(self):
        self.err_popup.destroy()
        self.err_popup = None # reset so that pre-write check catches the need to re-build the window
    
    def flush(self):
        pass

    def __enter__(self):
        return self

    def __exit__(self, *args):
        pass