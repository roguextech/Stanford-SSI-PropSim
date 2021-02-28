'''
    InputVar:

    An abstract base class containing information about an input variable. Input variables have the following properties:

    - a name, corresponding to the name of the matlab variable they modify
    - a widget, corresponding to a tK widget object created on init
    - a value, which can be retrieved using the get() function or set using put() (initially set to a user-defined default)
    - a baseunit, which is either a unit string (e.g. 'kg', 'ft', or 'psi') indicating the unit of the MATLAB var, 'boolean', 'file', or 'gas', accessed with get_type()
    - a struct name, corresponding to which struct in MATLAB this variable belongs (None or '' means the variable isn't part of a struct)

    In addition to the methods described above, InputVars should have a build(matlabeng) function that constructions that variable in the workspace 
    of the matlab engine passed as a function argument. They should also have a makewidget(parent) function that constructs a tkinter widget, using the
    passed argument as the parent widget. Finally, inheritors should have a validate() function that confirms if the user input for that value is consistent 
    (return a string describing the err if not).

    All children inherit the function make_tooltip(widget), which creates a tooltip linked to the widget passed as an argument. When users hover their mouse over
    that widget, a pop-up window appears providing a description of that InputVar.
'''
from .ToolTip import ToolTip

MAX_TOOLTIP_LINELEN = 40

class InputVar():
    def __init__(self, name, defaultval, baseunit, structname = None, description = ''):
        self.name = name
        self.defaultval = defaultval
        self.baseunit = baseunit
        self.structname = structname
        self.description = description
        self.var = None # a Tk variable storing current status of this variable
        self.widget = None # a Tk widget
        self.tooltip = None # a Tooltip object, initialized with maketooltip()

    def get(self):
        ''' Accesses the current value of self.var and returns it. '''
        raise NotImplementedError()

    def put(self, val):
        ''' Set current value of self.var. '''
        raise NotImplementedError()

    def get_type(self):
        ''' Return the base type of this input var. '''
        return self.baseunit

    def build(self, matlabeng):
        ''' Build this variable in the MATLAB engine's workspace. '''
        raise NotImplementedError()

    def makewidget(self, parent):
        ''' Create the tk widget for this input, using parent as the parent widget. '''
        raise NotImplementedError()

    def validate(self):
        ''' Confirm whether the user input is valid or not. '''
        raise NotImplementedError()

    def maketooltip(self, tip_widget):
        ''' Create a tooltip that is linked to a tip_widget. makewidget() must be called first! '''
        if self.get_type().lower() not in ('gas','boolean','file'):
            descrip_str = self.name + '       ( unit: [' + self.get_type() + '] )\n'
        else:
            descrip_str = self.name + '       ( type: ' + self.get_type() + ' )\n'
        descrip_str += '-'*len(descrip_str)+ '\n'
        split_desc = self.description.split(' ') # split description by spaces
        curr_line_len = 0
        while split_desc: # while words remain in list
            nextword = split_desc.pop(0)
            if curr_line_len + len(nextword) < MAX_TOOLTIP_LINELEN:
                descrip_str += ' ' + nextword # if room on line, add next word (with space before it)
                curr_line_len += len(nextword)
            else:
                descrip_str += '\n' # if no room on line, end line
                descrip_str += nextword # add word
                curr_line_len = len(nextword) # line is now this long

        self.tooltip = ToolTip(tip_widget, descrip_str) # use ToolTip constructor
