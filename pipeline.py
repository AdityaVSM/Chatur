import random
import nltk
import numpy as np
import json
import  pickle

import nltk
from nltk.stem import WordNetLemmatizer
# from app_logger import logger
from keras.models import load_model

from yaml_parser import Parser
from named_entity.NER import NamedEntityRecognition
from database.retrive import Retrive
from constants import Constants

class ChatBot:
    def __init__(self):
        p = Parser()
        self.dataset_path = p.dataset_path
        self.saved_model_path = p.saved_model_path
        self.ner = NamedEntityRecognition()
        self.retriver = Retrive()
        self.constants = Constants()
        # self.mapper = {'PER'}
        self.lemmatizer = WordNetLemmatizer()
        self.intents = json.loads(open(self.dataset_path).read())
            
        self.words = pickle.load(open('model_building/saved_models/words.pkl', 'rb'))
        self.classes = pickle.load(open('model_building/saved_models/classes.pkl', 'rb'))
        self.model = load_model(self.saved_model_path)
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
    
    def start_bot(self,message=None):
        self.__load_models()
        print("Bot is ready to chat! (type quit to stop)")
        while True:
            message = input("")
            new_message = " ".join(message.split())
            for words in message.split(" "):
                if words:
                    new_message+=words[0].upper()+words[1:]+" "
            message = new_message
            if message.lower() == "quit":
                print("Thank for visiting!")
                break
            ints = self.__predict_class(message)
            res = self.__get_response(ints, self.intents)
            res_response_code = self.__get_response_code(ints,self.intents)
            print(ints)
            if(res_response_code ==  0):
                print(res+"\n")
                continue
            
            if(res_response_code >=  1):
                res = self.ner.getresponse(message)
                if len(res) > 0: 
                    key = list(res.keys())

                    name = list(res[key[0]])[0][0]
                    # name = name.split(' ')
                    # name = ''.join(name[:])
                    print(name)
                    print('key',key[0])
                    collection = self.constants.get_collection_name(key[0])
                    # print(collection)
                    idx = self.constants.get_serach_index(collection)
                    details = self.retriver.wildQuery(collection,name,idx)
                    if(len(details) == 0):
                        string = "Sorry, I couldn't find any details/nCan you please be more specific?"
                        print(string)
                        # print("Can you please be more specific?")
                    else:
                        print("Here is/are the "+str(len(details))+" match/matches I found:")
                        # print("Name : "+  details[0]['Name'])
                        # print("Email : "+  details[0]['Email'])
                        # print("Gender : "+ details[0]['Gender'])
                        # print("Designation : "+ details[0]['Designation'])     
                        string = self.extract_info(details,ints,res_response_code)
                        print(string)                   
                else:
                    print("Can you please be more specific?")
                continue
            
            if(res_response_code ==  2):
                print(res+"\n")
                continue
            print("\n")
    def extract_info(self,info,res,respo_code):
        avoid = ['_id','id','ID number/   Aaadhaar number              (Not mandatory)','Gender','Date of joining the institution','Designation']
        stri = ''
        if respo_code == 1:
            for key,value in info[0].items():
                if key == 'url' and value ==None:
                    urls = res
                elif key in avoid or value==None:
                    continue
                else:
                    stri += key +':' + str(value)+'\n'
            stri = stri + 'For more info visit : ' + res
            # stri = "Name : "+  info[0]['Name']+'\n'+"Email : "+  info[0]['Email'] + "\nGender : "+ info[0]['Gender'] + "\nDesignation : "+ info[0]['Designation']
        elif respo_code ==2:
            if res[0]['intent'] == 'fee':
            
                stri = 'Management fees: ' + str(info[0]['fees']) + ' lakhs only' +
        return stri
    
    def return_reponse(self, requetMessage):
        # self.__load_models()
        string = ""
        parse_message = " ".join(requetMessage.split())
        for words in requetMessage.split(" "):
            if words:
                parse_message += words[0].upper() + words[1:] + " "
        message = parse_message
        if message.lower() == "quit":
            return "quit"
        ints = self.__predict_class(message)
        res = self.__get_response(ints, self.intents)
        res_response_code = self.__get_response_code(ints, self.intents)
        if(res_response_code ==  0):
            string = res
            return res
        
        if(res_response_code >=  1):
            res = self.ner.getresponse(message)
            if len(res) > 0: 
                key = list(res.keys())

                name = list(res[key[0]])[0][0]
                # name = name.split(' ')
                # name = ''.join(name[:])
                # print(name)
                # print('key',key[0])
                collection = self.constants.get_collection_name(key[0])
                # print(collection)
                idx = self.constants.get_serach_index(collection)
                details = self.retriver.wildQuery(collection,name,idx)
                if(len(details) == 0):
                    string = "Sorry, I couldn't find any details/nCan you please be more specific?"
                    return string
                    print(string)
                    # print("Can you please be more specific?")
                else:
                    print("Here is/are the "+str(len(details))+" match/matches I found:")
                    # print("Name : "+  details[0]['Name'])
                    # print("Email : "+  details[0]['Email'])
                    # print("Gender : "+ details[0]['Gender'])
                    # print("Designation : "+ details[0]['Designation'])     
                    string = self.extract_info(details,ints,res_response_code,ints)
                    # print(string)
                    return string                   
            else:
                # logger.debug("unhandledQuery : ")
                # string = "Can you please be more specific? + 1"
                # return string
                pass
                # print("Can you please be more specific?")
        return string
            

