import random
import nltk
import numpy as np
import json
import  pickle

import nltk
from nltk.stem import WordNetLemmatizer

from keras.models import load_model

from yaml_parser import Parser
from named_entity.NER import NamedEntityRecognition

class ChatBot:
    def __init__(self):
        p = Parser()
        self.dataset_path = p.dataset_path
        self.saved_model_path = p.saved_model_path
        self.ner = NamedEntityRecognition()

    def __load_models(self):
        self.lemmatizer = WordNetLemmatizer()
        self.intents = json.loads(open(self.dataset_path).read())
            
        self.words = pickle.load(open('model_building/saved_models/words.pkl', 'rb'))
        self.classes = pickle.load(open('model_building/saved_models/classes.pkl', 'rb'))

        self.model = load_model(self.saved_model_path)
    
    def __clean_up_sentence(self,sentence):
        sentence_words = nltk.word_tokenize(sentence)
        sentence_words = [self.lemmatizer.lemmatize(word.lower()) for word in sentence_words]
        return sentence_words

    def __bag_of_words(self,sentence):
        sentence_words = self.__clean_up_sentence(sentence)
        bag = [0] * len(self.words)
        for s in sentence_words:
            for i, word in enumerate(self.words):
                if word == s:
                    bag[i] = 1
        return np.array(bag)

    def __predict_class(self,sentence):
        bow = self.__bag_of_words(sentence)
        res = self.model.predict(np.array([bow]))[0]
        ERROR_THRESHOLD = 0.25
        results = [[i,r] for i,r in enumerate(res) if r>ERROR_THRESHOLD]
    
        results.sort(key=lambda x: x[1], reverse=True)
        return_list = []
        for r in results:
            return_list.append({"intent": self.classes[r[0]], "probability": str(r[1])})
        return return_list

    def __get_response(self,ints, intents_json):
        tag = ints[0]['intent']
        list_of_intents = intents_json['intents']
        for i in list_of_intents:
            if(i['tag']== tag):
                result = random.choice(i['responses'])
                break
        return result
    
    def __get_response_code(self, ints, intents_json):
        tag = ints[0]['intent']
        list_of_intents = intents_json['intents']
        for i in list_of_intents:
            if(i['tag'] == tag):
                response_code = i['response_code']
                break
        return response_code
    
    def start_bot(self):
        self.__load_models()
        print("Bot is ready to chat! (type quit to stop)")
        while True:
            message = input("")
            if message.lower() == "quit":
                break
            ints = self.__predict_class(message)
            res = self.__get_response(ints, self.intents)
            res_response_code = self.__get_response_code(ints,self.intents)
            if(res_response_code ==  1):
                res = self.ner.predict(message)
                # if res=={}:
                #     res = message.split(' ')[-1]
            print(res)
