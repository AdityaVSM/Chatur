import pandas as pd
import pymongo
from pymongo import MongoClient
import os

class Convert:
    def __init__(self):
        self.__dataframe = None
        self.client = client = pymongo.MongoClient("mongodb+srv://Niranjan:Niranjan15!@cluster0.lxzx5gk.mongodb.net/?retryWrites=true&w=majority")
        # self.client = pymongo.MongoClient("localhost",27017)      #for connecting to loacal db
        self.db = self.client.Chatur
        self.collection = None
    def __read(self,path):
        self.__dataframe = pd.read_excel(path)
    def __getcollection(self,name):
        self.collection = self.db[name]
        # if name in self.db.list_collection_names:
        # else:
        #     return 0
        return 1
    def insert(self,path,name):
        self.__read(path)
        mp = self.__dataframe.to_dict(orient='records')
        if self.__getcollection(name) == 1:
            if self.collection.insert_many(mp):
                return 1

if __name__ == '__main__':
    c = Convert()
    path = os.path.join('database','Person.xlsx')
    # c.__read('Person.xlsx')
    c.insert(path,'Person')