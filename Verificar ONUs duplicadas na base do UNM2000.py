#Importando os pacotes
import mysql.connector
import re
from getpass import getpass
from socket import *
import time
import datetime
from tqdm import tqdm
import os
#from pyfiglet import Figlet

#Inicio do código
#Apenas para embelezar o código (Utilizado o PYFIGLET para criar um banner!)
print('\nCOLETAR ONUS DUPLICADAS NA REDE xPON UNM2000\n')

#f = Figlet(font='banner3-D')
#print (f.renderText('FIBER LIRA\n'))

print('''

'########:'####:'########::'########:'########:::::'##:::::::'####:'########:::::'###::::
 ##.....::. ##:: ##.... ##: ##.....:: ##.... ##:::: ##:::::::. ##:: ##.... ##:::'## ##:::
 ##:::::::: ##:: ##:::: ##: ##::::::: ##:::: ##:::: ##:::::::: ##:: ##:::: ##::'##:. ##::
 ######:::: ##:: ########:: ######::: ########::::: ##:::::::: ##:: ########::'##:::. ##:
 ##...::::: ##:: ##.... ##: ##...:::: ##.. ##:::::: ##:::::::: ##:: ##.. ##::: #########:
 ##:::::::: ##:: ##:::: ##: ##::::::: ##::. ##::::: ##:::::::: ##:: ##::. ##:: ##.... ##:
 ##:::::::'####: ########:: ########: ##:::. ##:::: ########:'####: ##:::. ##: ##:::: ##:
..::::::::....::........:::........::..:::::..:::::........::....::..:::::..::..:::::..::

FELIPE LIRA 2023

''')

#print('FELIPE LIRA\n\n')


#Informando o endereço IPv4 do UNM2000 e realizando a verificação se o endereço é válido!
server = input("Insert IP of UNM2000 Server: ")
match = re.match(r"[0-9]{1,3}\.[0-9]{1,3}\.[0-9]{1,3}\.[0-9]{1,3}", f"{server}")

while bool(match) == False:
    print("Invalid IP Address!")
    print("Formato aceito: xxx.xxx.xxx.xxx\n")
    server = input("Insert IP of UNM2000 Server: ")
    match = re.match(r"[0-9]{1,3}\.[0-9]{1,3}\.[0-9]{1,3}\.[0-9]{1,3}", f"{server}")


#Coletando o usuario do banco de dados
user_db = input("Insert User of Database UNM2000: ")
while user_db == '':
    user_db = input("Insert User of Database UNM2000: ")

#Coletando a senha do banco de dados
pass_db = getpass("Insert Password of Database UNM2000: ")
while pass_db == '':
    pass_db = getpass("Insert User of Database UNM2000: ")    


try:
    dataBase = mysql.connector.connect(
                            host = server,
                            user = user_db,
                            passwd = pass_db,
                            database = "integratecfgdb" )
        
    print(f"\nConection Estabilished with {server}\n")

   
except:
    print(f"Error in conection of database {server}")
    exit(0)


print("\nPor favor aguarde, coletando as informações...")

#Verificar todas os seriais em duplicidade
cursorObject = dataBase.cursor()
query = f"SELECT `cslotno`,  `cponno`,`cauthno`, `contmac`, `cobjectname`, Count(*) FROM `integratecfgdb`.`t_ontdevice`GROUP BY contmac HAVING Count(*) > 1;"
cursorObject.execute(query)
retorno = cursorObject.fetchall()

#Armazenar o numero de linhas de seriais em duplicidade.
total = (len(retorno))

try:
    #Para cada linha de serial em duplicidade, irá ser realizada uma consulta sobre o serial, coletando as informações de SLO | PON | ONU | SERIAL | Cliente
    #Usado oo tqdm para embelezar com uma barra de progesso
    for onu in tqdm(retorno):
        serial_onu = onu[3]
        #Realizar a consulta por serial em duplicidade
        query = f"SELECT `cslotno`,  `cponno`,`cauthno`, `contmac`, `cobjectname` FROM `integratecfgdb`.`t_ontdevice` where contmac='{serial_onu}';"
        cursorObject.execute(query)
        retorno = cursorObject.fetchall()
        #A cada consulta, é escrita as informações em um arquivo .txt
        with open(f"{server}_onus_duplicadas.txt", "a") as arquivo:
            for onu in retorno:
                onu = str(onu)
                #print(onu)
                arquivo.write(f"{onu}\n")

except:
    #Em caso de erro, o código para
    print("\nErro Encontrado\n")
    pause_app = input("Pressione alguma tecla para fechar a aplicação")
    exit(0)
    
cursorObject.close()

local = os.getcwd()

print(f"\nArquivo gravado com sucesso em: {local}")
print(f"\nTotal de ONUs duplicadas: {total}\n")

pause_app = input("Pressione alguma tecla para fechar a aplicação")
