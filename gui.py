from __future__ import division
import tkinter as tk
from tkinter import messagebox 
from tkinter import ttk
from matplotlib.figure import Figure
from matplotlib.axes import Axes
from matplotlib.backends.backend_tkagg import (FigureCanvasTkAgg, NavigationToolbar2Tk) 
from PIL import Image, ImageGrab, ImageTk
import cv2
import numpy as np
from scipy import ndimage
import turtle
from collections import deque
import random
import math
import re
import json

import time

import fractals

class App(tk.Tk):
    def __init__(self):
        tk.Tk.__init__(self)
        self.state('zoomed')
        self._frame = None
        self.switch_frame(StartFrame)

        NavigationToolbar2Tk.toolitems = (
            ('Home', 'Reset original view', 'home', 'home'),
            ('Back', 'Back to  previous view', 'back', 'back'),
            ('Forward', 'Forward to next view', 'forward', 'forward'),
            (None, None, None, None),
            ('Pan', 'Pan axes with left mouse, zoom with right', 'move', 'pan'),
            ('Zoom', 'Zoom to rectangle', 'zoom_to_rect', 'zoom'),
            (None, None, None, None),
            ('Save', 'Save the figure', 'filesave', 'save_figure'),)

    def switch_frame(self, frame_class):
        """Destroys current frame and replaces it with a new one."""
        new_frame = frame_class(self)
        if self._frame is not None:
            self._frame.destroy()
        self._frame = new_frame
        self._frame
        self._frame.pack(anchor = tk.NW)

class StartFrame(tk.Frame):
    def __init__(self, parent):
        tk.Frame.__init__(self, parent)

        button_frame = tk.Frame(self)
        
        button6 = ttk.Button(button_frame, text = "Zbiór Mandelbrota i Zbiory Julii", command= lambda: parent.switch_frame(MandelJuliaFrame))
        button2 = ttk.Button(button_frame, text = "Gra w chaos", command= lambda: parent.switch_frame(FractalFrame))
        button3 = ttk.Button(button_frame, text = "IFS - System Funkcji Iterowanych", command= lambda: parent.switch_frame(AffineFractalFrame))
        button7 = ttk.Button(button_frame, text = "L-System", command = lambda : parent.switch_frame(LSystemFrame))
        button4 = ttk.Button(button_frame, text = "Instrukcja", command= lambda : parent.switch_frame(TutorialFrame))
        button5 = ttk.Button(button_frame, text = "Biblioteka", command=lambda : parent.switch_frame(LibraryFrame))
        button8 = ttk.Button(button_frame, text = "IFS - Wersja graficzna", command= lambda: parent.switch_frame(ChaosGameFrame))

        button_frame.pack(side = tk.TOP, padx=20, pady = 20)
        button6.pack(pady = 10)
        button2.pack(pady = 10)
        button3.pack(pady = 10)
        button8.pack(pady = 10)
        button7.pack(pady = 10)
        button4.pack(pady = 10)
        button5.pack(pady = 10)

class FractalFrame(tk.Frame):

    def __init__(self, parent):

        ####################################

        self.__points = []
        self.__fractal_plotted : bool = False
        self.__vertex_number = 0
        self.__last_iterations_number = 0
        self.__last_jump = 0

        ####################################

        tk.Frame.__init__(self, parent, width = 1366, height = 768)
        restriction_choice = tk.IntVar()
        restriction_choice.set(0)
        color_choice = tk.BooleanVar()
        color_choice.set(False)

        widgets_frame = ttk.Frame(self)
        back_button_frame = ttk.Frame(widgets_frame)
        x_entry_frame = ttk.Frame(widgets_frame)
        y_entry_frame = ttk.Frame(widgets_frame)
        add_point_frame = ttk.Frame(widgets_frame)
        iter_frame = ttk.Frame(widgets_frame)
        jump_frame = ttk.Frame(widgets_frame)
        canvas_buttons_frame = ttk.Frame(widgets_frame)
        restrictions_frame = ttk.Frame(widgets_frame)
        color_frame = ttk.Frame(widgets_frame)

        canvas_frame = tk.Frame(self)

        fig = Figure(figsize = (6, 6), dpi = 100, facecolor="black")
        plot1 = fig.add_subplot(111)
        fig.subplots_adjust(0, 0, 1, 1)
        plot1.set_facecolor("black")
        plot1.set_xlim(0, 500)
        plot1.set_ylim(0, 500)
        plot1.autoscale(False)
        fig.patch.set_facecolor('black')
        canvas = FigureCanvasTkAgg(fig, master = canvas_frame)
        toolbar = NavigationToolbar2Tk(canvas, canvas_frame)
        toolbar.winfo_children()[7].configure(command=lambda: save_image(plot1))


        button = ttk.Button(back_button_frame, text="Powrót",
                           command=lambda: parent.switch_frame(StartFrame))
        point_entry_x = ttk.Entry(x_entry_frame, validate="key")
        point_entry_y = ttk.Entry(y_entry_frame, validate="key")
        point_accept = ttk.Button(add_point_frame, text="Dodaj punkt", command = lambda: [self.__addPoint(
            point_entry_x.get(), point_entry_y.get(), plot1, canvas), 
            point_entry_x.delete(0, tk.END), point_entry_y.delete(0, tk.END)])
        iterations_entry = ttk.Entry(iter_frame)
        jump_entry = ttk.Entry(jump_frame)
        draw_button = ttk.Button(canvas_buttons_frame, text="Rysuj", 
                                command=lambda: [self.__plotFractal(plot1, canvas ,iterations_entry.get(),
                                jump_entry.get(), self.__points, restriction_choice.get(), color_choice.get())])
        clear_button = ttk.Button(canvas_buttons_frame, text="Wyczyść", command= lambda : [self.__clearPlot(plot1, canvas),
                iterations_entry.delete(0, tk.END), jump_entry.delete(0, tk.END)])

        save_button = ttk.Button(canvas_buttons_frame, text="Zapisz", command = lambda : self.__saveConfig())
        load_button = ttk.Button(canvas_buttons_frame, text="Wczytaj", command= lambda : self.__loadConfig(plot1, 
                            canvas, iterations_entry, jump_entry))
        
        color_check = ttk.Checkbutton(color_frame, variable=color_choice)

        ####################################

        widgets_frame.pack(side=tk.LEFT, fill='y', anchor = tk.NW, padx=10, pady = 5)
        back_button_frame.pack(side = tk.TOP, fill='x', pady=5)
        button.pack(side=tk.LEFT, anchor = tk.W)

        x_entry_frame.pack(side = tk.TOP, fill = 'x', pady = 5)
        ttk.Label(x_entry_frame, text="X", width= 20, anchor=tk.W).pack(side = tk.LEFT, anchor = tk.W)
        point_entry_x.pack(side = tk.LEFT)

        y_entry_frame.pack(side = tk.TOP, fill = 'x', pady = 5)
        ttk.Label(y_entry_frame, text="Y", width= 20, anchor=tk.W).pack(side = tk.LEFT, anchor = tk.W)
        point_entry_y.pack(side = tk.LEFT)

        add_point_frame.pack(side = tk.TOP, fill = 'x', pady = 10)
        point_accept.pack(side=tk.LEFT, anchor = tk.W)

        iter_frame.pack(side = tk.TOP, fill='x', pady=5)
        ttk.Label(iter_frame, text='Iteracje', width= 20, anchor=tk.W).pack(side = tk.LEFT, anchor = tk.W)
        iterations_entry.pack(side = tk.LEFT)

        jump_frame.pack(side = tk.TOP, fill='x', pady=5)
        ttk.Label(jump_frame, text='Odległość skoku', width= 20, anchor=tk.W).pack(side = tk.LEFT, anchor = tk.W)
        jump_entry.pack(side = tk.LEFT)

        color_frame.pack(side = tk.TOP, fill='x', pady=5)
        ttk.Label(color_frame, text = "Kolor", width= 20, anchor=tk.W).pack(side=tk.LEFT, anchor = tk.W)
        color_check.pack(side=tk.LEFT, anchor=tk.W)

        canvas_buttons_frame.pack(side = tk.TOP, fill='x', pady=15)
        draw_button.pack(side = tk.LEFT)
        clear_button.pack(side = tk.LEFT, padx = 10)
        save_button.pack(side = tk.LEFT)
        load_button.pack(side = tk.LEFT, padx = 10)

        restrictions_frame.pack(side = tk.TOP, fill='x')
        ttk.Label(restrictions_frame, text="Ograniczenia (Zwróć uwagę na kolejność dodawania wierzchołków)", wraplength=200).pack(side = tk.TOP, pady = 5, anchor=tk.W)
        tk.Radiobutton(restrictions_frame, text="Brak", variable=restriction_choice, value=0, wraplength=200).pack(side = tk.TOP, anchor=tk.W)
        tk.Radiobutton(restrictions_frame, text="Następny losowy wierzchołek musi być inny niż poprzedni",
                       variable=restriction_choice, value=1, wraplength=200).pack(side = tk.TOP, anchor=tk.W)
        tk.Radiobutton(restrictions_frame, text="Następny wierzchołek nie może być poprzednim na liście",
                       variable=restriction_choice, value=2, wraplength=200).pack(side = tk.TOP, anchor=tk.W)
        tk.Radiobutton(restrictions_frame, text="Następny wierzchołek nie może być oddalony o dwa miejsca na liście od poprzedniego",
                       variable=restriction_choice, value=3, wraplength=200).pack(side = tk.TOP, anchor=tk.W)

        canvas_frame.pack(side=tk.RIGHT, pady = 10, padx = 50)
        canvas.get_tk_widget().pack()
        toolbar.update()
        canvas.get_tk_widget().pack()
    
    def __addPoint(self, xString, yString, plot1 : Axes, canvas : tk.Canvas):
        
        try:
            x = float(xString)
            y = float(yString)

            if(x < 0 or x > 500 or y < 0 or y > 500):
                raise RuntimeError()
        except ValueError:
            messagebox.showerror("Nieprawidłowa wartość", "x oraz y muszą być typu zmiennoprzecinkowego")
            return 
        except RuntimeError:
            messagebox.showerror("Nieprawidłowa wartość", "x oraz y muszą być w zakresie od 0 do 500")
            return

        self.__points.append((x, y))
        self.__vertex_number += 1

        if(self.__fractal_plotted):
            plot(plot1, canvas)
            self.__fractal_plotted = False
        plot(plot1, canvas, vertices=self.__points)

    def __plotFractal(self, plot1 : Axes, canvas, iterationsString, jumpString, points : list, restriction : int, color: bool):

        try:
            iterations = int(iterationsString)
        except(ValueError):
            messagebox.showerror("Nieprawidłowa wartość", "Iteracje muszą być liczbą naturalną")
            return
        try:
            jump = float(jumpString)
        except(ValueError):
            messagebox.showerror("Nieprawidłowa wartość", "Wartość skoku musi być liczbą zmiennoprzecinkową")
            return
        
        if len(points) == 0:
            messagebox.showerror("Błąd", "Dodaj co najmniej jeden punkt")
            return
        
        self.__last_iterations_number = iterations
        self.__last_jump = jump
        new_points = points.copy()

        if(restriction == 0):
            start = time.time()
            new_points, colors = fractals.chaos_game_fractal(iterations, jump, new_points)
            stop  = time.time()
            print("Punkty " + str(stop - start))
        else:
            start = time.time()
            new_points, colors = fractals.chaos_game_fractal_restricted(iterations, jump, new_points, restriction)
            stop  = time.time()
            print("Punkty " + str(stop - start))
        
        if color:
            plot(plot1, canvas, points = new_points, vertices = points,colors=colors, scaled=True)
        else:
            plot(plot1, canvas, points = new_points, vertices = points, scaled=True)
        plot1.axis('off')

        self.__fractal_plotted = True
        
    def __clearPlot(self, plot1 : Axes, canvas : tk.Canvas):
        plot(plot1, canvas)
        self.__emptyPoints()
        self.__fractal_plotted = False
        self.__last_iterations_number = 0
        self.__last_jump = 0
    
    def __emptyPoints(self):
        self.__points = []
        self.__vertex_number = 0

    def __saveConfig(self):
        file = tk.filedialog.asksaveasfile(mode="w", defaultextension=".frac", filetypes=[('Fractal files', '*.frac')])
        if(file is None):
            return
        
        dict = {
            "points": self.__points,
            "iterations": self.__last_iterations_number,
            "jump": self.__last_jump
        }

        info = json.dumps(dict)
        file.write(info)

        file.close()

    def __loadConfig(self, plot1, canvas, iterLabel: tk.Entry, jumpLabel: tk.Entry):

        file = tk.filedialog.askopenfile(mode="r", defaultextension=".frac", filetypes=[('Fractal files', '*.frac')])
        if(file is None):
            return
        
        self.__clearPlot(plot1, canvas)
        
        try:
            info = json.load(file)

            if not (all(
            isinstance(item, list) and len(item) == 2 and
            all(isinstance(coord, (int, float)) for coord in item)
            for item in info['points'])):
                raise json.decoder.JSONDecodeError("Error", "", 0)
            
        except json.decoder.JSONDecodeError:
            messagebox.showerror("Błąd", "Nieprawidłowy format danych")
            return

        self.__points = info['points']

        self.__last_iterations_number = info['iterations']
        self.__last_jump = info['jump']

        iterLabel.delete(0, tk.END)
        jumpLabel.delete(0, tk.END)
        iterLabel.insert(0, str(self.__last_iterations_number))
        jumpLabel.insert(0, str(self.__last_jump))

        plot(plot1, canvas, vertices=self.__points)
        self.__fractal_plotted = False

