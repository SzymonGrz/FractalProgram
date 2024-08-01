import tkinter as tk
from matplotlib.figure import Figure 
from matplotlib.backends.backend_tkagg import (FigureCanvasTkAgg,  
NavigationToolbar2Tk) 
import math

import fractals

class App(tk.Tk):
    def __init__(self):
        tk.Tk.__init__(self)
        self.geometry("1000x600")
        self.grid_columnconfigure(0, weight=1)
        self.grid_rowconfigure(0, weight=1)
        #self.resizable(0, 0)
        self._frame = None
        self.switch_frame(StartFrame)

    def switch_frame(self, frame_class):
        """Destroys current frame and replaces it with a new one."""
        new_frame = frame_class(self)
        if self._frame is not None:
            self._frame.destroy()
        self._frame = new_frame
        self._frame.grid(column=0, row=0, sticky="nsew")

class StartFrame(tk.Frame):
    def __init__(self, parent):
        tk.Frame.__init__(self, parent)
        button1 = tk.Button(self, text = "Paproć Barnsley'a", command= lambda: parent.switch_frame(PaprocFrame))
        button2 = tk.Button(self, text = "Własny fraktal", command= lambda: parent.switch_frame(FractalFrame))
        button3 = tk.Button(self, text = "Temp Affine Fractal", command= lambda: parent.switch_frame(AffineFractalFrame))
        
        button1.grid(row=0, sticky="W")
        button2.grid(row=1, sticky="W")
        button3.grid(row=2, sticky = "W")

class PaprocFrame(tk.Frame):
    def __init__(self, parent):
        tk.Frame.__init__(self, parent)
        button = tk.Button(self, text="Powrót",
                           command=lambda: parent.switch_frame(StartFrame))
        button.grid(row=0, column=0, sticky="W")
        tk.Label(self, text='Iteracje').grid(row=1, sticky="W")
        vcmd = (self.register(self.validate))

        iterationsEntry = tk.Entry(self, validate="all", validatecommand=(vcmd, "%P"))
        iterationsEntry.grid(row=1, column=1, sticky="W")

        draw_button = tk.Button(self, text="Rysuj", 
                                command=lambda: plot(plot1, canvas,
                                fractals.barnsley_fern(int(iterationsEntry.get()))))
        draw_button.grid(row=2, column=0, sticky="W")
        fig = Figure(figsize = (5, 5), dpi = 100)
        plot1 = fig.add_subplot(111)
        canvas_frame = tk.Frame(self)
        canvas_frame.grid(row = 0, column = 4, rowspan=30, sticky="W")
        canvas = FigureCanvasTkAgg(fig, master = canvas_frame)
        canvas.get_tk_widget().pack()
        toolbar = NavigationToolbar2Tk(canvas, canvas_frame) 
        toolbar.update()
        canvas.get_tk_widget().pack()
        tk.Label(self, text="           ").grid(row = 0, column = 3, sticky="W")
        

    def validate(self, P):
        if str.isdigit(P) or P == "":
            return True
        else:
            return False

    



