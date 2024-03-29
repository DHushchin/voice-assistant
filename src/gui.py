import PySimpleGUI as sg
import pyaudio
import numpy as np
import math
from assistant import VoiceAssistant
from multiprocessing.pool import ThreadPool as Pool


class ListenerGUI:
    
    def __init__(self):
        self.__create_window()
        self.stream = None
        self.audio_data = np.array([])
        self.audio_port = pyaudio.PyAudio()
        self.is_listening = False
        self.assistant = VoiceAssistant()
        self.process = None
        
        
    def __create_window(self):
        app_font = ('Helvetica', 14, 'bold italic')
        sg.theme('DarkBlue13')
        layout = [
                    [sg.Image(filename='images/voice.gif', 
                              size=(568, 300), key='_GIF_')],
                
                    [sg.ProgressBar(15000, orientation='h',
                                    size=(20, 20), key='prog_bar', 
                                    bar_color=('green', 'white'))],
                
                    [sg.Button('Listen', font=app_font),
                     sg.Button('Stop', font=app_font, disabled=True),
                     sg.Button('Exit', font=app_font, pad=((202, 0), 0),
                     button_color=('white', 'firebrick4'))]
                 ]
        
        self.window = sg.Window('Voice Assistant', layout, finalize=True)
        
        
    def __stop(self):        
        if self.stream:
            self.stream.stop_stream()
            self.stream.close()
            self.window['prog_bar'].update(0)
            self.window.find_element('Stop').Update(disabled=True)
            self.window.find_element('Listen').Update(disabled=False)
        self.is_listening = False
        self.assistant.interacting = False
        self.process.terminate()
        self.process.join()


    def __callback(self, in_data, frame_count, time_info, status):
        self.audio_data = np.frombuffer(in_data, dtype=np.int16)
        return (in_data, pyaudio.paContinue)


    def __listen(self, chunk=4056, rate=44100):
        self.window.find_element('Stop').update(disabled=False)
        self.window.find_element('Listen').update(disabled=True)
        self.stream = self.audio_port.open(format=pyaudio.paInt16,
                                           channels=1,
                                           rate=rate,
                                           input=True,
                                           frames_per_buffer=chunk,
                                           stream_callback=self.__callback)
        self.stream.start_stream()
        
    
    def __visualize(self):
        if self.audio_data.size != 0 and self.is_listening:
            loudness = np.amax(self.audio_data)
            
            if loudness > 1500:
                self.window['prog_bar'].update(math.ceil(loudness / 150) * 150)
                self.window['_GIF_'].UpdateAnimation('images/voice.gif', time_between_frames=30)
            else:
                self.window['prog_bar'].update(0)
                
            self.window.refresh()
            
            
    def __listen_process(self):
        self.process.apply_async(self.assistant.interact) 

                               
    def run(self):
        while True:
            event, values = self.window.read(timeout=0)             
            
            if event == sg.WIN_CLOSED or event == 'Exit':
                self.__stop()
                self.audio_port.terminate()
                break
            
            if event == 'Listen':
                self.process = Pool(1)
                self.is_listening = True
                self.assistant.interacting = True
                self.__listen()
                
            if self.is_listening:
                self.__listen_process()

            if event == 'Stop':
                self.__stop()
                
            self.__visualize()
                                  
        self.window.close()
