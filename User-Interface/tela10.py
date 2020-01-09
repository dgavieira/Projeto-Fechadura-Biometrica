#Title: Biometric Lock User Interface
#Organization: Optima-UFAM
#Screen 10: Check-in Screen
#Description: Check-in Screen for the User Interface
#Especs: Touchscreen LCD 3,5" 480x320
#Author: Leonardo Arcanjo
#!/usr/local/bin/python
#-*- coding: uft-8 -*-

try:
    #for Python2
    from Tkinter import *
except:
    #for Python3
    from tkinter import *
    
import tela01

def teladez():
    class ScreenTen:
        def __init__(self, master = None):
            self.widget1 = Frame(master)
            self.widget1["pady"] = 10
            self.widget1.pack()
            
            self.widget2 = Frame(master)
            self.widget2["padx"] = 10
            self.widget2.pack()
            
            self.titulo = Label(self.widget1, text = "Check-in Screen")
            self.titulo["font"] = ("Arial", "20", "bold")
            self.titulo.pack()
            
            self.texto = Text(self.widget2)
            self.texto["relief"] = SUNKEN
            self.texto["height"] = 13
            self.texto.pack()
            
            
    root = Tk()
    ScreenTen(root)
    root.title("Check-in Screen")
    root.geometry("478x270")
    root.mainloop()

if __name__ == "__main__":
    teladez()