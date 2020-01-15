'''
Raspberry Pi SenseHAT Desktop gimmick

Created by: hansvurst
Current version: 0.1.1

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
from os import uname
if uname().nodename == "raspberrypi":
    from sense_emu import SenseHat, ACTION_PRESSED, ACTION_HELD, ACTION_RELEASED


from clock.clock import *
from games.snake import *

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
    statusServer, colourClock = initClock()
    return statusServer, colourClock


if __name__ == "__main__":
    statusServer, colourClock = init()
    while True:
        clock()
        time.sleep(10)

        for event in sense.stick.get_events():
            if event.action == "pressed":
                if event.direction == "up":
                    sense.show_message("CPU="+str(tempCPU)+"'C", scroll_speed=0.075,text_colour=tcCPU)
                    sense.show_message(envData, scroll_speed=0.075,text_colour=(100,100,100)); time.sleep(1)
                if event.direction == "down":
                    statusServer, colourClock = checkServer()
                    sense.show_message("Server is "+statusServer, scroll_speed=0.07,text_colour=colourClock)

                if event.direction == "left"
                    snakeGame()
