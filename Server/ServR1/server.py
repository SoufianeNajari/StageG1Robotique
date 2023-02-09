import queue
import socket
import threading
from megapi import *
from math import *


if __name__ == "__main__":
    host = "10.3.141.1"
    port = 4455
    """ Creating the UDP socket """
    server = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    """ Bind the host address with the port """
    server.bind((host, port))
    l = [0, 0, 0]
    ip1 = '10.3.141.101'
    ip3 = '10.3.141.103'

    
    messages = queue.Queue()
    bot = MegaPi()
    bot.start()
    vitesse = 30
    bot.encoderMotorRun(1, vitesse);
    bot.encoderMotorRun(2, -vitesse);
    sleep(1);
    
    
    
    def receive():
        while True:
            try:
                message, addr = server.recvfrom(1024)
                messages.put((message, addr))
            except:
                pass
          
                           
    def send():
        global vitesse
        while True:
            while not messages.empty():
                message, addr = messages.get()
                if not addr in l and addr[0] == ip1:
                    l[0] = addr
                if not addr in l and addr[0] == ip3:
                    l[2] = addr
                print(message.decode("utf-8"))  
                info = message.decode("utf-8").split()
                if info[0] ==  'Distance':
                    if addr == l[2] and l[0]!=0:
                        server.sendto(message, l[0])
                if info[0] == 'Vitesse':
                    if addr == l[0]:
                        vitesse = floor(float(info[1]))
                               
                  
    t1 = threading.Thread(target=receive)
    t2 = threading.Thread(target=send)

    t1.start()
    t2.start()
    
    
    while True:
        sleep(0.5)
        bot.encoderMotorRun(1, vitesse)
        bot.encoderMotorRun(2, -vitesse)
    
    
    