class FractalFrame(tk.Frame):

    points = []
    fractal_plotted : bool = False

    def __init__(self, parent):
        tk.Frame.__init__(self, parent)

        vcmdInt = (self.register(self.validate))
        vcmdFloat = (self.register(self.validateFloat))

        button = tk.Button(self, text="Powrót",
                           command=lambda: parent.switch_frame(StartFrame))
        point_entry_x = tk.Entry(self, validate="key")
        point_entry_y = tk.Entry(self, validate="key")
        point_accept = tk.Button(self, text="Dodaj punkt", command = lambda: [self.addPoint(
            point_entry_x.get(), point_entry_y.get(), plot1, canvas), 
            point_entry_x.delete(0, tk.END), point_entry_y.delete(0, tk.END)])
        iterations_entry = tk.Entry(self, validate="all", validatecommand=(vcmdInt, "%P"))
        jump_entry = tk.Entry(self, validate = 'key', validatecommand=(vcmdFloat, "%P"))
        draw_button = tk.Button(self, text="Rysuj", 
                                command=lambda: [self.plotFractal(plot1, canvas, iterations_entry.get(),
                                jump_entry.get(), self.points, restriction_choice.get()), 
                                iterations_entry.delete(0, tk.END), jump_entry.delete(0, tk.END)])
        clear_button = tk.Button(self, text="Wyczyść", command= lambda : self.clearPlot(plot1, canvas))

        fig = Figure(figsize = (5, 5), dpi = 100)
        plot1 = fig.add_subplot(111)

        canvas_frame = tk.Frame(self)
        canvas = FigureCanvasTkAgg(fig, master = canvas_frame)
        toolbar = NavigationToolbar2Tk(canvas, canvas_frame) 

        button.grid(row=0, column=0, sticky="W")
        tk.Label(self, text="X  ").grid(column = 0, sticky="W")
        point_entry_x.grid(row = 1, column= 1, sticky="W")
        tk.Label(self, text="Y  ").grid(column = 0, sticky="W")
        point_entry_y.grid(row = 2, column= 1, sticky="W")
        point_accept.grid(row = 3, sticky="W")
        tk.Label(self, text='Iteracje').grid(row=4, sticky="W")
        iterations_entry.grid(row=4, column=1, sticky="W")
        tk.Label(self, text='Odległość skoku').grid(row=5, sticky="W")
        jump_entry.grid(row=5, column = 1, sticky="W")
        draw_button.grid(row=6, column=0, sticky="W")
        clear_button.grid(row=6, column =1, sticky="W")

        restriction_choice = tk.IntVar()
        restriction_choice.set(0)
        tk.Label(self, text="Ograniczenia (Zwróć uwagę na kolejność dodawania wierzchołków)", wraplength=200).grid(row=7, sticky="W")
        tk.Radiobutton(self, text="Brak", variable=restriction_choice, value=0, wraplength=200).grid(row = 8, sticky="W")
        tk.Radiobutton(self, text="Następny losowy wierzchołek musi być inny niż poprzedni",
                       variable=restriction_choice, value=1, wraplength=200).grid(row=9, sticky="W")
        tk.Radiobutton(self, text="Następny wierzchołek nie może być poprzednim na liście",
                       variable=restriction_choice, value=2, wraplength=200).grid(row=10, sticky="W")
        tk.Radiobutton(self, text="Następny wierzchołek nie może być oddalony o dwa miejsca na liście od poprzedniego",
                       variable=restriction_choice, value=3, wraplength=200).grid(row=11, sticky="W")



        canvas_frame.grid(row = 0, column = 4, rowspan=30, sticky="W")
        canvas.get_tk_widget().pack()
        toolbar.update()
        canvas.get_tk_widget().pack()
        tk.Label(self, text="           ").grid(row = 0, column = 3)


    def validate(self, P):
        if str.isdigit(P) or P == "":
            return True
        else:
            return False
        
    def validateFloat(self, P):
        if(P == ""):
            return True
        try:
            float(P)
        except(ValueError):
            return False
        return True
    
    def addPoint(self, xString, yString, plot, canvas):
        

        try:
            x = float(xString)
            y = float(yString)
        except(ValueError):
            return 
        self.points.append((x, y))

        if(self.fractal_plotted):
            plot.clear()
            self.fractal_plotted = False
        plot.scatter(x, y, c="b")
        canvas.draw()

    def plotFractal(self, plot1, canvas, iterationsString, jumpString, points : list, restriction : int):

        try:
            iterations = int(iterationsString)
            jump = float(jumpString)
        except(ValueError):
            return
        
        if(restriction == 0):
            plot(plot1, canvas, fractals.chaos_game_fractal(iterations, jump, points))
        else:
            plot(plot1, canvas, fractals.chaos_game_fractal_restricted(iterations, jump, points, restriction))

        self.fractal_plotted = True
        self.emptyPoints()
        
    def clearPlot(self, plot1, canvas):
        plot(plot1, canvas, [])
        self.emptyPoints()
        self.fractal_plotted = False
    
    def emptyPoints(self):
        self.points = []
        
