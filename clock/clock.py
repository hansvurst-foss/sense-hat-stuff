'''
Simple clock for the Raspberry Pi SenseHAT

Created by: hansvurst
Current version: 0.1.2

Licensed under CC0
'''


def initClock():
    from clockwork_3 import *
    return

def getClockLayout(currentHour, currentMinute, colourClock):
    clockLayoutHours = [None] * 64; clockLayoutMinutes = [None] * 64
    clockLayout = [None] * 64

    if currentMinute == 0: clockLayoutMinutes = newhour;
    elif currentMinute == 15: clockLayoutMinutes = quarterpast;
    elif currentMinute == 30: clockLayoutMinutes = halfpast;
    elif currentMinute == 45: clockLayoutMinutes = quarterto;
    elif currentMinute == 60:
        clockLayoutMinutes = newhour
        currentHour += 1

    if currentHour == 1 or currentHour ==  13: clockLayoutHours = oneoclock;
    elif currentHour == 2 or currentHour == 14: clockLayoutHours = twooclock;
    elif currentHour == 3 or currentHour == 15: clockLayoutHours = threeoclock;
    elif currentHour == 4 or currentHour == 16: clockLayoutHours = fouroclock;
    elif currentHour == 5 or currentHour == 17: clockLayoutHours = fiveoclock;
    elif currentHour == 6 or currentHour == 18: clockLayoutHours = sixoclock;
    elif currentHour == 7 or currentHour == 19: clockLayoutHours = sevenoclock;
    elif currentHour == 8 or currentHour == 20: clockLayoutHours = eightoclock;
    elif currentHour == 9 or currentHour == 21: clockLayoutHours = nineoclock;
    elif currentHour == 10 or currentHour == 22: clockLayoutHours = tenoclock;
    elif currentHour == 11 or currentHour == 23: clockLayoutHours = elevenoclock;
    elif currentHour == 0 or currentHour == 12: clockLayoutHours = twelveoclock;
    #elif currentHour == 0: clockLayoutHours = [0] * 64

    for i in range(64):
        if (clockLayoutHours[i] or clockLayoutMinutes[i]) == 1: clockLayout[i] = colourClock;
        else: clockLayout[i] = bl
    return clockLayout

def getTime():
    currentHour = int(str(datetime.datetime.now().time())[:2])
    currentMinute = int(str(datetime.datetime.now().time())[3:5])
    return currentHour, currentMinute

def simpleTime(currentMinute):
    if currentMinute < 8: currentMinute = 0
    elif currentMinute >= 8 and currentMinute < 22: currentMinute = 15
    elif currentMinute >= 22 and currentMinute < 37: currentMinute = 30
    elif currentMinute >= 37 and currentMinute < 52: currentMinute = 45
    elif currentMinute >= 52: currentMinute = 60
    return currentMinute

def clock():
    currentHour, currentMinute = getTime()
    if currentMinute in [0,15,30,45]: statusServer = checkServer(serverURL)
    simpleMinute = simpleTime(currentMinute)
    clockLayout = getClockLayout(currentHour, simpleMinute, statusServer[1])
    sense.set_pixels(clockLayout)
