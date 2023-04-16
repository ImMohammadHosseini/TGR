
"""

"""
import torch
import torch.nn as nn

import torch.nn.functional as F

from .mp_encoder import Mp_encoder
from .sc_encoder import Sc_encoder

class GNNEncoder (nn.Module):
    def __init__ (self, in_features:list, hidden_dim:int, nodes_type, 
                  projection_drop, attn_drop, P):    
        super(GNNEncoder, self).__init__() 
        self.name = 'HeCo'
        self.nodes_type = nodes_type
     
        self.node_project = nn.ModuleList()
        for in_feat in in_features:
            self.node_project.append(nn.Linear(in_feat, hidden_dim, bias=True))
            
        for projection in self.node_project:
            nn.init.xavier_normal_(projection.weight, gain=1.414)
        
        if projection_drop > 0:
            self.feat_drop = nn.Dropout(projection_drop)
        else:
            self.feat_drop = lambda x: x
         
        self.mp = Mp_encoder(P, hidden_dim, attn_drop)
        self.sc = Sc_encoder(hidden_dim, attn_drop)
       
        self.contrastiveProj = nn.Sequential(
            nn.Linear(hidden_dim, hidden_dim),
            nn.ELU(),
            nn.Linear(hidden_dim, hidden_dim)
        )
        

    def forward (self, graph, mps, mode="embedding"):
        
        for i, ntype in enumerate(self.nodes_type):
            graph[ntype].x = F.elu(self.feat_drop(
                self.node_project[i](torch.nan_to_num(graph[ntype].x))))
        if mode == "train":
            z_mp = self.mp(graph, mps)
            z_sc = self.sc(graph)
        
            z_proj_mp = [self.contrastiveProj(zmp) for zmp in z_mp]
            z_proj_sc = [self.contrastiveProj(zsc) for zsc in z_sc]
            
            return z_proj_mp, z_proj_sc
        else: 
            host_z_mp, vm_z_mp, instance_z_mp = self.mp(graph, mps)
            return host_z_mp.detach(), vm_z_mp.detach(), instance_z_mp.detach() 
