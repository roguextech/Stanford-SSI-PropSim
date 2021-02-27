'''
    InputPane:

    A ttk.Notebook of SimPages, allowing the user to switch between which MATLAB function they want to use.

    If a page has a solution, users will be asked if they wish to save before switching tabs using SimPage.promptforsave() .

    This class also owns the Save and Save As methods, and directs them to the appropriate SimPage based on which is selected.
'''

import tkinter as tk
import tkinter.ttk as ttk

class InputPane(ttk.Notebook):
    def __init__(self, mainframe, mainwindow, matlabeng, simpages):
        super().__init__(mainframe)
        self.mainframe = mainframe
        self.mainwindow = mainwindow
        self.matlabeng = matlabeng
        self.simpages = simpages

        self.curr_tab = 0 # index of current tab

        for page in simpages:
            page.makewidget(self, self.matlabeng) # create each SimPage with self as the parent
            self.add(page, text = page.name) # create a tab for this frame, with name as the tab name

        #self.bind("<<NotebookTabChanged>>", lambda event: self.ontabchange() )

    def promptsave_sim(self):
        self.simpages[self.curr_tab].promptforsave(self.matlabeng)

    def save_sim(self):
        self.simpages[self.curr_tab].saveworkspace(self.matlabeng)

    def saveas_sim(self):
        self.simpages[self.curr_tab].saveworkspaceas(self.matlabeng)

    def ontabchange(self):
        if self.simpages[self.curr_tab].promptforsave(self.matlabeng): # prompt for SimPage save on the tab you're switching from
            self.curr_tab = self.index(self.select()) # if saved or rejected option, set new tab
        else:
            self.select(self.curr_tab) # if canceled or closed window, go back to previous tab
