import queue
import socket
import threading
from megapi import *
import time
import numpy as np
import json

def onReadVitD(v):
    global vD
    vD = (v/60)*perim
    
def onReadVitG(v):
    global vG
    vG = (v/60)*perim

def SendVitesse1(v):
    msg = "Vitesse " + str(v)
    msg = msg.encode("utf-8")
    client.sendto(msg, p[0])

def SendDistance1(v):
    msg = "Distance " + str(v) + " " + name
    msg = msg.encode("utf-8")
    client.sendto(msg, p[0])


def getValVitesseD(v):
    global vitesseD
    vitesseD = v


def getz(level):
	global z
	z = level  

def getValVitesseG(v):
    global vitesseG
    vitesseG = v


def getValDistance(v):
    global distance
    distance = v


def MsgRobot():
    global msgRobot
    bot.encoderMotorSpeed(1, getValVitesseD)
    bot.encoderMotorSpeed(2, getValVitesseG)
    bot.ultrasonicSensorRead(8, getValDistance)
    bot.gyroRead(0,3,getz);
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


def SendRobot3():
    global msgRobot
    client.sendto(msgRobot, p[2])


def getzinit(level):
	global zinit
	zinit = level

def straight(Distance): #Selon x pour l'instant
    global x 
    global y
    global phi
    global zstart
    #Gyro
    global zinit
    global z

    DistanceParcourue = 0
    xaux = x
    yaux = y
    bot.gyroRead(0,3,onReadzinit);

    bot.encoderMotorRun(1, vDc)
    bot.encoderMotorRun(2, -vGc)
    
    temps = time.time()
    while DistanceParcourue < Distance:
        sleep(0.001)
        
        if (time.time() - temps) >= deltaT:
            temps = time.time()
            
            
            bot.gyroRead(0,3,getz);
            angle = (z - zinit)/10 
            if z - zinit<0:
                temp = vDc - (33)*(angle)
                """ print("---------------GAUCHE-----------------") """
                bot.encoderMotorRun(1, int(temp))
                bot.encoderMotorRun(2, -vGc)
            else:
                temp = -vGc - (33)*(angle)
                """ print("---------------DROITE-----------------") """
                bot.encoderMotorRun(1, vDc) #c pour consigne
                bot.encoderMotorRun(2, int(temp))
            
            bot.encoderMotorSpeed(1,onReadVitD)
            bot.encoderMotorSpeed(2,onReadVitG);

            phiaux = (z-zstart)*0.01745
            
            bot.gyroRead(0,3,getz);
             
            x = x + (deltaT/2)*(vD - vG)*(1-(phiaux**2)/2)
            y = y + (deltaT/2)*(vD - vG)*phiaux
            
            DistanceParcourue = np.sqrt((x - xaux)**2 + (y - yaux)**2)

            
    # print("x : "+str(x)+ "            y  : "+str(y)+ "         phi : "+str(phi)) 
    #Gyro
    bot.gyroRead(0,3,getz);  
    # print("zinit : "+str(zinit) + "     z : "+str(z))

    bot.encoderMotorRun(1, 0) #c pour consigne
    bot.encoderMotorRun(2, 0)      

def turnRight(angle):
    global x 
    global y
    global phi
    global zstart
    #Gyro
    global zinit
    global z
    phiaux = phi
    angle = angle - 0.08
    while angle < 0:
        angle = angle + 2*np.pi
    sleep(0.02)
    bot.gyroRead(0,3,getzinit);
    sleep(0.1)
    zinit2 = zinit*0.01745 #en rad
    z2=zinit2
    print(zinit)
    temps = time.time()
    while (zinit2-angle<z2<zinit2+0.01 and zinit2>=angle - 3.1415) or (zinit2<=angle - 3.1415 and (z2>=zinit2+2*3.1415-angle or z2<zinit2+0.1)):
        sleep(0.002)
        
        if (time.time() - temps) >= deltaT:
            temps = time.time()
            
            bot.encoderMotorRun(1, -35)
            bot.encoderMotorRun(2, -35)
            
            bot.encoderMotorSpeed(1,onReadVitD);
            bot.encoderMotorSpeed(2,onReadVitG);
            
            bot.gyroRead(0,3, getz);
            phiaux = (z-zinit)*0.01745 
            
            
            x = x + (deltaT/2)*(vD - vG)*np.cos(phiaux)
            y = y + (deltaT/2)*(vD - vG)*np.sin(phiaux)

            bot.gyroRead(0,3,getz);
            sleep(0.005)
            z2 = z*0.01745
            sleep(0.001)
            
                
    """ print("x : "+str(x)+ "            y  : "+str(y)+ "         phi : "+str(phiaux)) """

    bot.encoderMotorRun(1, 0) #c pour consigne
    bot.encoderMotorRun(2, 0)
    sleep(0.2)
    bot.gyroRead(0,3,getzinit);
    sleep(0.1)
    print(z)
    sleep(0.1)


def onReadzinit(level):
	global zinit
	zinit = level

def receive():
    while True:
        try:
            message, ad = client.recvfrom(1024)
            info = message.decode("utf-8").split()
            if info[0] ==  "Stop":
                bot.encoderMotorRun(1,0);
                bot.encoderMotorRun(2, 0);
            if info[0] == "Avance":
                bot.encoderMotorRun(1,30);
                bot.encoderMotorRun(2, -30);
            print(message.decode("utf-8"))
        except:
            pass
                            
def send():
    while True:
        sleep(0.1);
        MsgRobot()
        SendServer()
        try:
            SendRobot3()
        except:
            pass


if __name__ == "__main__":
    ip_server = "10.3.141.1"
    port = 4455
    addr = (ip_server, port)
    name = "Robot2"
    client = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    ip1 = '10.3.141.101'
    ip2 = '10.3.141.102'
    ip3 = '10.3.141.103'
    client.bind(("", 4455))
    p = [(ip1, 4455), (ip2, 4455), (ip3, 4455)]
    bot = MegaPi()
    bot.start()
    distance = 0  
    zinit = 0
    zstart = 0
    vDc = 60
    vGc = 60
    L = 19
    perim = np.pi*5.75
    vD = 0
    vG = 0
    phi = 0
    x, y, z = 0, 0, 0
    deltaT = 0.07
    vitesseD = 30
    vitesseG = vitesseD
    bot.encoderMotorRun(1,vitesseD);
    bot.encoderMotorRun(2, -vitesseG);
    sleep(1);


    t1 = threading.Thread(target=receive)
    t2 = threading.Thread(target=send)

    t1.start()
    t2.start()
