import pyjokes

def execute():
    return pyjokes.get_joke(language='en', category='all')

print(execute())