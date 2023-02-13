import queue
import socket
import threading
import queue
from megapi import *
import json

host = "10.3.141.1"
port = 4455
addr = (host, port)
name = "Robot3"
client = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
ip1 = '10.3.141.101'
ip2 = '10.3.141.102'
ip3 = '10.3.141.103'
client.bind(("0.0.0.0", 4455))
p = [(ip1, 4455), (ip2, 4455), (ip3, 4455)]
bot = MegaPi()
bot.start()
# vitesseD = 30
# vitesseG = vitesseD
# bot.encoderMotorRun(1,vitesseD);
# bot.encoderMotorRun(2, -vitesseG);
sleep(1);


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
        while True:
            try:
                message, addr = client.recvfrom(1024)
                info = message.decode("utf-8")
                print(info)
            except:
                pass
          
                           
    def send():
        while True:
            sleep(1)
            SendServer()
            try:
                SendRobot1()
            except:
                pass


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