class AffineFractalFrame(tk.Frame):

    def __init__(self, parent):

        self.__chances = []
        self.__x_transform = []
        self.__y_transform = []
        self.__last_iterations_number = 0
        self.__changed_index = -1

        color_choice = tk.BooleanVar()
        color_choice.set(False)

        #####################################

        tk.Frame.__init__(self, parent, width = 1366, height = 768)
        vcmd = (self.register(self.__validate))

        widgets_frame = ttk.Frame(self)
        back_button_frame = ttk.Frame(widgets_frame)
        percentage_frame = ttk.Frame(widgets_frame)
        x_label_frame = ttk.Frame(widgets_frame)
        x_entry_frame = ttk.Frame(widgets_frame)
        y_label_frame = ttk.Frame(widgets_frame)
        y_entry_frame = ttk.Frame(widgets_frame)
        function_add_frame = ttk.Frame(widgets_frame)
        iter_frame = ttk.Frame(widgets_frame)
        canvas_buttons_frame = ttk.Frame(widgets_frame)
        list_outer_frame = ttk.Frame(widgets_frame)
        color_frame = ttk.Frame(widgets_frame)


        button = ttk.Button(back_button_frame, text="Powrót",
                           command=lambda: parent.switch_frame(StartFrame))
        iterations_entry = ttk.Entry(iter_frame, validate="all", validatecommand=(vcmd, "%P"))
        draw_button = ttk.Button(canvas_buttons_frame, text="Rysuj", 
                                command=lambda: self.__plotFractal(plot1, canvas, iterations_entry.get(), color_choice.get()))
        self.__chance_entry = ttk.Entry(percentage_frame)

        clear_button = ttk.Button(canvas_buttons_frame, text="Wyczyść", command=lambda : self.__clearPlot(plot1, canvas, list_frame, iterations_entry))
        save_button = ttk.Button(canvas_buttons_frame, text = "Zapisz", command=lambda : self.__saveConfig())
        load_button = ttk.Button(canvas_buttons_frame, text = "Wczytaj", command=lambda : self.__loadConfig(plot1, canvas, list_frame, iterations_entry))
        
        self.__x_entry_1 = ttk.Entry(x_entry_frame, width = 10)
        self.__x_entry_2 = ttk.Entry(x_entry_frame, width = 10)
        self.__x_entry_3 = ttk.Entry(x_entry_frame, width = 10)

        self.__y_entry_1 = ttk.Entry(y_entry_frame, width = 10)
        self.__y_entry_2 = ttk.Entry(y_entry_frame, width = 10)
        self.__y_entry_3 = ttk.Entry(y_entry_frame, width = 10)

        function_add_button = ttk.Button(function_add_frame, text="Dodaj", command = lambda : [self.__addFunction(list_frame
        ), self.__clearEntries()])

        function_delete_button = ttk.Button(function_add_frame, text = "Usuń", command = lambda : [self.__deleteFunction(list_frame
        ), self.__clearEntries()])

        
        def __scroll(event):
            list_canvas.configure(scrollregion=list_canvas.bbox("all"), width=200, height = 230)

        list_canvas = tk.Canvas(list_outer_frame, width=200, height = 230)
        list_frame = ttk.Frame(list_canvas, width=200, height = 230)
        scrollbar = ttk.Scrollbar(list_outer_frame, command=list_canvas.yview)
        list_canvas.configure(yscrollcommand=scrollbar.set)
        list_canvas.create_window((0, 0), window=list_frame, anchor='nw')
        list_frame.bind("<Configure>", __scroll)
       
        fig = Figure(figsize = (6, 6), dpi = 100, facecolor="black")
        plot1 = fig.add_subplot(111)
        plot1.set_facecolor("black")
        fig.subplots_adjust(0, 0, 1, 1)
        canvas_frame = tk.Frame(self)
        canvas = FigureCanvasTkAgg(fig, master = canvas_frame)
        toolbar = NavigationToolbar2Tk(canvas, canvas_frame) 
        toolbar.winfo_children()[7].configure(command=lambda: save_image(plot1))

        color_check = ttk.Checkbutton(color_frame, variable= color_choice)

        #########################################

        widgets_frame.pack(side=tk.LEFT, fill='y', anchor = tk.NW, padx=10, pady = 5)
        back_button_frame.pack(side = tk.TOP, fill='x', pady=5)
        button.pack(side=tk.TOP, anchor = tk.W)
        ttk.Label(back_button_frame, text="Dodaj funkcję afiniczną").pack(side = tk.BOTTOM, anchor = tk.W, pady = 15)

        percentage_frame.pack(side = tk.TOP, fill = 'x', pady = 5)
        ttk.Label(percentage_frame, text="Szansa", width = 20, anchor = tk.W).pack(side = tk.LEFT, anchor=tk.W)
        self.__chance_entry.pack(side = tk.LEFT)

        x_label_frame.pack(side = tk.TOP, fill = 'x', pady = (5, 0))
        ttk.Label(x_label_frame, text = "a", width = 10, anchor = tk.W).pack(side = tk.LEFT)
        ttk.Label(x_label_frame, text = "b", width = 10, anchor = tk.W).pack(side = tk.LEFT, padx = 14)
        ttk.Label(x_label_frame, text = "e", width = 10, anchor = tk.W).pack(side = tk.LEFT)

        x_entry_frame.pack(side = tk.TOP, fill = 'x')
        self.__x_entry_1.pack(side = tk.LEFT, anchor = tk.W)
        self.__x_entry_2.pack(side = tk.LEFT, anchor = tk.W, padx = 12)
        self.__x_entry_3.pack(side = tk.LEFT, anchor = tk.W, padx = 1)

        y_label_frame.pack(side = tk.TOP, fill = 'x', pady=(10, 0))
        ttk.Label(y_label_frame, text = "c", width = 10, anchor = tk.W).pack(side = tk.LEFT)
        ttk.Label(y_label_frame, text = "d", width = 10, anchor = tk.W).pack(side = tk.LEFT, padx = 14)
        ttk.Label(y_label_frame, text = "f", width = 10, anchor = tk.W).pack(side = tk.LEFT)

        y_entry_frame.pack(side = tk.TOP, fill = 'x')
        self.__y_entry_1.pack(side = tk.LEFT, anchor = tk.W)
        self.__y_entry_2.pack(side = tk.LEFT, anchor = tk.W, padx = 12)
        self.__y_entry_3.pack(side = tk.LEFT, anchor = tk.W, padx = 1)

        function_add_frame.pack(side = tk.TOP, fill = 'x', pady = 15)
        function_add_button.pack(side = tk.LEFT, anchor = tk.W)
        function_delete_button.pack(side = tk.LEFT, anchor = tk.W, padx = 10)

        iter_frame.pack(side = tk.TOP, fill = 'x')
        ttk.Label(iter_frame, text='Iteracje', width = 20, anchor= tk.W).pack(side = tk.LEFT)
        iterations_entry.pack(side = tk.LEFT)

        color_frame.pack(side = tk.TOP, fill='x', pady=5)
        ttk.Label(color_frame, text = "Kolor", width= 20, anchor=tk.W).pack(side=tk.LEFT, anchor = tk.W)
        color_check.pack(side=tk.LEFT, anchor=tk.W)

        canvas_buttons_frame.pack(side = tk.TOP, fill = 'x', pady = 20)
        draw_button.pack(side = tk.LEFT)
        clear_button.pack(side = tk.LEFT, padx = 10)
        save_button.pack(side = tk.LEFT)
        load_button.pack(side = tk.LEFT, padx = 10)

        list_outer_frame.pack(side = tk.TOP, fill = 'x', pady = 10)
        list_canvas.pack(side = tk.LEFT)
        scrollbar.pack(side = tk.LEFT, fill = 'y', anchor = tk.W)

        canvas_frame.pack(side=tk.RIGHT, pady = 10, padx = 50)
        canvas.get_tk_widget().pack()
        toolbar.update()
        canvas.get_tk_widget().pack()


    def __validate(self, P):
        if str.isdigit(P) or P == "":
            return True
        else:
            return False
        
    def __addFunction(self, frame) :

        if self.__changed_index >= 0:
            self.__chances.pop(self.__changed_index)
            self.__x_transform.pop(self.__changed_index)
            self.__y_transform.pop(self.__changed_index)

        chance = self.__chance_entry.get()
        x1 = self.__x_entry_1.get()
        x2 = self.__x_entry_2.get()
        x3 = self.__x_entry_3.get()
        y1 = self.__y_entry_1.get()
        y2 = self.__y_entry_2.get()
        y3 = self.__y_entry_3.get()

        try:
            self.__addChances(chance)
        except(ValueError):
            messagebox.showerror("Nieprawidłowa wartość", "Szansa musi być dodatnią liczbą zmiennoprzecinkową")
            return
        
        try:
            self.__x_transform.append([float(x1), float(x2), float(x3)])
        except(ValueError):
            self.__chances.pop()
            messagebox.showerror("Nieprawidłowa wartość", "a, b, e, muszą być liczbami")
            return
        
        try:
            self.__y_transform.append([float(y1), float(y2), float(y3)])
        except(ValueError):
            self.__chances.pop()
            self.__x_transform.pop()
            messagebox.showerror("Nieprawidłowa wartość", "c, d, f, muszą być liczbami")
            return

        self.__refreshFunctionLabel(frame)
        self.__changed_index = -1

    def __deleteFunction(self, frame):

        if self.__changed_index == -1:
            return
        
        self.__chances.pop(self.__changed_index)
        self.__x_transform.pop(self.__changed_index)
        self.__y_transform.pop(self.__changed_index)

        self.__refreshFunctionLabel(frame)
        self.__changed_index = -1
        
        
    def __clearEntries(self, *args):
        
        self.__chance_entry.delete(0, tk.END)
        self.__x_entry_1.delete(0, tk.END)
        self.__x_entry_2.delete(0, tk.END)
        self.__x_entry_3.delete(0, tk.END)
        self.__y_entry_1.delete(0, tk.END)
        self.__y_entry_2.delete(0, tk.END)
        self.__y_entry_3.delete(0, tk.END)
        

    def __clearLists(self):
        self.__chances = []
        self.__x_transform = []
        self.__y_transform = []
        self.__changed_index = -1
    
    def __plotFractal(self, plot1, canvas, iterationsString : str, color: bool):
        
        try:
            iterations = int(iterationsString)
        except(ValueError):
            messagebox.showerror("Nieprawidłowa wartość", "Iteracje muszą być liczbą całkowitą")
            return

        if len(self.__chances) == 0:
            messagebox.showerror("Błąd", "Dodaj co najmniej jedną funkcję")
            return
        
        if(sum(self.__chances) < 100):
            messagebox.showerror("Nieprawidłowa wartość", "Suma procentowych szans jest mniejsza od 100")
            return
        
        self.__last_iterations_number = iterations

        start = time.time()
        points, colors = fractals.affine_fractal(iterations,self.__chances, self.__x_transform, self.__y_transform)
        stop = time.time()
        print("Punkty " + str(stop-start))
        if color:
            plot(plot1, canvas, points = points, colors = colors)
        else:
            plot(plot1, canvas, points = points)
        plot1.axis('off')

    def __clearPlot(self, plot1, canvas, frame: tk.Frame, iterEntry : tk.Entry):
        plot(plot1, canvas)
        self.__clearLists()
        self.__clearFrames(frame)
        iterEntry.delete(0, tk.END)

    def __clearFrames(self, frame):
        for widget in frame.winfo_children():
            widget.destroy()
    
    def __addChances(self, chanceString: str) :

        chance = float(chanceString)

        if chance < 0:
            raise ValueError
        
        sum_of_chances = sum(self.__chances)

        if(sum_of_chances >= 100):
            return
        
        if(100 - sum_of_chances <= chance):
            chance = 100 - sum(self.__chances)

        self.__chances.append(chance)
    
    def __saveConfig(self):
        file = tk.filedialog.asksaveasfile(mode="w", defaultextension=".ifs", filetypes=[('Fractal files', '*.ifs')])
        if(file is None):
            return
        
        dict = {
            "chances": self.__chances,
            "x_transform": self.__x_transform,
            "y_transform": self.__y_transform,
            "iterations": self.__last_iterations_number
        }
        info = json.dumps(dict)
        file.write(info)
        file.close()

    def __loadConfig(self, plot1, canvas, functionFrame : tk.Frame, iterEntry : tk.Entry):
        file = tk.filedialog.askopenfile(mode="r", defaultextension=".ifs", filetypes=[('Fractal files', '*.ifs')])
        if(file is None):
            return
        self.__clearPlot(plot1, canvas, functionFrame, iterEntry)

        try:
            info = json.load(file)

            if not( all(isinstance(item, float) for item in info['chances']) ):
                raise json.decoder.JSONDecodeError("", "", 0)
            
            if not (all(isinstance(item, list) and all(isinstance(coord, float) for coord in item)
            for item in info['x_transform'])):
                raise json.decoder.JSONDecodeError("", "", 0)
            
            if not (all(isinstance(item, list) and all(isinstance(coord, float) for coord in item)
            for item in info['y_transform'])):
                raise json.decoder.JSONDecodeError("", "", 0)

        except json.decoder.JSONDecodeError:
            messagebox.showerror("Błąd", "Nieprawidłowy format danych")
            return

        self.__chances = info['chances']
        self.__x_transform = info['x_transform']
        self.__y_transform = info['y_transform']
        self.__last_iterations_number = info['iterations']
        self.__refreshFunctionLabel(functionFrame)

        iterEntry.delete(0, tk.END)
        iterEntry.insert(0, str(self.__last_iterations_number))

    def __refreshFunctionLabel(self, functionFrame: tk.Frame):
        
        self.__clearFrames(functionFrame)

        for i in range(len(self.__chances)):
            chance = self.__chances[i]
            x = self.__x_transform[i]
            y = self.__y_transform[i]

            functionLabel = tk.Label(functionFrame)
            functionLabel['text'] += " x = " + str(x[0]) +"x " + "%+.2f" % x[1] + "y " + "%+ .2f" % x[2] + "\n"
            functionLabel['text'] += " y = " + str(y[0]) +"x " +"%+.2f" % y[1] + "y " + "%+ .2f" % y[2] + "\n"
            functionLabel['text'] += "Szansa na wystąpienie: " + str(chance)

            functionLabel.pack(fill="x", padx=10, pady=2)

            functionLabel.bind("<Button-1>", lambda e, label = functionLabel, index = i: self.__editFunction(index, label))

    def __editFunction(self, index, label: tk.Label):
        bg = label.cget("bg")
        label.config(bg="lightblue")
        self.__restoreEntries(index)

        label.after(500, lambda: label.config(bg=bg))

    def __restoreEntries(self, index):
        self.__clearEntries()
        self.__chance_entry.insert(0, self.__chances[index])
        x_transform = self.__x_transform[index]
        self.__x_entry_1.insert(0, x_transform[0])
        self.__x_entry_2.insert(0, x_transform[1])
        self.__x_entry_3.insert(0, x_transform[2])
        y_transform = self.__y_transform[index]
        self.__y_entry_1.insert(0, y_transform[0])
        self.__y_entry_2.insert(0, y_transform[1])
        self.__y_entry_3.insert(0, y_transform[2])
        self.__changed_index = index


