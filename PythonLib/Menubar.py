''' 
MenuBar:

The menu bar at the top of a MainWindow. Does not own any of the functions called, just organizes
them into a pretty little cascading menu bar.
'''

import tkinter as tk

class MenuBar(tk.Menu):
    def __init__(self, mainwindow):
        super().__init__(master = mainwindow) # initialize using parent constructor, with the mainwindow as the master

        # File menu
        # --> Save : saves the workspace
        # --> Save as: saves the workspace to a user-selected filename
        # --> Load MAT File: opens a dialog to select a .MAT file to load 
        filemenu = tk.Menu(self, tearoff=0)
        filemenu.add_command(label="Save...", command = mainwindow.inputPane.save_sim)
        filemenu.add_command(label="Save as...", command = mainwindow.inputPane.saveas_sim)
        filemenu.add_command(label="Load MAT File", command = mainwindow.inputPane.load_sim)
        self.add_cascade(label="File", menu=filemenu)

        # Edit menu
        # --> Restore defaults: returns all variables to their default values
        editmenu = tk.Menu(self, tearoff=0)
        editmenu.add_command(label='Restore defaults...', command = mainwindow.inputPane.restoredefaults)
        self.add_cascade(label="Edit", menu=editmenu)
