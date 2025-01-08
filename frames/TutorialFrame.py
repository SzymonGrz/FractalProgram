import tkinter as tk
from tkinter import ttk
from PIL import Image, ImageTk
from functions.resources import resource_path

from functions.image_functions import plot, save_image

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
                           command=lambda: parent.switch_frame("start"))
        chaos_game_tutorial_button = ttk.Button(buttons_frame, text = "Gra w chaos",
                command = lambda : self.__showCanvas('chaos'))
        rectangle_tutorial_button = ttk.Button(buttons_frame, text = "IFS - wersja graficzna",
                command = lambda: self.__showCanvas('rect'))
        affine_tutorial_button = ttk.Button(buttons_frame, text = "IFS",
                command = lambda: self.__showCanvas('ifs'))
        mandelbrot_tutorial_button = ttk.Button(buttons_frame, text = "Zbiór Mandelbrota",
                command = lambda : self.__showCanvas('mandelbrot'))
        lsystem_tutorial_button = ttk.Button(buttons_frame, text = "L-system",
                command = lambda : self.__showCanvas('lsys'))

        self.__canvas = tk.Canvas(canvas_frame, width = 900, height = 700)

        #---------------------------------------#

        widgets_frame.pack(side=tk.LEFT, fill='y', anchor = tk.NW, padx=10, pady = 5)
        buttons_frame.pack(side = tk.TOP, fill='x', pady=5)

        button.pack(side=tk.TOP, anchor = tk.W)
        chaos_game_tutorial_button.pack(side=tk.TOP, anchor = tk.W, pady = 10)
        affine_tutorial_button.pack(side=tk.TOP, anchor = tk.W)
        rectangle_tutorial_button.pack(side=tk.TOP, anchor = tk.W, pady = 10)
        lsystem_tutorial_button.pack(side=tk.TOP, anchor = tk.W)
        mandelbrot_tutorial_button.pack(side=tk.TOP, anchor = tk.W, pady = 10)

        canvas_frame.pack(side = tk.LEFT, padx = 15)
        self.__canvas.pack(side = tk.LEFT)

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
            case 'chaos':
                self.img = Image.open(resource_path("images/chaos_game.png"))
                self.img = ImageTk.PhotoImage(self.img)
                self.__canvas.create_image(200, 280, image = self.img)
                self.__canvas.create_text(320, 50, text = "Koordynaty x, y nowego punktu", anchor=tk.W, justify="left")
                self.__canvas.create_text(320, 135, text = "Liczba punktów które zostaną wyznaczone na obrazie", anchor=tk.W, justify="left")
                self.__canvas.create_text(320, 170, text = "Odległość pomiędzy losowym wierzchołkiem a poprednim punktem\n" 
                                          "w jakiej pojawi się nowy punkt", anchor=tk.W, justify="left")
                self.__canvas.create_text(320, 200, text = "Czy obraz ma być pokolorowany", anchor=tk.W, justify="left")
                self.__canvas.create_text(380, 240, text = "Opcje pozwalające na narysowanie i usunięcie obrazu\n"
                    "a także zapisanie i wczytanie konfiguracji", anchor=tk.W, justify="left")
                self.__canvas.create_text(220, 300, text = "Lista dodanych punktów,\n mozna ją edytować poprzez kliknięcie wybranej pozycji", anchor=tk.W, justify="left")
            case 'ifs':
                self.img = Image.open(resource_path("images/ifs.png"))
                self.img = ImageTk.PhotoImage(self.img)
                self.__canvas.create_image(200, 250, image = self.img)
                self.__canvas.create_text(300, 70, text = "Szansa na wylosowanie danej funkcji", anchor=tk.W, justify="left")
                self.__canvas.create_text(300, 140, text = "Parametry funkcji", anchor=tk.W, justify="left")
                self.__canvas.create_text(300, 240, text = "Liczba punktów które zostaną wyznaczone na obrazie", anchor=tk.W, justify="left")
                self.__canvas.create_text(300, 270, text = "Czy obraz ma być pokolorowany", anchor=tk.W, justify="left")
                self.__canvas.create_text(400, 320, text = "Opcje pozwalające na narysowanie i usunięcie obrazu\n"
                    "a także zapisanie i wczytanie konfiguracji(tj. listy punktów, liczby punktów i odległości skoku)", anchor=tk.W, justify="left")
                self.__canvas.create_text(300, 400, text = "Lista dodanych funkcji, mozna ją edytować poprzez kliknięcie wybranej pozycji", anchor=tk.W, justify="left")
            case 'lsys':
                self.img = Image.open(resource_path("images/lsystem.png"))
                self.img = ImageTk.PhotoImage(self.img)
                self.__canvas.create_image(180, 290, image = self.img)
                self.__canvas.create_text(320, 120, text = "Dodaj lub edytuj regułę.\nZmienna musi byc jednym znakiem a reguła ciągiem znaków", anchor=tk.W, justify="left")
                self.__canvas.create_text(300, 200, text = "Parametry algorytmu. Start - startowy ciąg znaków\n"
                    "Kąt obrotu pióra,\nliczba powtórzeń algortymu", anchor=tk.W, justify="left")
                self.__canvas.create_text(300, 270, text = "Długość rysowanego odcinka")
                self.__canvas.create_text(320, 320, text = "Rozpocznij lub zatrzymaj rysowanie, wyczyść płótno obrazu", anchor=tk.W, justify="left")
                self.__canvas.create_text(320, 350, text = "Zapisz lub wczytaj konfigurację, zapisz obraz do pliku", anchor=tk.W, justify="left")
                self.__canvas.create_text(300, 420, text = "Lista obsługiwanych znaków", anchor=tk.W, justify="left")
                self.__canvas.create_text(300, 520, text = "Lista dodanych funkcji", anchor=tk.W, justify="left")                          
            case 'rect':
                self.img = Image.open(resource_path("images/rect_ifs.png"))
                self.img = ImageTk.PhotoImage(self.img)
                self.__canvas.create_image(220, 300, image = self.img)
                self.__canvas.create_text(350, 30, text = "Dodaj nowy prostokąt lub usuń istniejący", anchor=tk.W, justify="left")
                self.__canvas.create_text(350, 90, text = "Parametry generowania obrazu.\n"
                    "Liczba punktów na obrazie, liczba powtórzeń algorytmu określająca dokładność obrazu\n"
                    "Poziom kolorowania określający sposób kolorowania elementów obrazu", anchor=tk.W, justify="left")
                self.__canvas.create_text(430, 200, text = "Obszar roboczy, na którym można dostosowywać\n(tj. przesuwać, obracać, zmieniać rozmiar)"
                    "dodane prostokaty", anchor=tk.W, justify="left")
                self.__canvas.create_text(350, 570, text = "Opcje pozwalające na narysowanie i usunięcie obrazu\n"
                    "a także zapisanie i wczytanie konfiguracji", anchor=tk.W, justify="left")
            case 'mandelbrot':
                self.img = Image.open(resource_path("images/mandel_julia.png"))
                self.img = ImageTk.PhotoImage(self.img)
                self.__canvas.create_image(120, 100, image = self.img)
                self.__canvas.create_text(200, 50, text = "Opcja pozwalająca na wybór zbioru Mandelbrota i zbioru Julii", anchor=tk.W, justify="left")
                self.__canvas.create_text(200, 100, text = "Parametry zbioru Julii(dowolne liczby zmiennoprzecinkowe)", anchor=tk.W, justify="left")
                self.__canvas.create_text(215, 160, text = "Narysuj lub usuń obraz\n", anchor=tk.W, justify="left")
            case _ :
                pass