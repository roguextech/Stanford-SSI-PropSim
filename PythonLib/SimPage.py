'''
    SimPage:

    An abstract base class for creating new pages for new MATLAB functions (a la SimulateLiquid, SimulateHybrid, DesignLiquid). Define your page as
    a derived class with no inputs of this type in a separate file. Import that file into MainWindow.py and add the object to the simPages list.

    NOTE: If you have Pressurant() objects or other MATLAB classdef objects, make sure to override the build file here and initialize those objects in the workspace
    before calling super().build()
''' 
import tkinter as tk
import tkinter.ttk as ttk
import tkinter.messagebox as msg
import tkinter.filedialog as dialog
import threading
from io import StringIO

class SimPage(ttk.Frame):
    def __init__(self, name, sections, inputstructs, plotnames, resultvars):
        ''' Constructor used by derived classes, which will have no arguments passed into their constructor. '''
        self.name = name # name of the MATLAB function that should be run, also the title of the tab
        self.inputstructs = inputstructs # in-order list of variable names passed to the matlab engine
        self.sections = sections # list of Section objects, in order they should appear on the page
        self.plotnames = plotnames # dict whose keys are names of defaults plots, with values being their base unit, i.e. {'Ox Tank Pressure':'Pa'}
        self.resultvars = resultvars # list of ResultVar objects, describing the expected output of a run

        self.simfunction = None # variable that will reference the anonymous simulation function after self.build is called

        self.savefilename = None # variable storing the savefilename for this MATLAB workspace
        self.saved = False # determines whether the solution has been saved since last run

        self.ans = None # solution associated with the most recently built workspace - None if no solution for the current workspace

        self.run_button = None # button at bottom of page that starts simulation run, initialized in makewidget()
        self.validate_button = None # button at bottom of page that validates input without running, initialized in makewidget()
        self.canvas = None # canvas for scrolling
        self.scrollbar = None # scrollbar

        self.matlabeng = None
        self.inputPane = None

    def prebuild(self, matlabeng):
        ''' Must be implemented by inheritor, even if just passes. If certain structs or variables need to
            be initialized before others, do that in this function.
        '''
        raise NotImplementedError()

    def postbuild(self, matlabeng):
        ''' Must be implemented by inheritor, even if just passes. If certain structs or variables must be 
            processed before running, do that here.
        '''
        raise NotImplementedError()

    def build(self):
        ''' Function called on "Validate & Build" button press - validates, then prompts for save if ans has been generated.
            If validation successful, calls build() function, doing inheritor-specific things, then builds all inputvars.
        '''
        if not self.validate():
            return # don't try to build if validation fails

        print('Validation successful, building MATLAB workspace...')

        if self.ans and not self.saved: # if a solution exists and hasn't been saved, prompt for saving before overwriting the associated workspace
            self.promptforsave()

        self.matlabeng.clearvars(nargout=0) # clear workspace
        self.ans = None # ans has been cleared in the workspace, no solution exists for the current workspace
        self.saved = False # the solution hasn't been saved because it doesn't exist yet
        self.prebuild(self.matlabeng) # call inheritor's version of "prebuild"

        for section in self.sections:
            section.build(self.matlabeng) # build every inputvar inside of every section

        self.postbuild(self.matlabeng) # call inheritor's version of "postbuild"
        print("Build complete. Ready to run. ")

    def validate(self):
        ''' Validates each section on the page. '''
        err_list = []
        for section in self.sections:
            err_list += section.validate() # returns a list of err messages (empty if no errors)
        if err_list:
            print("Validation failed. The following errors were encountered in the input:")
            for err in err_list:
                print(err)
            return False
        else:
            return True

    def restoredefaults(self):
        ''' Restores all inputvars on the page to their defaults. '''
        for section in self.sections:
            section.restoredefaults()

    def run(self, stdout):
        ''' Virtual function - derived classes will have this method called when the user presses Run on that page. 
            Here, the sim page should build a workspace of variables, then call their own simfunction. '''
        raise NotImplementedError() # virtual method, not implemented

    def _run(self):
        ''' Wrapper for above function to allow standard printout before running. '''
        for section in self.sections: # if any section has been modified since last build, re-build
            if section.modified:
                self.build()
                break # once you've built once, break

        print("Starting MATLAB run. Please do not switch tabs or close.", flush=True)
        print('>> ' + self.name, flush =True)
        run_thread = threading.Thread(target = self._thread_run, name='run_thread')
        run_thread.start()
    
    def _thread_run(self):
        ''' Function for running in separate thread. '''
        output = StringIO() # use a stringIO object to collect MATLAB output
        try:
            self.validate_button['state'] = 'disabled'
            self.run_button['state'] = 'disabled'
            self.inputPane.disable_tabs()
            self.run(output)
        finally:
            print(output.getvalue()) # print stringIO stuff
            print()
            output.close()
            self.validate_button['state'] = 'normal'
            self.run_button['state'] = 'normal'
            self.inputPane.enable_tabs()
        self.ans = self.matlabeng.workspace['ans'] # collect answer struct
        self.saved = False # the new answer has not been saved yet!
        print("Run complete.")

    def makewidget(self, parent, matlabeng):
        ''' Uses the ttk.Frame constructor to initialize the frame, then builds and adds each section plus the Validate and Run buttons. '''
        self.matlabeng = matlabeng
        self.inputPane = parent
        super().__init__(parent) # use super constructor
        # create a vertical scrollbar
        vscrollbar = tk.Scrollbar(self, orient = tk.VERTICAL)
        vscrollbar.grid(row = 0, column = 3, sticky ='nsew')

         #Create a canvas object and associate the scrollbars with it
        self.canvas = tk.Canvas(self, bd = 0, highlightthickness = 0, yscrollcommand = vscrollbar.set, bg = 'black')
        self.canvas.grid(row = 0, column = 0, columnspan=3, sticky = 'nsew')
        self.rowconfigure(0,weight = 1)
        self.columnconfigure(0, weight=1)

        #Associate scrollbars with canvas view
        vscrollbar.config(command = self.canvas.yview)

        # set the view to 0,0 at initialization
        self.canvas.yview_moveto(0)

        # create an interior frame to be created inside the canvas
        self.interior = interior = ttk.Frame(self.canvas)
        interior_id = self.canvas.create_window(0, 0, window=interior,anchor=tk.NW)
        self.canvas.rowconfigure(0,weight=1)
        self.canvas.columnconfigure(0, weight=1)

        # track changes to the canvas and frame width and sync them,
        # also updating the scrollbar

        def _configure_interior(event):
            # update the scrollbars to match the size of the inner frame
            size = (interior.winfo_reqwidth(), interior.winfo_reqheight())
            self.canvas.config(scrollregion='0 0 %s %s' % size)
            if interior.winfo_reqwidth() != self.canvas.winfo_width():
                # update the canvas's width to fit the inner frame
                self.canvas.config(width = interior.winfo_reqwidth())
        self.canvas.bind('<Configure>', _configure_interior)

        def _on_mousewheel(event):
            self.canvas.yview_scroll(int(-1*(event.delta/120)), "units")
        def _on_enter(event):
            self.canvas.bind_all("<MouseWheel>", _on_mousewheel)  
        def _on_exit(event):
            self.canvas.unbind_all("<MouseWheel>")

        self.canvas.bind("<Enter>", _on_enter)
        self.canvas.bind("<Leave>", _on_exit)

        i = 0
        for section in self.sections:
            section.makewidget(interior) # build each section's frame widget (and constituent children)
            section.grid(row = i, column = 0, columnspan = 6, sticky = 'nsew') # grid into SimPage
            i += 1 
        self.run_button = ttk.Button(self, text = 'Run', command = self._run )
        self.validate_button = ttk.Button(self, text = 'Validate & Build Workspace', command = self.build )
        self.run_button.grid(row = 1, column = 2, sticky='nsew')
        self.validate_button.grid(row=1, column = 1, sticky = 'nsew')
        self.columnconfigure(0, weight = 1)
        interior.columnconfigure(0, weight=1)

        _configure_interior(0)

    def promptforsave(self):
        ''' Prompt the user to save the file. If a savefilename has previously been selected, saves to that filename. 
            If the user cancels or exits the window, returns False. Otherwise returns True. '''
        response = msg.askyesnocancel('Save Workspace?', 'You have a solved solution that has not been saved.\n The MATLAB workspace associated with this file will be overwritten. Would you like to save?')
        if response is not None:
            if response:
                if self.saveworkspaceas():
                    return True
                else:
                    return False # user canceled in save as
            return True
        else:
            return False #if cancelled, don't close
        return True 
    
    def saveworkspace(self):
        ''' Saves the workspace to savefilename - if hasn't been defined yet, prompts user to select a file. '''
        if self.savefilename:
            self.matlabeng.save(self.savefilename, nargout = 0)
            self.saved = True
        else:
            self.saveworkspaceas() # don't have a filename - do a save as!

    def saveworkspaceas(self):
        ''' Prompts the user for a filename before saving. Returns False if user cancels, True otherwise. '''
        if not self.savefilename:
            filepicked = dialog.asksaveasfilename(title='Save Simulation Workspace', initialfile = self.name + '_workspace.mat', defaultextension = '.mat', filetypes = [('.MAT files', '.mat')])
        else:
            filepicked= dialog.asksaveasfilename(title='Save Simulation Workspace', initialfile = self.savefilename, defaultextension = '.mat', filetypes = [('.MAT files', '.mat')])
        if filepicked:
            self.savefilename = filepicked
            self.saveworkspace()
        else:
            return False

        return True