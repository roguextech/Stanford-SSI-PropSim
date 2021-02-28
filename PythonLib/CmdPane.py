'''
    CmdPane:

    An Entry object that handles user input and passes it straight to MATLAB, while also including it in the application printRedirector.
'''
 
import tkinter as tk
import tkinter.ttk as ttk
from io import StringIO
import threading

class CmdPane(ttk.Frame):
    def __init__(self, parent, matlabeng):
        super().__init__(parent)
        self.subframe = tk.Frame(self, bg='white', relief = 'sunken')
        self.matlabeng = matlabeng
        matlab_lab = ttk.Label(self, text = 'MATLAB Cmd Line\t')
        matlab_lab.grid(row=0,column=0,sticky='nsew')
        self.subframe.grid(row=0,column=1,sticky='nsew')
        self.rowconfigure(0, weight=1)
        self.columnconfigure(1, weight=1)

        lab = tk.Label(self.subframe, text = '>>', bg ='white', font = ('Courier New', 11))
        self.var = tk.StringVar(self.subframe)
        self.var.set(' ')
        self.entry = tk.Entry(self.subframe, textvariable = self.var, bg = 'white', font = ('Courier New', 11), relief = 'flat')
        self.entry.bind('<Return>', lambda event: self.on_return() )
        lab.grid(row=0,column=0,sticky='nsew')
        self.entry.grid(row=0,column=1,sticky='nsew')
        self.subframe.rowconfigure(0,weight=1)
        self.subframe.columnconfigure(1,weight=1)

    def get(self):
        return self.var.get()

    def on_return(self):
        myline = self.var.get()
        self.var.set('')
        if myline.strip() == 'clc':
            print('clc')
            return
        print('>> '+myline) # print to GUI
        cmd_thread = threading.Thread(target = lambda: self._cmd_thread(myline.strip()), name = 'cmd_thread')
        cmd_thread.start()
    
    def _cmd_thread(self, cmd):
        output = StringIO()
        try:
            self.entry.unbind("<Return>") # prevent additional commands from being sent
            self.matlabeng.eval(cmd, nargout = 0, stdout = output)
        finally:
            results = output.getvalue()
            if results == None or results == '':
                pass
            else:
                print(results) # print stringIO stuff
            output.close()
            self.entry.bind("<Return>", lambda event: self.on_return() ) # re-bind enter key