class MandelJuliaFrame(tk.Frame) :
    def __init__(self, parent):
        tk.Frame.__init__(self, parent, width = 1366, height = 768)

        self.__xmin = -2.0
        self.__xmax = 2.0
        self.__ymin = -2.0
        self.__ymax = 2.0

        widgets_frame = ttk.Frame(self)
        radio_frame = ttk.Frame(widgets_frame)
        entry_label_frame = ttk.Frame(widgets_frame)
        entry_frame = ttk.Frame(widgets_frame)
        canvas_button_frame = ttk.Frame(widgets_frame)

        button = ttk.Button(widgets_frame, text="Powrót",
                           command=lambda: parent.switch_frame(StartFrame))
        
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

        fig = Figure(figsize = (6, 6), dpi = 100)
        self.__plot = fig.add_subplot(111)
        self.__plot.set_xlim(self.__xmin, self.__xmax)
        self.__plot.set_ylim(self.__ymin, self.__ymax)
        self.__plot.axis('off')
        fig.subplots_adjust(0, 0, 1, 1)
        canvas_frame = ttk.Frame(self)
        canvas = FigureCanvasTkAgg(fig, master = canvas_frame)
        toolbar = NavigationToolbar2Tk(canvas, canvas_frame) 
        toolbar.update()

        home = toolbar.home
        back = toolbar.back
        forward = toolbar.forward
        def newHome(*args, **kwargs):
            home(*args, **kwargs)
            callback_wrapper()
        def newBack(*args, **kwargs):
            back(*args, **kwargs)
            callback_wrapper()
        def newForward(*args, **kwargs):
            forward(*args, **kwargs)
            callback_wrapper()

        toolbar.winfo_children()[0].configure(command=newHome)
        toolbar.winfo_children()[1].configure(command=newBack)
        toolbar.winfo_children()[2].configure(command=newForward)
        toolbar.winfo_children()[7].configure(command=lambda: save_image(self.__plot))

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

        canvas_frame.pack(side=tk.RIGHT,anchor=tk.W, pady = 10, padx = 50)
        canvas.get_tk_widget().pack()

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


