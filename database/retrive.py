import pymongo
from pymongo import MongoClient
import os

class Retrive:
    def __init__(self):
        self.client = client = pymongo.MongoClient("mongodb+srv://Niranjan:Niranjan15!@cluster0.lxzx5gk.mongodb.net/?retryWrites=true&w=majority")
        # self.client = pymongo.MongoClient("localhost",27017)      #for connecting to loacal db
        self.db = self.client.Chatur
    def retrive(self,collection):
        collection = self.db[collection]
        a = collection.find_one({'Designation':"Principal"}) 
        print(a)

if __name__ =='__main__':
    r = Retrive()
    r.retrive('Person')
