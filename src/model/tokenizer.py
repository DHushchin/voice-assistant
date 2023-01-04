import numpy as np
from transformers import DistilBertTokenizerFast


class Tokenizer:
    def __init__(self, model_name: str):
        self.tokenizer = DistilBertTokenizerFast.from_pretrained(model_name)
        
    def encode(self, texts, texts_labels, max_len):  
            
        """
            Encode a sequence of strings using the provided tokenizer.
            Returns an encoded ID and an attention mask
            Inputs: 
            - texts:        sequence of strings to be tokenized
            - texts_labels: word-level lables for the text sequences
            - max_len:      integer controling the maximum number of tokens to tokenize
            
            Outputs:
            - input_ids:      sequence of encoded tokens as a np array
            - attention_mask: sequence of attention masks as a np array
            - labels:         sequence of token-level labels as a np array
        """

        input = [self.__tokenize_and_preserve_labels(
                text, text_labels, max_len=max_len
                ) for text, text_labels in zip(texts, texts_labels)]

        input_ids = np.array([i[0] for i in input])
        attention_masks = np.array([i[1] for i in input])
        labels = np.array([i[2] for i in input])
        
        return input_ids, attention_masks, labels


    def encode_without_labels(self, texts, max_len):
        
        """
            Encode a sequence of strings using the provided tokenizer.
            Returns an encoded ID and an attention mask
            Inputs: 
            - texts:     sequence of strings to be tokenized
            - max_len:   integer controling the maximum number of tokens to tokenize
            
            Outputs:
            - input_ids:      sequence of encoded tokens as a np array
            - attention_mask: sequence of attention masks as a np array
        """

        input = self.tokenizer(
            texts,
            max_length=max_len,
            padding='max_length',
            truncation=True,
            return_attention_mask=True,
            return_token_type_ids=False,
            return_tensors='np'
        )

        return input['input_ids'], input['attention_mask']


    def __tokenize_and_preserve_labels(self, text, text_labels, max_len):
        
        """
            Tokenize a sequence while preserving word-level labels
            Inputs:
            - text:        prompt
            - text_labels: list of labels for each word in the prompt
            - max_len:     maximum length of a prompt after tokenization
            Outputs:
            - token_ids:      list token IDs for the input text
            - attention_mask: attention mask for the input text
            - labels:         list of token-level labels
        """

        tokenized_sequence = []
        labels = []
        attention_mask = []

        for word, label in zip(text.split(), text_labels):
            tokenized_word = self.tokenizer.tokenize(word)
            n_tokens = len(tokenized_word)
            
            tokenized_sequence.extend(tokenized_word)
            labels.extend([label] * n_tokens)

        # add in the [CLS] and [SEP] tokens to mark the start and end
        tokenized_sequence.insert(0, '[CLS]')
        labels.insert(0, 0)

        tokenized_sequence.append('[SEP]')
        labels.append(0)

        attention_mask = [1] * len(tokenized_sequence)

        # pad the lists
        while len(tokenized_sequence) < max_len:
            tokenized_sequence.append('[PAD]')
            attention_mask.append(0)
            labels.append(0)

        token_ids = [self.tokenizer.convert_tokens_to_ids(token) for token in tokenized_sequence]

        return token_ids, attention_mask, labels
    
    
    def decode(self, token_ids):
        return self.tokenizer.decode(token_ids)
