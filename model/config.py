import os

class Config:
    def __init__(self):
        self.root_path = os.path.abspath(os.path.dirname(__file__))
        self.dataset_path = self.root_path + '/dataset'
        self.samples_per_intent = 512
        self.duplicates = False
        self.model_path = self.root_path + '/results/'
        self.model_name = 'model.h5'
