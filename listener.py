import PySimpleGUI as sg
import pyaudio
import numpy as np


class Listener:
    def __init__(self):
        self.__create_window()
        self.stream = None
        self.audio_data = np.array([])
        self.audio_port = pyaudio.PyAudio()
        
    def __create_window(self):
        AppFont = ('Helvetica', 14, 'bold italic')
        sg.theme('DarkBlue13')
        layout = [[sg.Graph(canvas_size=(400, 200),
                        graph_bottom_left=(-2, -2),
                        graph_top_right=(100, 100),
                        background_color='white',
                        key='graph')],
                    
                        [sg.ProgressBar(4000, orientation='h',
                        size=(20, 20), key='prog_bar', bar_color=('orange', 'white'))],
                    
                        [sg.Button('Listen', font=AppFont),
                        sg.Button('Stop', font=AppFont, disabled=True),
                        sg.Button('Exit', font=AppFont, pad=((202, 0), 0),
                                  button_color=('white', 'firebrick4'), )]]
        
        self.window = sg.Window('Voice Assistant', layout, finalize=True)
        
        
    def stop(self):
        if self.stream:
            self.stream.stop_stream()
            self.stream.close()
            self.window['prog_bar'].update(0)
            self.window.find_element('Stop').Update(disabled=True)
            self.window.find_element('Listen').Update(disabled=False)


    def callback(self, in_data, frame_count, time_info, status):
        self.audio_data = np.frombuffer(in_data, dtype=np.int16)
        return (in_data, pyaudio.paContinue)


    def listen(self, chunk=1024, rate=44100):
        self.window.find_element('Stop').update(disabled=False)
        self.window.find_element('Listen').update(disabled=True)
        self.stream = self.audio_port.open(format=pyaudio.paInt16,
                                           channels=1,
                                           rate=rate,
                                           input=True,
                                           frames_per_buffer=chunk,
                                           stream_callback=self.callback)
        self.stream.start_stream()
        
        
    def visualize(self, chunk=1024):
        self.window['prog_bar'].update(np.amax(self.audio_data))
        self.window['graph'].erase()
        for x in range(chunk):
            self.window['graph'].DrawCircle((x, (self.audio_data[x] / 140) + 50), 0.6,
                            line_color='orange', fill_color='orange')
        
      
    def run(self):
        while True:
            event, values = self.window.read(timeout=10)
            if event == sg.WIN_CLOSED or event == 'Exit':
                self.stop()
                self.audio_port.terminate()
                break
            
            if event == 'Listen':
                self.listen()
                
            if event == 'Stop':
                self.stop()

            # updates the waveform plot
            elif self.audio_data.size != 0:
                self.visualize()
                
        self.window.close()
        

if __name__ == '__main__':  
    listener = Listener()
    listener.run()
