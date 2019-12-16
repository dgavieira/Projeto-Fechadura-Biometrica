#Title: Biometric Lock User Interface
#Organization: Optima-UFAM
#Screen 1: Main Screen
#Description: Main Screen for the User Interface
#Especs: Touchscreen LCD 3,5" 480x320
#Autor: Diego Vieira
#!/usr/local/bin/python
# -*- coding: utf-8 -*-

import RPi.GPIO as gpio
import time

try:
    # for Python2
    from Tkinter import *
except ImportError:
    # for Python3
    from tkinter import *

import tela02, tela08 #importa as telas seguintes

def telaum():
    class ScreenOne:
        def __init__(self, master=None):   #construtor do layout
            #frame externo da tela principal
            self.widget1 = Frame(master)
            self.widget1.pack(fill=X)

            fontePadrao = ('Arial', '24')
            
            #construtor do botao OPTIONS
            self.button1 = Button(self.widget1)
            self.button1["text"] = "OPTIONS"
            self.button1["font"] = fontePadrao
            self.button1["height"] = 2
            self.button1["command"] = doublefuncoptions
            self.button1.pack(side = TOP, fill=X)

            #construtor do botao OPEN THE DOOR
            self.button2 = Button(self.widget1)
            self.button2["text"] = "OPEN THE DOOR"
            self.button2["font"] = fontePadrao
            self.button2["height"] = 2
            self.button2["command"] = openDoor
            self.button2.pack(side = TOP, fill=X)

            #construtor do botao CANCEL
            self.button3 = Button(self.widget1)
            self.button3["text"] = "CANCEL"
            self.button3["font"] = fontePadrao
            self.button3["height"] = 4
            self.button3["command"] = fechar
            self.button3.pack(side = TOP, fill=X)

    #metodos
    def doublefuncoptions(): #chama transição para tela dois
        fechar()
        tela02.teladois()
    
    def openDoor(): #envia sinal para destravar a trava quando pressionado "OPEN THE DOOR"
        gpio.setmode(gpio.BOARD)
        gpio.setup(40,gpio.OUT)
        gpio.output(40,gpio.HIGH)
        time.sleep(1)
        gpio.output(40,gpio.LOW)
        time.sleep(0.5)
        gpio.cleanup()
        fechar()
        tela08.telaoito()
    
    def fechar(): #encapsula metodo interno do python para nao gerar excecao
        root.destroy()

    #loop de inicialização da tela
    root = Tk()
    ScreenOne(root)
    root.title("Main Screen")
    root.geometry('478x270')
    root.mainloop()
    #root.overrideredirect(True) #trava ponteiro do mouse e força app no primeiro plano
    
if __name__ == "__main__": #permite executar esse script como principal
    telaum()