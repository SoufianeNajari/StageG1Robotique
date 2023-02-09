import queue
import socket
import threading
from megapi import *
import random


host = "10.3.141.1"
port = 4455
addr = (host, port)
client = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)

u =0


def onReadDist(v):
    msg = "Distance " + str(v)
    msg = msg.encode("utf-8")
    client.sendto(msg, addr)


def onReadVit(v):
    msg = "Vitesse " + str(v)
    msg = msg.encode("utf-8")
    client.sendto(msg, addr)
    


def getVal(v):
    global u
    u = v
    
    
    
if __name__ == "__main__":
    name = "Robot1"
    """ Creating the UDP socket """
    data = "Connexion"
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
          
                           
    def send():
        while True:  
            sleep(1);
            #bot.ultrasonicSensorRead(8,onReadDist);
            bot.encoderMotorSpeed(1,onReadVit);
            
            
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
