'''
Simple weather station for the Raspberry Pi SenseHAT

Created by: hansvurst
Current version: 0.1.3

Licensed under CC0
'''

from ..config import sense
from pyowm import OWM # OpenWeatherMap API

# OWM API can either be accessed via pyowm wrapper or directly in JSON format from api.openweathermap.org
#from requests import get
#import json

from pprint import pprint

def init_weather():
    location = input("Which town you want the data from?\n--> ")
    country = input("In which country is your preferred weather station?\n--> ")
    return (location, country)

def get_env_data():
    ''' reading sensor data of SenseHAT '''

    pressure = str(round(sense.get_pressure(),2))
    pressure_temp = sense.get_temperature_from_pressure()
    temperature = str(round(sense.get_temperature()))
    humidity = str(round(sense.get_humidity()))
    envOut = ("tem="+temperature+"'C"+" "+"hum="+humidity+"%"+" "+"pre="+pressure+"hPa")
    return (pressure, pressure_temp, temperature, humidity), envOut

def get_weather(location):
    ''' accessing the OpenWeatherMap API for local weather data '''

    apiKey = "a65147edaa8f7a3a607aee92181aa2a8"
    owm = OWM(apiKey)
    #url = "https://api.openweathermap.org/data/2.5/weather?q="+location+"&appid="+apiKey
    if owm.is_API_online() == True:
        #stationData = get(url).json()
        #pprint(stationData["main"])
        weatherAtPlace = owm.weather_at_place(location[0]+","+location[1])
        weather = weatherAtPlace.get_weather()
        weather = {
            "description":weather.get_status(),
            "description_detailed":weather.get_detailed_status(),
            "clouds":weather.get_clouds(),
            "temperature":weather.get_temperature(),
            "wind":weather.get_wind(),
            "rain":weather.get_rain(),
            "snow":weather.get_snow(),
            "humidity":weather.get_humidity(),
            "pressure":weather.get_pressure(),
            "sunrise":weather.get_sunrise_time(),
            "sunset":weather.get_sunset_time()
        }
    else: print("OWM API offline")
    return weather


def get_weather_icon(weather):
    ''' translates weather status into displayed icon
        not completed yet -> where to find complete possible options? '''

    displayIcons = {
        "Clear":"./pkg/service/weather-icons/sun.png",
        "Clouds":"./pkg/service/weather-icons/cloud.png",
        "Rain":"./pkg/service/weather-icons/rain.png",
        "Thunderstorm":"11d",
        "Snow":"13d",
        "Mist":"50d"
    }

    weatherIcon = displayIcons[weather["description"]]
    return weatherIcon
