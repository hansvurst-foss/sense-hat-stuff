'''
Simple weather station for the Raspberry Pi SenseHAT

Created by: hansvurst
Current version: 0.1.1

Licensed under CC0
'''

def getWeather():
    # reading sensor data
    pressure = str(round(sense.get_pressure(),2))
    pressure_temp = sense.get_temperature_from_pressure()
    temperature = str(round(sense.get_temperature()))
    humidity = str(round(sense.get_humidity()))
    envOut = ("tem="+temperature+"'C"+" "+"hum="+humidity+"%"+" "+"pre="+pressure+"hPa")
    return (pressure, pressure_temp, temperature, humidity), envOut
