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
    
from pyfingerprint.pyfingerprint import PyFingerprint
import time
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
            
            self.texto.insert(END, "Initializing the sensor\n")
            
            self.connectSensor()
            
        def connectSensor(self):            
            try:
                f = PyFingerprint('/dev/ttyUSB0', 57600, 0xFFFFFFFF, 0x00000000)
                msg = "Sensor Fingerprint Connected\n"
                self.texto.insert(END, msg)

            except Exception as e:
                msg = "Sensor Fingerprint could not be initialized!!!\nError: " + str(e) + "\n"
                self.texto.insert(END, msg)
            
            """try:
                msg = 'Waiting for finger...\n'
                self.texto.insert(END, msg)
                
                while(f.readImage() == False):
                    pass
                
                f.convertImage(0x01)
                
                result = f.searchTemplate()
                
                positionIndex = result[0]
                
                if (positionIndex == -1):
                    msg = 'No match found!!!\n'
                    self.texto.insert(END, msg)
                else:
                    msg = 'Found template at position #'+ str(positionIndex)+"\n"
                    self.texto.insert(END, msg)
                    #DBAcess(positionIndex)
                    #writeDatalog()
                    #fechar()
            except Exception as e:
                msg = 'Operation Failed!!!\nError: '+ str(e)+'\n'
                #self.texto.insert(END, msg)"""
    
    def fechar():
        root.destroy()
        tela01.telaum()
    
    root = Tk()
    ScreenTen(root)
    root.title("Check-in Screen")
    root.geometry("478x270")
    root.mainloop()

if __name__ == "__main__":
    teladez()