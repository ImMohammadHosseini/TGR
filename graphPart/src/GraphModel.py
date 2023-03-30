#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Mon Jan 30 11:06:22 2023

@author: mohammad
"""

import torch
import torch.nn as nn
import numpy as np

from torch_geometric.nn import HeteroConv, GraphConv, SAGEConv, GATv2Conv, GCNConv, Linear
import torch.nn.functional as F

#TODO ADD unsupervized graph repre

class GNNEncoder (nn.Module):
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
            self.instance_lin(x_dict['instance'])
    
    