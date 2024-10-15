from __future__ import division
import tkinter as tk
from tkinter import ttk
from matplotlib.figure import Figure
from matplotlib.axes import Axes
from matplotlib.backends.backend_tkagg import (FigureCanvasTkAgg,  
NavigationToolbar2Tk) 
from PIL import Image
from PIL import ImageTk
import cv2
import numpy as np
from scipy import ndimage
import turtle
from collections import deque
import random
import math

import fractals

class App(tk.Tk):
    def __init__(self):
        tk.Tk.__init__(self)
        self.geometry("1366x768")
        self.state('zoomed')
        self._frame = None
        self.switch_frame(StartFrame)

    def switch_frame(self, frame_class):
        """Destroys current frame and replaces it with a new one."""
        new_frame = frame_class(self)
        if self._frame is not None:
            self._frame.destroy()
        self._frame = new_frame
        self._frame
        self._frame.pack()

class StartFrame(tk.Frame):
    def __init__(self, parent):
        tk.Frame.__init__(self, parent, width = 1366, height = 768)

        # button1 = tk.Button(self, text = "Paproć Barnsley'a", command= lambda: parent.switch_frame(FernFrame))
        button6 = tk.Button(self, text = "Zbiór Mandelbrota i Zbiory Julii", command= lambda: parent.switch_frame(MandelJuliaFrame))
        button2 = tk.Button(self, text = "Gra w chaos", command= lambda: parent.switch_frame(FractalFrame))
        button3 = tk.Button(self, text = "IFS - System Funkcji Iterowanych", command= lambda: parent.switch_frame(AffineFractalFrame))
        button7 = tk.Button(self, text = "L-System", command = lambda : parent.switch_frame(LSystemFrame))
        button4 = tk.Button(self, text = "Instrukcja", command= lambda : parent.switch_frame(TutorialFrame))
        button5 = tk.Button(self, text = "Biblioteka", command=lambda : parent.switch_frame(LibraryFrame))

        button8 = tk.Button(self, text = "Temporary", command= lambda: parent.switch_frame(ChaosGameFrame))

        # button1.place(x = 10, y = 10)
        button6.place(x = 10, y = 10)
        button2.place(x = 10, y = 60)
        button3.place(x = 10, y = 110)
        button7.place(x = 10, y=  160)
        button4.place(x = 10, y = 210)
        button5.place(x = 10, y = 260)

        button8.place(x = 10, y = 360)

# class FernFrame(tk.Frame):
    # def __init__(self, parent):
    #     tk.Frame.__init__(self, parent)
    #     button = tk.Button(self, text="Powrót",
    #                        command=lambda: parent.switch_frame(StartFrame))
    #     button.place(x = 10, y = 20)
    #     tk.Label(self, text='Iteracje').place(x = 10, y = 60)
    #     vcmd = (self.register(self.__validate))

    #     iterationsEntry = tk.Entry(self, validate="all", validatecommand=(vcmd, "%P"))
    #     iterationsEntry.place(x = 10, y = 90)

    #     draw_button = tk.Button(self, text="Rysuj", 
    #                             command=lambda: plot(plot1, canvas,
    #                             fractals.barnsley_fern(int(iterationsEntry.get()))))
    #     draw_button.place(x = 10, y = 120)
    #     fig = Figure(figsize = (5, 5), dpi = 100)
    #     plot1 = fig.add_subplot(111)
    #     canvas_frame = tk.Frame(self)
    #     canvas_frame.place(x = 200, y = 0)
    #     canvas = FigureCanvasTkAgg(fig, master = canvas_frame)
    #     canvas.get_tk_widget().pack()
    #     toolbar = NavigationToolbar2Tk(canvas, canvas_frame) 
    #     toolbar.update()
    #     canvas.get_tk_widget().pack()
    #     tk.Label(self, text="           ").grid(row = 0, column = 3, sticky="W")
        

    # def __validate(self, P):
    #     if str.isdigit(P) or P == "":
    #         return True
    #     else:
    #         return False

