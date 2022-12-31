import pyjokes

class Joker:
    def execute(self, entities) -> str:
        joke =  pyjokes.get_joke(language='en', category='all')
        print(joke)
        return joke
