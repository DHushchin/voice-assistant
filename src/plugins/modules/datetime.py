import datetime

def execute(self, intent, entities) -> str:
    now = datetime.datetime.now()
    
    if intent == 'get_date':
        return now.strftime('%d/%m/%Y')
    elif intent == 'get_time':
        return now.strftime('%H:%M')
        