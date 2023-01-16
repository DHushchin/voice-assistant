from .base import BaseModule

import requests, webbrowser, bs4
import wikipedia


class SearchModule(BaseModule):   
    
    def execute(self, entities) -> str:    
        entities = [e[1] for e in entities]      
        wiki = self.__wiki(entities)
        self.__google(entities)
        return wiki
        
        
    def __wiki(self, entities):
        wiki = None

        try:
            wiki = f'Wikipedia says: {wikipedia.summary(" ".join(entities), sentences=3)}. I am also opening top 5 google pages for you.'
        except:
            wiki = 'Opening top 5 google pages for you.'
            
        return wiki
    
    
    def __google(self, entities):
        res = requests.get('https://google.com/search?q=' + ' '.join(entities))
        res.raise_for_status()
        soup = bs4.BeautifulSoup(res.text, "html.parser")
        link_elems = soup.select('div#main > div > div > div > a')
        num_open = min(5, len(link_elems))
        for i in range(num_open):
            webbrowser.open('https://google.com' + link_elems[i].get('href'))
        