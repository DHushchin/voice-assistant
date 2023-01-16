from .base import BaseModule
import pyjokes


class JokeModule(BaseModule):
    def execute(self, entities) -> str:
        joke =  pyjokes.get_joke(language='en', category='all')
        print(joke)
        return joke
