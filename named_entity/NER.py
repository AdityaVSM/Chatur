from flair.data import Sentence
from flair.models import SequenceTagger
import requests
class NamedEntityRecognition:
    def __init__(self) -> None:
        # self.model = SequenceTagger.load('flair/ner-english-large')
        pass
    def predict(self,sentence):
        sentence = Sentence(sentence)
        self.model.predict(sentence)
        entities = sentence.get_spans('ner')
        print(entities)
        entity_tags = {}
        for entity in entities:
            tag = entity.tag
            text = entity.text
            score = entity.score
            if tag in entity_tags:
                
                temp = entity_tags[tag]
                temp.append((text,score))
                entity_tags[tag] = temp
            else:
                entity_tags[tag] = [(text,score)]
        return entity_tags
    def getresponse(self,sentence):

        API_URL = "https://api-inference.huggingface.co/models/flair/ner-english-large"
        headers = {"Authorization": "Bearer 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"}

        def query(payload):
            response = requests.post(API_URL, headers=headers, json=payload)
            return response.json()
        entities = query({
            "inputs": sentence,
        })
        print(entities)
        entity_tags = {}
        for entity in entities:
            tag = entity['entity_group']
            text = entity['word']
            score = entity['score']
            if tag in entity_tags:
                
                temp = entity_tags[tag]
                temp.append((text,score))
                entity_tags[tag] = temp
            else:
                entity_tags[tag] = [(text,score)]
        return entity_tags

if __name__ =='__main__':
     ner = NamedEntityRecognition()
     s = 'How much i have pay to get into Computer Science and Engineering department?'
     print(ner.getresponse(s))