import queue
import socket
import threading
from megapi import *

host = "172.31.208.173"
port = 4455
addr = (host, port)
client = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
data = "Connexion"
data = data.encode("utf-8")
client.sendto(data, addr)
message, addr = client.recvfrom(1024)
adresses = message.decode("utf-8").split()
p = [(adresses[0], int(adresses[1])), 0, (adresses[2], int(adresses[3]))]

distance = 0        
        
def onReadDist(v):
    msg = "Distance " + str(v)
    msg = msg.encode("utf-8")
    client.sendto(msg, addr)


def SendVitesse1(v):
    msg = "Vitesse " + str(v)
    msg = msg.encode("utf-8")
    client.sendto(msg, p[0])

def SendDistance1(v):
    msg = "Distance " + str(v)
    msg = msg.encode("utf-8")
    client.sendto(msg, p[0])


def getValDistance(v):
    global distance
    distance = v


if __name__ == "__main__":
    name = "Robot3"
    """ Creating the UDP socket """
    bot = MegaPi()
    bot.start()
    sleep(1);
    
    
    
    def receive():
        while True:
            try:
                message, addr = client.recvfrom(1024)
                info = message.decode("utf-8").split()
                
                print(message)
            except:
                pass
          
                           
    def send():
        while True:
            sleep(2);
            bot.ultrasonicSensorRead(8, getValDistance)
            if distance < 20:
               bot.ultrasonicSensorRead(8,SendDistance1)
            #bot.encoderMotorSpeed(1,onReadVit);
             
            
    t1 = threading.Thread(target=receive)
    t2 = threading.Thread(target=send)

    t1.start()
    t2.start()
    
    
   # while True:
   #     sleep(0.1)
   #     bot.encoderMotorRun(1, vitesse)
    #    bot.encoderMotorRun(2, -vitesse)
    #    if f