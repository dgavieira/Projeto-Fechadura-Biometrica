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
LED_BLUE = 36
LOCK_PIN = 32

try:
    f = PyFingerprint('/dev/ttyUSB0', 57600, 0xFFFFFFFF, 0x00000000)
except Exception as e:
    print('Exception message: ' + str(e))
    teladez.fechar()
    exit(1)


def acendeLed(pino_led):
    gpio.output(pino_led, 1)
    return


def apagaLed(pino_led):
    gpio.setmode(gpio.BOARD)
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
            
            self.texto.insert(END, "Initializing the sensor\n")
            
            self.widget2.after(1000, self.connectSensor) #this method calls the funcion connectSensor after 1 second.
            
            
        def connectSensor(self):
            #this function tries to connect the Fingerprint sensor e shows message of confirmation or not
            try:
                if (f.verifyPassword() == True):
                    self.showMessage("Sensor Connect\n")
                else:
                    self.showMessage("Sensor not Connected\n")
                    exit(1)
                    fechar()
            except Exception as e:
                self.showMessage("Sensor not connected\n")
                self.showMessage("Error: " + str(e) + "\n")
                self.widget2.after(2000, fechar)
                #exit(1)
                #fechar()
            
            
            self.showMessage("Waiting for finger...\n")
            
            acendeLed(LED_BLUE) #acende o LED azul
                                               
            positionIndex = readSensor()
            
            if (positionIndex == -1):
                self.showMessage("No match found!!!\n")
                self.showMessage("Try again...\n")
                pisca_led(LED_RED)
                self.connectSensor()
            else:
                pisca_led(LED_GREEN)
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
            
    def pisca_led(pin): #rotina para piscar ou o led vermelho ou verde
        apagaLed(LED_BLUE)
        acendeLed(pin)
        time.sleep(0.5)
        apagaLed(pin)
        time.sleep(0.5)
        acendeLed(pin)
        time.sleep(0.5)
        apagaLed(pin)       
    
    def fechar(): #fecha tela com o destroy e chama a tela01
        gpio.setmode(gpio.BOARD)
        gpio.setup(LED_BLUE, gpio.OUT)
        apagaLed(LED_BLUE)
        root.destroy()
        tela01.telaum()
        exit(1)
        
    def configura_GPIO(): #configura o GPIO do Rasp como modo BOARD e os pinos do LED e da trava como SAIDA
        gpio.setmode(gpio.BOARD)
        gpio.setup(LED_RED, gpio.OUT)
        gpio.setup(LED_GREEN, gpio.OUT)
        gpio.setup(LED_BLUE, gpio.OUT)
        
    def readSensor(): #le a impressao digital no sensor e retorna o index associado a impressao digital 
        i = 0
        while (f.readImage() == False):
            if (i == 1400):
                fechar()
            i = i + 1
            pass
        f.convertImage(0x01)
        result = f.searchTemplate()
        return result[0]
    
    def unlockDoor():
        gpio.setmode(gpio.BOARD)
        gpio.setup(LOCK_PIN, gpio.OUT)
        gpio.output(LOCK_PIN, 1)
        time.sleep(0.5)
        gpio.output(LOCK_PIN, 0)
        time.sleep(0.5)
        gpio.cleanup()
    
    root = Tk()
    ScreenTen(root)
    root.title("Check-in Screen")
    root.geometry("478x270")
    root.mainloop()

if __name__ == "__main__":
    teladez()