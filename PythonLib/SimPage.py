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
        self.saved = False # determines whether the solution has been saved

        self.ans = None # variable that holds the struct returned by the simfunction - if None, no solution has been run

        self.run_button = None # button at bottom of page that starts simulation run, initialized in makewidget()
        self.validate_button = None # button at bottom of page that validates input without running, initialized in makewidget()
        self.canvas = None # canvas for scrolling
        self.scrollbar = None # scrollbar

        self.matlabeng = None

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

    def build(self, matlabeng):
        ''' Function called on "Validate & Build" button press - validates, then prompts for save if ans has been generated.
            If validation successful, calls build() function, doing inheritor-specific things, then builds all inputvars.
        '''
        if not self.validate():
            return # don't try to build if validation fails

        print('Validation successful, building MATLAB workspace...')

        if self.ans: # if a solution exists, prompt for saving before overwriting the file
            self.promptforsave()

        matlabeng.clearvars(nargout=0) # clear workspace
        self.ans = None # ans has been cleared, don't keep it around
        self.prebuild(matlabeng) # call inheritor's version of "prebuild"

        for section in self.sections:
            section.build(matlabeng) # build every inputvar inside of every section

        self.postbuild(matlabeng) # call inheritor's version of "postbuild"
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


    def run(self, matlabeng):
        ''' Virtual function - derived classes will have this method called when the user presses Run on that page. 
            Here, the sim page should build a workspace of variables, then call their own simfunction. '''
        raise NotImplementedError() # virtual method, not implemented

    def _run(self, matlabeng):
        ''' Wrapper for above function to allow standard printout before running. '''
        print("Starting MATLAB run. The window may become unresponsive for a few seconds.", flush=True)
        print()
        print('>> ' + self.name)
        self.run(matlabeng)
        print("Run complete.")

    def makewidget(self, parent, matlabeng):
        ''' Uses the ttk.Frame constructor to initialize the frame, then builds and adds each section plus the Validate and Run buttons. '''
        super().__init__(parent) # use super constructor
        # create a vertical scrollbar
        vscrollbar = tk.Scrollbar(self, orient = tk.VERTICAL)
        vscrollbar.grid(row = 0, column = 3, sticky ='nsew')

         #Create a canvas object and associate the scrollbars with it
        self.canvas = tk.Canvas(self, bd = 0, highlightthickness = 0, yscrollcommand = vscrollbar.set)
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
        interior.bind('<Configure>', _configure_interior)

        def _configure_canvas(event):
            # update the frame's width to match that of the canvas
            if self.winfo_reqwidth() != self.canvas.winfo_width():
                # update the inner frame's width to fit the canvas
                self.canvas.config(width = self.winfo_reqwidth()-vscrollbar.winfo_reqwidth())
        self.bind('<Configure>',_configure_canvas)

        def _on_mousewheel(event):
            self.canvas.yview_scroll(int(-1*(event.delta/120)), "units")
        self.canvas.bind_all("<MouseWheel>", _on_mousewheel)  

        i = 0
        for section in self.sections:
            section.makewidget(interior) # build each section's frame widget (and constituent children)
            section.grid(row = i, column = 0, columnspan = 6, sticky = 'nsew') # grid into SimPage
            i += 1 
        self.run_button = ttk.Button(self, text = 'Run', command = lambda: self._run(matlabeng) )
        self.validate_button = ttk.Button(self, text = 'Validate & Build Workspace', command = lambda : self.build(matlabeng))
        self.run_button.grid(row = 1, column = 2, sticky='nsew')
        self.validate_button.grid(row=1, column = 1, sticky = 'nsew')
        self.columnconfigure(0, weight = 1)
        interior.columnconfigure(0, weight=1)

        _configure_interior(0)

    def promptforsave(self, matlabeng):
        ''' Prompt the user to save the file. If a savefilename has previously been selected, saves to that filename. 
            If the user cancels or exits the window, returns False. Otherwise returns True. '''
        response = msg.askyesnocancel('Save Workspace?', 'You have a solved solution that has not been saved.\n This MATLAB workspace may be overwritten. Would you like to save?')
        if response == 'yes':
            if self.saveworkspaceas(matlabeng):
                return True
            else:
                return False # user canceled in save as
        elif not response or response == 'cancel':
            return False
        return True
    
    def saveworkspace(self, matlabeng):
        ''' Saves the workspace to savefilename - if hasn't been defined yet, prompts user to select a file. '''
        if self.savefilename:
            matlabeng.save(self.savefilename)
            self.saved = True
        else:
            self.saveworkspaceas(matlabeng) # don't have a filename - do a save as!

    def saveworkspaceas(self, matlabeng):
        ''' Prompts the user for a filename before saving. Returns False if user cancels, True otherwise. '''
        if not self.savefilename:
            filepicked = dialog.asksaveasfilename(title='Save Simulation Workspace', initialfile = self.name + '_workspace.mat', defaultextension = '.mat', filetypes = (('.MAT files', '.mat')))
        else:
            filepicked= dialog.asksaveasfilename(title='Save Simulation Workspace', initialfile = self.savefilename, defaultextension = '.mat', filetypes = (('.MAT files', '.mat')))
        if filepicked:
            self.saveworkspace(matlabeng)
        else:
            return False

        return True