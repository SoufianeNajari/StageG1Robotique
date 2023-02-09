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
p = [(ip1, 5001), (ip2, 5002), (ip3, 5003)]

    
messages = queue.Queue()      
def receive():
    while True:
        try:
            message, addr = server.recvfrom(1024)
            messages.put((message, addr))
            print(message.decode("utf-8"))
        except:
            pass
          
                           
def send():
    while True:
        while not messages.empty():
            message, addr = messages.get()
            # server.sendto(message, p[0])
            # server.sendto(message, p[1])
            # server.sendto(message, p[2])
            

                
                                         
                  
t1 = threading.Thread(target=receive)
t2 = threading.Thread(target=send)

t1.start()
t2.start()
    