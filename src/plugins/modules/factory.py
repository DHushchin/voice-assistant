from plugins.modules.time import TimeModule
from plugins.modules.date import DateModule
from plugins.modules.greetings import Greetings
from plugins.modules.leaving import Leaving
from plugins.modules.joker import Joker
from plugins.modules.weather import Weather
from plugins.modules.search import GoogleSearch
from plugins.modules.currency import Currency


class PluginsFactory:
    def __init__(self, intent):
        self.plugin = None
        
        if intent == 'get_time':           
            self.plugin = TimeModule()
        elif intent == 'get_date':
            self.plugin = DateModule()
        elif intent == 'greetings':
            self.plugin = Greetings()
        elif intent == 'leaving':
            self.plugin = Leaving()
        elif intent == 'get_joke':
            self.plugin = Joker()
        elif intent == 'get_weather':
            self.plugin = Weather()
        elif intent == 'search':
            self.plugin = GoogleSearch()
        elif intent == 'get_rate':
            self.plugin = Currency()
            
            
    def execute(self, entities):
        return self.plugin.execute(entities)
