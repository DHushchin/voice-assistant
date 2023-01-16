from .base import BaseModule
import datetime


class TimeModule(BaseModule):   
    def execute(self, entities) -> str:
        return datetime.datetime.now().strftime('%H:%M')
        