
class Constants:
    def __init__(self):
        self.mapping = {
            "PER":"Person", 
            "ORG":"Departments"
            }
        self.serach_index = {
            'Person': 'faculty_data',
            'Departments' : 'departments_data'
        }
    
    def get_collection_name(self, key):
        return self.mapping[key]

    def get_serach_index(self,key):
        return self.serach_index[key]