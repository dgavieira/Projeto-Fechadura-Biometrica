#Title: Biometric Lock User Interface
#Organization: Optima-UFAM
#Screen 5: Fingerprint Enrolling Calibration Screen
#Description: Gets fingerprint data for the member previously enrolled
#INPUTS: example_enroll.py
#Especs: Touchscreen LCD 3,5" 480x320
#Autor: Diego Vieira
#Review: Leonardo Arcanjo
#!/usr/local/bin/python
# -*- coding: utf-8 -*-

#tratamento de excecao na portabilidade da biblioteca tkinter
try:
    # for Python2
    from Tkinter import *
except ImportError:
    # for Python3
    from tkinter import *
#importa arquivos de telas que interagem com a atual
import tela04, tela03
#importa bibliotecas utilizadas pelos metodos da classe
import subprocess, sys, os

def telacinco():
    class ScreenFive:
        def __init__(self, master = None): #construtor da classe

            #construtor da moldura do layout
            self.primeiroContainer = Frame(master)
            self.primeiroContainer["pady"] = 10
            self.primeiroContainer.pack()
            
            self.segundoContainer = Frame(master)
            self.segundoContainer["padx"] = 20
            self.segundoContainer["pady"] = 5
            self.segundoContainer.pack(fill = X, expand = YES)
            
            self.terceiroContainer = Frame(master)
            self.terceiroContainer["padx"] = 20
            self.terceiroContainer.pack()
            
            
            #elementos do primeiro Container
            #construtor dos objetos do layout
            self.titulo = Label(self.primeiroContainer)
            self.titulo["text"] = "FINGERPRINT ENROLL"
            self.titulo["font"] = ("Arial","20","bold")
            self.titulo.pack()
            
            #elementos do segundo Container
            self.prompt = Text(self.segundoContainer)
            self.prompt["relief"] = SUNKEN
            self.prompt["height"] = 10
            self.prompt.pack()
            
            fonteBotoes = ("Arial","12")
            #elementos do terceiro Container
            self.returnButton = Button(self.terceiroContainer)
            self.returnButton["text"] = "RETURN"
            self.returnButton["font"] = fonteBotoes
            self.returnButton["command"] = self.ret_screen_four
            self.returnButton["width"] = 10
            self.returnButton.pack(side = LEFT)
            
            self.runButton = Button(self.terceiroContainer)
            self.runButton["text"] = "RUN"
            self.runButton["font"] = fonteBotoes
            self.runButton["command"] = self.run_shell
            self.runButton["width"] = 10
            self.runButton.pack(side = LEFT)

            #preguica de mexer no layout
            self.loadButton = Button(self.terceiroContainer)
            self.loadButton["text"] = "OK"
            self.loadButton["font"] = fonteBotoes
            self.loadButton["width"] = 10
            self.loadButton["command"] = self.conclude
            self.loadButton.pack(side = LEFT)
            
            
        #metodos da classe    
        def ret_screen_four(self): #retorna a tela anterior - comandado por botao RETURN
            fechar()
            tela04.telaquatro()
            
        def run_shell(self): #metodo que executa o programa example_enroll embutido
            self.prompt.delete(1.0,END)
            msg = "Executing Fingerprint Enroll"
            path = '/home/pi/github/Projeto-Fechadura-Biometrica/pyfingerprint/src/files/examples/example_enroll.py'
            
            #rotina de subprocesso - ESTA FUNCIONANDO - nao mexa nem tente entender
            process = subprocess.Popen(['lxterminal','-e','python3', path],
                                                               stdout = subprocess.PIPE,
                                                               stderr = subprocess.PIPE,
                                                               stdin = subprocess.PIPE)
            
            self.prompt.insert(END, msg)
            process.stdin.write(b'\n')
            process.stdin.flush()
            stdout, stderr = process.communicate()
            
        def conclude(self): #invoca proxima tela do fluxo
            fechar()
            tela03.telatres()
            
    def fechar():
        root.destroy()

    #execucao da tela    
    root = Tk()
    ScreenFive(root)
    root.title('Fingerprint Calibration Screen')
    root.geometry('478x320')
    root.attributes("-fullscreen",True)
    root.mainloop()

if __name__ == "__main__":  # permite executar esse script como principal
    telacinco()
