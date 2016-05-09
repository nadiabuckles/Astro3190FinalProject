from __future__ import print_function, division
import Tkinter as tk
import ttk
import matplotlib
matplotlib.use("TkAgg")
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg, NavigationToolbar2TkAgg
from matplotlib import style 

import numpy as np
import numpy.ma as ma
from astropy.io import fits
from scipy.optimize import curve_fit
from scipy import asarray as ar,exp
from PyAstronomy import pyasl
import matplotlib.pylab as plt
from matplotlib.ticker import AutoMinorLocator
plt.interactive(True)

import tkFileDialog

LARGE_FONT = ("Verdana", 12) 
STND_FONT = ("Helvetica", 8) 
style.use("ggplot")

x = None
y = None

class SpectraApp(tk.Tk):

    def __init__(self, *args, **kwargs):

        tk.Tk.__init__(self, *args, **kwargs) 

        tk.Tk.iconbitmap(self, default = "TexasIcon.ico") 
        tk.Tk.wm_title(self, "Spectra Fitting Application") 

        container = tk.Frame(self)
        container.pack(side = "top", fill = "both", expand = True) 
        container.grid_rowconfigure(0, weight = 1) 
        container.grid_columnconfigure(0, weight = 1) 

        menubar = tk.Menu(container) 
        filemenu = tk.Menu(menubar, tearoff = 0) 
        filemenu.add_command(label = "Open", command = self.OpenPlot) 
        filemenu.add_separator() 
        menubar.add_cascade(label = 'File', menu = filemenu) 

        tk.Tk.config(self, menu = menubar)

        Welcome = "Welcome to our Spectra Fitting Application.\nAuthors: Cassidy Wagner and Nadia Buckles"
        
        label1 = ttk.Label(self, text = "Start Page", font = LARGE_FONT) ;
        label1.pack(pady = 10, padx = 10) ;

        label2 = ttk.Label(self, text = Welcome, font =STND_FONT) ;

        label2.pack(pady = 10, padx = 10) ;

    def OpenPlot(self):

        def getspec(self):

            global x
            global y

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

        print("Done!")

app = SpectraApp() 
app.mainloop() 
