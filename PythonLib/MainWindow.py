'''
    MainWindow:

    The primary owning window of the application - inherits the tk.Tk object.

    The MainWindow also owns a MATLABengine object from MATLAB's Python API.
'''

import tkinter as tk
import tkinter.ttk as ttk
import sys
import matlab.engine
import time

# fun ideas:
# - have a table that allows you to select which result variables are plotted on which plot name 
#       - the units have to be compatible; every time a column's base unit is changed, validate that all checked boxes have compatible units
#       - disable checkboxes for variables that have a incompatible units
# - let users add columns to that plot, adding a new plot (all plot names are entries)
# - also allow for unit conversions on this page; under plot name, include a display unit dropdown in addition to the base unit
# - put save button at bottom
#
# - load a .mat file to fill the boxes and plots (would it be possible to also save the ouput to a long MATLAB string in that workspace?)

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
# Results: each has a name, unit, and an associated plot name(s) (None if not plotted); by default, all are assumed to belong to the 'ans' struct

from .InputPane import InputPane
# from .OutputPane import OutputPane
from .PlotPane import PlotPane
from .CmdPane import CmdPane
from .PrintRedirector import PrintRedirector
from .Menubar import MenuBar

# IMPORT SIMPAGES and then add them to the simPages list to have them show up on the application
from .SimulateLiquidPage import SimulateLiquid
from .SimulateHybridPage import SimulateHybrid
from .DesignLiquidPage import DesignLiquid
simPages = [SimulateLiquid, SimulateHybrid, DesignLiquid]

# TODO: add regularly-timed background process that checks for updates to inputPane.getsimPage().ans and passes to the plot pane
# to make sure that all variables within the ans struct are always available for plotting
# - disable cmd pane if a simPage is being run (needs to pass through mainwindow)
# - add error output re-direction from MATLAB to the printRedirector

class MainWindow(tk.Tk):
    def __init__(self):
        super().__init__() #use inherited constructor for tk.Tk
        self.iconbitmap(default="PythonLib/ssi_logo.ico")

        # Build the primary frame that contains all other items.
        self.mainframe = ttk.Frame(self)
        self.mainframe.pack(fill=tk.BOTH, expand=1) 
        self.state('zoomed')
        self.title('PropSim - Stanford Student Space Initiative')

        # Create the matlab engine
        self.eng = matlab.engine.start_matlab()
        self.eng.addpath(self.eng.fullfile(self.eng.pwd(), 'Supporting Functions')) # add MATLAB library

        # Create styles
        self.style = ttk.Style()
        self.style.theme_use('clam')
        self.style.configure('EntryVar.TEntry',font=('TkDefaultFont', 10), fg = 'black', bg = 'white')
        self.style.map('EntryVar.TEntry', fieldbackground = [(['!invalid'],'white'),(['invalid'], '#f59a9a' )])
        self.style.configure('SectionHeader.TLabel', font = ('TkDefaultFont', 12,'bold'))

        # Bind close event to stop animation updating if the window is closed
        self.protocol("WM_DELETE_WINDOW", self.close)

        # Create Constituent Widgets
        self.rightPane = tk.PanedWindow(self.mainframe, orient = 'vertical')
        self.plotPane = PlotPane(self.rightPane, self.eng)
        self.printRedirector = PrintRedirector(self.mainframe)
        self.cmdPane = CmdPane(self.mainframe, self.eng)
        self.rightPane.add(self.plotPane)
        self.rightPane.add(self.printRedirector)

        self.inputPane = InputPane(self.mainframe, self, self.eng, simPages)
        self.menubar = MenuBar(self)

        # Pack Constituent Widgets
        self.config(menu = self.menubar) # set menubar
        self.inputPane.grid(row=0,column=0, rowspan=2,sticky='nsew')
        self.rightPane.grid(row=0,column=1, sticky='nsew')
        self.cmdPane.grid(row=1, column=1, sticky='nsew')
        self.mainframe.rowconfigure(0, weight = 1)
        self.mainframe.columnconfigure(1, weight = 1)

    def update_plot(self, resultvars):
        ''' Update plotPane to use most recent resultvars. '''
        self.plotPane.update_plot(resultvars)

    def close(self):
        if self.inputPane.promptsave_sim(): # prompt for save before closing window
            self.destroy()

    def run(self):
        ''' Starts the application loop, including the error logger and print redirector. '''
        old_stdout = sys.stdout
        old_stderr = sys.stderr
        # error_logger = ErrorLogger(self, old_stderr, ERROR_LOG)
        #with error_logger as sys.stderr:
        with self.printRedirector as sys.stdout:
            # Send a friendly message to get started
            print("Welcome to PropSim! This is where all print-out is directed. You can also use the command line below to interact\n"
                "with the active MATLAB session.")
            self.mainloop() # start GUI application running, on close will call kill() function above
        sys.stdout = old_stdout
        sys.stderr = old_stderr