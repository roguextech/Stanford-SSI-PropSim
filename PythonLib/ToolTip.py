'''
    ToolTip:

    A class that links to a parent widget, creating a pop-up suggestion whenever the mouse hovers over the parent widget.
'''
import tkinter as tk
import tkinter.ttk as ttk

class ToolTip(object):
    ''' Credit: https://stackoverflow.com/questions/20399243/display-message-when-hovering-over-something-with-mouse-cursor-in-python'''
    def __init__(self, parent, text):
        self.parent = parent
        parent.bind('<Enter>', self.showtip)
        parent.bind('<Leave>', self.hidetip)
        self.tipwindow = None
        self.text = text
        self.enabled = True

    def showtip(self, event):
        '''Display text in tooltip window'''
        if self.tipwindow or not self.enabled: 
            return #handle edge case where tipbox is still up, or disabled tips

        x, y, cx, cy = self.parent.bbox("insert")
        x = x + self.parent.winfo_rootx() + 57
        y = y + cy + self.parent.winfo_rooty() +27
        self.tipwindow = tk.Toplevel(self.parent)
        self.tipwindow.wm_overrideredirect(1)
        self.tipwindow.wm_geometry("+%d+%d" % (x, y))
        suggestion = tk.Label(self.tipwindow, text=self.text, justify=tk.LEFT,
                      background="#ffffe0", relief=tk.SOLID, borderwidth=1,
                      font=("TkDefaultFont", "8", "normal"))
        suggestion.grid(row = 0, column = 0, sticky='nsew')

    def hidetip(self, event):
        tw = self.tipwindow
        self.tipwindow = None
        if tw:
            tw.destroy()