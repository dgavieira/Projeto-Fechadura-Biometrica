#Title: Biometric Lock User Interface
#Organization: Optima-UFAM
#Screen 3: ADM level menu screen
#Description: shows options on ADM level access to subscribe or delete lab members from the software database
#Especs: Touchscreen LCD 3,5" 480x320
#Autor: Diego Vieira
#Review: Leonardo Arcanjo
#!/usr/local/bin/python
# -*- coding: utf-8 -*-

#tratamento de excecao para portabilidade do tkinter
try:
    # for Python2
    from Tkinter import *
except ImportError:
    # for Python3
    from tkinter import *
#importa telas que interagem com a atual
import tela01, tela02, tela04, tela06


def telatres():
    class ScreenThree: 
        def __init__(self, master=None): #construtor da classe referente a tela 03
            #constroi "moldura"
            self.widget1 = Frame(master)
            self.widget1.pack()
            
            fontePadrao = ('Arial', '24')

            #construtor do botao ENROLL
            self.button1 = Button(self.widget1)
            self.button1["text"] = "ENROLL"
            self.button1["font"] = fontePadrao
            self.button1["width"] = 30
            self.button1["height"] = 2
            self.button1["command"] = doubleFuncEnroll
            self.button1.pack()

            #construtor do botao DELETE
            self.button2 = Button(self.widget1, text = "DELETE", font = fontePadrao,
                                  width = 30, height = 2, command = goToDelete)
            self.button2.pack()
            
            #construtor do botao CANCEL
            self.button3 = Button(self.widget1)
            self.button3["text"] = "CANCEL"
            self.button3["font"] = fontePadrao
            self.button3["width"] = 30
            self.button3["height"] = 2
            self.button3["command"] = doubleFuncExit
            self.button3.pack()
            
            #construtor do botao EXIT
            self.button4 = Button(self.widget1)
            self.button4['text'] = "EXIT"
            self.button4['font'] = fontePadrao
            self.button4['width'] = 30
            self.button4['height'] = 2
            self.button4['command'] = closeApp
            self.button4.pack()
         
    #metodos da tela 03 - destroem tela atual e abrem tela referente de acordo com o fluxo da UI

    def doubleFuncEnroll():
        fechar()
        tela04.telaquatro()


    # funcao de retornar para tela inicial
    def doubleFuncExit():
        fechar()
        tela01.telaum()


    def fechar():
        root.destroy()


    def closeApp():
        fechar()
        exit(0)


    def goToDelete():
        fechar()
        tela06.telaseis()


    #execucao da tela
    root = Tk()
    ScreenThree(root)
    root.title("ADM Level Menu Screen")
    root.geometry('478x320')
    root.overrideredirect(True)
    root.mainloop()


if __name__ == "__main__":  # permite executar esse script como principal
    telatres()
