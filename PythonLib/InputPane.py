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

        self.curr_tab = None # index of current tab, None initially to prevent prompting for save on startup

        for page in simpages:
            page.makewidget(self, self.matlabeng) # create each SimPage with self as the parent
            self.add(page, text = page.name) # create a tab for this frame, with name as the tab name

        self.bind("<<NotebookTabChanged>>", lambda event: self.ontabchange() )

    def promptsave_sim(self):
        if (not self.simpages[self.curr_tab].saved) and (self.simpages[self.curr_tab].ans != None): # if an answer associated with the current SimPage exists and hasn't been saved
            return self.simpages[self.curr_tab].promptforsave()
        else:
            return True # if solution has already been saved or doesn't exist, don't bother prompting

    def save_sim(self):
        self.simpages[self.curr_tab].saveworkspace()

    def saveas_sim(self):
        self.simpages[self.curr_tab].saveworkspaceas()

    def restoredefaults(self):
        self.simpages[self.curr_tab].restoredefaults() 

    def get_simpage(self):
        return self.simpages[self.curr_tab]
    
    def set_simpage(self, new_tab):
        self.select(new_tab)

    def enable_tabs(self):
        for i in range(len(self.simpages)):
            if i is not self.curr_tab:
                self.tab(i, state = 'normal')

    def disable_tabs(self):
        for i in range(len(self.simpages)):
            if i is not self.curr_tab:
                self.tab(i, state = 'disabled')

    def ontabchange(self):
        if self.curr_tab is None:
            self.curr_tab = self.index(self.select())
            return
        if self.promptsave_sim(): # prompt for SimPage save on the tab you're switching from
            self.curr_tab = self.index(self.select()) # if saved or rejected option, set new tab
            #self.mainwindow.update_plot(self.simpages[self.curr_tab].resultvars) # update plotPane
        else:
            hold = self.curr_tab
            self.curr_tab = None # prevent this tabchange function from being triggered again
            self.select(hold) # if canceled or closed window, go back to previous tab
