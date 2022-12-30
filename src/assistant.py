from model.model import Model
from model.data_processing.generator import DatasetGenerator
from model.config import Config


class VoiceAssistant:
    
    def __init__(self):
        """ Initialize all integration classes & prepare Aurras for general use """
        self.cfg = Config()


    def load(self):
        """ Load in a pre-trained NLP model """

        intent_label_path = f'{self.cfg.dataset_path}/intent_labels.json'
        entity_label_path = f'{self.cfg.dataset_path}/entity_labels.json'

        self.nlp = Model(
                intent_label_path, 
                entity_label_path, 
                self.cfg.prompt_padding, 
                self.cfg.model_name
            )
        
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
        print(classification)
        # response = self.plugins.generate_response(classification['intent'], classification['entities'])
        
        # return response
    

    def interact(self):
        """ Start a conversation with Aurras - text based """
        print('\n\n')
        print('Live interactive console loaded')

        while True:
            # get the user's prompt
            print('=> ', end='')
            prompt = input()

            if (prompt.lower() == 'exit'): # exit case
                break

            response = self.ask(prompt)
            # print(response['response'])
            # print('')
            
            
assistant = VoiceAssistant()
train = True
if train:
    assistant.build_dataset()
    assistant.build_model()
    
assistant.load()
assistant.interact()
