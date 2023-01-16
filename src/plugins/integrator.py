from .modules.time import TimeModule
from .modules.date import DateModule
from .modules.greetings import GreetingsModule
from .modules.leaving import LeavingModule
from .modules.joke import JokeModule
from .modules.weather import WeatherModule
from .modules.search import SearchModule
from .modules.currency import CurrencyModule


class Integrator:
    """
        Integrator class

        This class is responsible for loading all plugins and executing them
    """
    def __init__(self):
        self.plugin = None
        

    def generate_response(self, intent: str, entities: dict) -> str:
        """
            Execute all plugins

            Inputs:
            - intent:   stringified intent provided by the NLP module
            - entities: dictionary of stringified entities provided by the NLP module

            Outputs:
            - response: Dictionary containing the plugin's responce in natural language
        """
            
        if intent == 'get_time':           
            self.plugin = TimeModule()
        elif intent == 'get_date':
            self.plugin = DateModule()
        elif intent == 'greetings':
            self.plugin = GreetingsModule()
        elif intent == 'leaving':
            self.plugin = LeavingModule()
        elif intent == 'get_joke':
            self.plugin = JokeModule()
        elif intent == 'get_weather':
            self.plugin = WeatherModule()
        elif intent == 'search':
            self.plugin = SearchModule()
        elif intent == 'get_rate':
            self.plugin = CurrencyModule()

        try:
            response = self.plugin.execute(entities)
        except Exception as e:
            print(e)
            print(f'Error executing plugin: {intent}')
            response = ''

        return response
