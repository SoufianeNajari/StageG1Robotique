from megapi import * 
import numpy as np
from random import *
import time

#Utilisation du gyro pour la correction de la trajectoire, fonction straight fonctionnelle !


phi = 0
x = 0
y = 0
z=0
zinit = 0
vD = 0
vG = 0
#Pas changer au dessus
deltaT = 0.07
L = 19
perim = np.pi*5.75
#Paramètres importants
vDc = 50
vGc = 50


def onReadVitD(v):
    global vD
    vD = (v/60)*perim
    
def onReadVitG(v):
    global vG
    vG = (v/60)*perim

def onReadzinit(level):
	global zinit
	zinit = level

def onReadz(level):
	global z
	z = level


def straight(Distance): #Selon x pour l'instant
    global x 
    global y
    global phi
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
            
            
            bot.gyroRead(0,3,onReadz);
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

            phiaux = (z-zinit)*0.01745 
            """ phiInst = (deltaT/L)*(vD + vG)
            phi = phiaux + phiInst """
            bot.gyroRead(0,3,onReadz);
            phi = (z-zinit)*0.01745 
            x = x + (deltaT/2)*(vD - vG)*(1-(phiaux**2)/2)
            y = y + (deltaT/2)*(vD - vG)*phiaux
            
            DistanceParcourue = np.sqrt((x - xaux)**2 + (y - yaux)**2)

            
    print("x : "+str(x)+ "            y  : "+str(y)+ "         phi : "+str(phi)) 
    #Gyro
    bot.gyroRead(0,3,onReadz);  
    print("zinit : "+str(zinit) + "     z : "+str(z))

    bot.encoderMotorRun(1, 0) #c pour consigne
    bot.encoderMotorRun(2, 0)

def turnRight():
    global x 
    global y
    global phi
    #Gyro
    global zinit
    global z
   
    
    phiaux = phi
    angle = 1.57
    sleep(0.01)
    bot.gyroRead(0,3,onReadzinit);
    sleep(0.01)
    zinit2 = zinit*0.01745 #en rad
    z2=zinit2
    print(zinit)
    temps = time.time()
    while (zinit2-angle<z2<zinit2+0.01 and zinit2>=-angle) or (zinit2<=-angle and (z2>=zinit2+3*angle or z2<zinit2+0.01)):
        sleep(0.002)
        
        if (time.time() - temps) >= deltaT and (zinit2-angle<z2<zinit2+0.01 and zinit2>=-angle) or (zinit2<=-angle and (z2>=zinit2+3*angle or z2<zinit2+0.01)):
            temps = time.time()
            bot.encoderMotorRun(1, -vDc+20)
            bot.encoderMotorRun(2, -vGc+20)
            bot.encoderMotorSpeed(1,onReadVitD);
            bot.encoderMotorSpeed(2,onReadVitG);
            
            bot.gyroRead(0,3,onReadz);
            phiaux = (z-zinit)*0.01745 
            
            
            x = x + (deltaT/2)*(vD - vG)*(1-(phiaux**2)/2)
            y = y + (deltaT/2)*(vD - vG)*phiaux

            bot.gyroRead(0,3,onReadz);
            sleep(0.005)
            z2 = z*0.01745
            sleep(0.001)
            
                
    """ print("x : "+str(x)+ "            y  : "+str(y)+ "         phi : "+str(phiaux)) """

    bot.encoderMotorRun(1, 0) #c pour consigne
    bot.encoderMotorRun(2, 0)
    sleep(0.2)
    bot.gyroRead(0,3,onReadz);
    sleep(0.1)
    print(z)
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
            x = x + (deltaT/2)*(vD - vG)*(1-(phiaux**2)/2)
            y = y + (deltaT/2)*(vD - vG)*phiaux
                 
    print("x : "+str(x)+ "            y  : "+str(y)+ "         phi : "+str(phi))
    bot.encoderMotorRun(1, 0) #c pour consigne
    bot.encoderMotorRun(2, 0)
    sleep(0.1)

bot = MegaPi()
bot.start()

turnRight()
turnRight()
turnRight()
turnRight()
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