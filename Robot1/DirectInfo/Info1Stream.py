import queue
import socket
import threading
from megapi import *
import random



# def onReadDist(v):
#     msg = "Distance " + str(v)
#     msg = msg.encode("utf-8")
#     client.sendto(msg, addr)


def getValVitesseD(v):
    global vitesseD
    vitesseD = v
    

def getValVitesseG(v):
    global vitesseG
    vitesseG = v


def getValDistance(v):
    global distance
    distance = v

def SendVitesseServer():
    bot.encoderMotorSpeed(1, getValVitesseD)
    bot.encoderMotorSpeed(2, getValVitesseG)
    msg = "Vitesse " + str(vitesseD) + " " + str(vitesseG) + " " + name
    msg = msg.encode("utf-8")
    client.sendto(msg, addr)

def SendVitesse2():
    bot.encoderMotorSpeed(1, getValVitesseD)
    bot.encoderMotorSpeed(2, getValVitesseG)
    msg = "Vitesse " + str(vitesseD) + " " + str(vitesseG) + " " + name
    msg = msg.encode("utf-8")
    client.sendto(msg, p[1])
    


def receive():
    global vitesseD
    global vitesseG
    while True:
        try:
            message, addr = client.recvfrom(1024)
            info = message.decode("utf-8").split()
            print(message.decode("utf-8"))
        except:
            pass
          
                           
def send():
    while True:  
        sleep(1);
        SendVitesseServer()
        try:
            SendVitesse2()
        except:
            pass

    
if __name__ == "__main__":
    ip4_server = "10.3.141.1"
    port = 4455
    addr = (ip4_server, port)
    name = "Robot1"
    ip1 = '10.3.141.101'
    ip2 = '10.3.141.102'
    ip3 = '10.3.141.103'
    client = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    client.bind(("0.0.0.0", 5001))
    p = [(ip1, 5001), (ip2, 5002), (ip3, 5003)]

    distance = 0
    vitesseD = 0
    vitesseG = 0  

    bot = MegaPi()
    bot.start()
    # vitesseD = 30
    # vitesseG = vitesseD
    # bot.encoderMotorRun(1,vitesseD);
    # bot.encoderMotorRun(2, -vitesseG);
    sleep(1);
    
    
      
    t1 = threading.Thread(target=receive)
    t2 = threading.Thread(target=send)

    t1.start()
    t2.start()
    
    
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
