from decouple import config
import os

os.environ['TF_CPP_MIN_LOG_LEVEL'] = '2' 

class Config:
    def __init__(self):
        self.__init_paths()
        self.__init_hyperparams()
        self.__init_keys()
        
    def __init_paths(self):
        self.root_path = os.path.abspath(os.path.dirname(__file__)) + '/model/'
        self.dataset_path = self.root_path + '/dataset'        
        self.model_path = self.root_path + '/results/model.h5'
        
    def __init_hyperparams(self):
        self.samples_per_intent = 512
        self.prompt_padding = 128
        self.duplicates = True
        self.model_name = 'distilbert-base-uncased'
        self.epochs = 2
        self.batch_size = 4
        
    def __init_keys(self):
        self.weather_api_key = config('WEATHER_TOKEN')
        self.geo_api_key = config('GEO_TOKEN')
        