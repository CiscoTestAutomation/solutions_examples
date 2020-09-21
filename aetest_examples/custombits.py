import yaml

class CustomBits:

    def __init__(self):
        self.job_dict={}
        self.basic_ping_dict ={}
        
        with open(f'./customize.yaml') as file:
            self.parameters_list = yaml.load(file, Loader=yaml.FullLoader)
        

    def joblist(self):

        self.job_dict = self.parameters_list['Jobs']
        return self.job_dict
    
    def ping_dest(self):
        self.basic_ping_dict = self.parameters_list['Ping_Dest']
        return self.basic_ping_dict


