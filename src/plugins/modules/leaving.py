from base import BaseModule
import random


class LeavingModule(BaseModule): 
    def __init__(self, *args, **kwargs):
      self.vocabulary = ['bye', 'goodbye', 'see you later', 'see you soon', 'take care']

    def execute(self, entities) -> str:
        return random.choice(self.vocabulary)
    