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
#from PyAstronomy import pyasl
#module not standard with python, not used in code yet
import matplotlib.pylab as plt
from matplotlib.ticker import AutoMinorLocator
plt.interactive(True)

import tkFileDialog

LARGE_FONT = ("Verdana", 12) ;
STND_FONT = ("Helvetica", 8) ;
style.use("ggplot") ;

class SpectraApp(tk.Tk):

    def __init__(self, *args, **kwargs):

        tk.Tk.__init__(self, *args, **kwargs) ;

        tk.Tk.iconbitmap(self, default = "TexasIcon.ico") ;
        tk.Tk.wm_title(self, "Spectra Fitting Application") ;

        container = tk.Frame(self)
        container.pack(side = "top", fill = "both", expand = True) ;
        container.grid_rowconfigure(0, weight = 1) ;
        container.grid_columnconfigure(0, weight = 1) ;

        menubar = tk.Menu(container) ;
        filemenu = tk.Menu(menubar, tearoff = 0) ;
        filemenu.add_command(label = "Open", command = self.getspec) ;
        filemenu.add_separator() ;
        menubar.add_cascade(label = 'File', menu = filemenu) ;
        menubar.add_cascade(label ='Edit', menu = filemenu) ;

        tk.Tk.config(self, menu = menubar) ;

        self.frames = {} ;

        for F in (StartPage, PageOne):
            
            frame = F(container, self) ;
            self.frames[F] = frame ;

            frame.grid(row = 0, column = 0, sticky = "nsew") ;

        self.show_frame(StartPage) ;

    def getspec(self):

        global x
        global y

        ftypes = [('Data files', '*.dat'), ('All files', '*')] ;
        dlg = tkFileDialog.Open(self, filetypes = ftypes) ;

        fl = dlg.show() ;

        if fl != '':
            data  = self.readFile(fl) ;

        x = data[:,0] ;
        y = data[:,1] ;

        self.frames[PageOne].plotdata(x,y) ;

        return data ;

    def readFile(self, filename):

        f = open(filename, "r") ;
        data = np.loadtxt(f) ;
        return data ;

    def show_frame(self, cont):

        frame = self.frames[cont] ;
        frame.tkraise() ;

class StartPage(tk.Frame):

    def __init__(self, parent, controller):

        Welcome = "Welcome to our Spectra Fitting Application.\nAuthors: Cassidy Wagner and Nadia Buckles"

        tk.Frame.__init__(self, parent) ;
        label1 = ttk.Label(self, text = "Start Page", font = LARGE_FONT) ;
        label1.pack(pady = 10, padx = 10) ;

        label2 = ttk.Label(self, text = Welcome, font =STND_FONT) ;

        label2.pack(pady = 10, padx = 10) ;

        button1 = ttk.Button(self, text = "Open Program", command = lambda: controller.show_frame(PageOne)) ;
        button1.pack() ;

class PageOne(tk.Frame):

    def __init__(self, parent, controller):

        tk.Frame.__init__(self, parent) ;
        label = ttk.Label(self, text = "Spectra App", font = LARGE_FONT) ;
        label.pack(pady = 10, padx = 10) ;

        button1 = ttk.Button(self, text = "Back to Start", command = lambda: controller.show_frame(StartPage));
        button1.pack() ;

        self.minorLocator = AutoMinorLocator(); 
        golden = (plt.sqrt(5) + 1.)/2. ;
        figprops = dict(figsize = (6., 6./golden), dpi = 128) ;
        adjustprops = dict(left = 0.15, bottom = 0.20, right = 0.90, top = 0.93, wspace = 0.2, hspace = 0.2) ;

        self.plot = plt.figure(1, **figprops) ;
        self.plot.subplots_adjust(**adjustprops) ;
        plt.clf () ;

        self.subplot = self.plot.add_subplot(1, 1, 1) ;

        self.subplot.plot([1,2,3,4,5],[3,4,5,6,7])

        plt.xlabel('$\lambda$ ($\AA$)', fontsize=18) ;
        plt.ylabel('$F_\lambda$ ($10^{-17}$ erg/$cm^2$/s/$\AA$)', fontsize=18) ;

        axes = plt.gca() ;

        plt.tick_params(which = 'both', width = 2) ;
        plt.tick_params(which = 'major', length = 4) ;
        plt.tick_params(which = 'minor', length = 4, color = 'r') ;

        plt.close(self.plot) ;

        canvas = FigureCanvasTkAgg(self.plot, self) ;
        canvas.show() ;
        canvas.get_tk_widget().pack(side = tk.BOTTOM, fill = tk.BOTH, expand = True) ;

        toolbar = NavigationToolbar2TkAgg(canvas, self) ;
        toolbar.update()
        canvas._tkcanvas.pack(side = tk.TOP, fill = tk.BOTH, expand = True) ;

    def plotdata(self, xdata, ydata):
        
        self.subplot = self.plot.add_subplot(1, 1, 1) ;

        self.subplot.xaxis.grid(True, which = 'both') ;
        plt.ticklabel_format(style = 'sci', axis = 'x', scilimits = (0,0)) ;
        self.subplot.xaxis.set_minor_locator(self.minorLocator) ;
        
        self.subplot.plot(xdata, ydata, 'k') ;
        print (xdata)
        print (ydata)

app = SpectraApp() ;
#app.geometry("640x540") ;
app.mainloop() ;
