import queue
import socket
import threading
import queue
from megapi import *
import json

host = "10.3.141.1"
port = 4455
addr = (host, port)
name = "Robot1"
client = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
ip1 = '10.3.141.101'
ip2 = '10.3.141.102'
ip3 = '10.3.141.103'
#Ajouter les adresses ip des robots supplémentaires ci-dessous
#ip4 = ...

client.bind(("", 4455))
p = [(ip1, 4455), (ip2, 4455), (ip3, 4455)] #ajouter des cases au tableau des adresses en fonction du nombre de robots supplémentaires ajoutés

distance = 0     
vitesseD = 0
vitesseG = 0   
z = 0

        
def onReadDist(v):
    msg = "Distance " + str(v)
    msg = msg.encode("utf-8")
    client.sendto(msg, addr)


def getValVitesseD(v):
    global vitesseD
    vitesseD = v

def getValVitesseG(v):
    global vitesseG
    vitesseG = v


def getValDistance(v):
    global distance
    distance = v

def getz(level):
	global z
	z = level  

def MsgRobot():
    global msgRobot
    global z
    bot.encoderMotorSpeed(1, getValVitesseD)
    bot.encoderMotorSpeed(2, getValVitesseG)
    bot.ultrasonicSensorRead(8, getValDistance)
    bot.gyroRead(0,3,getz)
    sleep(0.1)
    msg = {
        "VD" : vitesseD,
        "VG" : vitesseG,
        "Distance" : distance,
        "z" : z
    }
    msg = json.dumps(msg)
    msg = msg.encode("utf-8")
    msgRobot = msg


def SendServer():
    global msgRobot
    client.sendto(msgRobot, addr)

def SendRobot1():
    global msgRobot
    client.sendto(msgRobot, p[0])

if __name__ == "__main__":
    bot = MegaPi()
    bot.start()
    sleep(1);
    
    
    
    def receive():
        global vitesseD
        global vitesseG
        while True:
            #Editer ici pour manipuler les informations reçues

            try:
                message, addr = client.recvfrom(1024)
                info = json.loads(message.decode("utf-8"))
                print(info["Distance"])
                if addr[0] == ip3 and float(info["Distance"]) < 20:
                    vitesseD = vitesseD + 15
                    vitesseG = vitesseD
                if addr[0] == ip2 and float(info["Distance"]) < 20:
                    vitesseD = vitesseD - 15
                    vitesseG = vitesseD
            except:
                pass
          
                           
    # def send():
    #     while True:
    #         Editer la topologie de communication ici
    



    t1 = threading.Thread(target=receive)
    # t2 = threading.Thread(target=send)

    t1.start()
    # t2.start()
    
    while True:
        sleep(0.03)
        bot.ultrasonicSensorRead(8, getValDistance)
        if distance <20:
            vitesseG = -vitesseD 
        else:     
            vitesseG = vitesseD
        bot.encoderMotorRun(1, int(vitesseD))
        bot.encoderMotorRun(2, -int(vitesseG))
