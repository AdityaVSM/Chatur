import random
import numpy as np
import json
import pickle

import nltk
from nltk.stem import WordNetLemmatizer

from tensorflow.keras.models import Sequential
from tensorflow.keras.layers import Dense, Activation, Dropout
from tensorflow.keras.optimizers import SGD

import os, sys
sys.path.append('C:/personal/imp/Capstone project/Chatur')

from yaml_parser import Parser

class Trainer:
    def __init__(self):
        # nltk.download('punkt') # Uncomment if you don't have the punkt package
        # nltk.download('wordnet') # Uncomment if you don't have the wordnet package
        # nltk.download('omw-1.4') # Uncomment if you don't have the omw-1.4 package
        
        self.lemmatizer = WordNetLemmatizer()
        self.config = Parser()

    def load_data(self):
        self.intents = json.loads(open(self.config.dataset_path).read())
        self.words = []
        self.classes = []
        self.documents = []
        self.ignore_letters = ['?', '!', '.', ',']
        
        for intent in self.intents['intents']:
            for pattern in intent['patterns']:
                word_list = nltk.word_tokenize(pattern)
                self.words.extend(word_list)
                self.documents.append((word_list, intent['tag']))
                if intent['tag'] not in self.classes:
                    self.classes.append(intent['tag'])
        self.words = [self.lemmatizer.lemmatize(word.lower()) for word in self.words if word not in self.ignore_letters]
        self.words = sorted(list(set(self.words)))
        
    def save_data(self):
        pickle.dump(self.words, open('model_building/saved_models/words.pkl', 'wb'))
        pickle.dump(self.classes, open('model_building/saved_models/classes.pkl', 'wb'))


    def create_training_data(self):
        training = []
        output_empty = [0] * len(self.classes)
        for doc in self.documents:
            bag = []
            word_patterns = doc[0]
            word_patterns = [self.lemmatizer.lemmatize(word.lower()) for word in word_patterns]
            for word in self.words:
                bag.append(1) if word in word_patterns else bag.append(0)
            output_row = list(output_empty)
            output_row[self.classes.index(doc[1])] = 1
            training.append([bag, output_row])
        random.shuffle(training)
        training = np.array(training)
        train_x = list(training[:,0])
        train_y = list(training[:,1])
        return train_x, train_y

    def create_model(self, train_x, train_y):
        model = Sequential()
        model.add(Dense(128, input_shape=(len(train_x[0]),), activation='relu'))
        model.add(Dropout(0.5))
        model.add(Dense(64, activation='relu'))
        model.add(Dropout(0.5))
        model.add(Dense(len(train_y[0]), activation='softmax'))
        sgd = SGD(learning_rate=0.01)
        model.compile(loss='categorical_crossentropy', optimizer=sgd, metrics=['accuracy']) 
        return model
    
    def train_model(self, model, train_x, train_y):
        history = model.fit(np.array(train_x), np.array(train_y), epochs=200, batch_size=5, verbose=1)
        return history
    
    def save_model(self, model):
        model.save(self.config.saved_model_path, model)
      
if __name__ == '__main__':
    trainer = Trainer()
    trainer.load_data()
    trainer.save_data()
    train_x, train_y = trainer.create_training_data()
    model = trainer.create_model(train_x, train_y)
    history = trainer.train_model(model, train_x, train_y)
    trainer.save_model(model)  
    
        
            