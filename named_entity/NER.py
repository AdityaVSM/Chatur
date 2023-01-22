from flair.data import Sentence
from flair.models import SequenceTagger

class NamedEntityRecognition:
    def __init__(self) -> None:
        self.model = SequenceTagger.load('flair/ner-english-large')
    def predict(self,sentence):
        sentence = Sentence(sentence)
        self.model.predict(sentence)
        entities = sentence.get_spans('ner')
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

if __name__ =='__main__':
     ner = NamedEntityRecognition()
     s = 'Hi Mahesh?'
     print(ner.predict(s))