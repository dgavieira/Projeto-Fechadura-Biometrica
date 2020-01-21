#Title: Biometric Lock User Interface
#Organization: Optima-UFAM
#Screen 4: Enroll Screen
#Description: Screen for enroll a brand new lab member // Allows admin level user to confirm data before upload to database
#INPUTS: Name; Title; Button for Fingerprint Loop
#Especs: Touchscreen LCD 3,5" 480x320
#Autor: Diego Vieira
#!/usr/local/bin/python
# -*- coding: utf-8 -*-

#tratamento de excecao para portabilidade da biblioteca tkinter
try:
    # for Python2
    from Tkinter import *
except ImportError:
    # for Python3
    from tkinter import *
#importa arquivos de telas que interagem com a atual
import tela01, tela05, tela06
#importa bibliotecas adicionais utilizadas pelos metodos da classe
import sqlite3, logging, time

#cria arquivo de banco de dados e cursor
conn = sqlite3.connect('/home/pi/github/Projeto-Fechadura-Biometrica/User-Interface/optima.db')
cursor = conn.cursor()

#formata tabela
cursor.execute("""CREATE TABLE IF NOT EXISTS optima (
            member_id integer PRIMARY KEY,
            first_name TEXT NOT NULL,
            last_name TEXT NOT NULL,
            title TEXT NOT NULL,
            admin integer,
            UNIQUE (first_name, last_name))""" #cria indexação exclusiva para evitar duplicatas
            )
conn.commit()
conn.close()

