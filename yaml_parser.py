import yaml

class Parser:
    def __init__(self):
        self.file_name = 'config.yml'
        with open(self.file_name) as f:
            self.config = yaml.load(f, Loader=yaml.FullLoader)
        self.__parse_input()
        
    def __parse_input(self):
        self.dataset_path = self.config['dataset_path']
        self.saved_model_path = self.config['saved_model_path']