class FractalFrame(tk.Frame):

    def __init__(self, parent):

        self.__points = []
        self.__fractal_plotted : bool = False
        self.__vertex_number = 0
        self.__last_iterations_number = 0
        self.__last_jump = 0

        tk.Frame.__init__(self, parent, width = 1366, height = 768)
        vcmdInt = (self.register(self.__validate))
        vcmdFloat = (self.register(self.__validateFloat))

        button = tk.Button(self, text="Powrót",
                           command=lambda: parent.switch_frame(StartFrame))
        point_entry_x = tk.Entry(self, validate="key")
        point_entry_y = tk.Entry(self, validate="key")
        point_accept = tk.Button(self, text="Dodaj punkt", command = lambda: [self.__addPoint(
            point_entry_x.get(), point_entry_y.get(), plot1, canvas), 
            point_entry_x.delete(0, tk.END), point_entry_y.delete(0, tk.END)])
        iterations_entry = tk.Entry(self, validate="all", validatecommand=(vcmdInt, "%P"))
        jump_entry = tk.Entry(self, validate = 'key', validatecommand=(vcmdFloat, "%P"))
        draw_button = tk.Button(self, text="Rysuj", 
                                command=lambda: [self.__plotFractal(plot1, canvas, imageLabel ,iterations_entry.get(),
                                jump_entry.get(), self.__points, restriction_choice.get()), 
                                iterations_entry.delete(0, tk.END), jump_entry.delete(0, tk.END)])
        clear_button = tk.Button(self, text="Wyczyść", command= lambda : [self.__clearPlot(plot1, canvas, imageLabel),
                iterations_entry.delete(0, tk.END), jump_entry.delete(0, tk.END)])

        save_button = tk.Button(self, text="Zapisz", command = lambda : self.__saveConfig())
        load_button = tk.Button(self, text="Wczytaj", command= lambda : self.__loadConfig(plot1, 
                            canvas, imageLabel, iterations_entry, jump_entry))

        fig = Figure(figsize = (5, 5), dpi = 100)
        plot1 = fig.add_subplot(111)

        canvas_frame = tk.Frame(self)
        canvas = FigureCanvasTkAgg(fig, master = canvas_frame)
        toolbar = NavigationToolbar2Tk(canvas, canvas_frame)
        imageLabel = tk.Label(self) 

        button.place(x = 10, y = 10)
        tk.Label(self, text="X  ").place(x = 10, y = 60)
        point_entry_x.place(x = 120, y = 60)
        tk.Label(self, text="Y  ").place(x = 10, y = 90)
        point_entry_y.place(x = 120, y = 90)
        point_accept.place(x = 10, y = 130)
        tk.Label(self, text='Iteracje').place(x = 10, y = 170)
        iterations_entry.place(x = 120, y = 170)
        tk.Label(self, text='Odległość skoku').place(x=10, y = 210)
        jump_entry.place(x = 120, y = 210)
        draw_button.place(x = 10, y = 260)
        clear_button.place(x = 60, y = 260)
        save_button.place(x = 127, y = 260)
        load_button.place(x = 183, y = 260)

        restriction_choice = tk.IntVar()
        restriction_choice.set(0)
        tk.Label(self, text="Ograniczenia (Zwróć uwagę na kolejność dodawania wierzchołków)", wraplength=200).place(x = 10, y = 300)
        tk.Radiobutton(self, text="Brak", variable=restriction_choice, value=0, wraplength=200).place(x = 10, y = 330)
        tk.Radiobutton(self, text="Następny losowy wierzchołek musi być inny niż poprzedni",
                       variable=restriction_choice, value=1, wraplength=200).place(x = 10, y = 370)
        tk.Radiobutton(self, text="Następny wierzchołek nie może być poprzednim na liście",
                       variable=restriction_choice, value=2, wraplength=200).place(x = 10, y = 410)
        tk.Radiobutton(self, text="Następny wierzchołek nie może być oddalony o dwa miejsca na liście od poprzedniego",
                       variable=restriction_choice, value=3, wraplength=200).place(x = 10, y = 450)



        canvas_frame.place(x = 280, y = 10)
        canvas.get_tk_widget().pack()
        toolbar.update()
        canvas.get_tk_widget().pack()
        imageLabel.place(x = 800, y = 10)


    def __validate(self, P):
        if str.isdigit(P) or P == "":
            return True
        else:
            return False
        
    def __validateFloat(self, P):
        if(P == ""):
            return True
        try:
            float(P)
        except(ValueError):
            return False
        return True
    
    def __addPoint(self, xString, yString, plot, canvas):
        

        try:
            x = float(xString)
            y = float(yString)
        except(ValueError):
            return 
        self.__points.append((x, y))
        self.__vertex_number += 1

        if(self.__fractal_plotted):
            plot.clear()
            self.__fractal_plotted = False
        plot.scatter(x, y, c="b")
        canvas.draw()

    def __plotFractal(self, plot1, canvas, imageLabel, iterationsString, jumpString, points : list, restriction : int):

        try:
            iterations = int(iterationsString)
            jump = float(jumpString)
        except(ValueError):
            return
        
        self.__last_iterations_number = iterations
        self.__last_jump = jump
        new_points = points.copy()

        if(restriction == 0):
            new_points = fractals.chaos_game_fractal(iterations, jump, new_points)
            plot(plot1, canvas, new_points , points)
        else:
            new_points = fractals.chaos_game_fractal_restricted(iterations, jump, new_points, restriction)
            plot(plot1, canvas, new_points , points)
        
        image = ImageTk.PhotoImage(image=Image.fromarray(fractals.draw_image(new_points)))
        imageLabel.config(image = image)
        imageLabel.image = image

        self.__fractal_plotted = True
        
    def __clearPlot(self, plot1, canvas, imageLabel : tk.Label):
        plot(plot1, canvas)
        self.__emptyPoints()
        self.__fractal_plotted = False
        self.__last_iterations_number = 0
        self.__last_jump = 0
        imageLabel.config(image=None)
        imageLabel.image = None
    
    def __emptyPoints(self):
        self.__points = []
        self.__vertex_number = 0

    def __saveConfig(self):
        file = tk.filedialog.asksaveasfile(mode="w", defaultextension=".frac", filetypes=[('Fractal files', '*.frac')])
        if(file == None):
            return
        if(self.__vertex_number > 0):
            file.write(str(self.__vertex_number) + "\n")
        for i in range(len(self.__points)):
            file.write(str(self.__points[i][0]) + " " + str(self.__points[i][1]) + "\n")
        if(self.__last_iterations_number > 0):
            file.write(str(self.__last_iterations_number) + "\n")
        if(self.__last_jump != 0):
            file.write(str(self.__last_jump) + "\n")
        file.close()

    def __loadConfig(self, plot1, canvas, imageLabel, iterLabel: tk.Entry, jumpLabel: tk.Entry):
        file = tk.filedialog.askopenfile(mode="r", defaultextension=".frac", filetypes=[('Fractal files', '*.frac')])
        if(file == None):
            return
        self.__clearPlot(plot1, canvas, imageLabel)
        self.__vertex_number = int(file.readline())
        for i in range(self.__vertex_number):
            x, y = file.readline().split()
            self.__points.append((float(x), float(y)))
        self.__last_iterations_number = int(file.readline())
        self.__last_jump = float(file.readline())
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
        self.__functionList = tk.StringVar(value = "") 

        tk.Frame.__init__(self, parent, width = 1366, height = 768)
        vcmd = (self.register(self.__validate))

        button = tk.Button(self, text="Powrót",
                           command=lambda: parent.switch_frame(StartFrame))
        iterations_entry = tk.Entry(self, validate="all", validatecommand=(vcmd, "%P"))
        draw_button = tk.Button(self, text="Rysuj", 
                                command=lambda: self.__plotFractal(plot1, canvas, imageLabel, iterations_entry.get()))
        chance_entry = tk.Entry(self)

        clear_button = tk.Button(self, text="Wyczyść", command=lambda : self.__clearPlot(plot1, canvas, imageLabel, function_label, iterations_entry))
        save_button = tk.Button(self, text = "Zapisz", command=lambda : self.__saveConfig())
        load_button = tk.Button(self, text = "Wczytaj", command=lambda : self.__loadConfig(plot1, canvas, imageLabel, function_label, iterations_entry))
        
        x_entry_1 = tk.Entry(self, width = 10)
        x_entry_2 = tk.Entry(self, width = 10)
        x_entry_3 = tk.Entry(self, width = 10)

        y_entry_1 = tk.Entry(self, width = 10)
        y_entry_2 = tk.Entry(self, width = 10)
        y_entry_3 = tk.Entry(self, width = 10)

        function_add_button = tk.Button(self, text="Dodaj", command = lambda : [self.__addFunction(
            chance_entry.get(), x_entry_1.get(), x_entry_2.get(), x_entry_3.get(),
            y_entry_1.get(), y_entry_2.get(), y_entry_3.get(), function_label
        ), chance_entry.delete(0, tk.END), x_entry_1.delete(0, tk.END), x_entry_2.delete(0, tk.END),
        x_entry_3.delete(0, tk.END), y_entry_1.delete(0, tk.END), y_entry_2.delete(0, tk.END), 
        y_entry_3.delete(0, tk.END)])

        list_canvas = tk.Canvas(self, width=300, height = 230)
        list_frame = tk.Frame(list_canvas, width=300, height = 230)
        function_label = tk.Label(list_frame, text="")
        scrollbar = tk.Scrollbar(self, command=list_canvas.yview)
        list_canvas.configure(yscrollcommand=scrollbar.set)
       
        fig = Figure(figsize = (5, 5), dpi = 100)
        plot1 = fig.add_subplot(111)
        canvas_frame = tk.Frame(self)
        canvas = FigureCanvasTkAgg(fig, master = canvas_frame)
        toolbar = NavigationToolbar2Tk(canvas, canvas_frame) 

        imageLabel = tk.Label(self)
        
        button.place(x = 10, y = 10)
        
        tk.Label(self, text="Dodaj funkcję afiniczną").place(x = 10, y = 50)
        tk.Label(self, text="Procentowa szansa").place(x = 10, y = 80)
        chance_entry.place(x = 120, y = 80)

        tk.Label(self, text = "a").place(x = 10, y = 110)
        tk.Label(self, text = "b").place(x = 80, y = 110)
        tk.Label(self, text = "e").place(x = 150, y = 110)

        x_entry_1.place(x = 10, y = 135)
        x_entry_2.place(x = 80, y = 135)
        x_entry_3.place(x = 150, y = 135)

        tk.Label(self, text = "c").place(x = 10, y = 160)
        tk.Label(self, text = "d").place(x = 80, y = 160)
        tk.Label(self, text = "f").place(x = 150, y = 160)

        y_entry_1.place(x = 10, y = 185)
        y_entry_2.place(x = 80, y = 185)
        y_entry_3.place(x = 150, y = 185)

        function_add_button.place(x = 10, y = 220)

        tk.Label(self, text='Iteracje').place(x = 10, y = 260)
        iterations_entry.place(x = 120, y = 260)
        draw_button.place(x = 10, y = 310)
        clear_button.place(x = 60, y = 310)
        save_button.place(x = 127, y = 310)
        load_button.place(x = 183, y = 310)

        def __scroll(event):
            list_canvas.configure(scrollregion=list_canvas.bbox("all"), width=300, height = 230)

        list_canvas.place(x = 10, y = 350)
        list_canvas.create_window((0, 0), window=list_frame, anchor='nw')
        function_label.pack(side='left')
        scrollbar.place(x = 200, y = 350, height=230)
        list_frame.bind("<Configure>", __scroll)

        canvas_frame.place(x = 300, y = 10) 
        canvas.get_tk_widget().pack()
        toolbar.update()
        canvas.get_tk_widget().pack()

        imageLabel.place(x = 800, y = 10)


    def __validate(self, P):
        if str.isdigit(P) or P == "":
            return True
        else:
            return False
        
    def __addFunction(self, chance : str , x1 : str, x2 : str, x3 : str, y1 : str, y2 : str, y3 : str, label: tk.Label) :

        try:
            self.__addChances(chance)
        except(ValueError):
            return
        
        try:
            self.__x_transform.append([float(x1), float(x2), float(x3)])
        except(ValueError):
            self.__chances.pop()
            return
        
        try:
            self.__y_transform.append([float(y1), float(y2), float(y3)])
        except(ValueError):
            self.__chances.pop()
            self.__x_transform.pop()

        self.__updateLabel(label)
        


    def __clearLists(self):
        self.__chances = []
        self.__x_transform = []
        self.__y_transform = []
    
    def __plotFractal(self, plot1, canvas, imageLabel: tk.Label, iterationsString : str):
        
        try:
            iterations = int(iterationsString)
        except(ValueError):
            return
        
        if(sum(self.__chances) < 100):
            return
        
        self.__last_iterations_number = iterations

        points = fractals.affine_fractal(iterations,self.__chances, self.__x_transform, self.__y_transform)
        plot(plot1, canvas, points)
        image = ImageTk.PhotoImage(Image.fromarray(fractals.draw_image(points)))
        imageLabel.config(image = image)
        imageLabel.image = image

    def __clearPlot(self, plot1, canvas, imageLabel : tk.Label , label: tk.Label, iterEntry : tk.Entry):
        plot(plot1, canvas)
        self.__clearLists()
        label.config(text = "")
        iterEntry.delete(0, tk.END)
        imageLabel.config(image = None)
        imageLabel.image = None
    
    def __addChances(self, chanceString: str) :

        chance = float(chanceString)
        
        sum_of_chances = sum(self.__chances)

        if(sum_of_chances >= 100):
            return
        
        if(100 - sum_of_chances <= chance):
            chance = 100 - sum(self.__chances)

        self.__chances.append(chance)
    
    def __updateLabel(self, functionLabel: tk.Label):
        
        last_chance = self.__chances[-1]
        last_x = self.__x_transform[-1]
        last_y = self.__y_transform[-1]

        functionLabel['text'] += " x = " + str(last_x[0]) +"x " + "%+.2f" % last_x[1] + "y " + "%+ .2f" % last_x[2] + "\n"
        functionLabel['text'] += " y = " + str(last_y[0]) +"x " +"%+.2f" % last_y[1] + "y " + "%+ .2f" % last_y[2] + "\n"
        functionLabel['text'] += "Szansa na wystąpienie: " + str(last_chance) + "%\n\n"

    def __saveConfig(self):
        file = tk.filedialog.asksaveasfile(mode="w", defaultextension=".ifs", filetypes=[('Fractal files', '*.ifs')])
        if(file == None):
            return
        file.write(str(len(self.__chances)) + "\n")
        for i in range(len(self.__chances)):
            file.write(str(self.__chances[i]) + "\n")
            file.write(str(self.__x_transform[i]) + "\n")
            file.write(str(self.__y_transform[i]) + "\n")
        file.write(str(self.__last_iterations_number) +"\n")
        file.close()

    def __loadConfig(self, plot1, canvas, imageLabel : tk.Label , label : tk.Label, iterEntry : tk.Entry):
        file = tk.filedialog.askopenfile(mode="r", defaultextension=".ifs", filetypes=[('Fractal files', '*.ifs')])
        if(file == None):
            return
        self.__clearPlot(plot1, canvas, imageLabel, label, iterEntry)
        count = int(file.readline())
        for i in range(count):
            self.__chances.append(float(file.readline()))
            line = file.readline()
            self.__x_transform.append([float(item) for item in line[1:-2].split(", ")])
            line = file.readline()
            self.__y_transform.append([float(item) for item in line[1:-2].split(", ")])
            self.__updateLabel(label)
        self.__last_iterations_number = int(file.readline())
        iterEntry.insert(0, str(self.__last_iterations_number))

