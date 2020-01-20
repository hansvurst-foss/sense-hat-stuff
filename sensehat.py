'''
Raspberry Pi SenseHAT Desktop gimmick

Created by: hansvurst
Current version: 0.1.4

Licensed under CC0
'''

from sense_hat import SenseHat
from time import sleep
from signal import pause
from sys import exit

# adding compatibility to SenseHAT Emulator
try:
    from sense_emu import SenseHat
except ImportError:
    print("SenseHAT Emulator not available. Please install python module sense_emu for compatibility.")
    pass

# adding modules from local file system
from pkg.config import R,G,B,wh,bl,sense
from pkg.clock.clock import *
from pkg.games.snake import *
from pkg.games.pong import *
from pkg.service.weather import *
from pkg.service.system import *

def init():
    sense.set_rotation(180) # alt: flip_h() or flip_v()
    # change fixed rotation to dynamic solution in the future!
    sense.low_light = True
    #initClock()
    serverURL, statusServer = init_system()
    #initWeather()
    return serverURL, statusServer


if __name__ == "__main__":
    serverURL, statusServer = init()
    while True:
        if int(str(datetime.datetime.now().time())[3:5]) in [0,15,30,45]:
            statusServer = check_server(serverURL)
        clock(statusServer)
        sleep(10)

        events = sense.stick.get_events()
        if events and events[-1].action == "released":
            if events[-1].direction == "up":
                tempCPU = get_temp_cpu()
                envData, envOut = get_env_data()
                weatherData = get_weather()
                sense.show_message("CPU="+str(tempCPU[0])+"'C", scroll_speed=0.075,text_colour=tempCPU[1])
                sense.show_message(envOut, scroll_speed=0.075,text_colour=(100,100,100))
                sense.load_image(get_weather_icon(weatherData))
                sleep(10)
            elif events[-1].direction == "down":
                statusServer = check_server(serverURL)
                sense.show_message(serverURL[8:]+" is "+statusServer[0], scroll_speed=0.07,text_colour=statusServer[1])
            elif events[-1].direction == "left":
                snake_game()
            elif events[-1].direction == "right":
                pong_game()
