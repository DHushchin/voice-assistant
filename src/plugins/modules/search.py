import requests, webbrowser, bs4
import wikipedia

class GoogleSearch:   
    
    def execute(self, entities) -> str:    
        entities = [e[1] for e in entities]      
        wiki = self.__wiki(entities)
        self.__google(entities)
        return wiki
        
        
    def __wiki(self, entities):
        wiki = None

        try:
            wiki = f'Wikipedia says: {wikipedia.summary(" ".join(entities))}. I am also opening top 5 google pages for you.'
        except wikipedia.exceptions.DisambiguationError as e:
            wiki = 'Opening top 5 google pages for you.'
            
        return wiki
    
    
    def __google(self, entities):
        res = requests.get('https://google.com/search?q=' + ' '.join(entities))
        res.raise_for_status()
        soup = bs4.BeautifulSoup(res.text, "html.parser")
        linkElems = soup.select('div#main > div > div > div > a')
        numOpen = min(5, len(linkElems))
        for i in range(numOpen):
            webbrowser.open('https://google.com' + linkElems[i].get('href'))
        