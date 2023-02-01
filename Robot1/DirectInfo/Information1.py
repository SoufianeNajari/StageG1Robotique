import queue
import socket
import threading
from megapi import *
import random


host = "172.31.208.173"
port = 4455
addr = (host, port)
client = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)

distance = 0


def onReadDist(v):
    msg = "Distance " + str(v)
    msg = msg.encode("utf-8")
    client.sendto(msg, addr)


def onReadVitD(v):
    msg = "Vitesse " + str(v) + " 1"
    msg = msg.encode("utf-8")
    client.sendto(msg, addr)
    

def onReadVitG(v):
    msg = "Vitesse " + str(v) + " 2"
    msg = msg.encode("utf-8")
    client.sendto(msg, addr)


def getValDistance(v):
    global distance
    distance = v
    
    
    
if __name__ == "__main__":
    name = "Robot1"
    """ Creating the UDP socket """
    data = "Connexion"
    data = data.encode("utf-8")
    client.sendto(data, addr)
    message, addr = client.recvfrom(1024)
    adresses = message.decode("utf-8").split()
    p = [(adresses[0], int(adresses[1])), 0, (adresses[2], int(adresses[3]))]
    bot = MegaPi()
    bot.start()
    vitesseD = 30
    vitesseG = 30
    bot.encoderMotorRun(1,vitesseD);
    bot.encoderMotorRun(2, -vitesseG);
    sleep(1);
    
    
    
    
    def receive():
        global vitesseD
        global vitesseG
        while True:
            try:
                message, addr = client.recvfrom(1024)
                info = message.decode("utf-8").split()
                if info[0] == 'Distance':
                    if float(info[1]) < 10:
                        vitesseD = vitesseD + 15
                        vitesseG = vitesseD
                print(message)
            except:
                pass
          
                           
   # def send():
    #    while True:  
    #        sleep(0.01);
    #        #bot.ultrasonicSensorRead(8,onReadDist);
    #        bot.encoderMotorSpeed(1,onReadVitD);
    #        bot.encoderMotorSpeed(2,onReadVitG);
            
            
    t1 = threading.Thread(target=receive)
    t2 = threading.Thread(target=send)

    t1.start()
    t2.start()
    
    
    while True:
        sleep(0.03)
        bot.ultrasonicSensorRead(8, getVal)
        if u <20:
            bot.encoderMotorRun(1, 0)
            vitesseG = -vitesseD - vitesseD//2 
        else:
            
            vitesseG = vitesseD
        bot.encoderMotorRun(1, vitesseD)
        bot.encoderMotorRun(2, -vitesseG)
