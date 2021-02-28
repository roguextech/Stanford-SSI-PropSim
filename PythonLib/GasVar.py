'''
    GasVar:

    An InputVar class for a Gas object (see the Matlab code for Gas.m in Supporting Files). Users select from a dropdown of defined
    gases. To add gases, they must be manually included in the gas_library dict below.

    TODO: Add more common gases!
'''

import tkinter as tk
import tkinter.ttk as ttk
from .InputVar import InputVar

# gases available in GasVar dropdown - cv is in J/kg/K, molecular mass in kg/mol
gas_library =  {'nitrogen'   :{'c_v': 743.0, 'molecular_mass':0.0280134}, 
                'helium'    :{'c_v':3.12, 'molecular_mass': 0.0040026}
                }

class GasVar(InputVar):
    def __init__(self, name, defaultval, baseunit='gas', structname = None, description = ''):
        super().__init__(name, defaultval, baseunit, structname, description) # use parent constructor
    
    def get(self):
        ''' Accesses the current value of self.var and returns it. '''
        return self.var.get()

    def put(self, val):
        ''' Set current value of self.var. '''

        if isinstance(val, dict): # if setting using a Gas object dict
            for gas_name in gas_library.keys():
                if val == gas_library[gas_name]:
                    val = gas_name
                    break
            if val not in gas_library and 'c_v' in val and 'molecular_mass' in val: # if failed to find an existing gas, create new one!
                gas_library['loaded_gas'] = val
                val = 'loaded_gas'

        #self.widget['menu'].configure(state = 'normal')
        self.var.set(val)

    def get_type(self):
        ''' Return the base type of this input var. '''
        return self.baseunit

    def build(self, matlabeng):
        ''' Build this variable in the MATLAB engine's workspace. '''
        ''' NOTE: This assumes that a Pressurant object has already been created and assigned to the struct name. '''
        mygas = self.get() # get the name of the gas from the gas library to be used
        matlabeng.eval(self.name+' = Gas();' ,nargout=0) # create gas object
        matlabeng.eval(self.name+'.c_v = ' + str(gas_library[mygas]['c_v']) + ' ;', nargout=0)
        matlabeng.eval(self.name+'.molecular_mass = ' + str(gas_library[mygas]['molecular_mass']) + ' ;', nargout=0)
        matlabeng.eval(self.structname+'.gas_properties = '+self.name+' ;', nargout=0)

    def makewidget(self, parent):
        ''' Create the tk widget for this input, using parent as the parent widget. '''
        self.var = tk.StringVar(parent, self.defaultval) # a Tk variable storing current status of this variable (0/False is off, 1/True is on)
        self.widget = ttk.OptionMenu(parent, self.var, self.defaultval, *(gas_library.keys())) # create dropdown of gas names        

    def validate(self):
        ''' Determine if the selection is valid. '''
        if self.get() in gas_library.keys(): # should always be true, as the user has selected from a dropdown
            return True
        else:
            return "You have selected an invalid gas for " + self.name