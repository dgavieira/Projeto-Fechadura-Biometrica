#Title: Biometric Lock User Interface
#Organization: Optima-UFAM
#Screen 1: Main Screen
#Description: Main Screen for the User Interface
#Especs: Touchscreen LCD 3,5" 480x320
#Autor: Diego Vieira
#!/usr/local/bin/python
# -*- coding: utf-8 -*-

try:
    # for Python2
    from Tkinter import *
except ImportError:
    # for Python3
    from tkinter import *

import RPi.GPIO as GPIO
import time
import tela02, tela08, tela10 #importa as telas seguintes

#define o pino do botão 
BUTTON_ENTRY = 37

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
            self.button1["height"] = 3
            self.button1["command"] = doublefuncoptions
            self.button1.pack(side = TOP, fill=X)

            #construtor do botao OPEN THE DOOR
            self.button2 = Button(self.widget1)
            self.button2["text"] = "OPEN THE DOOR"
            self.button2["font"] = fontePadrao
            self.button2["height"] = 4
            self.button2["command"] = openDoor
            self.button2.pack(side = TOP, fill=X)
            
            configura_GPIO() #funcao para configurar o GPIO

    #metodos
    def doublefuncoptions(): #chama transição para tela dois
        fechar()
        tela02.teladois()
    
    def openDoor(): #envia sinal para destravar a trava quando pressionado "OPEN THE DOOR"
        fechar()
        tela08.telaoito()
    
    def fechar(): #encapsula metodo interno do python para nao gerar excecao
        root.destroy()
    
    def configura_GPIO():
        #configura o GPIO do rasp como modo BOARD e o pino do botao como ENTRADA
        GPIO.setmode(GPIO.BOARD)
        GPIO.setup(BUTTON_ENTRY, GPIO.IN)
    
    def checkButton():
        """a cada 200 milissegundos, o tk.mainloop chama essa rotina para ficar checando se
            o botao foi pressionado, se sim fecha a tela01.py e chama a tela10.py que eh a
            tela para a pessoa entrar. Se o botao não for pressionado, fica num loop entre criar
            a tela01 e checar o botao"""
        if GPIO.input(BUTTON_ENTRY) == True:
            fechar()
            tela10.teladez()
        else:
            pass

        root.after(200, checkButton)
        
    #loop de inicialização da tela
    root = Tk()
    ScreenOne(root)
    root.title("Main Screen")
    root.geometry('478x270')
    root.after(200, checkButton)
    root.mainloop()
    #root.overrideredirect(True) #trava ponteiro do mouse e força app no primeiro plano
    
if __name__ == "__main__": #permite executar esse script como principal
    telaum()