class MandelJuliaFrame(tk.Frame) :
    def __init__(self, parent):
        tk.Frame.__init__(self, parent , width = 1366, height = 768)

        self.__xmin = -2.0
        self.__xmax = 2.0
        self.__ymin = -2.0
        self.__ymax = 2.0

        imageLabel = tk.Label(self)

        button = tk.Button(self, text="Powrót",
                           command=lambda: parent.switch_frame(StartFrame))
        
        draw_button = tk.Button(self, text = "Rysuj", 
            command = lambda : [self.__setLimits(plot_choice.get()) ,self.__plotFractal(self.__plot, canvas, imageLabel, 
                    c_real_entry.get(), c_imag_entry.get(), plot_choice.get())])
        clear_button = tk.Button(self, text = "Wyczyść", 
            command = lambda : self.__clearPlot(self.__plot, canvas, imageLabel))
        
        save_image_button =tk.Button(self, text = "Zapisz obraz" , command = lambda : self.__saveImageToFile(imageLabel))
        
        plot_choice = tk.IntVar()
        plot_choice.set(0)
        choose_mandel_radio = tk.Radiobutton(self, text = "Zbiór Mandelbrota", variable=plot_choice, value = 0)
        choose_julia_radio = tk.Radiobutton(self, text = "Zbiór Julii", variable=plot_choice, value = 1)

        c_real_entry = tk.Entry(self, width = 10)
        c_imag_entry = tk.Entry(self, width = 10)

        fig = Figure(figsize = (5, 5), dpi = 100)
        self.__plot = fig.add_subplot(111)
        self.__plot.set_xlim(self.__xmin, self.__xmax)
        self.__plot.set_ylim(self.__ymin, self.__ymax)
        canvas_frame = tk.Frame(self)
        canvas = FigureCanvasTkAgg(fig, master = canvas_frame)
        toolbar = NavigationToolbar2Tk(canvas, canvas_frame) 

        button.place(x = 10, y = 10)
        c_real_entry.place(x = 10, y = 60)
        c_imag_entry.place(x = 90, y = 60)
        choose_mandel_radio.place(x = 10, y = 100)
        choose_julia_radio.place(x = 10, y = 130)
        draw_button.place(x = 10, y = 180)
        clear_button.place(x = 70, y = 180)
        save_image_button.place(x = 10, y = 220)

        canvas_frame.place(x = 280, y = 10)
        canvas.get_tk_widget().pack()
        toolbar.update()
        canvas.get_tk_widget().pack()
        imageLabel.place(x = 800, y = 10)

        def callback_wrapper(event = None):
            xlim = self.__plot.get_xlim()
            ylim = self.__plot.get_ylim()

            self.__xmin, self.__xmax = xlim 
            self.__ymin, self.__ymax = ylim
            self.__plotFractal(self.__plot, canvas, imageLabel, c_real_entry.get(), c_imag_entry.get(),
                                               plot_choice.get())
            

        fig.canvas.mpl_connect('button_release_event', callback_wrapper)
        #self.__plot.callbacks.connect('xlim_changed', callback_wrapper)



    def __plotFractal(self, plot1, canvas, imageLabel : tk.Label, c_real_string : str, c_imag_string : str, plot_choice):

        if(plot_choice == 0):
            points = fractals.mandelbrot_c(1000, 1000, 255, self.__xmin, self.__xmax, self.__ymin, self.__ymax)
        else:
            try:
                c_real = float(c_real_string)
                c_imag = float(c_imag_string)
            except(ValueError):
                return
            points = fractals.julia_c(c_real + c_imag *1j, 1000, 1000, 255, self.__xmin, self.__xmax, self.__ymin, self.__ymax)

        normalized_points = cv2.normalize(points, None, 0, 255, cv2.NORM_MINMAX)
        normalized_points = np.uint8(normalized_points)
        colored_points = cv2.applyColorMap(normalized_points, cv2.COLORMAP_HOT)
        colored_points = cv2.flip(colored_points, 0)

        image = Image.fromarray(colored_points)
        res_image = image.resize((500, 500))
        image = ImageTk.PhotoImage(res_image)
        imageLabel.config(image = image)
        imageLabel.image = image


        points = ndimage.rotate(points, 90)
        plot1.clear()
        plot1.imshow(np.flipud(np.fliplr(points.T)), extent=(self.__xmin, self.__xmax, self.__ymin, self.__ymax))
        canvas.draw()
        
        
    def __clearPlot(self, plot1, canvas, imageLabel : tk.Label):
        plot1.clear()
        canvas.draw()
        imageLabel.config(image = None)
        imageLabel.image = None

    def __saveImageToFile(self, imageLabel: tk.Label):
        image = imageLabel.image
        saveImageToFile(image)

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

        button = tk.Button(self, text="Powrót",
                           command=lambda: parent.switch_frame(StartFrame))
        chaos_game_tutorial_button = tk.Button(self, text = "Gra w chaos")
        affine_tutorial_button = tk.Button(self, text = "Funkcje afiniczne")
        mandelbrot_tutorial_button = tk.Button(self, text = "Zbiór Mandelbrota")
        julia_tutorial_button = tk.Button(self, text = "Zbiory Julii")


        button.place(x = 10, y = 10)
        tk.Label(self, text="Wprowadzenie", font=("Arial", 30)).place(x = 10, y = 60)
        tk.Label(self, text="Fraktal to figura samopodobna itd."). place(x = 10, y = 130)

        chaos_game_tutorial_button.place(x = 10, y = 200)
        affine_tutorial_button.place(x = 10, y = 230)
        mandelbrot_tutorial_button.place(x = 10, y = 260)
        julia_tutorial_button.place(x = 10, y = 290)