class TutorialFrame(tk.Frame):

    def __init__(self, parent):
        tk.Frame.__init__(self, parent, width = 1366, height = 768)

        # self.__current_frame : ttk.Frame = None

        widgets_frame = ttk.Frame(self)
        buttons_frame = ttk.Frame(widgets_frame)
        # introduction_frame = ttk.Frame(self)
        # chaos_game_frame = ttk.Frame(self)
        # rectangle_frame = ttk.Frame(self)
        # lsystem_frame = ttk.Frame(self)
        # ifs_frame = ttk.Frame(self)
        # mandelbrot_frame = ttk.Frame(self)
        # julia_frame = ttk.Frame(self)

        canvas_frame = ttk.Frame(self)

        ##BUTTONS

        button = ttk.Button(buttons_frame, text="Powrót",
                           command=lambda: parent.switch_frame(StartFrame))
        intro_button = ttk.Button(buttons_frame, text = "Wprowadzenie", command = lambda: self.__showCanvas('intro'))
        chaos_game_tutorial_button = ttk.Button(buttons_frame, text = "Gra w chaos",
                command = lambda : self.__showCanvas('chaos'))
        rectangle_tutorial_button = ttk.Button(buttons_frame, text = "IFS - wersja graficzna",
                command = lambda: self.__showCanvas('rect'))
        affine_tutorial_button = ttk.Button(buttons_frame, text = "IFS",
                command = lambda: self.__showCanvas('ifs'))
        mandelbrot_tutorial_button = ttk.Button(buttons_frame, text = "Zbiór Mandelbrota",
                command = lambda : self.__showCanvas('mandelbrot'))
        julia_tutorial_button = ttk.Button(buttons_frame, text = "Zbiory Julii",
                command = lambda: self.__showCanvas('julia'))
        lsystem_tutorial_button = ttk.Button(buttons_frame, text = "L-system",
                command = lambda : self.__showCanvas('lsys'))

        self.__canvas = tk.Canvas(canvas_frame, width = 1000, height = 700)

        #---------------------------------------#

        widgets_frame.pack(side=tk.LEFT, fill='y', anchor = tk.NW, padx=10, pady = 5)
        buttons_frame.pack(side = tk.TOP, fill='x', pady=5)

        button.pack(side=tk.TOP, anchor = tk.W)
        intro_button.pack(side=tk.TOP, anchor = tk.W, pady = 10)
        chaos_game_tutorial_button.pack(side=tk.TOP, anchor = tk.W, pady = 10)
        affine_tutorial_button.pack(side=tk.TOP, anchor = tk.W)
        rectangle_tutorial_button.pack(side=tk.TOP, anchor = tk.W, pady = 10)
        lsystem_tutorial_button.pack(side=tk.TOP, anchor = tk.W)
        mandelbrot_tutorial_button.pack(side=tk.TOP, anchor = tk.W, pady = 10)
        julia_tutorial_button.pack(side=tk.TOP, anchor = tk.W)

        canvas_frame.pack(side = tk.LEFT, anchor = tk.W, padx = 15)
        self.__canvas.pack(side = tk.LEFT, anchor = tk.W)

        # introduction_frame.pack(side = tk.TOP, anchor = tk.W, padx = 20)
        # ttk.Label(introduction_frame, text = "Wprowadzenie", font = ('Arial', 30)).pack(pady = 15)
        # ttk.Label(introduction_frame, text = "Objaśnienie czym jest fraktal")

    # def __packFrame(self, new_frame : ttk.Frame):

    #     if(self.__current_frame != None):
    #         self.__current_frame.pack_forget()
    #     elif(self.__current_frame is new_frame):
    #         return
    #     new_frame.pack()
    #     self.__current_frame = new_frame

    def __showCanvas(self, frac_name : str):
        self.__canvas.delete('all')
        match(frac_name):
            case 'intro':
                self.__canvas.create_text(150, 50, text='Wprowadzenie', font=('Arial', 30))
                self.__canvas.create_text(20, 100, text = 'Czym jest fraktal', anchor='nw')
                self.__canvas.create_text(20, 150, text = "Fraktal to rodzaj złożonej figury geometrycznej", anchor='nw')
                self.__canvas.create_text(20, 170, text ="Charakteryzują go cechy (ale niekoniecznie muszą) takie jak:", anchor='nw')
                self.__canvas.create_text(20, 190, text ="- Samopodobieństwo - fragmenty figury są podobne do całości", anchor='nw')
                self.__canvas.create_text(20, 210, text ="- Nietrywialna struktura - nie da się go łatwo opisać za pomocą tradycyjnej geometrii", anchor='nw')
                self.__canvas.create_text(20, 230, text ="- Jego wymiar fraktalny jest różny od jego wymiaru topologicznego - Wymiar fraktalny można zdefiniować", anchor='nw')
                self.__canvas.create_text(20, 250, text ="jako logarytm o podstawie równej skali w jakiej pomniejszone są fragmenty fraktala z liczby elementów samopodobnych", anchor='nw')
            case 'chaos':
                self.img = tk.PhotoImage(file = "./images/chaosGame.png")
                self.__canvas.create_image(350, 300, image = self.img)
            case 'ifs':
                self.img = tk.PhotoImage(file = "./images/ifs.png")
                self.__canvas.create_image(350, 300, image = self.img)
            case 'lsys':
                self.img = tk.PhotoImage(file = "./images/lsys.png")
                self.__canvas.create_image(385, 300, image = self.img)
            case 'rect':
                self.img = tk.PhotoImage(file = "./images/rect.png")
                self.__canvas.create_image(380, 300, image = self.img)
            case 'mandelbrot':
                self.img = Image.open("./images/mandelbrot.png")
                self.img = self.img.resize((int(self.img.width*0.9), int(self.img.height*0.9)))
                self.img = ImageTk.PhotoImage(self.img)
                self.__canvas.create_image(380, 350, image = self.img)
            case 'julia':
                self.img = Image.open("./images/julia.png")
                self.img = self.img.resize((int(self.img.width*0.9), int(self.img.height*0.9)))
                self.img = ImageTk.PhotoImage(self.img)
                self.__canvas.create_image(380, 350, image = self.img)
            case _ :
                pass
            
            
                




