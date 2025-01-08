from tkinter import ttk

class StartFrame(ttk.Frame):
    def __init__(self, parent):
        ttk.Frame.__init__(self, parent)

        button_frame = ttk.Frame(self)
        
        button6 = ttk.Button(button_frame, text = "Zbiór Mandelbrota i Zbiory Julii", command= lambda: parent.switch_frame("mandel"))
        button2 = ttk.Button(button_frame, text = "Gra w chaos", command= lambda: parent.switch_frame("fractals"))
        button3 = ttk.Button(button_frame, text = "IFS - System Funkcji Iterowanych", command= lambda: parent.switch_frame("affine"))
        button7 = ttk.Button(button_frame, text = "L-System", command = lambda : parent.switch_frame("lsys"))
        button4 = ttk.Button(button_frame, text = "Instrukcja", command= lambda : parent.switch_frame("tutor"))
        
        button8 = ttk.Button(button_frame, text = "IFS - Wersja graficzna", command= lambda: parent.switch_frame("rect"))

        button_frame.pack(side = "top", padx=20, pady = 20)
        button6.pack(pady = 10)
        button2.pack(pady = 10)
        button3.pack(pady = 10)
        button8.pack(pady = 10)
        button7.pack(pady = 10)
        button4.pack(pady = 10)