class LibraryFrame(tk.Frame):
    def __init__(self, parent):
        tk.Frame.__init__(self, parent, width = 1366, height = 768)

        button = tk.Button(self, text="Powrót",
                           command=lambda: parent.switch_frame(StartFrame))
        

        fig = Figure(figsize = (5, 5), dpi = 100)
        plot1 = fig.add_subplot(111)
        canvas_frame = tk.Frame(self)
        canvas = FigureCanvasTkAgg(fig, master = canvas_frame)

        fractalList = tk.Listbox(self, selectmode='single')

        
        imageLabel = tk.Label(self)

        list = ["Trójkąt Sierpińskiego","Dywan Sierpińskiego", "Paproć Barnsley'a", "Fraktal Viscek'a", 
                "Krzywa Koch'a", "Smok Heighway'a", "Krzywa Levy'ego", "Zbiór Mandelbrota", "Zbiór Julii - Przykład"]
        for i in range(len(list)):
            fractalList.insert(i, list[i])
        fractalList.bind('<<ListboxSelect>>', lambda event:  self.__onSelect(event, plot1, canvas, imageLabel))

        button.place(x=10, y = 10)
        fractalList.place(x = 10, y = 60)

        imageLabel.place( x = 800, y = 10)

        canvas_frame.place(x = 300, y = 10)
        canvas.get_tk_widget().pack()
        canvas.get_tk_widget().pack()

    def __onSelect(self, event : tk.Event, plot1, canvas, imgLabel : tk.Label):
        w = event.widget
        index = w.curselection()[0]
        value = w.get(index)

        points = []

        if(index == 0):
            points = fractals.chaos_game_fractal(60000, 0.5, [(0, 0), (10, 0), (5, 8.65)])
            plot1.set_xlim(10)
            plot1.set_ylim(10)
        elif(index == 1):
            points = fractals.chaos_game_fractal(60000, (2/3), 
                [(0, 0), (12, 0), (12, 12), (0, 12), (0, 6), (6, 0), (12, 6), (6, 12)])
            plot1.set_xlim(10)
            plot1.set_ylim(10)
        elif(index == 2):
            points = fractals.barnsley_fern(60000)
            plot1.set_xlim(10)
            plot1.set_ylim(10)
        elif(index == 3):
            points = fractals.chaos_game_fractal(60000, 0.667,
                     [(0, 0),(12, 0), (12, 12), (0, 12), (6, 6)])
            plot1.set_xlim(10)
            plot1.set_ylim(10)
        elif(index == 4):
            points = fractals.affine_fractal(60000, [25, 25, 25, 25],
            [[0.3333, 0.0, 0.0], [0.1667, -0.2887, 0.3333], [0.1667, 0.2887, 0.5], [0.3333, 0.0, 0.667]],
            [[0.0, 0.3333, 0.0], [0.2887, 0.1667, 0.0],[-0.2887, 0.1667, 0.2887], [0.0, 0.3333, 0.0]])
            plot1.set_xlim(10)
            plot1.set_ylim(10)
        elif(index == 5):
            points = fractals.affine_fractal(60000, [50, 50], 
            [[0.5, 0.5, 0.0], [-0.5, 0.5, 1.0]], 
            [[-0.5, 0.5, 0.0], [-0.5, -0.5, 0.0]])
            plot1.set_xlim(10)
            plot1.set_ylim(10)
        elif(index == 6):
            points = fractals.affine_fractal(60000, [50, 50], 
            [[0.5, 0.5, 0.0], [0.5, -0.5, 0.5]], 
            [[-0.5, 0.5, 0.0], [0.5, 0.5, -0.5]])
            plot1.set_xlim(10)
            plot1.set_ylim(10)
        elif(index == 7):
            plot(plot1, canvas)
            points = fractals.mandelbrot_c(500, 500, 255, -2, 1, -1.5, 1.5)
            plot1.imshow(points.T, aspect='auto')
            canvas.draw()
            image = ImageTk.PhotoImage(image=Image.fromarray(points))
            imgLabel.config(image=image)
            imgLabel.image = image
            return
        elif(index == 8):
            plot(plot1, canvas)
            points = fractals.julia_c(c = 0.37 + 0.1j, width = 500, 
                                height = 500, iterations=255, xmin=-2.0, xmax = 2.0, ymin=-2.0, ymax = 2.0)
            plot1.imshow(points.T, aspect= 'auto')
            canvas.draw()
            image = ImageTk.PhotoImage(image=Image.fromarray(points))
            imgLabel.config(image=image)
            imgLabel.image = image
            return

        plot(plot1, canvas, points = points)
        img = fractals.draw_image(points)
        image = ImageTk.PhotoImage(image=Image.fromarray(img))
        imgLabel.config(image=image)
        imgLabel.image = image

    # def __loadFromFile(self, filename : str):
    #     chances = []
    #     x_transform = []
    #     y_transform = []

    #     file = open(filename)
    #     if(file == None):
    #         return
    #     count = int(file.readline())
    #     for i in range(count):
    #         chances.append(float(file.readline()))
    #         line = file.readline()
    #         x_transform.append([float(item) for item in line[1:-2].split(", ")])
    #         line = file.readline()
    #         y_transform.append([float(item) for item in line[1:-2].split(", ")])
        
    #     return (chances, x_transform, y_transform)

