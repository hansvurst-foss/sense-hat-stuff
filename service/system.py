'''
Simple script providing system information to Raspberry Pi SenseHAT

Created by: hansvurst
Current Version: 0.1.3

Licensed under CC0
'''
def initSystem():
    import urllib.request # for checking server-status

    serverURL = input("Please insert serverURL: \n-> ")
    statusServer = checkServer(serverURL)
    return serverURL, statusServer

def getTempCPU():
    tempFile = open("/sys/class/thermal/thermal_zone0/temp")
    tempCPU = round(int(tempFile.read())/1000)
    if tempCPU < 55:
        tcCPU = (0,100,0)
    elif tempCPU >= 55 and tempCPU < 65:
        tcCPU = (50,50,0)
    elif tempCPU >= 65:
        tcCPU = (100,0,0)
    return (tempCPU, tcCPU)

def checkServer(serverURL):
    try:
        #print(urllib.request.urlopen('''INSERT URL HERE!''').getcode())
        if urllib.request.urlopen(serverURL).getcode() == 200:
            statusServer = "up"
            colourClock = g
    except urllib.error.URLError:
            statusServer = "down"
            colourClock = r
    return (statusServer, colourClock)
