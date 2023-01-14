from plugins.modules.base import BaseModule

import datetime
from timefhuman import timefhuman
import geocoder
import requests

import os
import sys

current = os.path.dirname(os.path.realpath(__file__))
parent = os.path.dirname(os.path.dirname(current))
sys.path.append(parent)

from config import Config


class WeatherModule(BaseModule):
    
    def __init__(self):
        self.cfg = Config()
        self.exclude = "minutely, hourly"
        self.units = "metric"
        self.date_format = "%B %d"
        
        
    def execute(self, entities) -> str:        
        time = self.__get_time(entities)
        time_delta = (time - datetime.datetime.now()).days

        if time_delta > 8:
            return "Forecasts can't be predicted  more than 7 days ahead"
        
        lat, lng, city = self.__get_coords(entities)

        temp, weather = self.__get_weather(lat, lng, time_delta)

        if time_delta == 0:
            response = f'Today it is {temp} degrees with {weather} in {city}'
        else:
            response = f'On {time.strftime(self.date_format)} it will be {temp} degrees with {weather} in {city}'

        return response
    
    
    def __get_time(self, entities):
        time = datetime.datetime.now()

        for e in entities:
            if e[0] == 'datetime':
                predicted_time = timefhuman(e[1], now=time)
                if predicted_time != []:
                    time = predicted_time
                break
      
        return time
     
     
    def __get_coords(self, entities):
        for e in entities:
            if e[0] == 'city':
                city = e[1]
                break
            
        coords = geocoder.bing(city, key=self.cfg.geo_api_key).json
        
        return coords['lat'], coords['lng'], city
    
    
    def __get_weather(self, lat, lng, time_delta):
        request = f'https://api.openweathermap.org/data/2.5/onecall?lat={lat}&lon={lng}&exclude={self.exclude}&units={self.units}&appid={self.cfg.weather_api_key}'
        res = requests.get(request)
        x = res.json()
        
        temperature = round(x['daily'][time_delta]['temp']['day'])
        weather = x['daily'][time_delta]['weather'][0]['description']
        
        return temperature, weather
