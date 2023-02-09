import socket
import threading
from megapi import *


if __name__ == "__main__":
    bot = MegaPi()
    bot.start()
    bot.motorRun(M1,0);
    bot.motorRun(M2, 0);
    bot.encoderMotorRun(1,0);
    bot.encoderMotorRun(2,0);
    sleep(1);