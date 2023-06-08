import pymongo
from pymongo import MongoClient
import os
from pprint import PrettyPrinter

printer = PrettyPrinter()

class Retrive:
    def __init__(self):
        self.client = pymongo.MongoClient("mongodb+srv://Niranjan:Niranjan15!@cluster0.lxzx5gk.mongodb.net/?retryWrites=true&w=majority",connectTimeoutMS=30000, socketTimeoutMS=None, connect=False, maxPoolsize=1)
         #for connecting to loacal db
        # self.client = pymongo.MongoClient("localhost",27017)     
        self.db = self.client.Chatur
        
    def retrive(self,collection):
        collection = self.db[collection]
        a = collection.find_one({'Name':"Hemavathi"}) 
        print(a)

    def wildQuery(self,collection,queryText,serachIndex):
        query = [
            {
            '$search': {
            'index': serachIndex, 
            'text': {
                'query': queryText,
                'path': {
                'wildcard': '*'
                },
                "fuzzy": {}
                }
            }
        }
        ]
        
        result = list(self.db[collection].aggregate(query))
        # print(len(list(result)))
        # printer.pprint(list(result))
        return result

if __name__ =='__main__':
    r = Retrive()
    # r.retrive('Person')
    r.wildQuery('Person','Shmbhavi')

    
