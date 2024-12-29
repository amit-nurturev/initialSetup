from abc import abstractmethod

class InitialDataInterface():    
    @staticmethod
    def get_instance():
        pass
        
    @abstractmethod
    def get_data(self):
        pass
