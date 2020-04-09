#Title: Biometric Lock User Interface
#Organization: Optima-UFAM
#Screen 2: Search Screen for ADM users
#Description:Starts the Fingerprint search loop only for ROOT ADM users
#Especs: Touchscreen LCD 3,5" 480x320
#Autor: Diego Vieira
#!/usr/local/bin/python
#-*- coding: utf-8 -*-

#tratamento de excecao para portabilidade do tkinter
try:
    # for Python2
    from Tkinter import *
except ImportError:
    # for Python3
    from tkinter import *

import tela01, tela03
import sqlite3, hashlib

#essa tela ainda precisa ser trocada pra chamar via fingerprint

def teladois():

    class ScreenTwo:  # classe
        def __init__(self, master=None):
            # construtores de containers

            self.fontePadrao = ("Arial", "10")
            self.primeiroContainer = Frame(master)
            self.primeiroContainer["pady"] = 10
            self.primeiroContainer.pack()

            self.segundoContainer = Frame(master)
            self.segundoContainer["padx"] = 20
            self.segundoContainer.pack()

            self.terceiroContainer = Frame(master)
            self.terceiroContainer["padx"] = 20
            self.terceiroContainer.pack()

            self.quartoContainer = Frame(master)
            self.quartoContainer["pady"] = 20
            self.quartoContainer.pack()

            self.quintoContainer = Frame(master)
            self.quintoContainer["pady"] = 20
            self.quintoContainer.pack()

            # contrutores de objetos
            self.titulo = Label(self.primeiroContainer, text="MASTER FINGER")
            self.titulo["font"] = ("Arial", "10", "bold")
            self.titulo.pack()

            self.nomeLabel = Label(self.segundoContainer, text="Nome", font=self.fontePadrao)
            self.nomeLabel.pack(side=LEFT)

            self.nome = Entry(self.segundoContainer)
            self.nome["width"] = 30
            self.nome["font"] = self.fontePadrao
            self.nome.pack(side=LEFT)

            self.senhaLabel = Label(self.terceiroContainer, text="Senha", font=self.fontePadrao)
            self.senhaLabel.pack(side=LEFT)

            self.senha = Entry(self.terceiroContainer)
            self.senha["width"] = 30
            self.senha["font"] = self.fontePadrao
            self.senha["show"] = "*"
            self.senha.pack(side=LEFT)

            self.autenticar = Button(self.quartoContainer)
            self.autenticar["text"] = "LOGIN"
            self.autenticar["font"] = ("Calibri", "8")
            self.autenticar["width"] = 12
            self.autenticar["command"] = self.verificaSenha
            self.autenticar.pack()

            self.mensagem = Label(self.quartoContainer, text="", font=self.fontePadrao)
            self.mensagem.pack()

            self.home = Button(self.quintoContainer)
            self.home["text"] = "MAIN MENU"
            self.home["font"] = ("Calibri", "8")
            self.home["width"] = 12
            self.home["command"] = returntohome
            self.home.pack(side=BOTTOM)

        # metodos
        def verificaSenha(self):
            usuario = self.nome.get()
            senha = self.senha.get()
            
            puser = usuario.casefold()
            
            #tenta conectar o usuario de acordo com o nome digitado, senão existir executa-se a excessao
            try:
                senha = senha.encode('utf-8')
                senha = hashlib.sha256(senha).hexdigest()
                
                conn = sqlite3.connect('/home/pi/github/Projeto-Fechadura-Biometrica/User-Interface/optima.db')
                cursor = conn.cursor()
                
                cursor.execute("""SELECT senhas, admin FROM optima WHERE first_name=?""", (puser,))
                
                row = cursor.fetchall()
                
                conn.commit()
                conn.close()
                
                vetor = []
                i = 0
                
                for j in row[0]:
                    vetor.insert(i,j)
                    i += 0
                
                if (vetor[0] == 1) and (vetor[1] == senha):
                    self.mensagem['text'] = "Access Allow"
                    fechar()
                    tela03.telatres()
                elif (vetor[0] == 1) and (vetor[1] != senha):
                    self.mensagem['text'] = "Password Wrong"
                else:
                    self.mensagem['text'] = "Access Denied"
                
            except:
                self.mensagem['text'] = "User does not exist"
                

    # metodo de retorno a tela um - chamado pelo comando do botao MAIN MENU
    def returntohome():
        fechar()
        tela01.telaum()

    def fechar():
        root.destroy()

    # loop de inicializacao da tela

    root = Tk()
    ScreenTwo(root)
    root.title("Admin Access")
    root.geometry('478x270')
    # root.overrideredirect(True)
    root.mainloop()

if __name__ == "__main__": #permite executar esse script como principal
    teladois()

