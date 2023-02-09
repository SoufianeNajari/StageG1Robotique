import queue
import socket
import threading
from megapi import *

          



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

def getValVitesseG(v):
    global vitesseG
    vitesseG = v


def getValDistance(v):
    global distance
    distance = v


def getValRobot():
    global msgRobot
    bot.encoderMotorSpeed(1, getValVitesseD)
    bot.encoderMotorSpeed(2, getValVitesseG)
    msg = "{" + '"VD"' + " : " + str(vitesseD) + " , " + '"VG"' + " : " + str(vitesseG) + "}" 
    msg = msg.encode("utf-8")
    msgRobot = msg



def SendVitesseServer():
    # bot.encoderMotorSpeed(1, getValVitesseD)
    # bot.encoderMotorSpeed(2, getValVitesseG)
    # msg = "Vitesse " + str(vitesseD) + " " + str(vitesseG) + " " + name
    # msg = msg.encode("utf-8")
    global msgRobot
    client.sendto(msgRobot, addr)

def SendVitesseR3():
    # bot.encoderMotorSpeed(1, getValVitesseD)
    # bot.encoderMotorSpeed(2, getValVitesseG)
    # msg = "Vitesse " + str(vitesseD) + " " + str(vitesseG) + " " + name
    # msg = msg.encode("utf-8")
    global msgRobot
    client.sendto(msgRobot, p[2])

def receive():
    while True:
        try:
            message, ad = client.recvfrom(1024)
            info = message.decode("utf-8").split()
            print(ad)
            print(message.decode("utf-8"))
        except:
            pass
                            
def send():
    while True:
        sleep(0.1);
        getValRobot()
        SendVitesseServer()
        try:
            SendVitesseR3()
        except:
            pass


if __name__ == "__main__":
    ip4_server = "10.3.141.1"
    port = 4455
    addr = (ip4_server, port)
    name = "Robot2"
    client = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    ip1 = '10.3.141.101'
    ip2 = '10.3.141.102'
    ip3 = '10.3.141.103'
    client.bind(("", 4455))
    p = [(ip1, 5001), (ip2, 5002), (ip3, 5003)]
    bot = MegaPi()
    bot.start()
    distance = 0  
    vitesseD = 30
    vitesseG = vitesseD
    bot.encoderMotorRun(1,vitesseD);
    bot.encoderMotorRun(2, -vitesseG);
    sleep(1);


    t1 = threading.Thread(target=receive)
    t2 = threading.Thread(target=send)

    t1.start()
    t2.start()
