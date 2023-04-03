
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
       
        
       
        
    
    
    
    '''
    def __init__ (self, 
                  hidden_channels : int = 8,
                  num_layers : int = 2,
                  emb_dim : int = 5):
        super(GNNEncoder, self).__init__()
        
        self.convs = torch.nn.ModuleList()
        self.s=SAGEConv((-1,-1), hidden_channels, add_self_loops=False)
        for _ in range(num_layers):
            conv = HeteroConv({
                ('datacenter', 'dsho', 'host'): GraphConv((-1,-1), hidden_channels,
                                                        add_self_loops=False),
                ('datacenter', 'dsvm', 'vm'): GraphConv((-1,-1), hidden_channels,
                                                      add_self_loops=False),
                ('host', 'hods', 'datacenter'): GraphConv((-1,-1), hidden_channels,
                                                        add_self_loops=False),
                ('vm', 'vmds', 'datacenter'): GraphConv((-1,-1), hidden_channels,
                                                      add_self_loops=False),
                ('task', 'depend', 'task'): GCNConv(-1, hidden_channels,
                                                    add_self_loops=False),
                ('task', 'part_of', 'instance'): GATv2Conv((-1,-1), hidden_channels,
                                                         add_self_loops=False),
                ('instance', 'run_in', 'vm'): GraphConv((-1,-1), hidden_channels,
                                                      add_self_loops=False),
                ('vm', 'run_by', 'host'): GATv2Conv((-1,-1), hidden_channels,
                                                  add_self_loops=False),
            }, aggr='sum')
            self.convs.append(conv)
            
        self.vm_lin = Linear(hidden_channels, emb_dim)
        self.instance_lin = Linear(hidden_channels, emb_dim)
        self.host_lin = Linear(hidden_channels, emb_dim)
    
                
    def forward (self, graph_data):
        x_dict = graph_data.x_dict
        edge_index_dict = graph_data.edge_index_dict
        
        for conv in self.convs:
            x_dict = conv(x_dict, edge_index_dict)
            x_dict = {key: x.relu() for key, x in x_dict.items()}

        return self.host_lin(x_dict['host']), \
            self.vm_lin(x_dict['vm']), \
            self.instance_lin(x_dict['instance'])'''
    
    