import queue
import socket
import threading
from megapi import *
import random


host = "10.3.141.1"
port = 4455
addr = (host, port)
name = "Robot1"
ip1 = '10.3.141.101'
ip2 = '10.3.141.102'
ip3 = '10.3.141.103'
client = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
p = [(ip1, port), (ip2, port), (ip3, port)]

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
    bot = MegaPi()
    bot.start()
    vitesseD = 30
    vitesseG = vitesseD
    # bot.encoderMotorRun(1,vitesseD);
    # bot.encoderMotorRun(2, -vitesseG);
    sleep(1);
    
    
    
    
    def receive():
        global vitesseD
        global vitesseG
        while True:
            try:
                message, addr = client.recvfrom(1024)
                info = message.decode("utf-8").split()
                print(info)
                if info[0] == 'Distance':
                    if info[2] == "Robot3":
                        if float(info[1]) < 20:
                            vitesseD = vitesseD + 15
                    if info[2] == "Robot2" and vitesseD >= 15:
                        if float(info[1]) < 20:
                            vitesseD = vitesseD - 15
                    vitesseG = vitesseD
            except:
                pass
          
                           
   # def send():
    #    while True:  
    #        sleep(0.01);
    #        bot.ultrasonicSensorRead(8,onReadDist);
    #        bot.encoderMotorSpeed(1,onReadVitD);
    #        bot.encoderMotorSpeed(2,onReadVitG);
            
            
    t1 = threading.Thread(target=receive)
    #t2 = threading.Thread(target=send)

    t1.start()
    #t2.start()
    
    
    # while True:
    #     sleep(0.03)
    #     bot.ultrasonicSensorRead(8, getValDistance)
    #     if distance <20:
    #         bot.encoderMotorRun(1, 0)
    #         vitesseG = -vitesseD - vitesseD//2 
    #     else:
            
    #         vitesseG = vitesseD
    #     bot.encoderMotorRun(1, vitesseD)
    #     bot.encoderMotorRun(2, -vitesseG)
