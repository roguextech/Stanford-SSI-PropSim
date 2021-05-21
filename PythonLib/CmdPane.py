'''
    CmdPane:

    An Entry object that handles user input and passes it straight to MATLAB, while also including it in the application printRedirector.
'''
 
import tkinter as tk
import tkinter.ttk as ttk
from io import StringIO
import threading

MAX_OLD_LINES = 10 # number of old lines to store for accessing w/ up + down arrows

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
        self.var.set('')
        self.var.trace("w",lambda *a : self.on_change())
        self.entry = tk.Entry(self.subframe, textvariable = self.var, bg = 'white', font = ('Courier New', 11), relief = 'flat')
        self.entry.bind('<Return>', lambda event: self.on_return() )
        self.entry.bind('<Up>', lambda event: self.on_up() )
        self.entry.bind('<Down>', lambda event: self.on_down() )
        lab.grid(row=0,column=0,sticky='nsew')
        self.entry.grid(row=0,column=1,sticky='nsew')
        self.subframe.rowconfigure(0,weight=1)
        self.subframe.columnconfigure(1,weight=1)

        self.line_index = 0
        self.old_lines = ['']
        self.change_flag = False # flag used to indicated whether the entry was changed by the user (False) or in code (True)

    def get(self):
        return self.var.get()

    def put(self, msg):
        self.var.set(str(msg))

    def on_return(self):
        # Process input
        myline = self.var.get()
        if len(self.old_lines) == 1 or (myline != self.old_lines[1]): # don't add a repeated item to the history
            self.old_lines[0] = myline # the "current line" is whatever was just submitted
        else:
            self.old_lines = self.old_lines[1:] # if theres a repeat, cut out the repeat
        self.old_lines = self.old_lines[0:MAX_OLD_LINES] # limit the total number of old lines
        self.old_lines.insert(0,'') # the new current line is empty
        self.change_flag = True # indicate that we're going to change Entry programatically
        self.var.set('') # clear line (also resets line counter)
        self.line_index = 0 # set line index back to zero

        # Issue command
        if myline.strip() == 'clc':
            print('clc')
            return
        print('>> '+myline) # print to GUI
        cmd_thread = threading.Thread(target = lambda: self._cmd_thread(myline.strip()), name = 'cmd_thread')
        cmd_thread.start()

    def on_up(self):
        self.line_index = min(self.line_index+1, len(self.old_lines)-1) # limit upward movement to number of stored lines
        self.change_flag = True # indicate that we're going to change Entry programatically
        self.var.set(self.old_lines[self.line_index]) # set the entry variable to whatever line we're on

    def on_down(self):
        self.line_index = max(self.line_index-1, 0) # limit downward movement 
        self.change_flag = True # indicate that we're going to change Entry programatically
        self.var.set(self.old_lines[self.line_index]) # set the entry variable to whatever line we're on

    def on_change(self):
        # When the entry is changed, the contents of the variable are now the "current line", not an old line, and are saved in old_lines[0]
        if not self.change_flag: # if the flag isn't set
            self.old_lines[0] = self.var.get() # save contents
            self.line_index = 0 # this is the line we're on (even if we're editing an old line, that is now the "current line")
        self.change_flag = False # clear flag

    def _cmd_thread(self, cmd):
        output = StringIO()
        errout = StringIO()
        try:
            self.entry.unbind("<Return>") # prevent additional commands from being sent
            self.matlabeng.eval(cmd, nargout = 0, stdout = output, stderr = errout)
        except:
            pass # errors are caught in errout, which will be output differently from runtime errors
        finally:
            errs = errout.getvalue()
            if errs != None and errs != '':
                errs = errs.split('\n') # First line is "error using eval", which we don't need to print
                errs = '\n'.join(errs[1:-1])
                print("{0}".format(errs))
            results = output.getvalue()
            if results == None or results == '':
                pass
            else:
                print(results) # print stringIO stuff
            output.close()
            self.entry.bind("<Return>", lambda event: self.on_return() ) # re-bind enter key
