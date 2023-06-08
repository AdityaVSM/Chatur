import json
common_url = "https://www.bmsce.ac.in/"
fees_url = "https://bmsce.ac.in/home/Under-Graduation"

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
    
class Faculty:
    def __init__(self, name, email, gender, designation, department, profileUrl):
        self.name = name
        self.email = email
        self.gender = gender
        self.designation = designation
        self.department = department
        self.profileUrl = profileUrl

    def to_json(self):
        """Returns a JSON representation of the Faculty object."""
        return json.dumps({
            "name": self.name,
            "email": self.email,
            "gender": self.gender,
            "designation": self.designation,
            "department": self.department,
            "url": self.profileUrl,
        }, indent=4)
    
# class Department:
#     def __init__(self, branchName, location, deptUrl, fees):
#         self.branchName = branchName
#         self.location = location
#         self.deptUrl = deptUrl
#         self.fees = fees
    
#     def to_json(self):
#         return json.dumps({
#             "name": self.branchName,
#             "location": self.location,
#             "url": self.deptUrl,
#             "fees": self.fees
#         }, indent=4)
    
class Department:
    def __init__(self, branchName, location, deptUrl):
        self.branchName = branchName
        self.location = location
        self.deptUrl = deptUrl

    def to_json(self):
        return json.dumps({
            "name": self.branchName,
            "location": self.location,
            "url": self.deptUrl
        }, indent=4)
    