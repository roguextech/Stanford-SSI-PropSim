'''
    MainWindow:

    The primary owning window of the application - inherits the tk.Tk object.

    The MainWindow also owns a MATLABengine object from MATLAB's Python API.
'''

import tkinter as tk
import tkinter.ttk as ttk
import sys
import matlab.engine

# fun ideas:
# - have a table that allows you to select which result variables are plotted on which plot name 
#       - the units have to be compatible; every time a column's base unit is changed, validate that all checked boxes have compatible units
#       - disable checkboxes for variables that have a incompatible units
# - let users add columns to that plot, adding a new plot (all plot names are entries)
# - also allow for unit conversions on this page; under plot name, include a display unit dropdown in addition to the base unit
# - put save button at bottom
#
# - load a .mat file to fill the boxes and plots (would it be possible to also save the ouput to a long MATLAB string in that workspace?)
# - split out the "output on" shit in Performance code to allow users of this function to determine whether they want to output RasAero data

# Items that a function's page has:
# Function name: a string corresponding to the name of the MATLAB function to be run (normally PerformanceCode or DesignLiquid)
# Function: an anonymous function that is called on Run (includes the passed arguments and all)
# build(): a build(matlabeng) function that uses the matlab engine of the main window to actually create the Function
# Sections - The page is broken up by section. The section has a name and is either toggleable (Can gray out the section); the sections come in a dictionary,with section name keys yielding a list of input vars (in order) for that section
# Input Variables: each has a name, a struct name, an associated section, an associated value (set to default), a base unit (or if not unit, "boolean" or "gas"), and a status (enabled or disabled)
#                       - consider also adding a validation function, to allow values to be restricted to ranges or something
#                       - struct name is included to condense arguments passed to MATLAB
#                       - need to figure out how to build a struct from Python into a MATLAB workspace (best case - convert python dict to MATLAB struct)
# Plot names: name of plots added after running, with their base unit
# Result struct name: the name of the struct into which all results are output
# Results: each has a name, unit, value, and an associated plot name(s) (None if not plotted); by default, all are assumed to belong to the 'ans' struct

# Basic function:
# - On start-up, user selects which function they want to run by clicking on the desired tab at the top of the page
#       - bind tab change so that it also switches which variables we're accessing
# - User can hover over entry labels to see descriptions of what that variable is, the unit, etc.
#       - if users input <some-value> [<unit>], the value will be converted to the appropriate unit
#       - if users input <some-value>, the value will be assumed to be in the variable's base unit
# - User presses Run at bottom of LHS
# - On Run, all entry inputs are validated for unit and using the variables validation function. If unsuccessful, prints an error message and turns that entry red (entries should return to normal color on entry).
# - After successful validation, a "CreateMatlabWorkspace" function is called, which runs through all the input variables, adding them to a Matlab workspace
# - Once the workspace has been created, the Function's associated anonymous function is run
# - After a run returns, plots are updated based on the result struct


from .InputPane import InputPane
# from .OutputPane import OutputPane
# from .PlotPane import PlotPane
from .PrintRedirector import PrintRedirector
from .Menubar import MenuBar

# IMPORT SIMPAGES and then add them to the simPages list to have them show up on the application
from .SimulateLiquidPage import SimulateLiquid
simPages = [SimulateLiquid]
#simPages = [SimulateLiquidPage, SimulateHybridPage, DesignLiquidPage]

## TODO: 
#   - Allow users to modify the "options" struct to change the integration time and time step

class MainWindow(tk.Tk):
    def __init__(self):
        super().__init__() #use inherited constructor for tk.Tk

        # Build the primary frame that contains all other items.
        self.mainframe = ttk.PanedWindow(self, orient = 'horizontal')
        self.mainframe.pack(fill=tk.BOTH, expand=1) 
        self.state('zoomed')
        self.title('PropSim - Stanford Student Space Initiative')

        # Create the matlab engine
        self.eng = matlab.engine.start_matlab()
        self.eng.addpath(self.eng.fullfile(self.eng.pwd(), 'Supporting Functions')) # add MATLAB library

        # Create styles
        self.style = ttk.Style()
        self.style.configure('EntryVal.TEntry',font=('TkDefaultFont', 8), fg = 'black', bg = 'white')
        self.style.map('EntryVal.TEntry', background = [('!invalid','white'),('invalid', '#f59a9a' )])
        self.style.configure('SectionHeader.TLabel', font = ('TkDefaultFont', 10,'bold'))

        # Bind close event to stop animation updating if the window is closed
        self.bind("<Destroy>", lambda event: self.close())

        # Create Constituent Widgets
        self.inputPane = InputPane(self.mainframe, self, self.eng, simPages)
        self.rightPane = tk.PanedWindow(self, orient = 'vertical')
        self.printRedirector = PrintRedirector(self)
        self.rightPane.add(self.printRedirector.widget)
        self.menubar = MenuBar(self)

        # Pack Constituent Widgets
        self.config(menu = self.menubar) # set menubar
        self.mainframe.add(self.inputPane)
        self.mainframe.add(self.rightPane)

    def close(self):
        #self.inputPane.promptsave_sim() # prompt for save before closing window
        pass

    def run(self):
        ''' Starts the application loop, including the error logger and print redirector. '''
        old_stdout = sys.stdout
        old_stderr = sys.stderr
        # error_logger = ErrorLogger(self, old_stderr, ERROR_LOG)
        #with error_logger as sys.stderr:
        with self.printRedirector as sys.stdout:
            self.mainloop() # start GUI application running, on close will call kill() function above
        sys.stdout = old_stdout
        sys.stderr = old_stderr