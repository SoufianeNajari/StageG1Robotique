from megapi import * 
import numpy as np

vD = 0
vG = 0
vDc = 50
vGc = 50 

def onReadVitD(v):
    global vD
    vD = v

def onReadVitG(v):
    global vG
    vG = v

deltaT = 0.1
phi = 0
x = 0
y = 0
L = 5

bot = MegaPi()
bot.start()

bot.encoderMotorRun(1, vDc) #c pour consigne
bot.encoderMotorRun(2, -vGc)
while 1:
    sleep(deltaT)
    bot.encoderMotorSpeed(1,onReadVitD);
    bot.encoderMotorSpeed(1,onReadVitG);
    phiaux = phi
    phi = phi + (deltaT/L)*(vD - vG)
    x = x + (deltaT/2)*(vD + vG)np.cos(phiaux)
    y = y + (deltaT/2)*(vD + vG)np.sin(phiaux)
    print("x : "+str(x))
    