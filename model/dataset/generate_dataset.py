import os
import json
import random
import itertools
import glob
import pandas as pd
from pathlib import Path


class DatasetGenerator:
    def __init__(self, samples_per_intent=512, duplicates=False):
        """
        Inputs:
            - dataset_path:       path to the train.pkl output
            - samples_per_intent: number of samples to generate per intent
            - duplicates:         allow duplicate prompts to fill the [samples_per_intent] quota
        """
        self.samples_per_intent = samples_per_intent
        self.duplicates = duplicates
        
    
    def generate_dataset(self):
        """
            Generate the dataset from .entity and .intent files in the dataset directory.
            
            Outputs:
            - entity_labels.json: JSON mapping to convert entity IDs into the plain-text entities
            - intent_labels.json: JSON mapping to convert intent IDs into the plain-text intents
            - train.pkl:          full training dataset
        """

        if not os.path.isdir(self.dataset_path):
            print('Dataset directory does not exist')
            return

        entities = self.__load_entities()
        intents = self.__load_intents()
        intent_labels, entity_labels = self.__generate_labels(intents, entities)
        
        filled_prompts = self.__slot_filling(intents, entities)
        permutated_prompts = self.__permutate_prompts(filled_prompts)
        generated_prompts = self.__entity_labels_to_words(permutated_prompts)
        
        dataset = self.__generate_dataset(generated_prompts, intent_labels, entity_labels)
        self.__save_dataset(dataset, intent_labels, entity_labels)
            
            
    def __load_entities(self):
        entity_files = glob.glob(f'./raw/entities/*.entity', recursive=True)
        
        entities = {}
        entity_id = 1
        for file in entity_files:
            name = Path(file).stem
            samples = [(e.lower(), entity_id) for e in open(file).read().splitlines() if not e.startswith('#')]
            entities[name] = samples
            entity_id += 1
            
        return entities
    
    
    def __load_intents(self):
        intent_files = glob.glob(f'./raw/intents/*.intent', recursive=True)
        
        intents = {}
        for file in intent_files:
            name = Path(file).stem
            samples = [i.lower() for i in open(file).read().splitlines() if not i.startswith('#')]
            intents[name] = samples
        
        return intents
        
        
    def __get_labels(self, intents, entities):
        intent_labels = {}
        entity_labels = {}

        x = 0
        for category in intents:
            intent_labels[x] = category
            x += 1

        x = 1 
        # start at 1 to make room for null entity
        for category in entities:
            entity_labels[x] = category
            x += 1
            
        return intent_labels, entity_labels
    
    
    def __slot_filling(self, entities, intents):
        filled_prompts = {}
        
        for category in intents:
            filled_prompts[category] = []
            
            for sample in intents[category]:
                filled_prompts[category].append(
                    [entities[word[1:-1]] if word.startswith('{') and word.endswith('}') 
                    else [(word, 0)] for word in sample.split()]
                )  
                
        return filled_prompts     
    
    
    def __permutate_prompts(self, filled_prompts):
        permutated_prompts = {}
        
        for category in filled_prompts:
            permutations = []
            
            for sample in filled_prompts[category]:
                permutations.extend(list(itertools.product(*sample)))

            permutated_prompts[category] = permutations
            
        return permutated_prompts   
    
    
    def __entity_labels_to_words(self, permutated_prompts):
        generated_prompts = {}
        for category in permutated_prompts: # intent categories
            category_prompts = []

            for sample in permutated_prompts[category]: # intent samples
                new_sample = []

                for word in sample: # individual words / entities
                    if word[0] == '': # remove empty intents
                        continue

                    new_sample.extend([(w, word[1]) for w in word[0].split()])

                category_prompts.append(new_sample)
            
            generated_prompts[category] = category_prompts
            
        return generated_prompts    
    
    
    def __generate_dataset(self, generated_prompts, intent_labels, entity_labels):
        dataset = []

        for category in generated_prompts:
            if not self.duplicates and len(generated_prompts[category]) < self.samples_per_intent:
                samples = generated_prompts[category]
                print(f'not enough "{category}" intents were generated from templates. \
                      Limiting number of samples to {len(generated_prompts[category])}')
            else:
                samples = random.choices(generated_prompts[category], k=self.samples_per_intent)

            # convert the data into a json so pandas can read it
            for sample in range(len(samples)):
                dataset.append({
                    'prompts':  ' '.join([w[0] for w in samples[sample]]),
                    'prompt_intent': list(intent_labels.values()).index(category),
                    'word_entities': [w[1] for w in samples[sample]]
                })    
                
        return dataset
    
    
    def __save_dataset(self, dataset, intent_labels, entity_labels):
        df = pd.DataFrame(dataset)
        df.to_pickle(f'./train.pkl')

        with open(f'./intent_labels.json', 'w') as f:
            json.dump(intent_labels, f)
        
        with open(f'./entity_labels.json', 'w') as f:
            json.dump(entity_labels, f)
            
            
if __name__ == '__main__':
    generator = DatasetGenerator()
    generator.generate_dataset()
     