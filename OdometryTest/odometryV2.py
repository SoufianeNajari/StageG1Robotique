from megapi import * 
import numpy as np
from random import *
import time

phi = 0
x = 0
y = 0
vD = 0
vG = 0
#Pas changer au dessus
deltaT = 0.07
L = 17
perim = np.pi*6.3
#Paramètres importants
vDc = 50
vGc = 50


def onReadVitD(v):
    global vD
    vD = (v/60)*perim
    
def onReadVitG(v):
    global vG
    vG = (v/60)*perim

def straight(Distance): #Selon x pour l'instant
    global x 
    global y
    global phi
    DistanceParcourue = 0
    xaux = x
    yaux = y
    
    DistanceParcourue = np.sqrt((x - xaux)**2 + (y - yaux)**2)
    
  
    


    bot.encoderMotorRun(1, vDc)
    bot.encoderMotorRun(2, -vGc)
    sleep(5*deltaT)
    phi = 0
    phiInst = 0
    phiprec = phi
    temps = time.time()
    while DistanceParcourue < Distance:
        sleep(0.005)
        
        if (time.time() - temps) >= deltaT:
            temps = time.time()
            angle = phiInst-phiprec
            if angle<0:
                temp = vDc - (100/np.pi)*(angle)
                print("---------------GAUCHE-----------------")
                bot.encoderMotorRun(1, int(temp))
                bot.encoderMotorRun(2, -vGc)
            else:
                temp = -vGc - (100/np.pi)*(angle)
                print("---------------DROITE-----------------")
                bot.encoderMotorRun(1, vDc) #c pour consigne
                bot.encoderMotorRun(2, int(temp))
            bot.encoderMotorSpeed(1,onReadVitD)
            bot.encoderMotorSpeed(2,onReadVitG);

            phiaux = phi
            phiInst = (deltaT/L)*(vD + vG)
            phi = phiaux + phiInst

            x = x + (deltaT/2)*(vD - vG)*np.cos(phiaux)
            y = y + (deltaT/2)*(vD - vG)*np.sin(phiaux)
            
            DistanceParcourue = np.sqrt((x - xaux)**2 + (y - yaux)**2)

            print("x : "+str(x)+ "            y  : "+str(y)+ "         phi : "+str(phiInst))
            

            
    
    bot.encoderMotorRun(1, 0) #c pour consigne
    bot.encoderMotorRun(2, 0)

def turnRight():
    global x 
    global y
    global phi

    phiturn = phi
    phiaux = phi
    temps = time.time()
    while phiaux - phiturn > -np.pi/2: 
        sleep(0.001)

        if (time.time() - temps) >= deltaT:
            temps = time.time()
            bot.encoderMotorRun(1, -vDc)
            bot.encoderMotorRun(2, -vGc)
            bot.encoderMotorSpeed(1,onReadVitD);
            bot.encoderMotorSpeed(2,onReadVitG);
            
            phiaux = phi
            phi = phi + (deltaT/L)*(vD + vG)
            x = x + (deltaT/2)*(vD - vG)*np.cos(phiaux)
            y = y + (deltaT/2)*(vD - vG)*np.sin(phiaux)
            

            print("x : "+str(x)+ "            y  : "+str(y))
            print("phi : "+str(phi))

    bot.encoderMotorRun(1, 0) #c pour consigne
    bot.encoderMotorRun(2, 0)
    sleep(0.1)

def turnLeft():
    global x 
    global y
    global phi

    phiturn = phi
    phiaux = phi
    temps = time.time()
    while phiaux - phiturn < np.pi/2: 
        sleep(0.001)
        
        if (time.time() - temps) >= deltaT:
            temps = time.time()
            bot.encoderMotorRun(1, vDc)
            bot.encoderMotorRun(2, vGc)
            bot.encoderMotorSpeed(1,onReadVitD);
            bot.encoderMotorSpeed(2,onReadVitG);
            
            phiaux = phi
            phi = phi + (deltaT/L)*(vD + vG)
            x = x + (deltaT/2)*(vD - vG)*np.cos(phiaux)
            y = y + (deltaT/2)*(vD - vG)*np.sin(phiaux)
            

            print("x : "+str(x)+ "            y  : "+str(y))
            print("phi : "+str(phi))

    bot.encoderMotorRun(1, 0) #c pour consigne
    bot.encoderMotorRun(2, 0)
    sleep(0.1)

bot = MegaPi()
bot.start()



straight(200)
turnRight()
straight(300)
turnLeft()
straight(300)

""" 
while 1:

    bot.encoderMotorSpeed(1,onReadVitD);
    bot.encoderMotorSpeed(2,onReadVitG);
    
    phiaux = phi
    phi = phi + (deltaT/L)*(vD + vG)
    x = x + (deltaT/2)*(vD - vG)*np.cos(phiaux)
    y = y + (deltaT/2)*(vD - vG)*np.sin(phiaux)
    

    print("x : "+str(x)+ "            y  : "+str(y))
    print("phi : "+str(phi))
"""    