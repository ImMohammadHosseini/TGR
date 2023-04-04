
"""

"""

import torch
import torch.nn as nn
import numpy as np

from torch_geometric.nn import HeteroConv, GraphConv, SAGEConv, GATv2Conv, GCNConv, Linear
import torch.nn.functional as F

from .mp_encoder import Mp_encoder
from .sc_encoder import Sc_encoder

class GNNEncoder (nn.Module):
    def __init__ (self, hidden_dim, nodes_type, projection_drop, attn_drop, P):    
        super(GNNEncoder, self).__init__() 
        self.name = 'HeCo'
        self.nodes_type = nodes_type
     
        self.node_project = nn.ModuleList([nn.LazyLinear(hidden_dim, bias=True)
                                      for _ in range(len(self.nodes_type)-1)])
    
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
    def forward (self, graph, mps, device="cpu", mode="test"):
        for i, ntype in enumerate(self.nodes_type):
            graph[ntype].x = F.elu(self.feat_drop(
                self.node_project[i](graph[ntype].x)))
        
        z_mp = self.mp(graph.x_dict.detach(), mps)
        z_sc = self.sc(graph)
        
        if mode == "train":
            z_proj_mp = [self.contrastiveProj(zmp) for zmp in z_mp]
            z_proj_sc = [self.contrastiveProj(zsc) for zsc in z_sc]
            
            return z_proj_mp, z_proj_sc
        else: return z_mp.detach() 
