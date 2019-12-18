#Teste do Algoritmo de Verificação de Entrada
#Author: Leonardo Arcanjo

from pyfingerprint.pyfingerprint import PyFingerprint
import sqlite3
from datetime import datetime

try:
    f = PyFingerprint('/dev/ttyUSB0', 57600, 0xFFFFFFFF, 0x00000000)
    print('Sensor Connected')
except Exception as e:
    print('The Fingerprint sensor could not be initialized!')
    print('Exception message: ' + str(e))
    exit(1)
    
try:
    print('Waiting for finger...')
    
    while(f.readImage() == False):
        pass
    
    f.convertImage(0x01)
    
    result = f.searchTemplate()
    
    positionIndex = result[0]
    
    if(positionIndex == -1):
        print('No match found!!!')
        exit(0)
    else:
       print('Found template at position #' + str(positionIndex))
       #AcessoBanco(positionIndex)
       conn = sqlite3.connect('optima.db')
       cursor = conn.cursor()
       cursor.execute("""SELECT
                        first_name AS FIRST_NAME,
                        last_name AS LAST_NAME,
                        title as TITLE
                    FROM optima WHERE pos_number=?""", (str(positionIndex)))
       rows = cursor.fetchall()
       
       conn.commit()
       conn.close()
     
       for row in rows:
           print("Imprimindo row... ")
           print(row)
       
       now = datetime.now()
       hora = now.strftime("%d/%m/%Y %H:%M:%S")
       arquivo = open('Stream.txt', 'a')
       arquivo.writelines(str(row[0]) + " " + str(row[1]) + " " + str(row[2]) + " " + hora + " Entrada" + "\n")
       
       arquivo.flush()
       arquivo.close()
       
       arquivo_controle = open('Control.txt', 'a')
       arquivo_controle.writelines(str(row[0]) + " " + str(row[1]) + " " + str(row[2]) + "\n")
       arquivo_controle.flush()
       arquivo_controle.close()
       
except Exception as e:
    print('Operation failed!!!')
    print('Exception message: ' + str(e))
    exit(1)        
    