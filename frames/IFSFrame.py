from __future__ import division
import tkinter as tk
from tkinter import ttk
from tkinter import messagebox
from matplotlib.figure import Figure
from matplotlib.backends.backend_tkagg import (FigureCanvasTkAgg, NavigationToolbar2Tk) 
import json

import functions.fractals as fractals
from functions.image_functions import plot, save_image

class IFSFrame(tk.Frame):

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
        example_frame = ttk.Frame(widgets_frame)


        button = ttk.Button(back_button_frame, text="Powrót",
                           command=lambda: parent.switch_frame("start"))
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

        load_exanmple_button = ttk.Button(example_frame, text = "Przykład", 
            command = lambda: self.__loadExample(plot1, canvas, iterations_entry, list_frame))

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
        ttk.Label(iter_frame, text='Liczba punktów', width = 20, anchor= tk.W).pack(side = tk.LEFT)
        iterations_entry.pack(side = tk.LEFT)

        color_frame.pack(side = tk.TOP, fill='x', pady=5)
        ttk.Label(color_frame, text = "Kolor", width= 20, anchor=tk.W).pack(side=tk.LEFT, anchor = tk.W)
        color_check.pack(side=tk.LEFT, anchor=tk.W)

        canvas_buttons_frame.pack(side = tk.TOP, fill = 'x', pady = 20)
        draw_button.pack(side = tk.LEFT)
        clear_button.pack(side = tk.LEFT, padx = 10)
        save_button.pack(side = tk.LEFT)
        load_button.pack(side = tk.LEFT, padx = 10)

        example_frame.pack(side = tk.TOP, fill = 'x')
        load_exanmple_button.pack(side = tk.LEFT, anchor = tk.W)

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
            messagebox.showerror("Nieprawidłowa wartość", "Liczba punktów musi być liczbą naturalną")
            return

        if len(self.__chances) == 0:
            messagebox.showerror("Błąd", "Dodaj co najmniej jedną funkcję")
            return
        
        if(sum(self.__chances) < 100):
            messagebox.showerror("Nieprawidłowa wartość", "Suma procentowych szans jest mniejsza od 100")
            return
        
        if iterations > 1000000:
            messagebox.showerror("Nieprawidłowa wartość", "Liczba punktów musi być mniejsza od 1 000 000")
            return
        
        self.__last_iterations_number = iterations

        points, colors = fractals.affine_fractal(iterations,self.__chances, self.__x_transform, self.__y_transform)
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
        bg = "SystemButtonFace"
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

    def __loadExample(self, plot1, canvas, iterEntry, functionFrame):
        
        self.__clearPlot(plot1, canvas, functionFrame, iterEntry)

        info = {"chances": [1.0, 85.0, 7.0, 7.0], 
                "x_transform": [[0.0, 0.0, 0.0], [0.85, 0.04, 0.0], [0.2, -0.26, 0.0], [-0.15, 0.28, 0.0]], 
                "y_transform": [[0.0, 0.16, 0.0], [-0.04, 0.85, 1.6], [0.23, 0.22, 1.6], [0.26, 0.24, 0.44]], 
        "iterations": 100000}

        self.__chances = info['chances']
        self.__x_transform = info['x_transform']
        self.__y_transform = info['y_transform']
        self.__last_iterations_number = info['iterations']
        self.__refreshFunctionLabel(functionFrame)

        iterEntry.delete(0, tk.END)
        iterEntry.insert(0, str(self.__last_iterations_number))
