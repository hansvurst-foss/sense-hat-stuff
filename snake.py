'''
Snake Game on Python and Raspberry Pi SenseHAT

Created by: hansvurst
Current Version: 0.1.1

CC0
'''

from sense_hat import SenseHat, ACTION_PRESSED, ACTION_HELD, ACTION_RELEASED
from random import randint
from time import sleep
from signal import pause
from sys import exit

def init():
	global R, G, B
	R = (100,0,0)
	G = (0,100,0)
	B = (0,0,100)
	
	global sense, snakePosition, pointPosition, ledMatrix
	sense = SenseHat()
	sense.clear()
	sense.set_rotation(180)
	sense.low_light = True
	ledMatrix = 64 * [R]
	#snakePosition = [10,11,12,13,21,29,30]
	snakePosition = [randint(0,32)]
	pointPosition = randint(33,63)
	for i in snakePosition:
		ledMatrix[pointPosition] = B
		ledMatrix[i] = G
	sense.set_pixels(ledMatrix)
	
	global direction
	direction = "right"
	return
	
def update_matrix():
	global ledMatrix
	ledMatrix = 64 * [R]
	for i in snakePosition:
		ledMatrix[pointPosition] = B
		ledMatrix[i] = G
	sense.set_pixels(ledMatrix)
	return
	
def move_right():
	global snakePosition, pointPosition
	if snakePosition[-1] in [7,15,23,31,39,47,55,63]:
		sense.show_message("Right!")
		exit(0)
	elif snakePosition[-1] == (pointPosition-1):
		snakePosition.append(pointPosition)
		pointPosition = randint(0,63)
	else:
		first = snakePosition[-1]
		first += 1
		for i in range(len(snakePosition)-1):
			snakePosition[i] = snakePosition[i+1]
		snakePosition[-1] = first 
	return

def move_left():
	global snakePosition, pointPosition
	if snakePosition[-1] in [0,8,16,24,32,40,48,56]:
		sense.show_message("Left!")
		exit(0)
	elif snakePosition[-1] == (pointPosition+1):
		snakePosition.append(pointPosition)
		pointPosition = randint(0,63)
	else:
		first = snakePosition[-1]
		first -= 1
		for i in range(len(snakePosition)-1):
			snakePosition[i] = snakePosition[i+1]
		snakePosition[-1] = first 
	return
	
def move_up():
	global snakePosition, pointPosition
	if snakePosition[-1] in [0,1,2,3,4,5,6,7]:
		sense.show_message("Up!")
		exit(0)
	elif snakePosition[-1] == (pointPosition+8):
		snakePosition.append(pointPosition)
		pointPosition = randint(0,63)
	else:
		first = snakePosition[-1]
		first -= 8
		for i in range(len(snakePosition)-1):
			snakePosition[i] = snakePosition[i+1]
		snakePosition[-1] = first 
	return

def move_down():
	global snakePosition, pointPosition
	if snakePosition[-1] in [56,57,58,59,60,61,62,63]:
		sense.show_message("Down!")
		exit(0)
	elif snakePosition[-1] == (pointPosition-8):
		snakePosition.append(pointPosition)
		pointPosition = randint(0,63)
	else:
		first = snakePosition[-1]
		first += 8
		for i in range(len(snakePosition)-1):
			snakePosition[i] = snakePosition[i+1]
		snakePosition[-1] = first 
	return

def pushed_up(event):
	global direction
	if event.action != ACTION_RELEASED:
		direction = "up"
		print(direction)
	return

def pushed_down(event):
	global direction
	if event.action != ACTION_RELEASED:
		direction = "down"
	return

def pushed_left(event):
	global direction
	if event.action != ACTION_RELEASED:
		direction = "left"
	return

def pushed_right(event):
	global direction
	if event.action != ACTION_RELEASED:
		direction = "right"
	return

if __name__ == "__main__":
	init()
	while True:
		sleep(1)
		
		if direction == "up": move_up()
		elif direction == "down": move_down()
		elif direction == "right": move_right()
		elif direction == "left": move_left()
		
		if len(snakePosition) != len(set(snakePosition)):
			sense.show_message("Yam")
			exit(0)
		
		sense.stick.direction_up = pushed_down
		sense.stick.direction_down = pushed_up
		sense.stick.direction_left = pushed_right
		sense.stick.direction_right = pushed_left
		sense.stick.direction_any = update_matrix

		update_matrix()
		#pause()
