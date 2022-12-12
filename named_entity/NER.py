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
            proba = entity.score
            print(proba)
            if tag in entity_tags:
                temp = entity_tags[tag]
                temp.append(text)
                entity_tags[tag] = temp
            else:
                entity_tags[tag] = [text]
        return entity_tags

if __name__ =='__main__':
     ner = NamedEntityRecognition()
     s = 'where can i find Guruprasad ?'
     print(ner.predict(s))