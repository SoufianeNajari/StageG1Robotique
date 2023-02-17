import queue
import socket
import threading
from megapi import *
from math import *
import numpy as np





host = "10.3.141.1"
port = 4455
server = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
server.bind((host, port))
ip1 = '10.3.141.101'
ip2 = '10.3.141.102'
ip3 = '10.3.141.103'
#Ajouter les adresses ip des robots supplémentaires ci-dessous
#ip4 = ...

p = [(ip1, 4455), (ip2, 4455), (ip3, 4455)] #ajouter des cases au tableau des adresses en fonction du nombre de robots supplémentaires ajoutés


    
messages = queue.Queue()      
def receive():
    while True:
        try:
            message, addr = server.recvfrom(1024)
            #Editer ici pour manipuler les informations reçues

            messages.put((message, addr))
            print(message.decode("utf-8"))
        except:
            pass
          
                           
def send():
    while True:
        while not messages.empty():
            #Editer la topologie de communication ici
            
            message, addr = messages.get()
            server.sendto(message, p[0])
            server.sendto(message, p[1])
            server.sendto(message, p[2])
            

                
                                         
                  
t1 = threading.Thread(target=receive)
t2 = threading.Thread(target=send)

t1.start()
t2.start()
    