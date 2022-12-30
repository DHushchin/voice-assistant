import os
from dotenv import load_dotenv
from huggingface_hub.hf_api import HfFolder

class Config:
    def __init__(self):
        self.root_path = os.path.abspath(os.path.dirname(__file__))
        self.dataset_path = self.root_path + '/dataset'
        self.samples_per_intent = 512
        self.prompt_padding = 128
        self.duplicates = False
        self.model_path = self.root_path + '/results/model.h5'
        self.model_name = 'distilbert-base-uncased'
        self.epochs = 1
        self.batch_size = 4