class LSystemFrame(tk.Frame):
    def __init__(self, parent):

        self.__rules = {}
        self.__turtle_x: float = 0
        self.__turtle_y: float = 0
        self.__turtle_heading : float = 90
        self.__turtle_running = False

        tk.Frame.__init__(self, parent, width = 1366, height = 768)

        button = tk.Button(self, text="Powrót",
                           command=lambda: parent.switch_frame(StartFrame))
        
        turtle_canvas = tk.Canvas(self, width = 1000, height = 650)
        self.__screen = turtle.TurtleScreen(turtle_canvas)
        self.__turtle = turtle.RawTurtle(self.__screen)
        self.__turtle.speed(0)
        self.__screen.delay(0)
        self.__screen.cv.bind('<Button-1>', self.__onLeftClick)
        self.__screen.cv.bind('<Button-3>', self.__onRightClick)

        variable_entry = tk.Entry(self, width = 10)
        rule_entry  = tk.Entry(self, width = 30)
        add_rule_button = tk.Button(self, text = "Dodaj", 
                        command=lambda : self.__addRule(variable_entry.get(), rule_entry.get(), rules_label))
        clear_rules_button = tk.Button(self, text = "Wyczyść", command=lambda: self.__clearRules(rules_label))
        start_entry = tk.Entry(self, width = 10)
        angle_entry = tk.Entry(self, width = 10)
        iter_entry = tk.Entry(self, width = 10)
        length_slider = tk.Scale(self, from_=0, to=100, orient=tk.HORIZONTAL)
        self.draw_button = tk.Button(self, text = "Rysuj", 
                        command = lambda: self.__drawTurtle(self.__rules, start_entry.get(), 
                                                angle_entry.get(), length_slider.get(), iter_entry.get()))
        self.stop_button = tk.Button(self, text = "Stop", command= self.__stopTurtle)
        self.clear_button = tk.Button(self, text = "Wyczyść", command=self.__clearScreen)

        rules_label = tk.Label(self, text="", justify="left")

        turtle_canvas.place(x = 300, y = 10)
        button.place(x=10, y = 10)
        tk.Label(self, text = "Dodaj regułę").place(x = 10, y = 50)
        tk.Label(self, text = "Zmienna").place(x = 10, y = 80)
        tk.Label(self, text = "Reguła").place(x = 80, y = 80)
        variable_entry.place(x = 10, y = 120)
        rule_entry.place(x = 80, y = 120)
        add_rule_button.place(x = 10, y = 160)
        clear_rules_button.place(x = 80, y = 160)
        tk.Label(self, text = "Start").place(x = 10, y = 200)
        start_entry.place(x = 10, y = 240)
        tk.Label(self, text = "Kąt").place(x = 80, y = 200)
        angle_entry.place(x = 80, y = 240)
        tk.Label(self, text = "Iteracje").place(x = 150, y = 200)
        iter_entry.place(x = 150, y = 240)
        tk.Label(self, text = "Długość odcinka").place(x = 10, y = 280)
        length_slider.place(x = 10, y = 300)
        self.draw_button.place(x = 10, y = 360)
        self.stop_button.place(x = 80, y = 360)
        self.clear_button.place(x = 150, y = 360)
        rules_label.place(x = 10, y = 400)

    def __addRule(self, variable: str, rule: str, label : tk.Label):

        if len(variable) > 1:
            return

        if variable in self.__rules:
            return

        self.__rules[variable] = rule
        label['text'] += variable + " = " + rule + "\n"

    def __drawTurtle(self, rules, axiom, angle_str, length, iterations):
        
        if len(axiom) < 1: 
            return
        try:
            angle = float(angle_str)
            iter = int(iterations)
        except:
            return

        # canvas = self.__turtle.getscreen()

        self.draw_button.configure(state="disabled")
        self.__screen.cv.unbind("<Button-1>")
        self.__screen.cv.unbind('<Button-3>')

        route = fractals.l_system_fractal(axiom, rules, iter)

        turtle_stack = deque()
        angle_stack  = deque()

        forward = length

        # canvas.clear()
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
        
        self.draw_button.configure(state="normal")
        self.__screen.cv.bind("<Button-1>", self.__onLeftClick)
        self.__screen.cv.bind('<Button-3>', self.__onRightClick)
        self.__turtle.st()
        self.__turtle_running = False

    def __clearScreen(self):
        self.__turtle_running = False
        self.__screen.reset()
        self.__turtle.penup()
        self.__turtle.setpos(self.__turtle_x, self.__turtle_y)
        self.__turtle.seth(self.__turtle_heading)
        self.__turtle.pendown()

    def __clearRules(self, label: tk.Label):
        self.__rules.clear()
        label['text'] = ""


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


