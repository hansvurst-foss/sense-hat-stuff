'''
Pong Game on Python and Raspberry Pi SenseHAT

Created by: hansvurst
Current Version: 0.1.1

Licensed under CC0
'''

from time import sleep

from sense_hat import ACTION_PRESSED, ACTION_HELD, ACTION_RELEASED
try:
    from sense_emu import ACTION_PRESSED, ACTION_HELD, ACTION_RELEASED
except ImportError:
    pass

from ..config import R,G,B,wh,bl,sense

def pong_init():
    sense.clear()
    gameStatus  = "Running"
    global ledMatrix
    ledMatrix = 64 * [bl]
    racket = [16,24,32]

    ballPosition = 28
    ballDirection = ["right","flat"]

    for i in racket:
        ledMatrix[ballPosition] = B
        ledMatrix[i] = G
    sense.set_pixels(ledMatrix)

    #signal.signal(signal.SIGALRM, handler)
    #signal.alarm(3)
    return gameStatus, racket, ballPosition, ballDirection

def refresh_pong(racket, ballPosition):
    global ledMatrix
    ledMatrix = 64 * [bl]
    for i in racket:
        ledMatrix[ballPosition] = B
        ledMatrix[i] = G
    sense.set_pixels(ledMatrix)
    return

def move_racket(racket, direction):
    if direction == "down":
        if racket[0] != 0:
            for i in range(len(racket)):
                racket[i] -= 8
        else:
            pass
    elif direction == "up":
        if racket[-1] != 56:
            for i in range(len(racket)):
                racket[i] += 8
            else:
                pass
    return racket

def move_ball(ballPosition, ballDirection, racket):
    if ballPosition in [x+1 for x in racket]:
        ballDirection[0] = "right"
        if ballPosition == racket[0]+1:
            ballDirection[1] = "up"
        elif ballPosition == racket[1]+1:
            ballDirection[1] = "flat"
        elif ballPosition == racket[2]+1:
            ballDirection[1] = "down"
    elif ballPosition in [7,15,23,31,39,47,55,63]:
        ballDirection[0] = "left"
        if ballPosition == 7:
            ballDirection[1] = "down"
        elif ballPosition == 63:
            ballDirection[1] = "up"
    elif ballPosition in [1,2,3,4,5,6]:
        ballDirection[1] = "down"
    elif ballPosition in [57,58,59,60,61,62]:
        ballDirection[1] = "up"
    elif ballPosition in [0,8,16,24,32,40,48,56]:
        global gameStatus
        gameStatus = "Game Over"
        return None, None

    if ballDirection[0] == "right":
        if ballDirection[1] == "up":
            ballPosition -= 7
        elif ballDirection[1] == "flat":
            ballPosition += 1
        elif ballDirection[1] == "down":
            ballPosition += 9
    elif ballDirection[0] == "left":
        if ballDirection[1] == "up":
            ballPosition -= 9
        elif ballDirection[1] == "flat":
            ballPosition -= 1
        elif ballDirection[1] == "down":
            ballPosition += 7
    return ballPosition, ballDirection

def pong_game():
    global gameStatus
    gameStatus, racket, ballPosition, ballDirection = pong_init()
    while gameStatus == "Running":
        refresh_pong(racket, ballPosition)
        events = sense.stick.get_events()
        for event in events:
            if event.action != "released":
                move_racket(racket, event.direction)
        ballPosition, ballDirection = move_ball(ballPosition, ballDirection, racket)
        print(ballPosition)
        sleep(0.15)


    sense.show_message("Game over!")
    return


if __name__ == "__main__":
    from sense_hat import SenseHat
    try:
        from sense_emu import SenseHat
    except ImportError:
        pass

    R = (100,0,0)
    G = (0,100,0)
    B = (0,0,100)
    wh = (100,100,100)
    bl = (0,0,0)
    sense = SenseHat()
    sense.set_rotation(180)
    pong_game()
