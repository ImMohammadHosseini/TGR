
import numpy as np

from os import path, makedirs
from copy import deepcopy
import torch
import itertools

from scipy.sparse import csr_matrix

from .src.models.graphModel import GNNEncoder
from .src.contrastiveLoss import ContrastiveLoss

class GraphEmbedding ():
    def __init__ (self, data_type, node_types, device, in_features:list,
                  embed_dim, feat_drop, attn_drop, lr, lam, tau, 
                  pretrainedModelPath="graphPart/pretrained/"):
        self.mpTypes = ['host_datacenter_host', 'vm_datacenter_vm', 'vm_host_vm', 
                        'instance_task_instance', 'instance_vm_instance']
        self.P = len(self.mpTypes)
        self.pretrainedModelPath = pretrainedModelPath
        self.device=device
        self.model = GNNEncoder(in_features, embed_dim, node_types, feat_drop, 
                                attn_drop, self.P)
        self.model.to(device=self.device)
        
        self.optimizer = torch.optim.Adam(self.model.parameters(), lr=lr)
        
        self.conLoss = ContrastiveLoss(lam, tau)
        
        if path.exists(self.pretrainedModelPath):
            self.load_model()
            
        self.embedModel = deepcopy(self.model)
        self.embedModel.to(self.device)
        
        self.host_size = int(data_type.split('_')[-2])
        self.vm_size = int(data_type.split('_')[-1])
        
    def setEmbedModel (self):
        self.embedModel = deepcopy(self.model)
        self.embedModel.to(self.device)
        
    def load_model (self):
        file_path = self.pretrainedModelPath + self.model.name + ".ckpt"
        checkpoint = torch.load(file_path)
        self.model.load_state_dict(checkpoint['model_state_dict'])
        self.optimizer.load_state_dict(checkpoint['optimizer_state_dict'])
         
    def save_model (self):
        if not path.exists(self.pretrainedModelPath):
            makedirs(self.pretrainedModelPath)
        
        file_path = self.pretrainedModelPath + self.model.name + ".ckpt"
            
        torch.save({
            'model_state_dict': self.model.state_dict(),
            'optimizer_state_dict': self.optimizer.state_dict()}, file_path)
        
    def sparse_mx_to_torch_sparse_tensor(self, sparse_mx):
        """Convert a scipy sparse matrix to a torch sparse tensor."""
        sparse_mx = sparse_mx.tocoo().astype(np.float32)
        indices = torch.from_numpy(
            np.vstack((sparse_mx.row, sparse_mx.col)).astype(np.int64))
        values = torch.from_numpy(sparse_mx.data)
        shape = torch.Size(sparse_mx.shape)
        return torch.sparse.FloatTensor(indices, values, shape)

    def get_matrix (self, graph, mode="train"):
        "find mps dataframe and update pos"
        
        mps = {}
        base_pos={'host':csr_matrix((self.host_size, self.host_size), 
                                     dtype=np.int8),
                  'vm':csr_matrix((self.vm_size, self.vm_size), dtype=np.int8),
                  'instance':csr_matrix((graph['instance'].x.shape[0], 
                                         graph['instance'].x.shape[0]), 
                                        dtype=np.int8)}
        
        for mpt in self.mpTypes:
            nodes = [node for node in mpt.split('_')[int(len(mpt.split('_'))/2):]]
            new_nei = []
            sourceName=nodes[-1]; destName=nodes[-1] 
            linkName=nodes[0]
            for graphEdge in graph.edge_types:
                if nodes[0] in graphEdge and nodes[1] in graphEdge:
                    source = graph[graphEdge].edge_index[0]
                    source = source.cpu().detach().numpy()
                    dest = graph[graphEdge].edge_index[1]
                    dest = dest.cpu().detach().numpy()
                    break
            
            unique_source = np.unique(source)
            for us in unique_source:
                indx = np.where(source == us)
                if len(indx[0]) > 1:
                    new_nei+=list(itertools.combinations(dest[indx[0]],2))
            
            if len(new_nei) > 0:
                new_nei=list(np.array(new_nei).T)
                new_source=list(new_nei[0])+list(new_nei[1])
                new_dest=list(new_nei[1])+list(new_nei[0])
                new_nei=np.unique([new_source,new_dest],axis=1)
                if mode=="train":
                    new_value = [1] * len(new_nei[0])
                    add_pos = csr_matrix((new_value,(new_nei[0],new_nei[1])),
                                         shape=base_pos[sourceName].shape)
                    base_pos[sourceName] += add_pos
                mps[(sourceName,linkName,destName)] = torch.tensor(new_nei).to(self.device) 
        #TODO change and add base pos
        #base_pos['vm'].data[np.where(base_pos['vm'].data <= 1)] = 0
        #base_pos['vm'].eliminate_zeros()
        base_pos['vm'].data[np.where(base_pos['vm'].data > 1)] = 1
        
        #base_pos['instance'].data[np.where(base_pos['instance'].data <= 1)] = 0
        #base_pos['instance'].eliminate_zeros()
        base_pos['instance'].data[np.where(base_pos['instance'].data > 1)] = 1
        return mps, (self.sparse_mx_to_torch_sparse_tensor(base_pos['host']).to(self.device), 
                     self.sparse_mx_to_torch_sparse_tensor(base_pos['vm']).to(self.device), 
                     self.sparse_mx_to_torch_sparse_tensor(base_pos['instance']).to(self.device))
    
    def get_host_pos (self):
        pass
    
    def get_vm_pos (self):
        pass
    
    def get_instance_pos (self):
        pass
    
    def train_step (self, graph):
        self.model.train()
        self.optimizer.zero_grad()
        mps, pos = self.get_matrix(graph)
        mp_outs, sc_outs = self.model (graph.to(self.device), mps, mode="train")
        #pos = self.get_pos()#TODO check
        loss = self.conLoss(mp_outs, sc_outs, pos)
        loss.backward()
        self.optimizer.step()
        return float(loss)
    
    def embedding_step (self, graph):
        mps, _ = self.get_matrix(graph, mode="embedding")
        return self.embedModel(graph.to(self.device), mps, mode="embedding")
    
    

