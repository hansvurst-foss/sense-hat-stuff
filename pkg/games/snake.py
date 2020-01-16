'''
Snake Game on Python and Raspberry Pi SenseHAT

Created by: hansvurst
Current Version: 0.1.2

Licensed under CC0
'''

from random import randint
from time import sleep
from sense_hat import ACTION_PRESSED, ACTION_HELD, ACTION_RELEASED
try:
    from sense_emu import ACTION_PRESSED, ACTION_HELD, ACTION_RELEASED
except ImportError:
    pass

from ..config import R,G,B,wh,bl,sense


def snakeInit():
    global gameStatus
    gameStatus = "Running"
    global snakePosition, pointPosition, ledMatrix
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

def refreshSnake():
    global ledMatrix
    ledMatrix = 64 * [R]
    for i in snakePosition:
        ledMatrix[pointPosition] = B
        ledMatrix[i] = G
    sense.set_pixels(ledMatrix)
    return

def move_right():
    global snakePosition, pointPosition, gameStatus
    if snakePosition[-1] in [7,15,23,31,39,47,55,63]:
        sense.show_message("Right!")
        gameStatus = "GameOver"
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
    global snakePosition, pointPosition, gameStatus
    if snakePosition[-1] in [0,8,16,24,32,40,48,56]:
        sense.show_message("Left!")
        gameStatus = "GameOver"
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
    global snakePosition, pointPosition, gameStatus
    if snakePosition[-1] in [0,1,2,3,4,5,6,7]:
        sense.show_message("Up!")
        gameStatus = "GameOver"
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
    global snakePosition, pointPosition, gameStatus
    if snakePosition[-1] in [56,57,58,59,60,61,62,63]:
        sense.show_message("Down!")
        gameStatus = "GameOver"
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

def snakeGame():
    global gameStatus, direction, snakePosition
    snakeInit()
    while gameStatus != "GameOver":
        refreshSnake()
        sleep(1)
        events = sense.stick.get_events()
        if events:
            if events[-1].direction == "down": direction = "up"
            elif events[-1].direction == "up": direction = "down"
            elif events[-1].direction == "left": direction = "right"
            elif events[-1].direction == "right": direction = "left"
        if len(snakePosition) == len(set(snakePosition)):
            if direction == "up": move_up()
            elif direction == "down": move_down()
            elif direction == "right": move_right()
            elif direction == "left": move_left()
        else:
            sense.show_message("Yam!")
            gameStatus = "GameOver"
            continue
    return
