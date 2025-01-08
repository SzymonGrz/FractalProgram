from __future__ import division
import tkinter as tk
from tkinter import ttk
from matplotlib.figure import Figure
from matplotlib.axes import Axes
from matplotlib.backends.backend_tkagg import (FigureCanvasTkAgg, NavigationToolbar2Tk) 
from tkinter import messagebox
import json

import functions.fractals as fractals
from functions.image_functions import plot, save_image

class ChaosGameFrame(tk.Frame):

    def __init__(self, parent):

        ####################################

        self.__points = []
        self.__fractal_plotted : bool = False
        self.__vertex_number = 0
        self.__last_iterations_number = 0
        self.__last_jump = 0
        self.__changed_index = -1

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
        list_outer_frame = ttk.Frame(widgets_frame)
        list_frame = ttk.Frame(list_outer_frame)

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
                           command=lambda: parent.switch_frame("start"))
        self.__point_entry_x = ttk.Entry(x_entry_frame, validate="key")
        self.__point_entry_y = ttk.Entry(y_entry_frame, validate="key")
        point_accept = ttk.Button(add_point_frame, text="Dodaj", command = lambda: [self.__addPoint(
            self.__point_entry_x.get(), self.__point_entry_y.get(), plot1, canvas, list_frame),
            self.__clearEntries()])
        point_delete = ttk.Button(add_point_frame, text="Usuń", command = lambda: [self.__deletePoint(
            plot1, canvas, list_frame),
            self.__clearEntries()])
        iterations_entry = ttk.Entry(iter_frame)
        jump_entry = ttk.Entry(jump_frame)
        draw_button = ttk.Button(canvas_buttons_frame, text="Rysuj", 
                                command=lambda: [self.__plotFractal(plot1, canvas ,iterations_entry.get(),
                                jump_entry.get(), self.__points, restriction_choice.get(), color_choice.get())])
        clear_button = ttk.Button(canvas_buttons_frame, text="Wyczyść", command= lambda : [self.__clearPlot(plot1, canvas,list_frame),
                iterations_entry.delete(0, tk.END), jump_entry.delete(0, tk.END), self.__clearEntries()])

        save_button = ttk.Button(canvas_buttons_frame, text="Zapisz", command = lambda : self.__saveConfig())
        load_button = ttk.Button(canvas_buttons_frame, text="Wczytaj", command= lambda : self.__loadConfig(plot1, 
                            canvas, iterations_entry, jump_entry, list_frame))
        
        color_check = ttk.Checkbutton(color_frame, variable=color_choice)

        def __scroll(event):
            list_canvas.configure(scrollregion=list_canvas.bbox("all"), width=120, height = 230)

        list_canvas = tk.Canvas(list_outer_frame, width=120, height = 230)
        list_frame = ttk.Frame(list_canvas, width=120, height = 230)
        scrollbar = ttk.Scrollbar(list_outer_frame, command=list_canvas.yview)
        list_canvas.configure(yscrollcommand=scrollbar.set)
        list_canvas.create_window((0, 0), window=list_frame, anchor='nw')
        list_frame.bind("<Configure>", __scroll)

        ####################################

        widgets_frame.pack(side=tk.LEFT, fill='y', anchor = tk.NW, padx=10, pady = 5)
        back_button_frame.pack(side = tk.TOP, fill='x', pady=5)
        button.pack(side=tk.LEFT, anchor = tk.W)

        x_entry_frame.pack(side = tk.TOP, fill = 'x', pady = 5)
        ttk.Label(x_entry_frame, text="X", width= 20, anchor=tk.W).pack(side = tk.LEFT, anchor = tk.W)
        self.__point_entry_x.pack(side = tk.LEFT)

        y_entry_frame.pack(side = tk.TOP, fill = 'x', pady = 5)
        ttk.Label(y_entry_frame, text="Y", width= 20, anchor=tk.W).pack(side = tk.LEFT, anchor = tk.W)
        self.__point_entry_y.pack(side = tk.LEFT)

        add_point_frame.pack(side = tk.TOP, fill = 'x', pady = 10)
        point_accept.pack(side=tk.LEFT, anchor = tk.W)
        point_delete.pack(side = tk.LEFT, anchor= tk.W, padx = 15)

        iter_frame.pack(side = tk.TOP, fill='x', pady=5)
        ttk.Label(iter_frame, text='Liczba punktów', width= 20, anchor=tk.W).pack(side = tk.LEFT, anchor = tk.W)
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

        # restrictions_frame.pack(side = tk.TOP, fill='x')
        # ttk.Label(restrictions_frame, text="Ograniczenia (Zwróć uwagę na kolejność dodawania wierzchołków)", wraplength=200).pack(side = tk.TOP, pady = 5, anchor=tk.W)
        # tk.Radiobutton(restrictions_frame, text="Brak", variable=restriction_choice, value=0, wraplength=200).pack(side = tk.TOP, anchor=tk.W)
        # tk.Radiobutton(restrictions_frame, text="Następny losowy wierzchołek musi być inny niż poprzedni",
        #                variable=restriction_choice, value=1, wraplength=200).pack(side = tk.TOP, anchor=tk.W)
        # tk.Radiobutton(restrictions_frame, text="Następny wierzchołek nie może być poprzednim na liście",
        #                variable=restriction_choice, value=2, wraplength=200).pack(side = tk.TOP, anchor=tk.W)
        # tk.Radiobutton(restrictions_frame, text="Następny wierzchołek nie może być oddalony o dwa miejsca na liście od poprzedniego",
        #                variable=restriction_choice, value=3, wraplength=200).pack(side = tk.TOP, anchor=tk.W)
        
        list_outer_frame.pack(side = tk.TOP, fill = 'x', pady = 10)
        list_canvas.pack(side = tk.LEFT)
        scrollbar.pack(side = tk.LEFT, fill = 'y', anchor = tk.W)

        canvas_frame.pack(side=tk.RIGHT, pady = 10, padx = 50)
        canvas.get_tk_widget().pack()
        toolbar.update()
        canvas.get_tk_widget().pack()

    
    def __addPoint(self, xString, yString, plot1 : Axes, canvas : tk.Canvas, pointsFrame : ttk.Frame):
        
        try:
            x = float(xString)
            y = float(yString)

        except ValueError:
            messagebox.showerror("Nieprawidłowa wartość", "x oraz y muszą być typu zmiennoprzecinkowego")
            return 

        if self.__changed_index == -1:
            self.__points.append([x, y])
            self.__vertex_number += 1
        else:
            self.__points[self.__changed_index] = [x, y]

        if(self.__fractal_plotted):
            plot(plot1, canvas)
            self.__fractal_plotted = False
        plot(plot1, canvas, vertices=self.__points)
        self.__refreshPointsList(pointsFrame)

    def __deletePoint(self, plot1: Axes, canvas, pointsFrame):
        if self.__changed_index != -1:
            self.__points.pop(self.__changed_index)
            self.__vertex_number -= 1
        plot(plot1, canvas, vertices=self.__points)
        self.__refreshPointsList(pointsFrame)
        self.__changed_index = -1

    def __plotFractal(self, plot1 : Axes, canvas, iterationsString, jumpString, points : list, restriction : int, color: bool):

        try:
            iterations = int(iterationsString)
        except(ValueError):
            messagebox.showerror("Nieprawidłowa wartość", "Liczba punktów musi być liczbą naturalną")
            return
        try:
            jump = float(jumpString)
        except(ValueError):
            messagebox.showerror("Nieprawidłowa wartość", "Wartość skoku musi być liczbą zmiennoprzecinkową")
            return
        
        if jump >= 1:
            messagebox.showerror("Nieprawidłowa wartość", "Wartość skoku musi być mniejsza od 1")
            return
        
        if iterations > 1000000:
            messagebox.showerror("Nieprawidłowa wartość", "Liczba punktów musi być mniejsza od 1 000 000")
            return
        
        if len(points) == 0:
            messagebox.showerror("Błąd", "Dodaj co najmniej jeden punkt")
            return
        
        self.__last_iterations_number = iterations
        self.__last_jump = jump
        new_points = points.copy()

        new_points, colors = fractals.chaos_game_fractal(iterations, jump, new_points)
        
        if color:
            plot(plot1, canvas, points = new_points, vertices = points,colors=colors, scaled=True)
        else:
            plot(plot1, canvas, points = new_points, vertices = points, scaled=True)
        plot1.axis('off')

        self.__fractal_plotted = True
        
    def __clearPlot(self, plot1 : Axes, canvas : tk.Canvas, pointsFrame : ttk.Frame):
        plot(plot1, canvas)
        self.__emptyPoints()
        self.__fractal_plotted = False
        self.__last_iterations_number = 0
        self.__last_jump = 0
        self.__refreshPointsList(pointsFrame)
    
    def __emptyPoints(self):
        self.__points = []
        self.__vertex_number = 0

    def __clearEntries(self):
        self.__point_entry_x.delete(0, tk.END)
        self.__point_entry_y.delete(0, tk.END)

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

    def __loadConfig(self, plot1, canvas, iterLabel: tk.Entry, jumpLabel: tk.Entry, pointsFrame: ttk.Frame):

        file = tk.filedialog.askopenfile(mode="r", defaultextension=".frac", filetypes=[('Fractal files', '*.frac')])
        if(file is None):
            return
        
        self.__clearPlot(plot1, canvas, pointsFrame)
        
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
        self.__refreshPointsList(pointsFrame)

        self.__last_iterations_number = info['iterations']
        self.__last_jump = info['jump']

        iterLabel.delete(0, tk.END)
        jumpLabel.delete(0, tk.END)
        iterLabel.insert(0, str(self.__last_iterations_number))
        jumpLabel.insert(0, str(self.__last_jump))

        plot(plot1, canvas, vertices=self.__points)
        self.__fractal_plotted = False

    def __refreshPointsList(self, pointsFrame : ttk.Frame):

        for widget in pointsFrame.winfo_children():
            widget.destroy()

        for i in range(len(self.__points)):
            pointLabel = tk.Label(pointsFrame, justify="left")
            pointLabel['text'] = str(i+1) + ". " + "[" + "{0:0.2f}".format(self.__points[i][0])  + ", " \
            + "{0:0.2f}".format(self.__points[i][1]) +"]"

            pointLabel.pack(side=tk.TOP, anchor=tk.W, padx=10, pady=1)

            pointLabel.bind("<Button-1>", lambda e, label = pointLabel, index = i: self.__editPoint(index, label))

    def __editPoint(self, index, label: tk.Label):
        bg = "SystemButtonFace"
        label.config(bg="lightblue")
        self.__restoreEntries(index)

        label.after(500, lambda: label.config(bg=bg))

    def __restoreEntries(self, index):
        self.__clearEntries()
        self.__point_entry_x.insert(0, "{0:0.2f}".format(self.__points[index][0]))
        self.__point_entry_y.insert(0, "{0:0.2f}".format(self.__points[index][1]))
        self.__changed_index = index
