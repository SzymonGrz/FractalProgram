from __future__ import division
import tkinter as tk
from tkinter import ttk
from tkinter import messagebox
import turtle
import re
import json
from collections import deque
from PIL import ImageGrab

import functions.fractals as fractals


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
        info_frame = ttk.Frame(widgets_frame)

        example_frame = ttk.Frame(widgets_frame)

        canvas_frame = tk.Frame(self)

        button = ttk.Button(back_button_frame, text="Powrót",
                           command=lambda: parent.switch_frame("start"))
        
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
        
        self.__load_example_button = ttk.Button(example_frame, text = "Przykład", 
                command = lambda: self.__loadExample(start_entry, angle_entry, rules_label))
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

        example_frame.pack(side = tk.TOP, fill = "x", pady = 5)
        self.__load_example_button.pack(side = tk.LEFT, anchor = tk.W)

        info_frame.pack(side = tk.TOP, fill = "x", pady = 20)
        ttk.Label(info_frame, text = "F, G - przesuń się i narysuj linię\n" "f - przesuń się\n"
            "+ - obrót w lewo\n" "- - obrót w prawo\n" "[ - zapisz bieżącą pozycję\n" 
            "] - odczytaj ostatnią pozycję\n" "Dowolny inny znak - zignoruj", justify="left").pack(side = tk.LEFT, anchor = tk.W)

        rule_list_frame.pack(side=tk.TOP, fill = tk.X)
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
        
        if iter > 5:
            messagebox.showerror("Nieprawidłowa wartość", "Liczba iteracji musi być mniejsza od 5")
            return

        self.__draw_button.configure(state="disabled")
        self.__load_button.configure(state="disabled")
        self.__save_button.configure(state = "disabled")
        self.__image_button.configure(state = "disabled")
        self.__stop_button.configure(state = "normal")
        self.__clear_button.configure(state = "disabled")
        self.__load_example_button.configure(state = "disabled")
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
        self.__load_example_button.configure(state = "normal")
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

    def __loadExample(self, startEntry, angleEntry, rulesLabel):

        info = {"rules": {"L": "-RF+LFL+FR-", "R": "+LF-RFR-FL+"}, "start": "LFL+F+LFL", "angle": "90"}

        self.__rules = info['rules']
        start = info['start']
        angle = info['angle']
        startEntry.delete(0, tk.END)
        angleEntry.delete(0, tk.END)
        startEntry.insert(0, start)
        angleEntry.insert(0, str(angle))


        self.__refreshRulesLabel(rulesLabel)