'''
    TXTVar:

    An InputVar class for a .txt file selection. Consists of a text entry and a "browse" button that allows users to select a file from 
    the file explorer.
'''

import tkinter as tk
import tkinter.ttk as ttk
import tkinter.filedialog as dialog
import os.path

from .InputVar import InputVar


class TXTVar(InputVar):
    def __init__(self, name, defaultval, baseunit='file', structname = None, description = ''):
        super().__init__(name, defaultval, baseunit, structname) # use parent constructor
        self.fullfile = defaultval # stores the full filepath, whereas just the .MAT filename is stored in the Entry

        self.browsebutton = None # Browse button, initialized on makewidget
        self.filetext = None # Read-only entry, initialized on makewidget

    def get(self):
        ''' Accesses self.fullfile and returns. '''
        return self.fullfile # we want to return the full filepath, not just the file name

    def put(self, val):
        ''' Set current value of self.var and self.fullfile. '''
        self.var.set(val.split('/')[-1])
        self.fullfile = val

    def get_type(self):
        ''' Return the base type of this input var. '''
        return self.baseunit

    def build(self, matlabeng):
        ''' Build this variable in the MATLAB engine's workspace. '''
        myval = self.get() # get full filename
        if self.structname:
            matlabeng.eval(self.structname + '.' + self.name + " = '" + myval + "' ;", nargout = 0) # use eval to make struct variable in MATLAB workspace
        else:
            matlabeng.eval(self.name + " = '" + myval + "' ;", nargout = 0)

    def makewidget(self, parent):
        ''' Create the tk widget for this input, using parent as the parent widget. '''
        self.var = tk.StringVar(parent, self.defaultval.split('/')[-1]) # a Tk variable storing current status of this  (just the filename, not full filepath)
        self.widget = ttk.Frame(parent)
        self.browsebutton = ttk.Button(self.widget, text = "Browse", command = self.onbrowse )
        self.browsebutton.grid(row = 0, column= 1, sticky='nsew')
        self.filetext = ttk.Entry(self.widget, textvariable=self.var, state = 'readonly', width = 30)
        self.filetext.grid(row = 0, column= 0, sticky='nsew')
        self.widget.rowconfigure(0, weight=1)
        self.widget.columnconfigure(0, weight=1)

    def validate(self):
        ''' Validate the filepath to ensure it exists. '''
        if 'disabled' in self.browsebutton.state():
            return True #if disabled, don't need to do it
        if os.path.isfile(self.fullfile):
            return True # if exists, obviously is valid
        try:
            testopen = open(self.fullfile, 'w+') # if file exists, tries to append (doesnt delete contents), otherwise makes new file
            testopen.close() # close file
            os.remove(self.fullfile) # delete the file
            return True
        except:
            return "Invalid filename for " + self.name + " : " + self.get()

    def onbrowse(self):
        getfilename = dialog.asksaveasfilename(title = 'Choose ' + self.name + ' .txt file...', filetypes = [('TXT Files', '.txt'),('ENG Files', '.eng')] )
        if getfilename:
            self.put(getfilename) # set vars to this filename

