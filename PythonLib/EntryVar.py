'''
    EntryVar:

    An InputVar class for a string-input value. Implements conversions to baseunit from the string-parsed unit before sending to MATLAB
    (assumes that the input unit has already been validated).
'''

import tkinter as tk
import tkinter.ttk as ttk

from .InputVar import InputVar
from .units import units


class EntryVar(InputVar):
    def __init__(self, name, defaultval, baseunit, structname = None, description = ''):
        super().__init__(name, defaultval, baseunit, structname, description) # use parent constructor

        self.numeric_val = None # the numeric value parsed from the input string, set in self.parse_value
        self.parsed_unit = None # the unit parsed from the input string, set in self.parse_value

    def get(self):
        ''' Accesses the current value of self.var and returns it. '''
        return self.var.get()

    def put(self, val):
        ''' Set current value of self.var. '''
        if not isinstance(val, str):
            val = str(val)
        splitstr = val.strip('] ')
        splitstr = splitstr.split('[')
        if len(splitstr) == 1 and len(self.baseunit.split('*')) == 1: # if no unit and base unit isn't composite, convert to preferred unit from base unit
            pref_unit = units.get_preferred_unit(self.baseunit)
            if pref_unit != 'unitless': # dont bother converting between unitless values
                val = str( round( units.convert(float(splitstr[0]), self.baseunit, pref_unit), 6 ) ) + ' [' + pref_unit + ']'

        holdstate = self.widget['state']
        self.widget['state'] = 'normal'
        self.var.set(val)
        self.widget['state'] = holdstate

    def get_type(self):
        ''' Return the base type of this input var. '''
        return self.baseunit

    def build(self, matlabeng):
        ''' Build this variable in the MATLAB engine's workspace. '''
        if self.numeric_val is None:
            myval = self.defaultval.split('[')[0].strip() # if entry is disabled, plug in a default value (won't matter except for the options struct)
        else:
            myval = units.convert(self.numeric_val, self.parsed_unit, self.baseunit) # convert to baseunit
        if self.structname:
            matlabeng.eval(self.structname + '.' + self.name + '=' + str(myval) + ' ;', nargout = 0) # use eval to make struct variable in MATLAB workspace
        else:
             matlabeng.eval(self.name + '=' + str(myval) + ' ;', nargout = 0)

    def makewidget(self, parent):
        ''' Create the tk widget for this input, using parent as the parent widget. '''
        self.var = tk.StringVar(parent, self.defaultval) # a Tk variable storing current status of this variable
        self.widget = ttk.Entry(parent, style = 'EntryVar.TEntry', textvariable=self.var)#, validate='focus', validatecommand=lambda *a: 'invalid' not in self.widget.state()) 
        self.widget.bind("<FocusOut>", lambda e: self.validate())
        self.widget.bind("<FocusIn>", lambda e: self.on_entry())           

    def validate(self):
        ''' Parse the user input, separating it into a value and a unit. Set the self.numeric_val and self.parsed_unit vars based on findings. '''
        # basic string format is <value> [<unit>] or just <value>. Handle both cases:
        if 'disabled' in self.widget.state():
            return True # if entry is disabled, don't bother validating
        splitstr = self.get()
        splitstr = splitstr.strip('] ') # remove closing brace and leading/trailing whitespace
        splitstr = splitstr.split('[') # split into a list

        if len(splitstr) > 2: # protect against too many arguments before using eval()
            self.set_err()
            return "Error: Variable " + self.name + " has an unparseable input: " + self.get()
        elif len(splitstr) == 1 :
            try:
                check = float(splitstr[0]) # check if no unit that the input is numeric
            except:
                self.set_err()
                return "Error: Variable " + self.name + " has an unparseable input: " + self.get()

        try:
            parse_this = splitstr[0].strip()
            if '__' in parse_this or 'lambda' in parse_this or "=" in parse_this:
                raise TypeError
            self.numeric_val = float(eval(parse_this,{"__builtins__":None},{})) # use eval to parse input for numeric expressions, protecting against harmful input
        except:
            self.set_err()
            return "Error: Variable " + self.name + " has an unparseable value: " + self.get()
        if len(splitstr) > 1 : # if a unit was included
            if units.validate_units(splitstr[1].strip(), self.baseunit):
                self.parsed_unit = splitstr[1]
                return True
            else:
                self.set_err()
                return "Error: Variable " + self.name + " has a unit incompatible with the base unit. \n" + "\t Base unit is [" + self.baseunit + "] and compatible units are: " + ', '.join(units.get_compatible_units(self.baseunit))          
        else: 
            self.parsed_unit = self.baseunit # if no unit was provided, assume the base unit
        return True # if you got here, you're good

    def set_err(self):
        ''' Change the style to reflect that an error was found during parsing. '''
        self.widget.state(['invalid'])

    def on_entry(self):
        ''' Change the style back to the default when the user clicks in this entry. This stops error color-changes from being permanent. '''
        self.widget.state(['!invalid'])