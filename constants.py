
class Constants:
    def __init__(self):
        self.mapping = {
            "PER":"Person", 
            "ORG":"Organisation"
            }
    
    def get_collection_name(self, key):
        return self.mapping[key]
    