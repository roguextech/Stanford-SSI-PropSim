'''
    PlotPane:

    This pane is a ttk.Notebook with a matplotlib plot on each page. When a user calls "Run", these plots are
    updated with solution data based on the plot names and ResultVars used to initialize that page.
'''

import tkinter as tk
import tkinter.ttk as ttk