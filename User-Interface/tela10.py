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
from datetime import datetime
import RPi.GPIO as gpio
import sqlite3, time, tela01

#define os pinos do LED RGB e o pino da trava
LED_RED = 40
LED_GREEN = 38
lock_pin = 36

try:
    f = PyFingerprint('/dev/ttyUSB0', 57600, 0xFFFFFFFF, 0x00000000)
except Exception as e:
    print('Exception message: ' + str(e))

def acendeLed(pino_led):
    gpio.output(pino_led, 1)
    return

def apagaLed(pino_led):
    gpio.output(pino_led,0)
    return

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
            
            configura_GPIO() #configura os GPIO
            
            acendeLed(LED_RED) #acende o LED vermelho
            
            self.texto.insert(END, "Initializing the sensor\n")
            
            self.widget2.after(1000, self.connectSensor) #this method calls the funcion connectSensor after 1 second.
            
            
        def connectSensor(self):
            #this function tries to connect the Fingerprint sensor e shows message of confirmation or not
            
            if (f.verifyPassword() == True):
                self.showMessage("Sensor Connect\n")
            else:
                self.showMessage("Sensor not Connected\n")
            
            self.showMessage("Waiting for finger...\n")
                                               
            positionIndex = readSensor()
            
            if (positionIndex == -1):
                self.showMessage("No match found!!!\n")
                self.showMessage("Try again...\n")
                apagaLed(LED_RED)
                time.sleep(0.5)
                acendeLed(LED_RED)
                time.sleep(0.5)
                apagaLed(LED_RED)
                time.sleep(0.5)
                self.connectSensor()
            else:
                apagaLed(LED_RED)
                acendeLed(LED_GREEN)
                time.sleep(0.5)
                apagaLed(LED_GREEN)
                time.sleep(0.5)
                acendeLed(LED_GREEN)
                time.sleep(0.5)
                apagaLed(LED_GREEN)
                time.sleep(0.5)
                self.DBAcess(positionIndex)
            
            unlockDoor()
            
            self.widget2.after(3000, fechar)
            
        
        def showMessage(self, mensagem):
            self.texto.insert(END, mensagem)
                
        def DBAcess(self, index):
            #this function connects optima DB and searches the user associated to fingerprint index
            #and salves the user's entry in Stream.txt file
            conn = sqlite3.connect("/home/pi/github/Projeto-Fechadura-Biometrica/User-Interface/optima.db")
            cursor = conn.cursor()
            cursor.execute("""SELECT
                        first_name AS FIRST_NAME,
                        last_name AS LAST_NAME,
                        title AS TITLE
                        FROM optima WHERE pos_number=?""", (str(index)))
            rows = cursor.fetchall()
        
            conn.commit()
            conn.close()
        
            for row in rows:
                continue
                
            msg = "Bem vindo " + str(row[0]) + " " + str(row[1])
            self.texto.insert(END, msg)
            
            now = datetime.now()
            hora = now.strftime("%d/%m/%Y %H:%M:%S")
            arquivo = open('/home/pi/github/Projeto-Fechadura-Biometrica/User-Interface/Stream.txt', 'a')
            arquivo.writelines(str(row[0]) + " " + str(row[1]) + " " + str(row[2]) + " " + hora
                               + " Entrada\n")
            arquivo.flush()
            arquivo.close()
            
            arquivo_controle = open('/home/pi/github/Projeto-Fechadura-Biometrica/User-Interface/Control.txt', 'a')
            arquivo_controle.writelines(str(row[0]) + " " + str(row[1]) + " " + str(row[2]) + "\n")
            arquivo_controle.flush()
            arquivo_controle.close()
            
    
    def fechar(): #fecha tela com o destroy e chama a tela01
        root.destroy()
        tela01.telaum()
        
    def configura_GPIO(): #configura o GPIO do Rasp como modo BOARD e os pinos do LED e da trava como SAIDA
        gpio.setmode(gpio.BOARD)
        gpio.setup(LED_RED, gpio.OUT)
        gpio.setup(LED_GREEN, gpio.OUT)
        gpio.setup(lock_pin, gpio.OUT)
        
    def readSensor(): #le a impressao digital no sensor e retorna o index associado a impressao digital 
        while (f.readImage() == False):
            pass
        f.convertImage(0x01)
        result = f.searchTemplate()
        return result[0]
    
    def unlockDoor():
        gpio.output(lock_pin, gpio.HIGH)
        time.sleep(1)
        gpio.output(lock_pin, gpio.LOW)
        time.sleep(1)
        gpio.cleanup()
    
    root = Tk()
    ScreenTen(root)
    root.title("Check-in Screen")
    root.geometry("478x270")
    root.mainloop()

if __name__ == "__main__":
    teladez()