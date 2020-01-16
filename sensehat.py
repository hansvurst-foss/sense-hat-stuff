'''
Raspberry Pi SenseHAT Desktop gimmick

Created by: hansvurst
Current version: 0.1.2

Licensed under CC0
'''

from sense_hat import SenseHat, ACTION_PRESSED, ACTION_HELD, ACTION_RELEASED
from random import randint
#from time import sleep
import time; import datetime
from signal import pause
from sys import exit
import urllib.request # for checking server-status

# adding compatibility to SenseHAT Emulator
try:
    from sense_emu import SenseHat, ACTION_PRESSED, ACTION_HELD, ACTION_RELEASED
except ImportError:
    print("SenseHAT Emulator not available. Please install python module sense_emu for compatibility.")
    pass

# adding modules from local file system
from clock.clock import *
from games.snake import *
from service.weather import *
from service.system import *

def init():
    global R, G, B, bl, wh
    R = (100,0,0)
    G = (0,100,0)
    B = (0,0,100)

    bl = (0,0,0)
    wh = (100,100,100)

    global sense
    sense = SenseHat()
    sense.clear()
    sense.set_rotation(180) # alt: flip_h() or flip_v()
    # change fixed rotation to dynamic solution in the future!
    sense.low_light = True
    initClock()
    serverURL, statusServer = initSystem()
    initWeather()
    return serverURL, statusServer


if __name__ == "__main__":
    serverURL, statusServer = init()
    while True:
        clock()
        time.sleep(10)

        for event in sense.stick.get_events():
            if event.action == "pressed":
                if event.direction == "up":
                    tempCPU = getTempCPU()
                    envData, envOut = getWeather()
                    sense.show_message("CPU="+str(tempCPU[0])+"'C", scroll_speed=0.075,text_colour=tempCPU[1])
                    sense.show_message(envOut, scroll_speed=0.075,text_colour=(100,100,100)); time.sleep(1)
                if event.direction == "down":
                    statusServer, colourClock = checkServer()
                    sense.show_message("Server is "+statusServer[0], scroll_speed=0.07,text_colour=statusServer[1])

                if event.direction == "left":
                    snakeGame()
