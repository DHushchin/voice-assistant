from .base import BaseModule

from forex_python.converter import CurrencyRates
import pandas as pd
import os


class CurrencyModule(BaseModule):
    def __init__(self):
        self.converter = CurrencyRates()     
        self.data = pd.read_csv(f'{os.path.abspath(os.path.dirname(__file__))}/data/iso.csv')
        
        
    def execute(self, entities): 
        curr1, curr2 = entities[0][1], entities[1][1]
        print(curr1, curr2)
        for i in range(len(self.data)):
            if curr1 in str(self.data['Currency'][i]).lower():
                curr1 = self.data['AlphabeticCode'][i]
            if curr2 in str(self.data['Currency'][i]).lower():
                curr2 = self.data['AlphabeticCode'][i]

        return str(self.converter.convert(curr1, curr2, 1))
