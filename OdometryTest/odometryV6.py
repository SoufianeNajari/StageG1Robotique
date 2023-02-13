from megapi import * 
import numpy as np
from random import *
import time

#Réglage de x et y ( odometry ) à l'aide de ztart


phi = 0
x = 0
y = 0
z=0
zinit = 0
zstart = 0
vD = 0
vG = 0
#Pas changer au dessus
deltaT = 0.07
L = 19
perim = np.pi*5.75
#Paramètres importants
vDc = 80
vGc = 80


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

def onReadzstart(level):
	global zstart
	zstart = level

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
    print("xstart : "+str(x) + "     ystart : "+str(y))
    print("--------------------------------------------")
    temps = time.time()
    while DistanceParcourue < Distance:
        sleep(0.002)
        
        if (time.time() - temps) >= deltaT:
            temps = time.time()
            
            
            bot.gyroRead(0,3,onReadz);
            angle = (z - zinit)/10 
            if z - zinit<0:
                temp = vDc - (33)*(angle)
                print("---------------GAUCHE-----------------")
                bot.encoderMotorRun(1, int(temp))
                bot.encoderMotorRun(2, -vGc)
            else:
                temp = -vGc - (33)*(angle)
                print("---------------DROITE-----------------")
                bot.encoderMotorRun(1, vDc) #c pour consigne
                bot.encoderMotorRun(2, int(temp))
            
            bot.encoderMotorSpeed(1,onReadVitD)
            bot.encoderMotorSpeed(2,onReadVitG);

            phiaux = (z-zstart)*0.01745
            
            bot.gyroRead(0,3,onReadz);
             
            x = x + (deltaT/2)*(vD - vG)*np.cos(phiaux)
            y = y + (deltaT/2)*(vD - vG)*np.sin(phiaux)
            print("x : "+str(x)+ "            y  : "+str(y)) 
            print("xaux : "+str(xaux)+ "            yaux  : "+str(yaux))
            DistanceParcourue = np.sqrt((x - xaux)**2 + (y - yaux)**2)
            print("Distance Parcourue : " + str(DistanceParcourue))
            print("---------------------------------------------")
            
    print("x : "+str(x)+ "            y  : "+str(y)) 
    #Gyro
    bot.gyroRead(0,3,onReadz);  
    print("zinit : "+str(zinit) + "     z : "+str(z))

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
    while angle > 2*np.pi:
        angle = angle - 2*np.pi
    
    sleep(0.02)
    bot.gyroRead(0,3,onReadzinit);
    sleep(0.1)
    zinit2 = zinit*0.01745 #en rad
    z2=zinit2

    temps = time.time()
    while (zinit2-angle<z2<zinit2+0.01 and zinit2>=angle - 3.1415) or (zinit2<=angle - 3.1415 and (z2>=zinit2+2*3.1415-angle or z2<zinit2+0.1)):
        sleep(0.002)
        
        if (time.time() - temps) >= deltaT:
            temps = time.time()
            
            bot.encoderMotorRun(1, -35)
            bot.encoderMotorRun(2, -35)
            
            bot.encoderMotorSpeed(1,onReadVitD);
            bot.encoderMotorSpeed(2,onReadVitG);
            
            bot.gyroRead(0,3,onReadz);
            phiaux = (z-zinit)*0.01745 
            
            
            x = x + (deltaT/2)*(vD - vG)*np.cos(phiaux)
            y = y + (deltaT/2)*(vD - vG)*np.sin(phiaux)

            bot.gyroRead(0,3,onReadz);
            sleep(0.005)
            z2 = z*0.01745
            sleep(0.001)
            
                
    """ print("x : "+str(x)+ "            y  : "+str(y)+ "         phi : "+str(phiaux)) """

    bot.encoderMotorRun(1, 0) #c pour consigne
    bot.encoderMotorRun(2, 0)
    sleep(0.2)
    

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

def go(X,Y):
    global x 
    global y
    global phi
    global zstart
    #Gyro
    global zinit
    global z

    bot.gyroRead(0,3,onReadz);
    sleep(0.1)
    if -10 < X-x < 10:
        if Y-y > 0:
            angle = -(np.pi/2 - z*0.01745)
        elif Y-y < 0:
            angle = -(-np.pi/2 - z*0.01745)
        else:
            angle = 0
    elif -10 < Y-y < 10:
        if X-x > 0:
            angle = z*0.01745
        elif X-x < 0:
            angle = -(np.pi - z*0.01745)
        else:
            angle = 0
    else:
        if X-x < 0:
            angle = -(np.arctan((Y-y)/(X-x)) - (np.pi-z*0.01745))
        else:
            angle = -(np.arctan((Y-y)/(X-x)) - z*0.01745)
    print("ANGLE : "+str(angle/0.01745))
    print("z : " + str(z))
    Distance = np.sqrt((Y-y)**2 + (X-x)**2)
    sleep(0.5)
    turnRight(angle)
    sleep(0.5)
    straight(Distance)
    print("-------------------------------------FIN GO--------------------------------------------------")




T = time.time()
bot = MegaPi()
bot.start()
sleep(0.1)
bot.gyroRead(0,3,onReadzstart);

#Couloir :
""" straight(220)
turnRight(np.pi/2)
straight(260)
turnRight(3*np.pi/2)
straight(260)
turnRight(3*np.pi/2)
straight(200)
sleep(5)
turnRight(np.pi)
straight(200)
turnRight(np.pi/2)
straight(260)
turnRight(np.pi/2)
straight(260)
turnRight(3*np.pi/2)
straight(220)
turnRight(np.pi)
 """
#Carré : 
""" straight(100)
turnRight(np.pi/2)
straight(100)
turnRight(np.pi/2)
straight(100)
turnRight(np.pi/2)
straight(100)
turnRight(np.pi)
sleep(5)
straight(100)
turnRight(3*np.pi/2)
straight(100)
turnRight(3*np.pi/2)
straight(100)
turnRight(3*np.pi/2)
straight(100)
turnRight(np.pi) """


#Couloir
""" go(220,-260)
go(480,-260)
go(480,-460)


go(480,-260)
go(220,-260)
go(0,0)
 """


go(200,-200)
go(100,-100)
go(0,0)
go(100,0)