import pyttsx3 as tts

class Speaker:
    def __init__(self):
        self.engine = tts.init()
        voices = self.engine.getProperty('voices')
        self.engine.setProperty('voice', voices[1].id)
        self.engine.setProperty('rate', 140)

    def text_to_voice(self, text):
        self.engine.say(text)
        self.engine.runAndWait()
