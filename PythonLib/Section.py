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
from .GasVar import GasVar

class Section(ttk.Frame):
    def __init__(self, name, inputvars):
        self.name = name
        self.inputvars = inputvars
        self.modified = True # tracks whether inputvars in this section have been modified since last build (initialy true, since no build has occured)

    def build(self, matlabeng):
        ''' Build all inputvars in the MATLAB workspace. '''
        for var in self.inputvars:
            var.build(matlabeng)
        self.modified = False # haven't been modified since last build!
    
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
        for inputvar in self.inputvars:
            subframe = ttk.Frame(self, borderwidth=5, relief = 'groove')
            subframe.grid(row=i,column=0,sticky='nsew',padx=(40,10),pady=(0,0))
            inputvar.makewidget(subframe) # initialize the widget of this inputvar, using the section frame as the parent
            lab = ttk.Label(subframe, text = inputvar.name+': \t')
            lab.grid(row = 0, column = 0, sticky = 'nsew')
            inputvar.maketooltip(lab) # connect a tooltip to the label to the left of the inputvar
            inputvar.var.trace_add("write", lambda *a: self.make_modified()) # connect changes to the state of this variable to the make_modified function
            inputvar.widget.grid(row = 0, column = 1, sticky = 'nsew')
            subframe.columnconfigure(0,weight=1)
            subframe.rowconfigure(0,weight=1)
            i = i + 1
        for inputvar in self.inputvars:
            if isinstance(inputvar, ToggleVar):
                inputvar.toggle_linkedvars() # make sure that if a section is disabled by default, its widgets are disabled
        self.rowconfigure(i-1,weight=1)
        self.columnconfigure(0,weight=1)

    def load_from_workspace(self, matlabeng):
        ''' Load all inputvar values from MATLAB workspace. '''
        matlabeng.eval("warning('off','all');", nargout=0)
        for inputvar in self.inputvars:
            try:
                matlabeng.eval('temp = ' + inputvar.structname + '.' + inputvar.name + ';', nargout=0)
                if isinstance(inputvar, GasVar): # if a Gas object, have to convert to struct first!
                    matlabeng.eval('temp= struct(temp);', nargout=0)
                inputvar.put(matlabeng.workspace['temp'])
            except:
                print("Failed to load input " + inputvar.structname + '.'+ inputvar.name + " from MATLAB workspace.")
        matlabeng.eval("warning('on','all');",nargout=0)
        matlabeng.clear('temp', nargout=0)



    def restoredefaults(self):
        ''' Restore every inputvar in section to its default value. '''
        for var in self.inputvars:
            var.put(var.default) # set all vars to their default value
        
    def make_modified(self):
        self.modified = True # if an inputvar is modified, switch to True
        