#Title: Biometric Lock User Interface#for 
#Organization: Optima-UFAM
#Screen 5: Member Deleting Screen
#Description: Shows list of enrolled member for admin level user to delete one of them from database
#INPUTS: optima.db
#Especs: Touchscreen LCD 3,5" 480x320
#Autor: Diego Vieira
#Revision: Leonardo Arcanjo
#!/usr/local/bin/python
# -*- coding: utf-8 -*-

#tratamento de excecao de portabilidade da biblioteca tkinter
try:
    # for Python2
    from Tkinter import *
except ImportError:
    # for Python3
    from tkinter import *
#importa bibliotecas utilizadas pelos metodos da classe
from pynput.keyboard import Key, Controller
import sqlite3, readline
from pyfingerprint.pyfingerprint import PyFingerprint
from confirmation import *

#importa telas que interagem com tela atual
import tela03, tela07

def telaseis():
    class ScreenSix:
        def __init__(self, master = None):  #construtor da classe

            #layout em formato de grid
            self.primeiroContainer = Frame(master)
            self.primeiroContainer.grid(row = 0, column = 0,
                                        rowspan = 2, columnspan = 2, sticky = NW)
            
            #elementos do primeiro container
            self.lista = Listbox(self.primeiroContainer, width= 30, height = 10,
                                 font = ('MS', '12'), selectmode = BROWSE)
            
            self.scroll = Scrollbar(self.primeiroContainer, command = self.lista.yview)
            self.lista.configure(yscrollcommand = self.scroll.set)
            self.lista.pack(side=LEFT)
            self.scroll.pack(side = RIGHT, fill = Y)
            
            self.fontePadrao = ("Arial","10")
            
            #elementos do primeiro botao "UP"
            self.BotaoUp = Button(master, text = 'UP', font = self.fontePadrao,
                                  width = 18, height = 5, command = self.ScrollUp)
            self.BotaoUp.grid(row = 0, column = 2, sticky = NW)
            
            #elementos do segundo botao "DOWN"
            self.BotaoDown = Button(master, text = 'DOWN', font = self.fontePadrao,
                                    width = 18, height = 5, command = self.ScrollDown)
            self.BotaoDown.grid(row = 1, column = 2, sticky = NW)
            
            #elementos do terceiro botao "LOAD"
            self.BotaoLoad = Button(master, text = 'LOAD', font = self.fontePadrao,
                                    width = 18, height = 3, command = self.fetch_data)
            self.BotaoLoad.grid(row = 2, column = 0, sticky = SW)
            
            #elemento do quarto botao "BACK"
            self.BotaoBack = Button(master, text = "BACK", font = self.fontePadrao,
                                    width = 18, height = 3, command = backtoenroll)
            self.BotaoBack.grid(row = 2, column = 1, sticky = SW)
            
            #elemento do quinto botao "DELETE"
            self.BotaoDelete = Button(master, text = "DELETE", font = self.fontePadrao,
                                      width = 18, height = 3, command = self.run_listbox_delete)
            #A funcao delete chama a funcao run_listbox_delete
            self.BotaoDelete.grid(row = 2, column = 2, sticky = SW)
        
        
        #A funcao run_listbox_delete tem como objetivo chamar a funcao listbox_data_delete(),
        #em seguida chamar o destrutor da tela06 para construir a tela07
        def run_listbox_delete(self):
            self.listbox_data_delete()
            fechar()
            tela07.telasete()
            
        
        # Essa funcao, lista os dados presentes no DB e indica o indice (idx) associado ao usuário
        # em que se deseja apagar do DB
        def listbox_data_delete(self):
            items = self.lista.curselection()
            pos = 0
            for i in items:
                idx = int(i) - pos
                self.deletar(idx)
                pos = pos + 1

        #A funcao run_listbox_delete tem como objetivo chamar a funcao listbox_data_delete(),
        #em seguida chamar o destrutor da tela06 para construir a tela07
        def run_listbox_delete(self):
            self.listbox_data_delete()
            #fechar()
            #tela07.telasete()
        
        # Essa funcao, lista os dados presentes no db
        def listbox_data_delete(self):
            items = self.lista.curselection()
            pos = 0
            for i in items:
                idx = int(i) - pos
                print("numero da posicao da lista: %i" % idx)
                self.deletar(idx)
                pos = pos + 1
            return idx
        
        
        # This function deletes the user from DB and Listbox from the indicated number index
        # is passed as argument
        def deletar(self, number):
            self.database_data_delete(number) # Delete from DB
            self.lista.delete(number) #Delete from listbox

        def deletar(self, number):
            #tela07.telasete()
            self.lista.delete(number) #esta funcao apaga a linha da lista no Tkinter
            self.database_data_delete(number)
            
        def database_data_delete(self, numIdx):
            conn = sqlite3.connect('optima.db')
            cursor = conn.cursor()
            
            print('Idx passado como parâmetro: %i'% numIdx)
            
            cursor.execute("""SELECT member_id FROM optima ORDER BY pos_number ASC;""")
            
            row = cursor.fetchall() #Esta funcao retorna uma lista de tuplas
            
            vetor = []
            i = 0
            
            #for para pegar o conteudo das tuplas e organizá-las em uma lista
            for numero in row:
                vetor.insert(i,numero[0]) 
                i += 1
            
            print("Vetor com os member_id: ")
            print(vetor)
            
            cursor.execute("""DELETE FROM optima WHERE member_id=?""",(str(vetor[numIdx])))
            
            print("member_id apagado do Banco de Dados: %i" %vetor[numIdx])
            
            """menor = 0
            
            for i in vetor:
                if i == menor:
                    menor += 1
            
            print("Menor valor retornado eh: %i" % menor)"""
            
            
            #self.atualizaBanco()
            conn.commit()
            conn.close()
        
        
        # This function deletes the indicated indexSensor when it's passed as argument 
        def apagaIndex(self, indexSensor):
            try:
                f = PyFingerprint('/dev/ttyUSB0', 57600, 0xFFFFFFFF, 0x00000000)
                
                if(f.verifyPassword() == False ):
                    raise ValueError('The given fingerprint sensor password is wrong!')
            except Exception as e:
                print('The Fingerprint sensor could not be initialized!')
                print('Exception message: ' + str(e))
        
            try:
                if (f.deleteTemplate(indexSensor) == True):
                    print('Index Apagado!')
            except Exception as e:
                print('Operacao falhou')
                print('Excecao: ' + str(e))

        def atualizaBanco(self):
            conn = sqlite3.connect('optima.db')
            cursor = conn.cursor()
            cursor.execute("""SELECT pos_number FROM optima""")
            
            for linha in cursor.fetchall():
                numPos = linha
                print("numero do pos_number: %i" %numPos[0])
            #cursor.execute("""UPDATE optima SET pos_number = ? WHERE pos_number = ?""", (numeroAntigo,
            #                                                                             numeroNovo))
                
        
        #This function deletes the user in DB from numIdx is passed as argument
        def database_data_delete(self, numIdx):
            conn = sqlite3.connect('optima.db')
            cursor = conn.cursor()
            
            cursor.execute("""SELECT member_id FROM optima ORDER BY member_id ASC;""")
            
            row = cursor.fetchall() #This method returns a tuple list with the member_id's
            
            vetor = []
            i = 0
            
            #for loop to take the tuples content and organize them in a list
            for numero in row:
                vetor.insert(i,numero[0]) 
                i += 1
            
            cursor.execute("""SELECT pos_number FROM optima WHERE member_id=?""", (str(vetor[numIdx])))
            
            indSensor = cursor.fetchall()
            
            vetor_aux = []
            i = 0
            
            #for loop to take the only content of tuple list that's the Sensor index that it'll delete
            #on Sensor memory
            for indexSen in indSensor:
                vetor_aux.insert(0,indexSen[0])
            
            try:
                self.apagaIndex(int(vetor_aux[0]))#Deleting the fingerprint by Index in Sensor
            except TypeError:
                print("Nao ha index associado a este usuario")
            
            cursor.execute("""DELETE FROM optima WHERE member_id=?""",(str(vetor[numIdx])))
                    
            conn.commit()
            conn.close()
            
                        
        def fetch_data(self): #database query main loop
            conn = sqlite3.connect('optima.db')  #instancia o banco de dados
            cursor = conn.cursor()
            cursor.execute("""SELECT
                               first_name AS FIRST_NAME,
                               last_name AS LAST_NAME,
                               title AS TITLE,
                               admin AS ADMIN_LEVEL,
                               pos_number AS POSITION_NUMBER
                           FROM optima""")
            rows = cursor.fetchall()
            
            self.lista.delete(0,END) #essa funcao serve para deletar tudo que aparece na scroll bar
            
            for row in rows:
                self.lista.insert(END, row)
            
            self.lista.focus_set()
            
        def ScrollDown(self):
            keyboard = Controller()
            keyboard.press(Key.down)
            keyboard.release(Key.down)
            
        def ScrollUp(self):
            keyboard = Controller()
            keyboard.press(Key.up)
            keyboard.release(Key.up)
                
    def fechar():
        root.destroy()
        
    def backtoenroll():
        fechar()
        tela03.telatres()
            
    root = Tk()
    ScreenSix(root)
    root.title("Delete Screen")
    root.geometry('478x270')
    #root.overrideredirect(True)
    root.mainloop()

if __name__ == "__main__":  # permite executar esse script como principal
    telaseis()
