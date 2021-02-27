'''
    ToggleVar:

    An InputVar class for a toggle-able (checkbutton) value. 

    The ToggleVar has two additional optional argument: linkedvars and disableon. If linkedvars is a list of InputVar items, 
    those items will be disabled whenever the ToggleVar is in the disableon state.
'''

import tkinter as tk
import tkinter.ttk as ttk
from .InputVar import InputVar

class ToggleVar(InputVar):
    def __init__(self, name, defaultval, baseunit = 'boolean', structname = None, description = '', linkedvars = None, disableon = True):
        super().__init__(name, defaultval, baseunit, structname, description) # use parent constructor
        self.linkedvars = linkedvars
        self.disableon = disableon

    def get(self):
        ''' Accesses the current value of self.var and returns it. '''
        return self.var.get()

    def put(self, val):
        ''' Set current value of self.var. '''
        self.var.set(val)

    def get_type(self):
        ''' Return the base type of this input var. '''
        return self.baseunit

    def build(self, matlabeng):
        ''' Build this variable in the MATLAB engine's workspace. '''
        myval = self.get()
        matlabeng.eval(self.structname + '.' + self.name + '=' + str(myval) + ' ;', nargout = 0) # use eval to make struct variable in MATLAB workspace

    def makewidget(self, parent):
        ''' Create the tk widget for this input, using parent as the parent widget. '''
        self.var = tk.IntVar(parent, int(self.defaultval)) # a Tk variable storing current status of this variable (0/False is off, 1/True is on)
        if self.linkedvars is None:
            self.widget = ttk.Checkbutton(parent, variable=self.var)
        else:
            self.widget = ttk.Checkbutton(parent, variable=self.var, command = self.toggle_linkedvars)

    def validate(self):
        ''' Confirm whether the user input is valid or not. ''' 
        return True # can't mess this up really, I hope

    def toggle_linkedvars(self):
        newstate = self.var.get() # get current state of button
        if newstate != self.disableon: # determine if we need to enable or disable the linked vars
            setvars = 'disabled'
        else:
            setvars = 'normal'
        for myvar in self.linkedvars: 
            self.set_childstate(setvars, myvar.widget) # set state for the widget of all linkedvars

    def set_childstate(self, state, this_widget):
        wtype = this_widget.winfo_class()
        if wtype not in ('Frame','Labelframe','TFrame','TLabelframe'): # these types have no state variable
            if wtype == 'TMenuButton':
                this_widget['menu'].configure(state=state) # TMenuButtons require accessing the menu to disable the whole thing, can't be readonly
            elif 'readonly' not in this_widget.state(): # if an entry is read-only, don't disable/enable it 
                this_widget.configure(state=state)
        else:
            for child in this_widget.winfo_children():
                self.set_childstate(state, child) # recurse on frames, which may contain sub-widgets (like in MATVar)
            