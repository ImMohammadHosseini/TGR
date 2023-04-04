
import os
from os import path, makedirs
import torch

from src.models import GraphModel
from src import contrastiveLoss

class graphEmbedding ():
    def __init__ (self, node_types, device, embed_dim, feat_drop, 
                  attn_drop, lr, lam, tau, 
                  pretrainedModelPath="/graphPart/pretrained"):
        self.mpTypes = ['host_datacenter_host', 'vm_datacenter_vm', 'vm_host_vm', 
                        'instance_task_instance', 'instance_vm_instance']
        self.P = len(self.mpTypes)
        self.pretrainedModelPath = pretrainedModelPath
        self.device=device
        self.model = GraphModel(embed_dim, node_types, feat_drop, attn_drop, 
                                self.P)
        self.model = self.model.to(device=self.device)
        
        self.optimizer = torch.optim.Adam(self.model.parameters(), lr=lr)
        
        self.conLoss = contrastiveLoss(lam, tau)
        if not path.exists(self.pretrainedModelPath):
            makedirs(self.pretrainedModelPath)
        else :
            self.load_model()
        
        
    def getModel (self):
        return 
     
    def load_model (self, filename):
        #TODO check 
        file_path = self.pretrainedModelPath + "/" + filename + "_Trained.ckpt"
        checkpoint = torch.load(file_path)
        self.model.load_state_dict(checkpoint['model_state_dict'])
        self.optimizer.load_state_dict(checkpoint['optimizer_state_dict'])
        epoch = checkpoint['epoch']
        accuracy_list = checkpoint['accuracy_list']
        
    
    def save_model (self, epoch, accuracy_list):
        file_path = self.pretrainedModelPath + "/" + self.model.name + "_" + \
            str(epoch)+".ckpt"
            
        torch.save({
            'epoch': epoch,
            'model_state_dict': self.model.state_dict(),
            'optimizer_state_dict': self.optimizer.state_dict(),
            'accuracy_list': accuracy_list}, file_path)
    
    def get_mps (self):
        pass
    
    def get_pos (self):
        pass
    
    def train_step (self, graph):
        self.model.train()
        self.optimizer.zero_grad()
        mps = self.get_mps()#TODO check
        mp_outs, sc_outs = self.model (graph, mps, self.device, mode="train")
        pos = self.get_pos()#TODO check
        loss = self.conLoss(mp_outs, sc_outs, pos.to(self.device))
        loss.backward()
        self.optimizer.step()
        return float(loss)
    
    def embedding_step (self):
        pass
    
    

