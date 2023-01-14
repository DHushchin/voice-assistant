from base import BaseModule
import datetime


class DateModule(BaseModule):
    def execute(self, entities) -> str:
        return datetime.datetime.now().strftime('%d/%m/%Y')
                 