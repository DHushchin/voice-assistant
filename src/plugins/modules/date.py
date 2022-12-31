import datetime

class DateModule:
    def execute(self, entities) -> str:
        return datetime.datetime.now().strftime('%d/%m/%Y')
                 