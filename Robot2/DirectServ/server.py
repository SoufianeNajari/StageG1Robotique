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
    n = 0

    
    messages = queue.Queue()


    def receive():
        while True:
            try:
                message, addr = server.recvfrom(1024)
                messages.put((message, addr))
            except:
                pass
          
                           
    def send():
        global n
        while True:
            while not messages.empty():
                message, addr = messages.get()
                if not addr in l and addr[0] == ip1:
                    l[0] = addr
                if not addr in l and addr[0] == ip3:
                    l[2] = addr
                if l[0] != 0 and l[2] != 0 and n == 0:
                    s = ' '.join(map(str, l[0])) + ' ' + ' '.join(map(str, l[2]))
                    s = s.encode("utf-8")
                    server.sendto(s, l[0])
                    server.sendto(s, l[2])
                    n += 1
                    
                    
                
                               
                  
    t1 = threading.Thread(target=receive)
    t2 = threading.Thread(target=send)

    t1.start()
    t2.start()
    
 
