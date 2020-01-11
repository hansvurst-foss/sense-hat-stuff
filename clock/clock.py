'''
Simple clock for the Raspberry Pi SenseHAT
created by: hansvurst

Version: 0.1.1

CC0
'''

from clockwork_3 import *
from pictures import creeper_pixels

import os
import time as t; import datetime
from sense_hat import SenseHat
from random import randint as ri

import urllib.request # for checking server-status

def init():
	global sense, pressure, pressure_temp, temperature, humidity, envData
	global R,G,B,r,g,b,bl,wh,WH
	# initialising the Sense HAT
	sense = SenseHat()
	sense.clear()
	sense.set_rotation(180) # alt: flip_h() or flip_v()
	sense.low_light = True

	# reading sensor data
	pressure = str(round(sense.get_pressure(),2))
	pressure_temp = sense.get_temperature_from_pressure()
	temperature = str(round(sense.get_temperature()))
	humidity = str(round(sense.get_humidity()))
	envData = ("tem="+temperature+"'C"+" "+"hum="+humidity+"%"+" "+"pre="+pressure+"hPa")

	R = (255,0,0)
	G = (0,255,0)
	B = (0,0,255)

	r = (50,0,0)
	g = (0,50,0)
	b = (0,0,50)

	bl = (0,0,0)
	wh = (100,100,100)
	WH = (255,255,255)
	
	#sense.clear((r,g,b))

	#sense.show_letter("Z")
	#sense.show_message("Hello World") #scroll_speed, text_colour, back_colour
	#sense.set_pixel(x,y,(r,g,b))
	#sense.clear((r,g,b)) for static colour
	return

def getTempCPU():
	tempFile = open("/sys/class/thermal/thermal_zone0/temp")
	tempCPU = round(int(tempFile.read())/1000)
	return tempCPU

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
	#print(currentHour, currentMinute)
	return currentHour, currentMinute
	
def simpleTime(currentMinute):
	if currentMinute < 8: currentMinute = 0
	elif currentMinute >= 8 and currentMinute < 22: currentMinute = 15
	elif currentMinute >= 22 and currentMinute < 37: currentMinute = 30
	elif currentMinute >= 37 and currentMinute < 52: currentMinute = 45
	elif currentMinute >= 52: currentMinute = 60
	return currentMinute
	
def checkServer():
	try:
		#print(urllib.request.urlopen('''INSERT URL HERE!''').getcode())
		if urllib.request.urlopen('''INSERT URL HERE!''').getcode() == 200:
			statusServer = "up"
			colourClock = g
	except urllib.error.URLError:
			statusServer = "down"
			colourClock = r
	return statusServer, colourClock

init()
statusServer, colourClock = checkServer()
while True:
	currentHour, currentMinute = getTime()
	if currentMinute in [0,15,30,45]: statusServer, colourClock = checkServer()
	currentMinute = simpleTime(currentMinute)
	clockLayout = getClockLayout(currentHour, currentMinute, colourClock)
	sense.set_pixels(clockLayout); t.sleep(10)
	tempCPU = getTempCPU()
	if tempCPU < 55:
		tcCPU = (0,100,0)
	elif tempCPU >= 55 and tempCPU < 65:
		tcCPU = (50,50,0)
	elif tempCPU >= 65:
		tcCPU = (100,0,0)
		
	for event in sense.stick.get_events():
		if event.action == "pressed":
			if event.direction == "up":
				sense.show_message("CPU="+str(tempCPU)+"'C", scroll_speed=0.075,text_colour=tcCPU)
				sense.show_message(envData, scroll_speed=0.075,text_colour=(100,100,100)); t.sleep(1)
			if event.direction == "down":
				statusServer, colourClock = checkServer()
				sense.show_message("Server is "+statusServer, scroll_speed=0.07,text_colour=colourClock)


	
	#sense.set_pixels(creeper_pixels)
	#t.sleep(5); sense.clear(), t.sleep(5)
	
	
	
