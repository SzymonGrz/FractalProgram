from __future__ import division
import tkinter as tk
from tkinter import ttk
from tkinter import messagebox
from matplotlib.figure import Figure
from matplotlib.backends.backend_tkagg import (FigureCanvasTkAgg, NavigationToolbar2Tk) 
import math
import json
import random

import functions.fractals as fractals
from functions.image_functions import plot, save_image

class RectFrame(tk.Frame):
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

        example_frame = ttk.Frame(widgets_frame)

        button = ttk.Button(back_button_frame, text="Powrót",
                           command=lambda: parent.switch_frame("start"))

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

        clear_button = ttk.Button(canvas_buttons_frame, text = "Wyczyść", command = self.__clearPlot)

        load_example_button = ttk.Button(example_frame, text = "Przykład", command = self.__loadExample)

        #########################################

        widgets_frame.pack(side=tk.LEFT, fill='y', anchor = tk.NW, padx=10, pady = 10)
        back_button_frame.pack(side = tk.TOP, fill = tk.X)
        button.pack(side = tk.TOP, anchor=tk.W)

        rectangle_buttons_frame.pack(side = tk.TOP, fill = tk.X, pady = 25)
        rectangle_add_button.pack(side = tk.LEFT, anchor=tk.W)
        rectangle_delete_button.pack(side = tk.LEFT, anchor = tk.W, padx = 20)

        label_frame.pack(side = tk.TOP, fill = tk.X)
        ttk.Label(label_frame, text = "Liczba punktów", width = 15, anchor = tk.W).pack(side = tk.LEFT, anchor=tk.W)
        ttk.Label(label_frame, text = "Iteracje", anchor = tk.W).pack(side = tk.LEFT, anchor=tk.W, padx = (10, 58))
        ttk.Label(label_frame, text = "Poziom kolorowania", anchor = tk.W).pack(side = tk.LEFT, anchor=tk.W)

        entry_frame.pack(side =tk.TOP, fill = tk.X)
        iterations_entry.pack(side = tk.LEFT, anchor = tk.W)
        depth_entry.pack(side = tk.LEFT, anchor=tk.W, padx = 36)
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
        clear_button.pack(side = tk.LEFT, anchor = tk.W, padx = 12)

        example_frame.pack(side = tk.LEFT, fill = "x")
        load_example_button.pack(side = tk.LEFT, anchor = tk.W)

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
            messagebox.showerror("Nieprawidłowa wartość", "Liczba punktów, iteracje oraz poziom kolorowania muszą być liczbami naturalnymi")
            return
        
        if color_level > 5 or color_level < 0:
            messagebox.showerror("Nieprawidłowa wartość", "Poziom kolorowania musi być w zakresie 0-5")
            return
        
        if color_level > depth:
            messagebox.showerror("Nieprawidłowa wartość", "Poziom kolorowania nie może być większy od dokładności")
            return

        if iterations > 1000000:
            messagebox.showerror("Nieprawidłowa wartość", "Liczba punktów musi być mniejsza od 1 000 000")
            return
        
        if depth > 100:
            messagebox.showerror("Nieprawidłowa wartość", "Liczba iteracji musi być mniejsza od 100")
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

    def __clearPlot(self):
        plot(self.__plot1, self.__canvas)

    def __loadExample(self):

        info = {"1": [-12.810950318671843, 150.7512515070591, 93.2487484929409, -18.810950318671857, 262.8109503186718, 87.24874849294093, 156.75125150705904, 256.810950318672], 
                "27": [184.0, 308.0, 184.0, 108.0, 384.0, 108.0, 384.0, 308.0], 
                "69": [179.25208095264068, 448.4967409345892, 16.503259065410816, 332.2520809526406, 132.7479190473595, 169.50325906541073, 295.4967409345892, 285.74791904735946]}

        self.__draw_canvas.delete("all")
        self.__list_of_rectangles.clear()
        
            
        for _, value in info.items():
            x1, y1, x2, y2, x3, y3, x4, y4 = value
            self.__createRectangle(x1, y1, x2, y2, x3, y3, x4, y4)
