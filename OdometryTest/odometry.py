from megapi import * 
import numpy as np
from random import *

vD = 0
vG = 0
vDc = 35
vGc = 35

def onReadVitD(v):
    global vD
    vD = (v/60)*perim

def onReadVitG(v):
    global vG
    vG = (v/60)*perim

deltaT = 0.25
phi = 0
x = 0
y = 0
L = 17
perim = np.pi*6.3

bot = MegaPi()
bot.start()

bot.encoderMotorRun(1, vDc) #c pour consigne
bot.encoderMotorRun(2, -vGc)
while 1:
    sleep(deltaT)
    if x < 200:
        if phi<0:
            bot.encoderMotorRun(1, vDc+4)
            bot.encoderMotorRun(2, -vGc)
        else:
            bot.encoderMotorRun(1, vDc) #c pour consigne
            bot.encoderMotorRun(2, -vGc-4)
        
    else:
        bot.encoderMotorRun(1, 0) #c pour consigne
        bot.encoderMotorRun(2, 0)
        """ phiaux = phi
        phi = phi + (deltaT/L)*(vD + vG)
        x = x + (deltaT/2)*(vD - vG)*np.cos(phiaux)
        y = y + (deltaT/2)*(vD - vG)*np.sin(phiaux)
        print("x : "+str(x))
        print("phi : "+str(phi)) """
    bot.encoderMotorSpeed(1,onReadVitD);
    bot.encoderMotorSpeed(2,onReadVitG);
    
    phiaux = phi
    phi = phi + (deltaT/L)*(vD + vG)
    x = x + (deltaT/2)*(vD - vG)*np.cos(phiaux)
    y = y + (deltaT/2)*(vD - vG)*np.sin(phiaux)
    """ if randint(1,10) > 3:
        print("x : "+str(x))
        print("phi : "+str(phi)) """

    print("x : "+str(x))
    print("phi : "+str(phi))
    