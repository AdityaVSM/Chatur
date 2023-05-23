import pandas as pd
import pymongo
from pymongo import MongoClient
import os

class Convert:
    def __init__(self):
        self.__dataframe = None
        self.client = pymongo.MongoClient("mongodb+srv://Niranjan:Niranjan15!@cluster0.lxzx5gk.mongodb.net/?retryWrites=true&w=majority")
        # self.client = pymongo.MongoClient("localhost",27017)      #for connecting to loacal db
        self.db = self.client.Chatur
        self.collection = None
        self.dept_mapper = {
            'CV' : 'Civil Engineering',
            'ME' : 'Mechanical Engineering',
            'EE' : 'Electrical and Electronics Engineering',
            'EC' : 'Electronics and Communication Engineering',
            'IM' : 'Industrial Engineering and Management',
            'CS' : 'Computer Science and Engineering',
            'IS' :'Information Science and Engineering',
            'ET' : 'Electronics and Telecommunication Engineering',
            'EI' : 'Electronics and Instrumentation Engineering',
            'ML' : 'Medical Electronics Engineering',
            'CH' : 'Chemical Engineering',
            'BT' : 'Bio - Technology',
            'AE' : 'Aerospace Engineering',
            'AI' : 'Machine Learning(AI & ML)',
            'CHY':'Chemistry Department',
            'MAT' : 'Mathematics Department',
            'PHY': 'Physics Department',
            'HUM' : '',
            'MCA' : 'Computer Applications(MCA)',
            'MBA' : 'Management Studies and Research Centre'
        }
    def check(p= None):
        return "hi"
    def read(self,path):
        self.__dataframe = pd.read_excel(path)
        # print(self.__dataframe)
    def getcollection(self,name):
        self.collection = self.db[name]
        # if name in self.db.list_collection_names:
        # else:
        #     return 0
        return 1
    def insert(self,path,name):
        self.__read(path)
        mp = self.__dataframe.to_dict(orient='records')
        print(mp)
        if self.getcollection(name) == 1:
            if self.collection.insert_many(mp):
                return 1
    def update(self,path,name):

        self.read(path)
        self.getcollection(name)
        df = self.__dataframe
        # print(df)
        temp = dict()
        names = []
        vals = []
        count = 0
        for index, row in df.iterrows():
            name = row['Name']
            a = self.collection.find_one({'Name':name}) 
            url = row['URL']
            # department = self.dept_mapper[row['Dept']]
            # # gender = None
            # designation = row[i,'Designation']
            # print(url)
            if a==None:
                temp[name] = 0
                # names.append(name)
                # vals.append(0)
                count+=1
                print(count)
            else:
                temp[name] = 1
                self.collection.update_one({'Name':name},{"$set":{"URL":url}})
                print('0')
                # names.append(name)
                # vals.append(1)
        # d = {
        #     'Name':names,
        #     'present':vals
        # }
        df1 = pd.DataFrame(list(temp.items()))
        df1.to_csv('file2.csv', header=False, index=False)
        print(df1)
        
        



if __name__ == '__main__':
    # ch = Convert()
    c = Convert()
    path = os.path.join('','Faculty Profile-URL(2).xlsx')
    # ch.insert(path,'Departments')
    c.update(path,'Person')