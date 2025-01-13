from __future__ import division
import tkinter as tk
from tkinter import ttk
from tkinter import messagebox
from matplotlib.figure import Figure
from matplotlib.backends.backend_tkagg import (FigureCanvasTkAgg, NavigationToolbar2Tk) 
import cv2
import numpy as np
from matplotlib.axes import Axes
from scipy import ndimage

import functions.fractals as fractals
from functions.image_functions import plot, save_image
from functions.VerticalNavigationToolbar2tk import VerticalNavigationToolbar2Tk

class MandelJuliaFrame(tk.Frame) :
    def __init__(self, parent):
        tk.Frame.__init__(self, parent, width = 1366, height = 768)

        self.__xmin = -2.0
        self.__xmax = 2.0
        self.__ymin = -2.0
        self.__ymax = 2.0

        self.__fractalPlotted = False

        widgets_frame = ttk.Frame(self)
        radio_frame = ttk.Frame(widgets_frame)
        entry_label_frame = ttk.Frame(widgets_frame)
        entry_frame = ttk.Frame(widgets_frame)
        canvas_button_frame = ttk.Frame(widgets_frame)
        example_frame = ttk.Frame(widgets_frame)

        button = ttk.Button(widgets_frame, text="Powrót",
                           command=lambda: parent.switch_frame("start"))
        
        draw_button = ttk.Button(canvas_button_frame, text = "Rysuj", 
            command = lambda :  self.__plotFractal(self.__plot, canvas, 
                    c_real_entry.get(), c_imag_entry.get(), plot_choice.get(), True))
        clear_button = ttk.Button(canvas_button_frame, text = "Wyczyść", 
            command = lambda : self.__clearPlot(self.__plot, canvas))
        
        
        plot_choice = tk.IntVar()
        plot_choice.set(0)
        self.__oldChoice = 0
        choose_mandel_radio = ttk.Radiobutton(radio_frame, text = "Zbiór Mandelbrota", variable=plot_choice, value = 0)
        choose_julia_radio = ttk.Radiobutton(radio_frame, text = "Zbiór Julii", variable=plot_choice, value = 1)

        c_real_entry = ttk.Entry(entry_frame, width = 10)
        c_imag_entry = ttk.Entry(entry_frame, width = 10)

        fig = Figure(figsize = (7, 7), dpi = 100)
        self.__plot = fig.add_subplot(111)
        self.__plot.set_xlim(self.__xmin, self.__xmax)
        self.__plot.set_ylim(self.__ymin, self.__ymax)
        self.__plot.axis('off')
        fig.subplots_adjust(0, 0, 1, 1)
        canvas_frame = ttk.Frame(self)
        canvas = FigureCanvasTkAgg(fig, master = canvas_frame)
        toolbar = VerticalNavigationToolbar2Tk(canvas, self) 
        toolbar.update()

        home = toolbar.home
        back = toolbar.back
        forward = toolbar.forward
        def newHome(*args, **kwargs):
            home(*args, **kwargs)
            if(self.__fractalPlotted):
                callback_wrapper()
        def newBack(*args, **kwargs):
            back(*args, **kwargs)
            if(self.__fractalPlotted):
                callback_wrapper()
        def newForward(*args, **kwargs):
            forward(*args, **kwargs)
            if(self.__fractalPlotted):
                callback_wrapper()

        toolbar.winfo_children()[0].configure(command=newHome)
        toolbar.winfo_children()[1].configure(command=newBack)
        toolbar.winfo_children()[2].configure(command=newForward)
        toolbar.winfo_children()[7].configure(command=lambda: save_image(self.__plot))

        load_example_button = ttk.Button(example_frame, text = "Przykład", command= lambda : self.__loadExample(c_real_entry, c_imag_entry))

        ###########################################################

        widgets_frame.pack(side=tk.LEFT, fill='y', anchor = tk.NW, padx=10, pady = 10)
        button.pack(side = tk.TOP, anchor=tk.W)

        radio_frame.pack(side = tk.TOP, pady = 10, fill='x')
        choose_mandel_radio.pack(side=tk.TOP, anchor = tk.W)
        choose_julia_radio.pack(side = tk.BOTTOM,anchor = tk.W)

        entry_label_frame.pack(side = tk.TOP, fill = 'x')
        ttk.Label(entry_label_frame, text = "Re").pack(side = tk.LEFT)
        ttk.Label(entry_label_frame, text = "Im").pack()
        entry_frame.pack(side = tk.TOP, pady = 5, fill='x')
        c_real_entry.pack(side = "left")
        c_imag_entry.pack(padx = 10)

        canvas_button_frame.pack(side = tk.TOP, pady = 10, fill='x')
        draw_button.pack(side = tk.LEFT, anchor = tk.W)
        clear_button.pack(side = tk.LEFT, anchor = tk.W, padx = 10)

        example_frame.pack(side = tk.TOP, fill = 'x')
        load_example_button.pack(side = tk.LEFT, anchor = tk.W)

        canvas_frame.pack(side=tk.LEFT,anchor=tk.W, pady = 10, padx = (50, 0))
        canvas.get_tk_widget().pack()
        toolbar.pack(side=tk.LEFT, fill=tk.Y)

        ############################################################

        def callback_wrapper(event = None):
            xlim = self.__plot.get_xlim()
            ylim = self.__plot.get_ylim()

            self.__xmin, self.__xmax = xlim 
            self.__ymin, self.__ymax = ylim
            self.__plotFractal(self.__plot, canvas, c_real_entry.get(), c_imag_entry.get(),
                                               self.__oldChoice)
            
        fig.canvas.mpl_connect('button_release_event', callback_wrapper)

    def __plotFractal(self, plot1 : Axes, canvas, c_real_string : str, c_imag_string : str, plot_choice, clicked : bool = False):

        if(clicked):
            self.__setLimits(plot_choice)
            self.__oldChoice = plot_choice
            plot1.clear()
            plot1.get_figure().canvas.toolbar.update()

        if(plot_choice == 0):
            points = fractals.mandelbrot_c(1000, 1000, 255, self.__xmin, self.__xmax, self.__ymin, self.__ymax)
        else:
            try:
                c_real = float(c_real_string)
                c_imag = float(c_imag_string)
            except(ValueError):
                messagebox.showerror("Nieprawidłowa wartość", "Re, Im muszą być liczbami zmiennoprzecinkowymi")
                return
            points = fractals.julia_c(c_real + c_imag *1j, 1000, 1000, 255, self.__xmin, self.__xmax, self.__ymin, self.__ymax)

        normalized_points = cv2.normalize(points, None, 0, 255, cv2.NORM_MINMAX)
        normalized_points = np.uint8(normalized_points)
        colored_points = cv2.applyColorMap(normalized_points, cv2.COLORMAP_HOT)
        colored_points = cv2.flip(colored_points, 0)

        points = ndimage.rotate(points, 90)
        plot1.clear()
        plot1.imshow(np.flipud(np.fliplr(points.T)), extent=(self.__xmin, self.__xmax, self.__ymin, self.__ymax), cmap='twilight_shifted')
        plot1.axis('off')
        canvas.draw()
        self.__fractalPlotted = True
        
    def __clearPlot(self, plot1, canvas):
        plot1.clear()
        canvas.draw()

    def __setLimits(self, choice):
        if(choice == 0):
            self.__xmin = -2.0
            self.__xmax = 1.0
            self.__ymin = -1.5
            self.__ymax = 1.5
        else:
            self.__xmin = -2.0
            self.__xmax = 2.0
            self.__ymin = -2.0
            self.__ymax = 2.0

    def __loadExample(self, c_real_entry : ttk.Entry, c_imag_entry : ttk.Entry):
        c_real_entry.delete(0, tk.END)
        c_imag_entry.delete(0, tk.END)
        c_real_entry.insert(0, "0.123") 
        c_imag_entry.insert(0, "0.7") 


