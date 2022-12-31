import datetime

class TimeModule:   
    def execute(self, entities) -> str:
        return datetime.datetime.now().strftime('%H:%M')
        