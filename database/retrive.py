import pymongo
from pymongo import MongoClient
import os
from pprint import PrettyPrinter

printer = PrettyPrinter()

class Retrive:
    def __init__(self):
        self.client = pymongo.MongoClient("mongodb+srv://Niranjan:Niranjan15!@cluster0.lxzx5gk.mongodb.net/?retryWrites=true&w=majority")
        # self.client = pymongo.MongoClient("localhost",27017)      #for connecting to loacal db
        self.db = self.client.Chatur
        
    def retrive(self,collection):
        collection = self.db[collection]
        a = collection.find_one({'Name':"Principal"}) 
        print(a)

    def wildQuery(self,collection,queryText,serachIndex):
        query = [
            {
            '$search': {
            'index': serachIndex,  #'faculty_data'
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
    print(r.wildQuery('Departments','Computer Science & Engineering','departments_data'))

    