class ChaosGameFrame(tk.Frame):
    def __init__(self, parent):

        tk.Frame.__init__(self, parent, width = 1366, height = 768)

        self.__dot : int = 2

        self.__drag_data = {}

        self.__list_of_rectangles = {}

        button = tk.Button(self, text="Powrót",
                           command=lambda: parent.switch_frame(StartFrame))

        fig = Figure(figsize = (5, 5), dpi = 100)
        self.__plot1 = fig.add_subplot(111)
        self.__plot1.set_xlim(0, 300)
        self.__plot1.set_ylim(0, 300)
        
        canvas_frame = tk.Frame(self)
        self.__canvas = FigureCanvasTkAgg(fig, master = canvas_frame)
        toolbar = NavigationToolbar2Tk(self.__canvas, canvas_frame)

        self.__draw_canvas = tk.Canvas(self, width = 300, height = 300, bg="white")

        x_entry_1 = tk.Entry(self, width = 10)
        x_entry_2 = tk.Entry(self, width = 10)
        x_entry_3 = tk.Entry(self, width = 10)

        y_entry_1 = tk.Entry(self, width = 10)
        y_entry_2 = tk.Entry(self, width = 10)
        y_entry_3 = tk.Entry(self, width = 10)

        function_add_button = tk.Button(self, text = "Dodaj" ,command= 
            lambda: self.__drawFunction(x_entry_1.get(), x_entry_2.get(), x_entry_3.get(),
            y_entry_1.get(), y_entry_2.get(), y_entry_3.get()))
        draw_button = tk.Button(self, text = "Rysuj", command=self.__calculatePoints)

        #############################################

        rectangle_add_button = tk.Button(self, text="Prostokąt", command=lambda:
                                         self.create_rectangle(0, 0, int(self.__draw_canvas["width"])/2, int(self.__draw_canvas["height"])/2))
        
        rectangle_add_button.place(x = 10, y = 280)

        ###########################################

        button.place(x = 10, y = 10)
        draw_button.place(x = 10, y = 60)
        
        canvas_frame.place(x = 350, y = 10) 
        # canvas.get_tk_widget().pack()
        toolbar.update()
        self.__canvas.get_tk_widget().pack()

        tk.Label(self, text = "a").place(x = 10, y = 110)
        tk.Label(self, text = "b").place(x = 80, y = 110)
        tk.Label(self, text = "e").place(x = 150, y = 110)

        x_entry_1.place(x = 10, y = 135)
        x_entry_2.place(x = 80, y = 135)
        x_entry_3.place(x = 150, y = 135)

        tk.Label(self, text = "c").place(x = 10, y = 160)
        tk.Label(self, text = "d").place(x = 80, y = 160)
        tk.Label(self, text = "f").place(x = 150, y = 160)

        y_entry_1.place(x = 10, y = 185)
        y_entry_2.place(x = 80, y = 185)
        y_entry_3.place(x = 150, y = 185)

        function_add_button.place(x = 10, y = 230)

        self.__draw_canvas.place(x = 10, y = 350)

        
    def __drawFunction(self, a, b, e, c, d, f):

        width = int(self.__draw_canvas["width"])
        height = int(self.__draw_canvas["height"])

        main_rectangle = np.array([[0, 0], [0, height], [width, height] ,[width, 0]])
        pts = []

        for point in main_rectangle:
            x = (float(a) * point[0]) + (float(b) * point[1]) + (float(e) * width)
            y = (float(c) * point[0]) + (float(d) * point[1]) + (float(f) * height)
            pts.append([x, y])
            self.__draw_canvas.create_oval(x-3, height-y-3, x+3, height-y+3, fill="red")

        for i in range(len(pts)):
                x1, y1 = pts[i]
                x2, y2 = pts[(i + 1) % len(pts)] 
                self.__draw_canvas.create_line(x1, height-y1, x2, height-y2)

        for i in pts:
            i[1]  =height - i[1]
            
        self.__list_of_rectangles.append(pts)
        # self.__function_list.append([float(a),float(b),float(c),float(d),float(e)*width,float(f)*height])
        # self.__drawListOfPoints(pts)

    def __on_click(self, event):
        rect_id = self.__draw_canvas.find_withtag("current")[0]
        self.__drag_data[rect_id] = {"x": event.x, "y": event.y}
        x, y = self.__draw_canvas.coords(rect_id)[0], self.__draw_canvas.coords(rect_id)[1]
        self.__draw_dot(x, y)

    def __draw_dot(self, x, y):
        if self.__dot:
            self.__draw_canvas.delete(self.__dot) 
        self.__dot = self.__draw_canvas.create_oval(x - 3, y - 3,
                                              x + 3, y + 3,
                                              outline='red', fill='red')


    def __on_drag(self, event):
        rect_id = self.__draw_canvas.find_withtag("current")[0]

        delta_x = event.x - self.__drag_data[rect_id]["x"]
        delta_y = event.y - self.__drag_data[rect_id]["y"]
        
        self.__draw_canvas.move(rect_id, delta_x, delta_y)

        
        self.__drag_data[rect_id]["x"] = event.x
        self.__drag_data[rect_id]["y"] = event.y

        pts = self.__draw_canvas.coords(rect_id)
        pts = [pts[i:i + 2] for i in range(0, len(pts), 2)]
        self.__list_of_rectangles[rect_id] = pts

        self.__draw_dot(pts[0][0], pts[0][1])


    def __on_resize_drag(self, event):
        rect_id = self.__draw_canvas.find_withtag("current")[0]

        delta_x = event.x - self.__drag_data[rect_id]["x"]
        delta_y = event.y - self.__drag_data[rect_id]["y"]

        pts = self.__draw_canvas.coords(rect_id)
        x1, x2, y1, y2 = pts[0],pts[4],pts[1], pts[5]

        center_x = (pts[0] + pts[4]) / 2
        center_y = (pts[1] + pts[5]) / 2

        scale_x = 1 + delta_x / 100
        scale_y =  1 - delta_y / 100

        self.__draw_canvas.scale(rect_id, center_x, center_y, scale_x, scale_y)

        self.__drag_data[rect_id]["x"] = event.x
        self.__drag_data[rect_id]["y"] = event.y

        pts = self.__draw_canvas.coords(rect_id)
        pts = [pts[i:i + 2] for i in range(0, len(pts), 2)]
        self.__list_of_rectangles[rect_id] = pts
        self.__draw_dot(pts[0][0], pts[0][1])

    def __on_rotate_drag(self, event):

        rect_id = self.__draw_canvas.find_withtag("current")[0]

        delta_x = event.x - self.__drag_data[rect_id]["x"]
        delta_y = event.y - self.__drag_data[rect_id]["y"]

        angle = math.atan2(delta_y, delta_x) * 0.02

        pts = self.__draw_canvas.coords(rect_id)
        x1, y1, x2, y2, x3, y3, x4, y4 = pts

        center_x = (pts[0] + pts[4]) / 2
        center_y = (pts[1] + pts[5]) / 2

        def rotate_point(x, y, angle, cx, cy):
            cos_val = math.cos(angle)
            sin_val = math.sin(angle)
            nx = cos_val * (x - cx) - sin_val * (y - cy) + cx
            ny = sin_val * (x - cx) + cos_val * (y - cy) + cy
            return nx, ny

        # Oblicz nowe współrzędne dla każdego z wierzchołków
        new_x1, new_y1 = rotate_point(x1, y1, angle, center_x, center_y)
        new_x2, new_y2 = rotate_point(x2, y2, angle, center_x, center_y)
        new_x3, new_y3 = rotate_point(x3, y3, angle, center_x, center_y)
        new_x4, new_y4 = rotate_point(x4, y4, angle, center_x, center_y)

        # Ustaw nowe współrzędne prostokąta
        self.__draw_canvas.coords(rect_id, new_x1, new_y1, new_x2, new_y2, new_x3, new_y3, new_x4, new_y4)

        pts = self.__draw_canvas.coords(rect_id)
        pts = [pts[i:i + 2] for i in range(0, len(pts), 2)]
        self.__list_of_rectangles[rect_id] = pts
        self.__draw_dot(pts[0][0], pts[0][1])

    def get_random_color(self):
        return "#{:02x}{:02x}{:02x}".format(random.randint(0, 255), random.randint(0, 255), random.randint(0, 255))

    def create_rectangle(self, x1, y1, x2, y2, width=2):
        outline_color = self.get_random_color()
        pts = [(x1, y2), (x1, y1), (x2, y1), (x2, y2)]
        rect = self.__draw_canvas.create_polygon(pts, outline=outline_color, fill="white", width=width, stipple="gray12")
        
        self.__draw_canvas.tag_bind(rect, "<Button-1>", self.__on_click)
        self.__draw_canvas.tag_bind(rect, "<Button-2>", self.__on_click)
        self.__draw_canvas.tag_bind(rect, "<Button-3>", self.__on_click)
        self.__draw_canvas.tag_bind(rect, "<B1-Motion>", self.__on_drag)
        self.__draw_canvas.tag_bind(rect, "<B2-Motion>", self.__on_resize_drag)
        self.__draw_canvas.tag_bind(rect, "<B3-Motion>", self.__on_rotate_drag)

        pts = self.__draw_canvas.coords(rect)
        pts = [pts[i:i + 2] for i in range(0, len(pts), 2)]
        self.__list_of_rectangles[rect] = pts

        self.__draw_dot(pts[0][0], pts[0][1])

    def __calculatePoints(self):

        width = int(self.__draw_canvas["width"])
        height = int(self.__draw_canvas["height"])
        
        main_rectangle = np.array([[0, 0], [0, height],[width, height] ,[width, 0]])
        src = np.array(main_rectangle)
        src_homogeneous = np.hstack([src, np.ones((src.shape[0], 1))])

        function_list = []

        if(len(self.__list_of_rectangles) > 0):
            for i in self.__list_of_rectangles.values():
                dst_i = i
                dst = np.array(dst_i)
                transformation_matrix, _, _, _ = np.linalg.lstsq(src_homogeneous, dst, rcond=None)
                a, b = transformation_matrix[0]
                c, d = transformation_matrix[1]
                e, f = transformation_matrix[2]
                function_list.append([a, b, c, d, e, f])

        new_points = []

        for i in range(100000):
            point = (random.uniform(0, width), random.uniform(0, height))
            for j in range(20):
                a, b, c, d, e, f = function_list[random.randint(0, len(function_list) - 1)]
                
                new_point = (a * point[0]+ b*point[1] + e, height -(c*point[0]+d*point[1]+f))
                point = new_point
            new_points.append(new_point)

        plot(self.__plot1, self.__canvas, points=new_points)

def plot(plot1 : Axes, canvas, points : list = None, vertices : list = None):

    plot1.clear()

    if(vertices != None and len(vertices) != 0):
        plot1.scatter(*zip(*vertices), c="b")
    if(points != None and len(points) != 0):
        plot1.scatter(*zip(*points), s=0.09, c="g")
    canvas.draw()

def saveImageToFile(image):
    file = tk.filedialog.asksaveasfilename(defaultextension = ".png")
    if(file):
        img = ImageTk.getimage(image)
        img.save(file)
        img.close()


if __name__ == "__main__":
    app = App()
    app.mainloop()
    

