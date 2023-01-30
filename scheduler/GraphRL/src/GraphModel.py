#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Mon Jan 30 11:06:22 2023

@author: mohammad
"""

import torch
import torch.nn as nn
import numpy as np

from torch_geometric.nn import GATConv, GCNConv
import torch.nn.functional as F


class GNNEncoder (nn.Module):
    def __init__ (self, 
                  emb_dim : int = 7):
        super(GNNEncoder, self).__init__()
        
    def forward (self, graph_data):
        pass