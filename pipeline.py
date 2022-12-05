import random
import nltk
import numpy as np
import json
import  pickle

import nltk
from nltk.stem import WordNetLemmatizer

from tensorflow.keras.models import load_model

def load_models():
    global intents, words, classes, model, lemmatizer
    lemmatizer = WordNetLemmatizer()
    intents = json.loads(open('model_building/datasets/intents.json').read())
        
    words = pickle.load(open('model_building/saved_models/words.pkl', 'rb'))
    classes = pickle.load(open('model_building/saved_models/classes.pkl', 'rb'))

    model = load_model('model_building/saved_models/chatbot_model_v1.h5')
    
def clean_up_sentence(sentence):
    sentence_words = nltk.word_tokenize(sentence)
    sentence_words = [lemmatizer.lemmatize(word.lower()) for word in sentence_words]
    return sentence_words

def bag_of_words(sentence):
    sentence_words = clean_up_sentence(sentence)
    bag = [0] * len(words)
    for s in sentence_words:
        for i, word in enumerate(words):
            if word == s:
                bag[i] = 1
    return np.array(bag)

def predict_class(sentence):
    bow = bag_of_words(sentence)
    res = model.predict(np.array([bow]))[0]
    ERROR_THRESHOLD = 0.25
    results = [[i,r] for i,r in enumerate(res) if r>ERROR_THRESHOLD]
    
    results.sort(key=lambda x: x[1], reverse=True)
    return_list = []
    for r in results:
        return_list.append({"intent": classes[r[0]], "probability": str(r[1])})
    return return_list

def get_response(ints, intents_json):
    tag = ints[0]['intent']
    list_of_intents = intents_json['intents']
    for i in list_of_intents:
        if(i['tag']== tag):
            result = random.choice(i['responses'])
            break
    return result

if __name__=="__main__":
    load_models()
    print("Welcome to the chatbot. Type 'quit' to exit.")
    while True:
        message = input("")
        if message.lower() == "quit":
            break
            
        ints = predict_class(message)
        res = get_response(ints, intents)
        print(res)