class LibraryFrame(tk.Frame):
    def __init__(self, parent):
        tk.Frame.__init__(self, parent, width = 1366, height = 768)

        widgets_frame = ttk.Frame(self)


        button = ttk.Button(widgets_frame, text="Powrót",
                           command=lambda: parent.switch_frame(StartFrame))
        

        fig = Figure(figsize = (6.5, 6.5), dpi = 100)
        plot1 = fig.add_subplot(111)
        fig.subplots_adjust(0, 0, 1, 1)
        plot1.set_xlim(0, 500)
        plot1.set_ylim(0, 500)
        plot1.autoscale(False)
        fig.patch.set_facecolor('black')
        plot1.set_facecolor("black")
        plot2 = fig.add_subplot(111)
        self.__canvas_frame = tk.Frame(self)
        self.__instruction_frame = ttk.Frame(self)
        self.__instruction_label = ttk.Label(self.__instruction_frame, text = "TEST")
        canvas = FigureCanvasTkAgg(fig, master = self.__canvas_frame)

        fractal_list = tk.Listbox(widgets_frame, selectmode='single')

        image_label = tk.Label(self)

        
        list = ["Trójkąt Sierpińskiego","Dywan Sierpińskiego", "Paproć Barnsley'a", "Fraktal Viscek'a", 
                "Krzywa Koch'a", "Smok Heighway'a", "Krzywa Levy'ego", "Zbiór Mandelbrota", "Zbiór Julii - Przykład",
                "Dywan Sierpińskiego - L-System"]
        for i in range(len(list)):
            fractal_list.insert(i, list[i])
        fractal_list.bind('<<ListboxSelect>>', lambda event:  self.__onSelect(event, plot1, plot2, canvas, 
            image_label))

        ##############################################

        widgets_frame.pack(side=tk.LEFT, fill='y', anchor = tk.NW, padx=10, pady = 10)
        button.pack(anchor = tk.W)
        fractal_list.pack(pady = 20)

        self.__canvas_frame.pack(side = tk.LEFT, padx = 50, pady = 10)
        canvas.get_tk_widget().pack()
        canvas.get_tk_widget().pack()

        self.__instruction_label.pack(side = tk.TOP)


    def __onSelect(self, event : tk.Event, plot1, plot2, canvas, image_label: tk.Label):
        w = event.widget
        index = w.curselection()[0]
        value = w.get(index)

        points = []

        plot2.set_visible(False)
        plot1.set_visible(True)

        self.__instruction_frame.pack_forget()
        image_label.pack_forget()
        self.__canvas_frame.pack(side = tk.LEFT, padx = 50, pady = 10)

        if(index == 0):
            points, _ = fractals.chaos_game_fractal(60000, 0.5, [(0, 0), (10, 0), (5, 8.65)])
            self.__instruction_label.config(text = "Algorytm: Gra w chaos\nPunkty : (0, 0), (500, 0), (250, 500)\nSkok : 0.5")
            self.__instruction_label['text'] += ("\n\nAlgorytm: IFS\nFunkcje:\nszansa = 33.33%\nx = 0.5x + 0y + 0\ny = 0x + 0.5y + 0\n\n"
            "szansa = 33.33%\nx = 0.5x + 0y + 0.5\ny = 0x + 0.5y + 0\n\n"
            "szansa = 33.33%\nx = 0.5x + 0y + 0.25\ny = 0x + 0.5y + 0.43")

        elif(index == 1):
            points, _ = fractals.chaos_game_fractal(60000, (2/3), 
                [(0, 0), (500, 0), (500, 500), (0, 500), (0, 250), (250, 0), (500, 250), (250, 500)])
            self.__instruction_label.config(text = "Algorytm: Gra w chaos\nPunkty : (0, 0), (500, 0), (500, 500),\n (0, 500), (0, 250),\n"
            "(250, 0), (500, 250), (250, 500)\nSkok : 0.5")
            self.__instruction_label['text'] += ("\n\nAlgorytm: IFS\n"
            "Funkcje:\n"
            "szansa = 12.5%\nx = 0.333x + 0y + 0\ny = 0x + 0.333y + 0\n\n"
            "szansa = 12.5%\nx = 0.333x + 0y + 0.333\ny = 0x + 0.333y + 0\n\n"
            "szansa = 12.5%\nx = 0.333x + 0y + 0.666\ny = 0x + 0.333y + 0\n\n"
            "szansa = 12.5%\nx = 0.333x + 0y + 0\ny = 0x + 0.333y + 0.333\n\n"
            "szansa = 12.5%\nx = 0.333x + 0y + 0.666\ny = 0x + 0.333y + 0.333\n\n"
            "szansa = 12.5%\nx = 0.333x + 0y + 0\ny = 0x + 0.333y + 0.666\n\n"
            "szansa = 12.5%\nx = 0.333x + 0y + 0.333\ny = 0x + 0.333y + 0.666\n\n"
            "szansa = 12.5%\nx = 0.333x + 0y + 0.666\ny = 0x + 0.333y + 0.666\n\n")
        elif(index == 2):
            points, _ = fractals.affine_fractal(100000, [1.0, 85.0, 7.0, 7.0],
            [[0.0, 0.0, 0.0], [0.85, 0.04, 0.0], [0.2, -0.26, 0.0], [-0.15, 0.28, 0.0]], 
            [[0.0, 0.16, 0.0], [-0.04, 0.85, 1.6], [0.23, 0.22, 1.6], [0.26, 0.24, 0.44]])
            self.__instruction_label.config(text = "\n\nAlgorytm: IFS\n"
            "Funkcje:\n"
            "szansa = 1%\nx = 0x + 0y + 0\ny = 0x + 0.16y + 0\n\n"
            "szansa = 7%\nx = 0.2x - 0.26y + 0\ny = 0.23x + 0.22y + 1.6\n\n"
            "szansa = 7%\nx = -0.15x + 0.28y + 0\ny = 0.26x + 0.24y + 0.44\n\n"
            "szansa = 85%\nx = 0.85x + 0.04y + 0\ny = -0.04x + 0.85y + 1.6\n\n")
        elif(index == 3):
            points, _ = fractals.chaos_game_fractal(60000, 0.667,
                     [(0, 0),(12, 0), (12, 12), (0, 12), (6, 6)])
            self.__instruction_label.config(text = "Algorytm: Gra w chaos\nPunkty : (0, 0), (500, 0), (500, 500),\n"
            "(0, 500), (250, 250)\n"
            "Skok : 0.667")
        elif(index == 4):
            points, _ = fractals.affine_fractal(60000, [25, 25, 25, 25],
            [[0.3333, 0.0, 0.0], [0.1667, -0.2887, 0.3333], [0.1667, 0.2887, 0.5], [0.3333, 0.0, 0.667]],
            [[0.0, 0.3333, 0.0], [0.2887, 0.1667, 0.0],[-0.2887, 0.1667, 0.2887], [0.0, 0.3333, 0.0]])
            self.__instruction_label.config(text = "\n\nAlgorytm: IFS\n"
            "Funkcje:\n"
            "szansa = 25%\nx = 0.3333x + 0y + 0\ny = 0x + 0.3333y + 0\n\n"
            "szansa = 25%\nx = 0.1667x - 0.2887y + 0.3333\ny = 0.2887x + 0.1667y + 0\n\n"
            "szansa = 25%\nx = 0.1667x + 0.2887y + 0.5\ny = -0.2887x + 0.1667y + 2887\n\n"
            "szansa = 25%\nx = 0.3333x + 0y + 0.667\ny = 0x + 0.3333y + 0\n\n")
        elif(index == 5):
            points, _ = fractals.affine_fractal(60000, [50, 50], 
            [[0.5, 0.5, 0.0], [-0.5, 0.5, 1.0]], 
            [[-0.5, 0.5, 0.0], [-0.5, -0.5, 0.0]])
            self.__instruction_label.config(text = "\n\nAlgorytm: IFS\n"
            "Funkcje:\n"
            "szansa = 50%\nx = 0.5x + 0.5y + 0\ny = -0.5x + 0.5y + 0\n\n"
            "szansa = 50%\nx = -0.5x - 0.5y + 1\ny = -0.5x - 0.5y + 0\n\n")

        elif(index == 6):
            points, _ = fractals.affine_fractal(60000, [50, 50], 
            [[0.5, 0.5, 0.0], [0.5, -0.5, 0.5]], 
            [[-0.5, 0.5, 0.0], [0.5, 0.5, -0.5]])
            self.__instruction_label.config(text = "\n\nAlgorytm: IFS\n"
            "Funkcje:\n"
            "szansa = 50%\nx = 0.5x + 0.5y + 0\ny = 0.5x - 0.5y + 0.5\n\n"
            "szansa = 50%\nx = -0.5x + 0.5y + 0\ny = 0.5x + 0.5y - 0.5\n\n")

        elif(index == 7):
            plot2.set_visible(True)
            points = fractals.mandelbrot_c(1000, 1000, 255, -2, 1, -1.5, 1.5)
            plot2.imshow(np.fliplr(points.T), extent=(-2, 1, -1.5, 1.5), cmap='twilight_shifted')
            canvas.draw()
            self.__instruction_frame.pack(side = tk.LEFT, fill = 'y', pady = 20)
            self.__instruction_label.config(text = "")
            return
        elif(index == 8):
            plot2.set_visible(True)
            points = fractals.julia_c(c = 0.37 + 0.1j, width = 1000, 
                                height = 1000, iterations=255, xmin=-2.0, xmax = 2.0, ymin=-2.0, ymax = 2.0)
            plot2.imshow(np.flipud(np.fliplr(points.T)), extent=(-2.0, 2.0, -2.0, 2.0), cmap='twilight_shifted')
            canvas.draw()
            self.__instruction_frame.pack(side = tk.LEFT, fill = 'y', pady = 20)
            self.__instruction_label.config(text = "Algorytm: Zbiór Julii\nRe: 0.37\nIm: 0.1")
            return
        elif(index == 9):
            image = ImageTk.PhotoImage(Image.open("./fractals/pictures/sierpinski.png"))
            image_label.configure(image = image)
            image_label.image = image
            self.__canvas_frame.pack_forget()
            image_label.pack(side = tk.LEFT, padx = 50, pady = 10)
            self.__instruction_frame.pack(side = tk.LEFT, fill = 'y', pady = 20)
            self.__instruction_label.config(text = "Algorytm: L-System\nStart: F\nKąt: 90\n"
            "Reguły:\nF = F+F-F-F-f+F+F+F-F\nf = fff")
            return

        self.__instruction_frame.pack(side = tk.LEFT, fill = 'y', pady = 20)
        plot(plot1, canvas, points = points)