class AffineFractalFrame(tk.Frame):

    chances = []
    x_transform = []
    y_transform = []

    def __init__(self, parent):
        tk.Frame.__init__(self, parent)
        vcmd = (self.register(self.validate))

        button = tk.Button(self, text="Powrót",
                           command=lambda: parent.switch_frame(StartFrame))
        iterationsEntry = tk.Entry(self, validate="all", validatecommand=(vcmd, "%P"))
        draw_button = tk.Button(self, text="Rysuj", 
                                command=lambda: plot(plot1, canvas,
                                fractals.barnsley_fern(int(iterationsEntry.get()))))
        chanceEntry = tk.Entry(self)
        chanceAddButton = tk.Button(self, text="Dodaj", command= lambda : self.addChances(chanceEntry.get()))
       
        fig = Figure(figsize = (5, 5), dpi = 100)
        plot1 = fig.add_subplot(111)
        canvas_frame = tk.Frame(self)
        canvas = FigureCanvasTkAgg(fig, master = canvas_frame)
        toolbar = NavigationToolbar2Tk(canvas, canvas_frame) 
        
        button.grid(row=0, column=0, sticky="W")
        tk.Label(self, text='Iteracje').grid(row=1, sticky="W")
        iterationsEntry.grid(row=1, column=1, sticky="W")
        tk.Label(self, text="Dodaj funkcję afiniczną").grid(row=2, column=0, sticky="W")
        tk.Label(self, text="Procentowa szansa"). grid(row=3, sticky="W")
        chanceEntry.grid(row = 4, sticky = "W")
        chanceAddButton.grid(row = 5, sticky="W")

        draw_button.grid(column=0, sticky="W")

        canvas_frame.grid(row = 0, column = 4, rowspan=30, sticky="W")
        canvas.get_tk_widget().pack()
        toolbar.update()
        canvas.get_tk_widget().pack()
        tk.Label(self, text="           ").grid(row = 0, column = 3, sticky="W")


    def validate(self, P):
        if str.isdigit(P) or P == "":
            return True
        else:
            return False
        
    def addChances(self, chanceString: str):

        try:
            chance = float(chanceString)
        except(ValueError):
            return
        
        sum_of_chances = sum(self.chances)
        
        if(100 - sum_of_chances < chance):
            chance = 100 - sum(self.chances)

        if(sum_of_chances >= 100):
            return
        
        self.chances.append(chance)

    def addXTransform(self, x1: str, x2: str, x3: str):
        self.x_transform.append([x1, x2, x3])
    def addYTransform(self,  y1: str, y2: str, y3: str):
        self.chances.append(y1, y2, y3)

    def clearLists(self):
        self.chances = []
        self.x_transform = []
        self.y_transform = []
    
    def plotFractal(self, plot1, canvas, iterationsString):
        
        try:
            iterations = int(iterationsString)
        except(ValueError):
            return
        
        plot(plot1, canvas, fractals.affine_fractal(self.chances, self.x_transform, self.y_transform))
        self.clearLists()
        



def plot(plot1, canvas, points : list):

    if(len(points) == 0):
        plot1.clear()
        canvas.draw()
        return
    #points
    points_x = []
    points_y = []

    for p in points:
        points_x.append(p[0])
        points_y.append(p[1])

    plot1.scatter(points_x, points_y, s=0.09, c="g")
    canvas.draw()

    # creating the Matplotlib toolbar 
    # toolbar = NavigationToolbar2Tk(canvas, window) 
    # toolbar.update() 
  
    # # placing the toolbar on the Tkinter window 
    # canvas.get_tk_widget().pack() 


# window = tk.Tk()
# fig = Figure(figsize = (8, 8), dpi = 100)
# plot1 = fig.add_subplot(111)
# canvas = FigureCanvasTkAgg(fig, master = window)
# plot_button = tk.Button(master = window, 
#                     command = lambda : plot(test.paproc(10000)),
#                      height = 2, 
#                      width = 15, 
#                     text = "Paproć Barnsley'a")
# plot_button2 = tk.Button(master = window, command = lambda : plot(test.chaos_game_fractal(
#     10000, 0.5, [(0,0), (10, 0), (5, 5*math.sqrt(3))])), height = 2, width = 15, text = "Dywan Sierpińskiego") 


if __name__ == "__main__":
    app = App()
    app.mainloop()

