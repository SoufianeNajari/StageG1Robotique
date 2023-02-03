from megapi import *
import numpy as np
from odometryV2 import *

perim = np.pi*6.3

def onFinish(a):
    odometryV2.straight()


def onReadVitD(v):
    global vD
    vD = (v/60)*perim
    print(v)

def onReadVitG(v):
    global vG
    vG = (v/60)*perim
    print(v)

def onReadPosD(level):
	print("Encoder motor speed Value:%f" %level);

def onReadPosG(level):
	print("Encoder motor speed Value:%f" %level);

bot = MegaPi()
bot.start()
bot.encoderMotorRun(1,0);
bot.encoderMotorSetCurPosZero(1);
bot.encoderMotorRun(2,0);
bot.encoderMotorSetCurPosZero(2);
sleep(1);
bot.encoderMotorMoveTo(1,100,4000,onFinish);
bot.encoderMotorMoveTo(2,100,-4000,onFinish);
#1000->50