def telaquatro():
    class ScreenFour:
        def __init__(self, master = None):          #construtor da tela quatro
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
            self.quartoContainer["padx"] = 20
            self.quartoContainer.pack()
            
            self.quintoContainer = Frame(master)
            self.quintoContainer["padx"] = 20
            self.quintoContainer.pack()
            
            self.sextoContainer = Frame(master)
            self.sextoContainer["padx"] = 40
            self.sextoContainer.pack()
            
            self.setimoContainer = Frame(master)
            self.setimoContainer["padx"] = 60
            self.setimoContainer.pack(fill = X, expand = YES)
            
            self.oitavoContainer = Frame(master)
            self.oitavoContainer["padx"] = 60
            self.oitavoContainer.pack()
            
            fontePadrao = ("Arial","10")
            
            # elementos do primeiro container
            self.titulo = Label(self.primeiroContainer)
            self.titulo["text"] = "ENROLL"
            self.titulo["font"] = ("Arial", "10", "bold")
            self.titulo.pack()
            
            # elementos do segundo container
            self.firstnameLabel = Label(self.segundoContainer)
            self.firstnameLabel["text"] = "First Name"
            self.firstnameLabel["font"] = fontePadrao
            self.firstnameLabel.pack(side=LEFT)
            
            self.firstname = Entry(self.segundoContainer)
            self.firstname["width"] = 30
            self.firstname["font"] = fontePadrao
            self.firstname.pack(side=LEFT)
            
            # elementos do terceiro container
            self.lastnameLabel = Label(self.terceiroContainer)
            self.lastnameLabel["text"] = "Last Name"
            self.lastnameLabel["font"] = fontePadrao
            self.lastnameLabel.pack(side=LEFT)
    
            self.lastname = Entry(self.terceiroContainer)
            self.lastname["width"] = 30
            self.lastname["font"] = fontePadrao
            self.lastname.pack(side=LEFT)
            
            # elementos do quarto container
            self.titleLabel = Label(self.quartoContainer)
            self.titleLabel["text"] = "Title\t"
            self.titleLabel["font"] = fontePadrao
            self.titleLabel.pack(side=LEFT)
      
            self.title = Entry(self.quartoContainer)
            self.title["width"] = 30
            self.title["font"] = fontePadrao
            self.title.pack(side=LEFT)
            
            # elementos do quinto container
            self.var = IntVar()
            self.check = Checkbutton(self.quintoContainer)
            self.check["font"] = fontePadrao
            self.check["text"] = "Admin"
            self.check["variable"] = self.var
            self.check.pack(side = LEFT)
            
            # elementos do sexto container
            self.botaoLoad = Button(self.sextoContainer)
            self.botaoLoad["text"] = "LOAD"
            self.botaoLoad["font"] = fontePadrao
            self.botaoLoad["command"] = self.showinput
            self.botaoLoad["width"] = 30
            self.botaoLoad.pack()
            
            #elementos do setimo container
            self.msg = Message(self.setimoContainer)
            self.msg["text"] = "First Name: \n Last Name: \n Title: \n Admin:"
            self.msg["relief"] = SUNKEN
            self.msg.pack(fill = X, expand = YES)
            
            # elementos do oitavo container
            self.botaoMainMenu = Button(self.oitavoContainer)
            self.botaoMainMenu["text"] = "MAIN MENU"
            self.botaoMainMenu["font"] = fontePadrao
            self.botaoMainMenu["width"] = 10
            self.botaoMainMenu["command"] = returntohome
            self.botaoMainMenu.pack(side = LEFT)
            
            self.botaoCancel = Button(self.oitavoContainer)
            self.botaoCancel["text"] = "CANCEL"
            self.botaoCancel["width"] = 10
            self.botaoCancel["font"] = fontePadrao
            self.botaoCancel["command"] = self.eraseinput
            self.botaoCancel.pack(side = LEFT)
            
            self.botaoFingerprint = Button(self.oitavoContainer)
            self.botaoFingerprint["text"] = "FINGERPRINT"
            self.botaoFingerprint["width"] = 10
            self.botaoFingerprint["command"] = self.enabledb
            self.botaoFingerprint.pack(side = LEFT)

        def showinput(self):
            # capta variaveis digitadas no objeto entry

            p_first_name = self.firstname.get()
            p_last_name = self.lastname.get()
            p_title = self.title.get()
            p_admin = self.var.get()

            #troca texto para string com dados adicionados
            # escreve o que foi digitado no widget msg

            if self.msg["text"] == "First Name: \n Last Name: \n Title: \n Admin:":
                if p_admin == 1:
                    self.msg["text"] = "First Name: " + p_first_name + "\n Last Name: " + p_last_name + "\n Title: " + p_title + "\n Admin: YES"
                    self.botaoLoad["state"] = DISABLED
                if p_admin == 0:
                    self.msg["text"] = "First Name: " + p_first_name + "\n Last Name: " + p_last_name + "\n Title: " + p_title + "\n Admin: NO"
                    self.botaoLoad["state"] = DISABLED
            else:
                self.msg["text"] = "First Name: \n Last Name: \n Title: \n Admin:"
                
        def eraseinput(self): #metodo que apaga a entrada digitada - comandado pelo botao CANCEL
            p_first_name = self.firstname.get()
            p_last_name = self.lastname.get()
            p_title = self.title.get()
            p_admin = self.var.get()

            # apaga o que foi mostrado no widget msg

            if self.msg["text"] == "First Name: " + p_first_name + "\n Last Name: " + p_last_name + "\n Title: " + p_title + "\n Admin: YES":
                self.msg["text"] = "First Name: \n Last Name: \n Title: \n Admin:"
                self.botaoLoad["state"] = NORMAL
                self.check.toggle()
                self.firstname.delete(0,END)
                self.lastname.delete(0,END)
                self.title.delete(0,END)
                del(p_first_name)
                del(p_last_name)
                del(p_title)
                del(p_admin)
                self.botaoFingerprint["state"] = NORMAL
            elif self.msg["text"] == "First Name: \t" + p_first_name + "\n Last Name: \t" + p_last_name + "\n Title: \t" + p_title + "\n Admin: NO":
                self.msg["text"] = "First Name: \n Last Name: \n Title: \n Admin:"
                self.botaoLoad["state"] = NORMAL
                self.firstname.delete(0,END)
                self.lastname.delete(0,END)
                self.title.delete(0,END)
                del(p_first_name)
                del(p_last_name)
                del(p_title)
                del(p_admin)
                self.botaoFingerprint["state"] = NORMAL
            else:
                pass

        # insere a entrada de usuario no banco de dados
        def enabledb(self):
            #get info by user on entry input
            p_first_name = self.firstname.get()
            p_last_name = self.lastname.get()
            p_title = self.title.get()
            p_admin = self.var.get()
            
            # tratamento de excecao para verificacao de duplicata

            # converte as strings para minusculas
            pfirstname = p_first_name.casefold()
            plastname = p_last_name.casefold()
            ptitle = p_title.casefold()

            try:
                #escreve valores no banco
                conn = sqlite3.connect('optima.db')
                cursor = conn.cursor()
                cursor.execute("""
                    INSERT INTO optima (first_name, last_name, title, admin)
                    VALUES (?, ?, ?, ?)
                    """, (pfirstname, plastname, ptitle, p_admin)
                    )
                conn.commit()
                conn.close()
                fechar()
                
                #Logging Configuration
                #logging.basicConfig(filename = 'datalog.txt', format = '%(asctime)s  %(levelname)s:  %(message)s', datefmt = '%d/%m/%Y %H:%M:%S',level=logging.DEBUG)
                # creating custom logger
                # algumas IDEs precisam que o logger seja criado na mao
                logger = logging.getLogger(__name__)
                #handler setting
                f_handler = logging.FileHandler('datalog-teste.txt')
                # handler setting
                f_handler = logging.FileHandler('datalog.txt')
                f_handler.setLevel(logging.DEBUG)
                # setting format
                f_format = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s -- %(message)s','%d/%m/%Y %H:%M:%S')
                f_handler.setFormatter(f_format)
                # Add loggers to the handler
                logger.addHandler(f_handler)

                if p_admin == 1:
                    logger.info("First Name: %s \tLast Name: %s \tTitle: %s \tAdmin:YES", p_first_name, p_last_name, p_title)
                if p_admin == 0:
                    logger.info("First Name: %s \tLast Name: %s \tTitle: %s \tAdmin:NO", p_first_name, p_last_name, p_title)

                tela05.telacinco()
                
            except: #se o python levantar uma excecao - ocorre esse loop
                if self.msg["text"] == "First Name: " + p_first_name + "\n Last Name: " + p_last_name + "\n Title: " + p_title + "\n Admin: YES":
                    self.msg["text"] = "Name already enrolled. Input new data."
                    self.botaoLoad["state"] = DISABLED
                    self.botaoFingerprint["state"] = DISABLED
                    self.check.toggle()
                    self.firstname.delete(0,END)
                    self.lastname.delete(0,END)
                    self.title.delete(0,END)
                    del(p_first_name)
                    del(p_last_name)
                    del(p_title)
                    del(p_admin)
                    self.botaoFingerprint["state"] = NORMAL
                    self.botaoLoad["state"] = NORMAL
                elif self.msg["text"] == "First Name: " + p_first_name + "\n Last Name: " + p_last_name + "\n Title: " + p_title + "\n Admin: NO":
                    self.msg["text"] = "Name already enrolled. Input new data."
                    self.botaoLoad["state"] = DISABLED
                    self.botaoFingerprint["state"] = DISABLED
                    self.firstname.delete(0,END)
                    self.lastname.delete(0,END)
                    self.title.delete(0,END)
                    del(p_first_name)
                    del(p_last_name)
                    del(p_title)
                    del(p_admin)
                    self.botaoFingerprint["state"] = NORMAL
                    self.botaoLoad["state"] = NORMAL
                else:
                    self.msg["text"] = "First Name: \n Last Name: \n Title: \n Admin:"
                    
    def returntohome(): #metodo de retornar a tela principal
        fechar()
        tela01.telaum()
    
    def fechar(): #metodo de destruir a tela atual
        root.destroy()

    # loop de inicializacao da tela
    root = Tk()
    ScreenFour(root)
    root.title("Enroll Screen")
    root.geometry('478x270')
    #root.overrideredirect(True)
    root.mainloop()

if __name__ == "__main__":  # permite executar esse script como principal
    telaquatro()

