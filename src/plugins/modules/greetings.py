import random

class Greetings:
    def __init__(self):
      self.vocabulary = ['hello', 'greetings', 'happy to hear you']

    def execute(self, entities) -> str:
        return f"{random.choice(self.vocabulary)}. I am your personal voice assistant. How can I help you?"
                 