class LSystemFrame(tk.Frame):
    def __init__(self, parent):

        self.__rules = {}
        self.__turtle_x: float = 0
        self.__turtle_y: float = 0
        self.__turtle_heading : float = 90
        self.__turtle_running = False

        tk.Frame.__init__(self, parent, width = 1366, height = 768)

        widgets_frame = ttk.Frame(self)
        back_button_frame = ttk.Frame(widgets_frame)
        rule_label_frame = ttk.Frame(widgets_frame)
        rule_entry_frame = ttk.Frame(widgets_frame)
        rule_button_frame = ttk.Frame(widgets_frame)
        label_frame = ttk.Frame(widgets_frame)
        entry_frame = ttk.Frame(widgets_frame)
        line_length_frame = ttk.Frame(widgets_frame)
        canvas_buttons_frame = ttk.Frame(widgets_frame)
        save_load_frame = ttk.Frame(widgets_frame)
        rule_list_frame = ttk.Frame(widgets_frame)

        canvas_frame = tk.Frame(self)

        button = ttk.Button(back_button_frame, text="Powrót",
                           command=lambda: parent.switch_frame(StartFrame))
        
        turtle_canvas = tk.Canvas(canvas_frame, width = 1000, height = 650)
        self.__screen = turtle.TurtleScreen(turtle_canvas)
        self.__turtle = turtle.RawTurtle(self.__screen)
        self.__turtle.speed(0)
        self.__screen.delay(0)
        self.__turtle.setheading(self.__turtle_heading)
        self.__screen.cv.bind('<Button-1>', self.__onLeftClick)
        self.__screen.cv.bind('<Button-3>', self.__onRightClick)

        variable_entry = ttk.Entry(rule_entry_frame, width = 10)
        rule_entry  = ttk.Entry(rule_entry_frame, width = 30)
        add_rule_button = ttk.Button(rule_button_frame, text = "Dodaj", 
                        command=lambda : self.__addRule(variable_entry.get(), rule_entry.get(), rules_label))
        clear_rules_button = ttk.Button(rule_button_frame, text = "Wyczyść", command=lambda: self.__clearRules(rules_label))
        start_entry = ttk.Entry(entry_frame, width = 10)
        angle_entry = ttk.Entry(entry_frame, width = 10)
        iter_entry = ttk.Entry(entry_frame, width = 10)
        length_slider = ttk.Scale(line_length_frame, from_=0, to=100, orient=tk.HORIZONTAL)
        self.__draw_button = ttk.Button(canvas_buttons_frame, text = "Rysuj", 
                        command = lambda: self.__drawTurtle(self.__rules, start_entry.get(), 
                                                angle_entry.get(), length_slider.get(), iter_entry.get()))
        self.__stop_button = ttk.Button(canvas_buttons_frame, text = "Stop", command= self.__stopTurtle, state = "disabled")
        self.__clear_button = ttk.Button(canvas_buttons_frame, text = "Wyczyść", command=self.__clearScreen)

        rules_label = ttk.Label(rule_list_frame, text="", justify="left", anchor= tk.W, wraplength= 220)

        self.__save_button = ttk.Button(save_load_frame, text="Zapisz",
                 command = lambda: self.__saveConfig(start_entry.get(), angle_entry.get()))

        self.__load_button = ttk.Button(save_load_frame, text = "Wczytaj",
                    command = lambda: self.__loadConfig(start_entry, angle_entry, rules_label))
        
        self.__image_button = ttk.Button(save_load_frame, text = "Zapisz obraz", 
                                  command = self.__saveImageToFile)

        #######################################################

        widgets_frame.pack(side=tk.LEFT, fill='y', anchor = tk.NW, padx=10, pady = 10)
        back_button_frame.pack(side = tk.TOP, fill = tk.X)
        button.pack(side = tk.TOP, anchor=tk.W)

        rule_label_frame.pack(side = tk.TOP, fill = tk.X, pady = 10)
        ttk.Label(rule_label_frame, text = "Dodaj regułę").pack(side = tk.TOP, anchor = tk.W, pady = 10)
        ttk.Label(rule_label_frame, text = "Zmienna", width = 10, anchor= tk.W).pack(side = tk.LEFT, anchor = tk.W)
        ttk.Label(rule_label_frame, text = "Reguła", anchor = tk.W).pack(side = tk.LEFT, anchor = tk.W, padx = 14)

        rule_entry_frame.pack(side = tk.TOP, fill = tk.X)
        variable_entry.pack(side = tk.LEFT, anchor = tk.W)
        rule_entry.pack(side = tk.RIGHT, anchor = tk.W, padx = 12)

        rule_button_frame.pack(side = tk.TOP, fill = tk.X, pady = 15)
        add_rule_button.pack(side = tk.LEFT, anchor = tk.W)
        clear_rules_button.pack(side = tk.LEFT, anchor = tk.W, padx = 20)

        label_frame.pack(side = tk.TOP, fill = tk.X, pady = 5)
        ttk.Label(label_frame, text = "Start", width = 10, anchor=tk.W).pack( side = tk.LEFT, anchor = tk.W)
        ttk.Label(label_frame, text = "Kąt", width = 10, anchor=tk.W).pack(side= tk.LEFT, anchor = tk.W, padx = 14)
        ttk.Label(label_frame, text = "Iteracje", width = 10, anchor=tk.W).pack(side= tk.LEFT, anchor = tk.W)

        entry_frame.pack(side = tk.TOP, fill = tk.X, pady = 5)
        start_entry.pack(side = tk.LEFT, anchor=tk.W)
        angle_entry.pack(side = tk.LEFT, anchor=tk.W, padx = 12)
        iter_entry.pack(side = tk.LEFT, anchor=tk.W)

        line_length_frame.pack(side = tk.TOP, fill = tk.X, pady = 15)
        tk.Label(line_length_frame, text = "Długość odcinka", anchor=tk.W).pack(side  = tk.TOP, anchor=tk.W)
        length_slider.pack(side = tk.BOTTOM, anchor = tk.W)

        canvas_buttons_frame.pack(side = tk.TOP, fill = tk.X, pady = 5)
        self.__draw_button.pack(side = tk.LEFT, anchor=tk.W)
        self.__stop_button.pack(side = tk.LEFT, anchor=tk.W, padx = 15)
        self.__clear_button.pack(side = tk.LEFT, anchor=tk.W)

        save_load_frame.pack(side = tk.TOP, fill = tk.X)
        self.__save_button.pack(side = tk.LEFT, anchor = tk.W)
        self.__load_button.pack(side = tk.LEFT, anchor= tk.W, padx = 15)
        self.__image_button.pack(side = tk.LEFT, anchor = tk.W)

        rule_list_frame.pack(side=tk.TOP, fill = tk.X, pady = 20)
        rules_label.pack(side = tk.LEFT, anchor=tk.W)

        canvas_frame.pack(side  = tk.LEFT, padx = 40, pady = 10)
        turtle_canvas.pack()

        

    def __addRule(self, variable: str, rule: str, label : tk.Label):

        if len(variable) > 1:
            messagebox.showerror("Błąd", "Zmienna musi być oznaczona pojedynczym znakiem")
            return
        
        if re.search(r'[+\-\[\]]', variable):
            messagebox.showerror("Błąd", "Zmiennymi nie mogą być znaki +, -, [, ]")
            return

        self.__rules[variable] = rule
        self.__refreshRulesLabel(label)

    def __drawTurtle(self, rules, axiom, angle_str, length, iterations):
        
        if len(axiom) < 1: 
            messagebox.showerror("Błąd", "Brak wartości startowej")
            return
        try:
            angle = float(angle_str)
        except:
            messagebox.showerror("Błąd", "Wartość kąta musi być liczbą zmiennoprzecinkową")
            return
        try:
            iter = int(iterations)
        except:
            messagebox.showerror("Błąd", "Iteracje muszą być liczbą naturalną")
            return

        self.__draw_button.configure(state="disabled")
        self.__load_button.configure(state="disabled")
        self.__save_button.configure(state = "disabled")
        self.__image_button.configure(state = "disabled")
        self.__stop_button.configure(state = "normal")
        self.__clear_button.configure(state = "disabled")
        self.__screen.cv.unbind("<Button-1>")
        self.__screen.cv.unbind('<Button-3>')

        route = fractals.l_system_fractal(axiom, rules, iter)

        turtle_stack = deque()
        angle_stack  = deque()

        forward = length

        self.__screen.reset()
        self.__turtle.penup()
        self.__turtle.setpos(self.__turtle_x, self.__turtle_y)
        self.__turtle.seth(self.__turtle_heading)
        self.__turtle.pendown()
        self.__turtle.ht()

        self.__turtle_running = True

        for i in route:
            if(self.__turtle_running == False):
                break
            if i == 'F' : 
                self.__turtle.forward(forward)
            elif i == 'G':
                self.__turtle.forward(forward)
            elif i =='f':
                self.__turtle.penup()
                self.__turtle.forward(forward)
                self.__turtle.pendown()
            elif i == '+':
                self.__turtle.right(angle)
            elif i =='-':
                self.__turtle.left(angle)
            elif i == '[':
                turtle_stack.append(self.__turtle.pos())
                angle_stack.append(self.__turtle.heading())
            elif i == ']':
                new_pos = turtle_stack.pop()
                self.__turtle.penup()
                self.__turtle.setpos(new_pos)
                self.__turtle.seth(angle_stack.pop())
                self.__turtle.pendown()
            else:
                pass
        
        self.__draw_button.configure(state="normal")
        self.__load_button.configure(state="normal")
        self.__save_button.configure(state = "normal")
        self.__image_button.configure(state = "normal")
        self.__stop_button.configure(state = "disabled")
        self.__clear_button.configure(state = "normal")
        self.__screen.cv.bind("<Button-1>", self.__onLeftClick)
        self.__screen.cv.bind('<Button-3>', self.__onRightClick)
        self.__turtle.st()
        self.__turtle_running = False

    def __clearScreen(self):
        self.__turtle_running = False
        self.__screen.reset()
        self.__turtle.penup()
        self.__turtle.setpos(0, 0)
        self.__turtle.seth(90)
        self.__turtle_heading = 90
        self.__turtle_x = 0
        self.__turtle_y = 0
        self.__turtle.pendown()

    def __clearRules(self, label: tk.Label):
        self.__rules.clear()
        self.__refreshRulesLabel(label)

    def __stopTurtle(self):
        self.__turtle_running = False

    def __onLeftClick(self, event):
        # x, y = self.__turtle.getscreen().getcanvas().winfo_pointerxy()
        self.__turtle_x, self.__turtle_y = event.x - self.__turtle.getscreen().window_width()/2, -(event.y - self.__turtle.getscreen().window_height()/2)
        self.__turtle.penup()
        self.__turtle.setpos(self.__turtle_x, self.__turtle_y)
        self.__turtle.pendown()  

    def __onRightClick(self, event):
        x, y =  event.x - self.__turtle.getscreen().window_width()/2, -(event.y - self.__turtle.getscreen().window_height()/2)

        self.__turtle.setheading(self.__turtle.towards(x, y))
        self.__turtle_heading = self.__turtle.heading()     
    
    def __saveConfig(self, start, angle):
        
        file = tk.filedialog.asksaveasfile(mode="w", defaultextension=".lsys", filetypes=[('Fractal files', '*.lsys')])
        if(file is None):
            return
        
        dict = {
            "rules": self.__rules,
            "start" : start,
            "angle": angle
        }
        json.dump(dict, file)
        
        file.close()

    def __loadConfig(self, startEntry: tk.Entry,angleEntry: tk.Entry, rulesLabel: tk.Label):
        file = tk.filedialog.askopenfile(mode="r", defaultextension=".lsys", filetypes=[('Fractal files', '*.lsys')])

        if(file is None):
            return
        
        try:
            info = json.load(file)
        except json.decoder.JSONDecodeError:
            messagebox.showerror("Błąd", "Nieprawidłowy format danych")

        self.__rules = info['rules']
        start = info['start']
        angle = info['angle']
        startEntry.delete(0, tk.END)
        angleEntry.delete(0, tk.END)
        startEntry.insert(0, start)
        angleEntry.insert(0, str(angle))

        file.close()

        self.__refreshRulesLabel(rulesLabel)

    def __refreshRulesLabel(self, rulesLabel : tk.Label):
        rulesLabel['text'] = ""
        for key in self.__rules:
            rulesLabel['text'] += key + " = " + self.__rules[key] + "\n"

    def __saveImageToFile(self):

        if self.winfo_toplevel().state() != "zoomed":
            messagebox.showerror("Błąd", "Zmaksymalizuj okno programu")
            return

        file = tk.filedialog.asksaveasfile(mode="w", defaultextension=".png", filetypes=[('Image files', '*.png')])
        if file is None: 
            return
        canvas = self.__screen.getcanvas()
        x = canvas.winfo_rootx()
        y = canvas.winfo_rooty()
        x1 = x + canvas.winfo_width()
        y1 = y + canvas.winfo_height()
        self.__turtle.ht()
        ImageGrab.grab().crop((x, y, x1, y1)).save(file.name)
        self.__turtle.st()
        
