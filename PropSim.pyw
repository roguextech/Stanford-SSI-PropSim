import tkinter as tk
from tkinter import messagebox as msgbox # for writing errors during set-up

if __name__ == '__main__':
    try:
        from PythonLib.MainWindow import MainWindow
        mainwindow = MainWindow() # construct the MainWindow
    except Exception as err:
        # Create a tk root to base the pop-up off of
        root = tk.Tk()
        root.overrideredirect(1)
        root.withdraw()
        err_msg = "Encountered error during start-up:\n{0} \n\nPlease contact PropSim help: \nMax Newport, newpomax@alumni.stanford.edu".format(err)
        response = msgbox.showerror(title="Start-up Error", message = err_msg) # if encountered an error during start-up, show in pop-up
        root.destroy()
    
    mainwindow.run() # run the MainWindow
