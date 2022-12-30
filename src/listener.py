import speech_recognition as sr

class Listener:
    def __init__(self):
        self.rec = sr.Recognizer()
        
    def __listen(self):
        print('Listening...')
        with sr.Microphone() as source:     
            self.rec.adjust_for_ambient_noise(source)  
            try:
                audio_data = self.rec.listen(source, 
                                             timeout=5, 
                                             phrase_time_limit=5)   
            except:
                print("Sorry, I can't hear you!")
                return  
              
        return audio_data
            
    
    def __recognize(self, audio_data):
        print('Recognizing...')
        try:
            text = self.rec.recognize_google(
                audio_data, 
                show_all=False, 
                language='en-US'
            )
            print('You said:' + text)
        except:
            print("Sorry, I couldn't make that out. Try again!")    


    def audio_to_text(self):
        audio_data = self.__listen()
        if audio_data is not None:
            self.__recognize(audio_data)
        