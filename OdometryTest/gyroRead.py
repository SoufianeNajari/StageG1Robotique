from megapi import *
import time
vitesse =  0
x = 0
y = 0 
z = 0


def onReadx(level):
	global x
	x = level

def onReady(level):
	global y
	y = level

def onReadz(level):
	global z
	z = level + (time.time() - T)/100

if __name__ == '__main__':
	T = time.time()
	bot = MegaPi()
	bot.start()
	bot.encoderMotorRun(1,vitesse);
	bot.encoderMotorRun(2,vitesse);
	while 1:
		sleep(1);
		bot.gyroRead(0,1,onReadx);
		bot.gyroRead(0,2,onReady);
		bot.gyroRead(0,3,onReadz);
		sleep(0.1)
		print("x : "+str(round(x,2)) + "       y : "+str(round(y,2))+"       z : "+str(round(z,2)))
		print("----------------------")