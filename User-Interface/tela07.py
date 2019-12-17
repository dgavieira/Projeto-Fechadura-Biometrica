#Title: Biometric Lock User Interface
#Organization: Optima-UFAM
#Screen 7: Verification Screen
#Description: Screen for make sure the ADMIN really wants to delete a member from the database
#Especs: Touchscreen LCD 3,5" 480x320
#Autor: Diego Vieira
#Revison: Leonardo Arcanjo
#!/usr/local/bin/python
# -*- coding: utf-8 -*-

try:
    # for Python2
    from Tkinter import *
except ImportError:
    # for Python3
    from tkinter import *

import tela01, tela03, tela06
from confirmation import *

def telasete():
    class ScreenSeven():
        def __init__(self, master = None):
            
            self.fontePadrao = ("Arial","24")
            
            self.widget1 = Frame(master)
            self.widget1.pack()
            
            self.msg = Label(self.widget1, text = "ARE YOU SURE?", font = self.fontePadrao,
                             height = 5)
            self.msg.pack()
            
            self.yes = Button(self.widget1, text = "YES", font = self.fontePadrao, width = 12)
            self.yes["command"] = toConfirm
            #self.yes["command"] = returnTela03
            self.yes.pack(side=LEFT)
            
            self.no = Button(self.widget1,text = "NO", font = self.fontePadrao, width = 18,
                             command = returnTela06)
            self.no.pack(side=RIGHT)
            
            self.widget2 = Frame(master)
            self.widget2.pack(side=BOTTOM)
            
            self.home = Button(self.widget2,text = "MAIN MENU", font = ('Calibri', 8),
                               width = 12, command = returntohome)
            self.home.pack(side=BOTTOM)
            
            
        """def database_data_delete(self):
            num = listbox_data_delete()
            
            pos_number_db = num - 1
            
            conn = sqlite3.connect('optima.db')
            cursor = conn.cursor()
            sql = 'DELETE FROM optima WHERE pos_number=?'
            cursor.execute(sql,(pos_number_db,))
            
            fechar()
            tela03.telatres()"""
    
    def toConfirm():
        variable = True
        Confirmation(variable)
        fechar()
        tela06.telaseis()
            
    def returntohome():
        fechar()
        tela01.telaum()
    
    def fechar():
        root.destroy()
        
    def returnTela03():
        fechar()
        tela03.telatres()
    
    def returnTela06():
        fechar()
        tela06.telaseis()
        
            
    root = Tk()
    ScreenSeven(root)
    root.title("Verification Screen")
    root.geometry('478x270')
    #root.overrideredirect(True)
    root.mainloop()
        
if __name__ == "__main__":  # permite executar esse script como principal
    telasete()