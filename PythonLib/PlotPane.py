'''
    PlotPane:

    This pane is a ttk.Notebook with a matplotlib plot on each page. When a user calls "Run", these plots are
    updated with solution data based on the plot names and ResultVars used to initialize that page.

    Two plots are available by default. Users can select up to three variables from the ResultVars to plot simulataneously.

    Users may also select a unit to which the resultvar is converted. All variables are plotted vs. time.
'''

## TODO: 
# Add ability to adjust title (x-axis is time, sec, y-axis is units of data selected)
# Beneath each plot is a checkbutton menu; if nothing is selected, all resultvars are available for plotting
# and when extended, users can hover over the name of the variable to see a ToolTip description of that variable.
#

# Tie all menu options' checkboxes to the same function, which increments the number of 

import tkinter as tk
import tkinter.ttk as ttk
import numpy as np
import matplotlib.figure as figure
import matplotlib.style as plotstyle
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg, NavigationToolbar2Tk

from .units import units
from .ToolTip import ToolTip

class PlotPane(ttk.Frame):
    def __init__(self, parent, matlabeng):
        super().__init__(parent)
        self.matlabeng = matlabeng  
        self.num_vars_plotted = 0 # initially, no vars are plotted 
        self.base_unit

        self.ans = None # current ans being plotted

    def set_title(self, new_title):
        ''' Set a new title for the figure. '''
        self.fig.set_title(new_title)
        self.fig.show()

    def update_plot(self, new_resultvars, new_ans):
        ''' Take a new answer and update plotting as possible. '''
        pass

    def on_checkbox(self, index):
        ''' Whenever a checkbox is clicked on. Check status and pass to appropriate function. '''
        pass

    def on_deselect(self, index):
        ''' If a user deselects a menubutton. '''
        pass

    def on_last_deselect(self, index):
        ''' When user deselects the last checked object in the list - clears the unit picker and disables it. '''
        pass

    def on_select(self, index):
        ''' When user makes a new selection. '''
        pass

    def on_first_selection(self, index):
        ''' If selection made is the first selection. Enables the unit picker and updates to include compatible units. ''' 
        pass