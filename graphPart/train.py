
import os
import numpy as np
from os import path, makedirs
from copy import deepcopy
import torch
import itertools

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
        self.model.to(device=self.device)
        
        self.optimizer = torch.optim.Adam(self.model.parameters(), lr=lr)
        
        self.conLoss = contrastiveLoss(lam, tau)
        if not path.exists(self.pretrainedModelPath):
            makedirs(self.pretrainedModelPath)
        else :
            self.load_model()
            
        self.embedModel = deepcopy(self.model)
        self.embedModel.to(self.device)
  
    def setEmbedModel (self):
        self.embedModel = deepcopy(self.model)
        self.embedModel.to(self.device)
        
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
    
    def get_mps (self, graph):
        mps = {}
        #newLinkType = []
        for mpt in self.mpTypes:
            nodes = [node for node in mpt.split('_')[int(len(mpt.split('_'))/2):]]
            new_nei = []
            sourceName=nodes[-1]; destName=nodes[-1] 
            linkName=nodes[0]
            for graphEdge in graph.edge_types:
                if nodes[0] in graphEdge and nodes[1] in graphEdge:
                    source = graph[graphEdge].edge_index[0]
                    source = source.detach().numpy()
                    dest = graph[graphEdge].edge_index[1]
                    dest = dest.detach().numpy()
                    break
            
            unique_source = np.unique(source)
            for us in unique_source:
                indx = np.where(source == us)
                if len(indx[0]) > 1:
                    new_nei+=list(itertools.combinations(dest[indx[0]],2))
                #for i in new_nei: pos[i] += 1
                    
            new_nei=list(np.array(new_nei).T)
            new_source=list(new_nei[0])+list(new_nei[1])
            new_dest=list(new_nei[1])+list(new_nei[0])
            new_nei=np.unique([new_source,new_dest],axis=1)
            
            mps[(sourceName,linkName,destName)] = (torch.tensor(new_nei)) 
        return mps
    
    def get_pos (self):
        pass
    
    def train_step (self, graph):
        self.model.train()
        self.optimizer.zero_grad()
        mps = self.get_mps(graph)
        mp_outs, sc_outs = self.model (graph, mps, self.device, mode="train")
        pos = self.get_pos()#TODO check
        loss = self.conLoss(mp_outs, sc_outs, pos.to(self.device))
        loss.backward()
        self.optimizer.step()
        return float(loss)
    
    def embedding_step (self, graph):
        mps = self.get_mps(graph)
        return self.embedModel(graph, mps)
    
    