class ChaosGameFrame(tk.Frame):
    def __init__(self, parent):

        tk.Frame.__init__(self, parent, width = 1366, height = 768)

        self.__dot = None
        self.__drag_data = {}
        self.__list_of_rectangles = {}
        self.__currentRectangle = None

        #############################################

        widgets_frame = ttk.Frame(self)
        back_button_frame = ttk.Frame(widgets_frame)
        rectangle_buttons_frame = ttk.Frame(widgets_frame)
        label_frame = ttk.Frame(widgets_frame)
        entry_frame = ttk.Frame(widgets_frame)
        rectangle_frame = ttk.Frame(widgets_frame)
        canvas_buttons_frame = ttk.Frame(widgets_frame)

        button = ttk.Button(back_button_frame, text="Powrót",
                           command=lambda: parent.switch_frame(StartFrame))

        fig = Figure(figsize = (6, 6), dpi = 100)
        self.__plot1 = fig.add_subplot(111)
        self.__plot1.set_xlim(0, 400)
        self.__plot1.set_ylim(0, 400)
        fig.subplots_adjust(0, 0, 1, 1)
        fig.patch.set_facecolor('black')
        self.__plot1.set_facecolor("black")
        
        canvas_frame = tk.Frame(self)
        self.__canvas = FigureCanvasTkAgg(fig, master = canvas_frame)
        toolbar = NavigationToolbar2Tk(self.__canvas, canvas_frame)
        toolbar.winfo_children()[7].configure(command=lambda: save_image(self.__plot1))

        self.__draw_canvas = tk.Canvas(rectangle_frame, width = 400, height = 400, bg="white")

        draw_button = ttk.Button(canvas_buttons_frame, text = "Rysuj", command=lambda : 
                                self.__plotFractal(iterations_entry.get(), depth_entry.get(), color_level_entry.get()))

        iterations_entry = ttk.Entry(entry_frame, width = 10)
        depth_entry = ttk.Entry(entry_frame, width = 10)
        color_level_entry = ttk.Entry(entry_frame, width=10)

        rectangle_add_button = ttk.Button(rectangle_buttons_frame, text="Dodaj prostokąt", command=lambda:
            self.__createRectangle(0, int(self.__draw_canvas["height"])/2, 
            0, 0, 
            int(self.__draw_canvas["width"])/2, 0,
            int(self.__draw_canvas["height"])/2, int(self.__draw_canvas["width"])/2))
        
        rectangle_delete_button = ttk.Button(rectangle_buttons_frame, text = "Usuń prostokąt", command = self.__deleteRectangle)

        save_button = ttk.Button(canvas_buttons_frame, text = "Zapisz", command=self.__saveConfig)
        load_button = ttk.Button(canvas_buttons_frame, text = "Wczytaj", command=self.__loadConfig)

        #########################################

        widgets_frame.pack(side=tk.LEFT, fill='y', anchor = tk.NW, padx=10, pady = 10)
        back_button_frame.pack(side = tk.TOP, fill = tk.X)
        button.pack(side = tk.TOP, anchor=tk.W)

        rectangle_buttons_frame.pack(side = tk.TOP, fill = tk.X, pady = 25)
        rectangle_add_button.pack(side = tk.LEFT, anchor=tk.W)
        rectangle_delete_button.pack(side = tk.LEFT, anchor = tk.W, padx = 20)

        label_frame.pack(side = tk.TOP, fill = tk.X)
        ttk.Label(label_frame, text = "Iteracje", width = 10, anchor = tk.W).pack(side = tk.LEFT, anchor=tk.W)
        ttk.Label(label_frame, text = "Dokładność", anchor = tk.W).pack(side = tk.LEFT, anchor=tk.W, padx = 14)
        ttk.Label(label_frame, text = "Poziom kolorowania", anchor = tk.W).pack(side = tk.LEFT, anchor=tk.W)

        entry_frame.pack(side =tk.TOP, fill = tk.X)
        iterations_entry.pack(side = tk.LEFT, anchor = tk.W)
        depth_entry.pack(side = tk.LEFT, anchor=tk.W, padx = 12)
        color_level_entry.pack(side = tk.LEFT, anchor=tk.W)

        rectangle_frame.pack(side = tk.TOP,fill = tk.X, pady = 15)
        self.__draw_canvas.pack()

        canvas_buttons_frame.pack(side = tk.TOP,fill = tk.X)
        draw_button.pack(side = tk.LEFT, anchor=tk.W)

        canvas_frame.pack(side= tk.LEFT, anchor=tk.W, padx = 50, pady = 10)
        toolbar.update()
        self.__canvas.get_tk_widget().pack()

        save_button.pack(side = tk.LEFT, anchor=tk.W, padx = 12)
        load_button.pack(side = tk.LEFT, anchor=tk.W)

    def __saveConfig(self):
        
        file = tk.filedialog.asksaveasfile(mode="w", defaultextension=".rect", filetypes=[('Fractal files', '*.rect')])
        if(file is None):
            return

        dict = {key: value for key, value in self.__list_of_rectangles.items()}
        
        info = json.dumps(dict)
        file.write(info)
        file.close()

    def __loadConfig(self):

        file = tk.filedialog.askopenfile(mode="r", defaultextension=".rect", filetypes=[('Fractal files', '*.rect')])
        if(file is None):
            return

        self.__draw_canvas.delete("all")
        self.__list_of_rectangles.clear()
        
        try:
            info = json.load(file)
    
            for _, value in info.items():
                if not( all(isinstance(item, float) for item in value)):
                    raise json.decoder.JSONDecodeError("", "", 0)
    
        except json.decoder.JSONDecodeError:
            messagebox.showerror("Błąd", "Nieprawidłowy format danych")
            return
            
        for _, value in info.items():
            x1, y1, x2, y2, x3, y3, x4, y4 = value
            self.__createRectangle(x1, y1, x2, y2, x3, y3, x4, y4)

        file.close()

    def __onClick(self, event):
        rect_id = self.__draw_canvas.find_withtag("current")[0]
        self.__currentRectangle = rect_id
        self.__drag_data[rect_id] = {"x": event.x, "y": event.y}
        x, y = self.__draw_canvas.coords(rect_id)[0], self.__draw_canvas.coords(rect_id)[1]
        self.__draw_canvas.tag_raise(rect_id)
        self.__drawDot(x, y)

    def __drawDot(self, x, y):
        if self.__dot:
            self.__draw_canvas.delete(self.__dot) 
        self.__dot = self.__draw_canvas.create_oval(x - 3, y - 3,
                                              x + 3, y + 3,
                                              outline='red', fill='red')

    def __deleteDot(self):
        self.__draw_canvas.delete(self.__dot)


    def __onDrag(self, event):
        rect_id = self.__currentRectangle

        delta_x = event.x - self.__drag_data[rect_id]["x"]
        delta_y = event.y - self.__drag_data[rect_id]["y"]
        
        self.__draw_canvas.move(rect_id, delta_x, delta_y)

        
        self.__drag_data[rect_id]["x"] = event.x
        self.__drag_data[rect_id]["y"] = event.y

        pts = self.__draw_canvas.coords(rect_id)
        self.__list_of_rectangles[rect_id] = pts

        self.__drawDot(pts[0], pts[1])


    def __onResizeDrag(self, event):
        rect_id = self.__currentRectangle

        delta_x = event.x - self.__drag_data[rect_id]["x"]
        delta_y = event.y - self.__drag_data[rect_id]["y"]

        pts = self.__draw_canvas.coords(rect_id)

        height = math.sqrt((pts[2] - pts[0]) ** 2 + (pts[3] - pts[1]) ** 2)
        width = math.sqrt((pts[6] - pts[0]) ** 2 + (pts[7] - pts[1]) ** 2)

        center_x = (pts[0] + pts[4]) / 2
        center_y = (pts[1] + pts[5]) / 2

        scale_x = 1 + delta_x / 100
        scale_y =  1 - delta_y / 100

        if width < 5 and scale_x < 1:
            scale_x = 1

        if height < 5 and scale_y < 1:
            scale_y = 1

        self.__draw_canvas.scale(rect_id, center_x, center_y, scale_x, scale_y)

        self.__drag_data[rect_id]["x"] = event.x
        self.__drag_data[rect_id]["y"] = event.y

        self.__list_of_rectangles[rect_id] = pts
        self.__drawDot(pts[0], pts[1])

    def __onRotateDrag(self, event):

        rect_id = self.__currentRectangle

        delta_x = event.x - self.__drag_data[rect_id]["x"]
        delta_y = event.y - self.__drag_data[rect_id]["y"]

        angle = math.atan2(delta_y, delta_x) * 0.01

        pts = self.__draw_canvas.coords(rect_id)
        x1, y1, x2, y2, x3, y3, x4, y4 = pts

        center_x = (pts[0] + pts[4]) / 2
        center_y = (pts[1] + pts[5]) / 2

        def rotatePoint(x, y, angle, cx, cy):
            cos_val = math.cos(angle)
            sin_val = math.sin(angle)
            nx = cos_val * (x - cx) - sin_val * (y - cy) + cx
            ny = sin_val * (x - cx) + cos_val * (y - cy) + cy
            return nx, ny

        new_x1, new_y1 = rotatePoint(x1, y1, angle, center_x, center_y)
        new_x2, new_y2 = rotatePoint(x2, y2, angle, center_x, center_y)
        new_x3, new_y3 = rotatePoint(x3, y3, angle, center_x, center_y)
        new_x4, new_y4 = rotatePoint(x4, y4, angle, center_x, center_y)

        self.__draw_canvas.coords(rect_id, new_x1, new_y1, new_x2, new_y2, new_x3, new_y3, new_x4, new_y4)

        pts = self.__draw_canvas.coords(rect_id)
        self.__list_of_rectangles[rect_id] = pts
        self.__drawDot(pts[0], pts[1])

    def __getRandomColor(self):
        return "#{:02x}{:02x}{:02x}".format(random.randint(0, 255), random.randint(0, 255), random.randint(0, 255))

    def __createRectangle(self, x1, y1, x2, y2, x3, y3, x4, y4, width=2):
        outline_color = self.__getRandomColor()
        pts = [(x1, y1), (x2, y2), (x3, y3), (x4, y4)]
        rect = self.__draw_canvas.create_polygon(pts, outline="black", fill="white", width=width, stipple="gray12")
        
        self.__draw_canvas.tag_bind(rect, "<Button-1>", self.__onClick)
        self.__draw_canvas.tag_bind(rect, "<Button-2>", self.__onClick)
        self.__draw_canvas.tag_bind(rect, "<Button-3>", self.__onClick)
        self.__draw_canvas.tag_bind(rect, "<B1-Motion>", self.__onDrag)
        self.__draw_canvas.tag_bind(rect, "<B2-Motion>", self.__onResizeDrag)
        self.__draw_canvas.tag_bind(rect, "<B3-Motion>", self.__onRotateDrag)

        pts = self.__draw_canvas.coords(rect)
        self.__list_of_rectangles[rect] = pts
        self.__currentRectangle = rect

        self.__drawDot(pts[0], pts[1])

    def __deleteRectangle(self):
        if self.__currentRectangle is None:
            return
        self.__deleteDot()
        self.__draw_canvas.delete(self.__currentRectangle)
        if self.__currentRectangle in self.__drag_data:
            self.__drag_data.pop(self.__currentRectangle)
        self.__list_of_rectangles.pop(self.__currentRectangle)
        self.__currentRectangle = None


    def __plotFractal(self, iterations_str, depth_str, color_level_str):

        try:
            iterations = int(iterations_str)
            depth = int(depth_str)
            color_level = int(color_level_str)
        except:
            messagebox.showerror("Nieprawidłowa wartość", "Iteracje, dokładność oraz poziom kolorowania muszą być liczbami naturalnymi")
            return
        
        if color_level > 5 or color_level < 0:
            messagebox.showerror("Nieprawidłowa wartość", "Poziom kolorowania musi być w zakresie 0-5")
            return
        
        if color_level > depth:
            messagebox.showerror("Nieprawidłowa wartość", "Poziom kolorowania nie może być większy od dokładności")
            return


        
        if len(self.__list_of_rectangles) == 0:
            messagebox.showerror("Błąd", "Dodaj co najmniej jeden prostokąt")
            return 
        
        width = int(self.__draw_canvas['width'])
        height = int(self.__draw_canvas['height'])

        new_points, colors = fractals.rectangle_fractal(width, height, self.__list_of_rectangles, iterations, depth, color_level)
        if color_level > 0:
            plot(self.__plot1, self.__canvas, points=new_points, colors = colors, scaled = True)
        else:
            plot(self.__plot1, self.__canvas, points=new_points, scaled = True)
        self.__plot1.axis('off')

