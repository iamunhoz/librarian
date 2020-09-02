# -*- coding: latin-1 -*-

import requests
import json
import os
import secret #passcodes colocados num arquivo separado para não subir com git

class lexicon:
    def __init__(self, word_id):
        #dados de acesso fornecidos pela propria Oxford
        app_key = secret.SECRET_KEY # talvez eu precise mudar em que momento isso é atribuido
        app_id = secret.SECRET_ID   # idem acima
        language = 'en-gb'          # talvez de pra trocar?

        #ativa a api
        self.word_id = word_id
        url = "https://od-api.oxforddictionaries.com:443/api/v2/entries/" + language + "/" + self.word_id.lower()
        self.jsonfile = './dumpedWords/' + self.word_id + '.json'
        
        # checa se existe json local. Se existe, use este. Se não, faça um dump online
        if os.path.exists(self.jsonfile):
            with open (self.jsonfile) as f:
                self.jsonstr = json.loads(f.read())
        else:
            r = requests.get(url, headers = {"app_id": app_id, "app_key": app_key})
            self.jsonstr = json.loads(r.text)
            with open (self.jsonfile, 'w') as f:
                json.dump(self.jsonstr, f)
        
        #parameters
        self.pronunciation = self.jsonstr['results'][0]['lexicalEntries'][0]['entries'][0]['pronunciations'][0]['audioFile']
        self.type = self.jsonstr['results'][0]['type']
        self.ipa = self.jsonstr['results'][0]['lexicalEntries'][0]['entries'][0]['pronunciations'][0]['phoneticSpelling']
        self.grammarclass = self.jsonstr['results'][0]['lexicalEntries'][0]['lexicalCategory']['text']
        self.synonyms = []
        for i in self.jsonstr['results'][0]['lexicalEntries'][0]['entries'][0]['senses'][0]['synonyms']:
            self.synonyms.append(i['text'])
        self.definitions = self.jsonstr['results'][0]['lexicalEntries'][0]['entries'][0]['senses'][0]['definitions']
        self.etymology = self.jsonstr['results'][0]['lexicalEntries'][0]['entries'][0]['etymologies']
        #self.derivatives = self.jsonstr['results'][0]['lexicalEntries'][0]['derivatives'][0]['text'] não existe para todos
    
    # methods
    def speak(self): 
        os.system('mplayer -really-quiet ' + self.pronunciation) #deu certo. Futuramente implementar uma forma mais rapida #TODO

