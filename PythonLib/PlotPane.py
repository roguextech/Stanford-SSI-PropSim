'''
    PlotPane:

    This pane is a ttk.Notebook with a matplotlib plot on each page. SimPages plot() function is passed this object,
    and can add tabs to the notebook to make additional figures.
'''

## TODO: 
# Add ability to adjust title (x-axis is time, sec, y-axis is units of data selected)
# Beneath each plot is a checkbutton menu; if nothing is selected, all resultvars and array-type members of ans struct are available for plotting
# and when extended, users can hover over the name of the variable to see a ToolTip description of that variable.
#
# Need to add a function that keeps checking for more additions to the ans struct, in case added by the user

# Tie all menu options' checkboxes to the same function, which increments the number of variables plotted. Take special action on  

import tkinter as tk
import tkinter.ttk as ttk
import numpy as np
import matplotlib.figure as figure
import matplotlib.style as plotstyle
import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg, NavigationToolbar2Tk
from matplotlib.backend_bases import key_press_handler
import mplcursors

from .units import units
from .ToolTip import ToolTip

class PlotPane(ttk.Notebook):
    def __init__(self, parent, matlabeng):
        super().__init__(parent)

        self.current_tab = 0
        self.figs = []
        self.canvases = []
        self.toolbars= []
        self.names = []

        ## Add a default frame that just contains a message describing what will be here eventually
        self.make_default()

    def make_default(self):
        self.add_page("Welcome")

    def set_page(self, index = 0):
        ''' Set which page to look at. '''
        self.select(index)
    
    def add_page(self, page_title):
        ''' Make a new plotting page. Returns the figure.Figure() object on that page.'''
        frame = ttk.Frame(self) # make frame to hold canvas
        self.figs.append(figure.Figure())
        self.names.append(page_title)
        self.canvases.append(FigureCanvasTkAgg(self.figs[-1], master = frame))
        self.canvases[-1].get_tk_widget().pack(expand=True, fill=tk.BOTH)
        self.toolbars.append( NavigationToolbar2Tk(self.canvases[-1], frame) )
        self.toolbars[-1].update()
        self.add(frame, text = page_title)

        return self.figs[-1]

    def draw(self, canvas_index = None):
        ''' Draw the current (or indicated) canvas. '''

        if not canvas_index:
            canvas_index = self.current_tab

        # self.canvases[canvas_index].draw()
        ax = self.figs[canvas_index].axes
        mplcursors.cursor(ax, hover=2) # set plots so that hovering over generates a pop-up annotation, but goes away when mouse leaves
        on_key_press = lambda event, canvas=self.canvases[canvas_index], tbar = self.toolbars[canvas_index]: key_press_handler(event, canvas, tbar)
        self.canvases[canvas_index].mpl_connect("key_press_event", on_key_press)
    
    def draw_all(self):
        ''' Draw all canvases. '''
        for i in self.tabs():
            i = self.index(i) # get index number
            self.draw(i)

    def gcf(self):
        ''' Return the current (or indicated) canvas. '''
        return self.figs[self.current_tab]

    def clear_fig(self, fig_index = None):
        ''' Clear the current (or indicated) figure. '''
        if fig_index:
            self.figs[fig_index].clear()
        else:
            self.figs[self.current_tab].clear()

    def clear(self):
        ''' Clear all tabs and associated plots. '''
        for i in self.tabs():
            i = self.index(i) # get index number
            plt.close(self.figs[i])
            self.canvases[i].get_tk_widget().destroy() # delete canvas associated with plot

        for item in self.winfo_children():
                item.destroy()
        self.canvases = []
        self.figs = []
        self.toolbars = []
        self.names = []

    def save_plots(self):
        return (self.canvases, self.figs, self.toolbars, self.names)