#TODO prostokąt sie przykleił do myszki z jakiegoś powodu

def plot(plot1 : Axes, canvas, points : list = None, vertices : list = None, colors : list = None, scaled = False):

    [collection.remove() for collection in plot1.collections]
    [image.remove() for image in plot1.images]

    if(vertices is not None and len(vertices) != 0):
        plot1.scatter(*zip(*vertices), c="y")
    if(points is not None and len(points) != 0):

        xmin = min(points, key=lambda p: p[0])[0]
        ymin = min(points, key=lambda p: p[1])[1]
        xmax = max(points, key=lambda p: p[0])[0]
        ymax = max(points, key=lambda p: p[1])[1]

        start = time.time()

        if scaled:
            img = fractals.draw_image(points = points, colors=colors,  width = int(xmax-xmin), height = int(ymax-ymin))
        else:
            img = fractals.draw_image(points, colors)
    
        # img = np.flipud(img)
        image=Image.fromarray(img)
        
        stop = time.time()
        print("Obraz " + str(stop - start))

        if colors is None:
            height, width = img.shape
        else:
            height, width, _ = img.shape
            
        xmax = width + xmin
        ymax = height + ymin

        plot1.imshow(image, cmap='gist_grey', origin = 'lower', extent=(xmin, xmax, ymin, ymax))

    canvas.draw()

def save_image(subplot : Axes):
    file_path = tk.filedialog.asksaveasfilename(
    defaultextension=".png",
    filetypes=[("PNG files", "*.png"), ("All files", "*.*")])

    subplot.figure.savefig(file_path, dpi = 300)


if __name__ == "__main__":
    app = App()
    app.title("Fraktale")
    app.mainloop()
    

