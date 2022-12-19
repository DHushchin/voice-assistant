import speech_recognition as sr

class Listener:
    def __init__(self):
        self.rec = sr.Recognizer()

    def audio_to_text(self):
        # audio_data = sr.AudioData(audio, 44100, 2).get_wav_data()
        # audio_data = sr.AudioData(audio, 44100, 2).get_wav_data()
        
        with sr.Microphone() as source:     
            print('You can start talking now')  
            self.rec.adjust_for_ambient_noise(source)     
            audio_data = self.rec.listen(source)
            try:
                print('Text:' + self.rec.recognize_google(audio_data))
            except:
                print("Can't hear you")
        