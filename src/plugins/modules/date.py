from .base import BaseModule
import datetime as dt
import human_readable 


class DateModule(BaseModule):
    def execute(self, entities) -> str:
        return dt.date.today()
                 