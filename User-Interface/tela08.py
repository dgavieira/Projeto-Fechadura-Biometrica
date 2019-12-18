#Title: Biometric Lock User Interface
#Organization: Optima-UFAM
#Screen 8: Checkout Screen
#Description: Screen to check who is inside the lab and wants to leave. 
#Especs: Touchscreen LCD 3,5" 480x320
#Autor: Leonardo Arcanjo
#Revison: Leonardo Arcanjo
#!/usr/local/bin/python
# -*- coding: utf-8 -*-

try:
    #for python2 
    from Tkinter import *
except ImportError:
    #for python3
    from tkinter import *

from pynput.keyboard import Key, Controller
import sqlite3, readline
import RPi.GPIO as gpio
from datetime import datetime

import tela01

def telaoito():
    #vetores de apoio para armazenamento das pessoas que estao no datalog
    vetor_nome = []
    vetor_sobrenome = []
    vetor_cargo = []
    class ScreenEight:
        def __init__(self, master = None):
            
            self.primeiroConteiner = Frame(master)
            self.primeiroConteiner.grid(row = 0, column = 0, rowspan = 2, columnspan = 2,
                                        sticky = NW)
            
            self.lista = Listbox(self.primeiroConteiner, width = 30, height = 10,
                                 font = ('MS', '12'), selectmode = BROWSE)
            self.scroll = Scrollbar(self.primeiroConteiner, command = self.lista.yview)
            self.lista.configure(yscrollcommand = self.scroll.set)
            self.lista.pack(side = LEFT)
            self.scroll.pack(side = RIGHT,fill = Y)
            
            self.fontePadrao = ('Arial', '10')
            
            self.BotaoUp = Button(master, text = 'UP', font = self.fontePadrao,
                                  width = 18, height = 5, command = self.ScrollUp)
            self.BotaoUp.grid(row = 0, column = 2, sticky = NW)
            
            self.BotaoDown = Button(master, text = 'DOWN', font = self.fontePadrao,
                                    width = 18, height = 5, command = self.ScrollDown)
            self.BotaoDown.grid(row = 1, column = 2, sticky = NW)
            
            self.BotaoQuit = Button(master, text = 'QUIT', font = ['Arial', '10', 'bold'],
                                    width = 18, height = 3, command = self.toQuit)
            self.BotaoQuit.grid(row = 2, column = 2, sticky = SW)
            
            self.BotaoLoad = Button(master, text = 'LOAD', font = self.fontePadrao,
                                    width = 18, height = 3, command = self.fetchData)
            self.BotaoLoad.grid(row = 2, column = 0, sticky = SW)
            
            self.BotaoBack = Button(master, text = 'BACK', font = self.fontePadrao,
                                    width = 18, height = 3, command = backToMain)
            self.BotaoBack.grid(row = 2, column = 1, sticky = SW)
            
        def ScrollUp(self):
            keyboard = Controller()
            keyboard.press(Key.up)
            keyboard.release(Key.up)
        
        
        def ScrollDown(self):
            keyboard = Controller()
            keyboard.press(Key.down)
            keyboard.release(Key.down)
        
        def fetchData(self): #Funcao para busca dos nomes das pessoas que estao no LAB
            #Abrir o arquivo Control.txt em modo leitura
            arquivo = open('/home/pi/github/Projeto-Fechadura-Biometrica/User-Interface/Control.txt', 'r')
            
            #vetores de apoio para armazenamento dos dados de leitura do datalog.txt
            vetor_status = []
            i = 0
            
            #essa funcao serve para deletar tudo que aparece na scroll bar de modo que
            #ao se apertar o botao LOAD novamente, os dados nao apareçam repetidos
            self.lista.delete(0, END) 
            
            #laço for para preencher os vetores auxiliares com os nomes
            #E listar os nomes no scroll bar
            for linha in arquivo:
                nomes = linha.split()
                vetor_nome.insert(i, nomes[0])
                vetor_sobrenome.insert(i, nomes[1])
                vetor_cargo.insert(i, nomes[2])
                self.lista.insert(END, str(nomes[0] + " " + nomes[1]) + " " + nomes[2])
                i += 1
            
            #nao esquecer JAMAIS, NUNCA em HIPOTESE ALGUMA de fechar o arquivo
            arquivo.close()
        
        def toQuit(self):
            #esse metodo retorna uma lista com os items da lista/scroll bar
            items = self.lista.curselection()
            pos = 0
            
            #laço for para pegar o Indice do item/pessoa que irá sair
            for i in items:
                idx = int(i) - pos
                pos += 1
            
            now = datetime.now()
            hora = now.strftime("%d/%m/%Y %H:%M:%S")
            arquivo = open('/home/pi/github/Projeto-Fechadura-Biometrica/User-Interface/Stream.txt', 'a')
            arquivo.writelines(str(vetor_nome[idx]) + " " + str(vetor_sobrenome[idx]) + " " + str(vetor_cargo[idx]) + " " + hora + " Saida" + "\n")
            
            arquivo.flush()
            arquivo.close()
            
            j = 0
            arquivo_controle = open('Control.txt', 'w')
            for i in vetor_nome:
                if (i != vetor_nome[idx]):
                    arquivo_controle.writelines(str(vetor_nome[j]) + " " + str(vetor_sobrenome[j]) + " " + str(vetor_cargo[j]) + '\n')
                j += 1
            
            arquivo_controle.close()
            
            #método para apagar na lista/scroll bar
            self.lista.delete(idx)
            
            #falta acrescentar as demais coisas
            
            
            
            """gpio.setmode(gpio.BOARD)
                gpio.setup(40,gpio.OUT)
                gpio.output(40,gpio.HIGH)
                time.sleep(1)
                gpio.output(40,gpio.LOW)
                time.sleep(0.5)
                gpio.cleanup()"""
            #pass
        
            
    def backToMain():
        root.destroy()
        tela01.telaum()
        
    
    root = Tk()
    ScreenEight(root)
    root.title("Checkout Screen")
    root.geometry('478x270')
    root.mainloop()
    
if __name__ == '__main__':
    telaoito()