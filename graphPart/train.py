
import os
from os import path, makedirs
import torch

from src.models import GraphModel

class graphEmbedding ():
    def __init__ (self, pretrainedModelPath="/graphPart/pretrained"):
        
        self.pretrainedModelPath = pretrainedModelPath
        
        self.model = GraphModel #TODO init graphmodel
        
        if not path.exists(self.pretrainedModelPath):
            makedirs(self.pretrainedModelPath)
        else :
            self.model = self.load_model()
        
    def getModel (self):
        return 
    
    def load_model (self):#TODO add more details
        self.model.load_state_dict(torch.load(self.pretrainedModelPath+''))
    
    def save_model (self):
        torch.save(self.model.state_dict(), self.pretrainedModelPath)
    
    def train_step (self):
        pass
    
    def embedding_step (self):
        pass
    
    

