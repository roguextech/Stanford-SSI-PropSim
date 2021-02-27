'''
    Section:

    A section is a sub-group on a SimPage, and has:

    - name : the name of the section (placed at the top of the frame)
    - inputvars : a list of InputVar objects, in the order they should be placed in the section

    methods:

    - build(matlabeng) : builds all InputVars using their build() func
    - validate() : returns a list of error messages encountered while calling every InputVar's validate() function
    - makewidget(parent) : initializes the Tk widget for the section, adding all InputVar objects in order
'''
import tkinter as tk
import tkinter.ttk as ttk

from .ToggleVar import ToggleVar

class Section(ttk.Frame):
    def __init__(self, name, inputvars):
        self.name = name
        self.inputvars = inputvars

    def build(self, matlabeng):
        ''' Build all inputvars in the MATLAB workspace. '''
        for var in self.inputvars:
            var.build(matlabeng)
    
    def validate(self):
        ''' Compile error codes from the validation of the constituent InputVars. '''
        err_list = []
        for var in self.inputvars:
            val = var.validate()
            if isinstance(val, str): # if received an error
                err_list.append( val )
        return err_list

    def makewidget(self, parent):
        ''' Make tk widgets of input vars, and construct the section. '''
        super().__init__(parent) # initialize self as ttk.Frame
        sec_lab = ttk.Label(self, text = self.name, style = 'SectionHeader.TLabel')
        sec_lab.grid(row = 0, column = 0, sticky = 'nsew')
        i = 1
        for var in self.inputvars:
            subframe = ttk.Frame(self, borderwidth=5, relief = 'groove')
            subframe.grid(row=i,column=0,sticky='nsew',padx=(40,10),pady=(0,0))
            var.makewidget(subframe) # initialize the widget of this inputvar, using the section frame as the parent
            lab = ttk.Label(subframe, text = var.name+': \t')
            lab.grid(row = 0, column = 0, sticky = 'nsew')
            var.maketooltip(lab) # connect a tooltip to the label to the left of the inputvar
            var.widget.grid(row = 0, column = 1, sticky = 'nsew')
            subframe.columnconfigure(0,weight=1)
            subframe.rowconfigure(0,weight=1)
            i = i + 1
        for var in self.inputvars:
            if isinstance(var, ToggleVar):
                var.toggle_linkedvars() # make sure that if a section is disabled by default, its widgets are disabled
        self.rowconfigure(i-1,weight=1)
        self.columnconfigure(0,weight=1)
        
        