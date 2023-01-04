from model.model import Model
from model.data_processing.generator import DatasetGenerator
from config import Config
from plugins.integrator import Integrator
from speaker import Speaker
from listener import Listener


class VoiceAssistant:
    
    def __init__(self, train=False):
        self.cfg = Config()
        self.integrator = Integrator()
        self.listener = Listener()
        self.speaker = Speaker()
        
        if train:
            self.build_dataset()
            self.build_model()
            
        self.load_model()


    def load_model(self):
        """ Load in a pre-trained NLP model """

        intent_label_path = f'{self.cfg.dataset_path}/intent_labels.json'
        entity_label_path = f'{self.cfg.dataset_path}/entity_labels.json'

        self.nlp = Model(
                intent_label_path, 
                entity_label_path, 
                self.cfg.prompt_padding, 
                self.cfg.model_name
            )
        
        self.nlp.build_model()
        self.nlp.load_model(self.cfg.model_path)


    def build_model(self):
        """ Build & train NLP model """

        intent_label_path = f'{self.cfg.dataset_path}/intent_labels.json'
        entity_label_path = f'{self.cfg.dataset_path}/entity_labels.json'
        dataset_path = f'{self.cfg.dataset_path}/train.pkl'

        self.nlp = Model(
                intent_label_path, 
                entity_label_path, 
                self.cfg.prompt_padding, 
                self.cfg.model_name
            )
        
        self.nlp.build_model()
        self.nlp.train(dataset_path, epochs=self.cfg.epochs, batch_size=self.cfg.batch_size)
        self.nlp.save_model(self.cfg.model_path)


    def build_dataset(self):
        """ Build a dataset based on the provided intents & entities """
        print('Generating a dataset...')
        
        generator = DatasetGenerator(
            dataset_path=self.cfg.dataset_path, 
            samples_per_intent=self.cfg.samples_per_intent, 
            duplicates=self.cfg.duplicates
            )
        
        generator.generate_dataset()


    def ask(self, prompt: str) -> dict:
        """
            Pass a single prompt to Aurras

            Outputs:
             - response: Response json object
        """
        
        classification = self.nlp.classify(prompt, self.cfg.prompt_padding)  
        print(classification['intent'], classification['entities'])      
        response = self.integrator.generate_response(classification['intent'], classification['entities'])

        return response


    def interact(self):
        while True:
            print('=> ', end='')
            prompt = self.listener.voice_to_text()
            response = self.ask(prompt)
            self.speaker.text_to_voice(response)
