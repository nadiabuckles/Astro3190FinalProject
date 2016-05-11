from __future__ import print_function, division

import Tkinter as tk
import ttk
import tkFileDialog
import tkMessageBox as mbox

import matplotlib
matplotlib.use("TkAgg")
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg, NavigationToolbar2TkAgg
from matplotlib import style
import matplotlib.pylab as plt
from matplotlib.ticker import AutoMinorLocator
plt.interactive(True)

import numpy as np
import numpy.ma as ma
from astropy.io import fits
from scipy.optimize import curve_fit
from scipy import asarray as ar,exp
from PyAstronomy import pyasl
import copy

LARGE_FONT = ("Verdana", 12)
STND_FONT = ("Helvetica", 8)

style.use("ggplot")

x = None
y = None
data = None

class SpectraApp(tk.Tk):

    def __init__(self, *args, **kwargs):

        tk.Tk.__init__(self, *args, **kwargs)

        tk.Tk.iconbitmap(self, default = "TexasIcon.ico")
        tk.Tk.wm_title(self, "Spectra Fitting Application")

        self.columnconfigure(0, pad = 3)
        self.columnconfigure(1, pad = 3)
        self.columnconfigure(2, pad = 3)
        self.columnconfigure(3, pad = 3)
        self.columnconfigure(4, pad = 3)
        self.columnconfigure(5, pad = 3)

        self.rowconfigure(0, pad = 3)
        self.rowconfigure(1, pad = 3)
        self.rowconfigure(2, pad = 3)
        self.rowconfigure(3, pad = 3)
        self.rowconfigure(4, pad = 3)
        self.rowconfigure(5, pad = 3)

        container = tk.Frame(self)
        
        menubar  = tk.Menu(container)
        filemenu = tk.Menu(menubar, tearoff = 0)
        
        filemenu.add_command(label = "Open", command = self.OpenPlot)
        filemenu.add_separator()
        menubar.add_cascade(label = "File", menu = filemenu)

        tk.Tk.config(self, menu = menubar)

        welcome = "Welcome to our Spectra Fitting Application. \nAuthors: Nadia Buckles and Cassidy Wagner"

        StartLabel = ttk.Label(self, text = "Start Page", font = LARGE_FONT)
        StartLabel.grid(row = 0, column = 2, sticky = 'N')

        NameLabel = ttk.Label(self, text = welcome, font = STND_FONT)
        NameLabel.grid(row = 1, column = 2, sticky = 'N')

        XMinLabel = ttk.Label(self, text = "Minimum:", font = STND_FONT)
        XMinLabel.grid(row = 2, column = 0, sticky = 'E')

        XMaxLabel = ttk.Label(self, text = "Maximum:", font = STND_FONT)
        XMaxLabel.grid(row = 3, column = 0, sticky = 'E')

        XMinInput = tk.Entry(self)
        XMinInput.grid(row = 2, column = 1, columnspan = 4, sticky = 'E, W')

        XMaxInput = tk.Entry(self)
        XMaxInput.grid(row = 3, column = 1, columnspan = 4, sticky = 'E, W')

        SetXMin = ttk.Button(self, text = "Set", command = lambda: self.SetLimitFunc())
        SetXMin.grid(row = 2, column = 5, sticky = 'E')

        SetXMax = ttk.Button(self, text = "Set", command = lambda: self.SetLimitFunc())
        SetXMax.grid(row = 3, column = 5, sticky = 'E')

        PrintMax = ttk.Button(self, text ="Find Maximum", command = lambda: self.FitSpectra())
        PrintMax.grid(row = 4, column = 2, sticky = 'S')
        
    def OpenPlot(self):

        def getspec(self):

            global x
            global y
            global data

            ftypes = [('Data files', '*.dat'), ('All files', '*')]
            dlg = tkFileDialog.Open(self, filetypes = ftypes)

            fl = dlg.show()

            if fl != '':
                f = open(fl)
                data = np.loadtxt(f)

            x = data[:,0]
            y = data[:,1]

        getspec(self)

        minorLocator = AutoMinorLocator()
        golden = (plt.sqrt(5) + 1.)/2.
        figprops = dict(figsize = (6., 6./golden), dpi = 128)
        adjustprops = dict(left = 0.15, bottom = 0.20, right = 0.90, top = 0.93, wspace = 0.2, hspace = 0.2)

        MyPlot = plt.figure(1, **figprops)
        MyPlot.subplots_adjust(**adjustprops)
        plt.clf()

        MySubplot = MyPlot.add_subplot(1, 1, 1)

        MySubplot.plot(x,y)

        plt.xlabel('$\lambda$ ($\AA$)', fontsize = 18) 
        plt.ylabel('$F_\lambda$ ($10^{-17}$ erg/$cm^2$/s/$\AA$)', fontsize = 18)

        axes = plt.gca()

        plt.tick_params(which = 'both', width = 2) 
        plt.tick_params(which = 'major', length = 4) 
        plt.tick_params(which = 'minor', length = 4, color = 'r')

        MySubplot.xaxis.grid(True, which = "both")
        plt.ticklabel_format(style = 'sci', axis = 'x', scilimits = (0,0))
        MySubplot.xaxis.set_minor_locator(minorLocator)

    def SetLimitFunc(self):

        #xmin = XMinInput.get()
        #xmax = XMaxInput.get()
        
        #grab limit values from entry
        #how to make EntryName.get() be able to find EntryName in __init__
        #self.EntryName doesn't work
        #EntryName can't be defined as global
        #passing self as argument to EntryName.get() doesn't help
        #passing EntryName as a function argument doesn't work
        mbox.showerror("Error", "This feature is not available")

    def FitSpectra(self):

        if data != None:
            epos, mi = pyasl.quadExtreme(x, y, mode ="max", dp = (5, 5))

            fitinfo = [('Index of Maximum', mi), ('Value at Maximum', data[mi, 1]), ('Maximum found by parabolic fit', epos)]

            mbox.showinfo("Quadratic Fitting Results\n", fitinfo) 
        else:
            mbox.showerror("Error", "No data has been entered")

app = SpectraApp()
app.mainloop()
        
