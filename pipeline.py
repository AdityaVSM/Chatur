import random, datetime
import nltk
import numpy as np
import json
import  pickle
import constants

import nltk
from nltk.stem import WordNetLemmatizer
from keras.models import load_model

from yaml_parser import Parser
from named_entity.NER import NamedEntityRecognition
from database.retrive import Retrive
from constants import Constants, common_url, Faculty

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
    
    def start_bot(self, message = None):
        self.__load_models()
        print("Bot is ready to chat! (type quit to stop)")
        while True:
            message = input("")
            # new_message = " ".join(message.split())
            new_message = ""
            for words in message.split(" "):
                if words:
                    new_message += words[0].upper() + words[1:] + " "
            message = new_message
            if message.lower() == "quit":
                print("Thank for visiting!")
                break
            print("Input to Intent Recognition Module : " + message + "\n")
            ints = self.__predict_class(message)
            res = self.__get_response(ints, self.intents)
            res_response_code = self.__get_response_code(ints,self.intents)
            print("Output from Intent Recognition Module : " + str(ints))
            if(res_response_code ==  0):
                response = json.dumps({"response_message": res}, indent=4)
                print(response)
                continue
            
            if(res_response_code >=  1):
                print("Input to NER Module : " + message + "\n")
                res = self.ner.getresponse(message)
                print("Output from NER Module : " + str(res) + "\n")
                if len(res) > 0: 
                    key = list(res.keys())
                    res_temp = list(res[key[0]])
                    name = res_temp[0][0]
                    if len(res_temp) > 0 and (name.find("Where") >= 0 or name.find("Who") >= 0) :
                        name = res_temp[1][0]
                        print(name)
                    collection = self.constants.get_collection_name(key[0])
                    idx = self.constants.get_serach_index(collection)
                    details = self.retriver.wildQuery(collection, name, idx)
                    print("Output from MongoDB Knowledge Base : " + str(details) + "\n")
                    if(len(details) == 0):
                        responseString = "Sorry, I couldn't find any details :( \nCan you please be more specific?"
                        response = json.dumps({"response_message": responseString}, indent=4)
                        print(response)

                    else:
                        print("Here is/are the "+str(len(details))+" match/matches I found:")

                        if collection == 'Person':
                            response = self.extract_faculty(details)
                        elif collection == 'Departments':
                            response = self.extract_location(details, res_response_code)
                        else : 
                            response = self.extract_info(details,ints,res_response_code,ints)
                        
                        print(response)
                else:
                    response = json.dumps({"response_message": "Can you please be more specific?"}, indent=4)
                    print(response)

                continue
            
            if(res_response_code ==  2):
                print(res+"\n")
                continue
            print("\n")

    
    def extract_info(self,info,res,respo_code,ints):
        avoid = ['_id','id','ID number/   Aaadhaar number              (Not mandatory)','Gender','Date of joining the institution','Designation']
        stri = ''
        reqUrl = self.__get_response(ints, self.intents)
        if respo_code == 1:
            for key,value in info[0].items():
                if key == 'url' and value ==None:
                    urls = res
                elif key in avoid or value==None or value=='Nan':
                    continue
                else:
                    stri += key +':' + str(value)+'\n'
            stri = stri + 'For more info visit : ' + reqUrl
            # stri = "Name : "+  info[0]['Name']+'\n'+"Email : "+  info[0]['Email'] + "\nGender : "+ info[0]['Gender'] + "\nDesignation : "+ info[0]['Designation']
        elif respo_code == 2:
            if res[0]['intent'] == 'fee':
                stri = 'Management fees:'+ str(info[0]['fees']) + ' lakhs only\n For more information visit : '+ reqUrl
        return stri
    
    def extract_faculty(self, info):

        faculty = info[0]
        if 'URL' not in faculty.keys() or faculty['URL'] == "Nan":
            faculty['URL'] = common_url

        facultyResponse = Faculty(faculty['Name'], faculty['Email'], faculty['Gender'],
                                    faculty['Designation'], faculty['Department'],
                                    faculty['URL'])
        return facultyResponse.to_json()
    
    def extract_location(self, info, response_code):
        
        location = info[0]
        if response_code == 2:
            responseString = 'Management fees : '+ str(location['fees']) + ' lakhs only. \nFor more information vist'
            response = json.dumps({"code":response_code,"fee": responseString, "url":constants.fees_url}, indent=4)
            return response

        if 'URL' not in location.keys() or location['URL'] == "Nan":
            location['URL'] = common_url
        locationResponse = constants.Department(location['branch'], 
                                                location['location'], location['URL'])
        
        return locationResponse.to_json()
    
    def return_reponse(self, requetMessage):
        parse_message = " ".join(requetMessage.split())
        for words in requetMessage.split(" "):
            if words:
                parse_message += words[0].upper() + words[1:] + " "
        message = parse_message
        if message.lower() == "quit":
            return json.dumps({"code":0, "response_message": "Thanks for Visiting"}, indent=4)
        ints = self.__predict_class(message)
        res = self.__get_response(ints, self.intents)
        res_response_code = self.__get_response_code(ints, self.intents)
        if(res_response_code ==  0):
            return json.dumps({"code":0, "response_message": res}, indent=4)
        
        if(res_response_code >=  1):
            
            if res_response_code == 3:
                return(json.dumps({"code":0, "response_message": "Current time : " + str(datetime.now())}, indent=4))

            res = self.ner.getresponse(message)
            if len(res) > 0: 
                key = list(res.keys())

                name = list(res[key[0]])[0][0]
                if name.find("Where") >= 0 or name.find("Who") >= 0:
                    name = list(res[key[0]])[1][0]
                collection = self.constants.get_collection_name(key[0])
                idx = self.constants.get_serach_index(collection)
                details = self.retriver.wildQuery(collection, name, idx)
                if(len(details) == 0):
                    responseString = "Sorry, I couldn't find any details :( \nCan you please be more specific?"
                    response = json.dumps({"response_message": responseString}, indent=4)
                    return response
                else:
                    print("Here is/are the "+str(len(details))+" match/matches I found:")  

                    if collection == 'Person':
                        response = self.extract_faculty(details)
                    elif collection == 'Departments':
                        response = self.extract_location(details, res_response_code)
                    else : 
                        response = self.extract_info(details,ints,res_response_code,ints)

                    return response                   
            else:
                response = json.dumps({"code":0, "response_message": "Can you please be more specific?"}, indent=4)
                return response
        
                # print("Can you please be more specific?")
        return json.dumps({"code":0, "response_message": "I am a bot trained on constrained dataset, if you want answers - feed me with data!!!"}, indent=4)
            

