
"""

"""

import torch.nn as nn
from sys import argv
from .constants import Coeff_Energy, Coeff_Latency

class energy_latency_30_60_first (nn.Module):
    def __init__(self,
                 node_dim : int = 5):
        super(energy_latency_30_60_first, self).__init__()
        self.name = "energy_latency_30_60_first"
        self.find = nn.Sequential(
            nn.Linear(60*(60 + 2*node_dim), 512),
            nn.Softplus(),
            nn.Linear(512, 256),
            nn.Softplus(),
            nn.Linear(256, 128), 
            nn.Tanhshrink(),
            nn.Linear(128, 2),
            nn.Sigmoid())
        
    def forward (self, init ):
        xlayers = 0
        for x in init:
            x = x.flatten()
            x = self.find(x)
            if not('train' in argv[0] and 'train' in argv[2]):
                x = Coeff_Energy*x[0] + Coeff_Latency*x[1]
            xlayers += x
        return xlayers
    

class energy_latency_30_60_second (nn.Module):
    def __init__(self,
                 node_dim : int = 5):
        super(energy_latency_30_60_second, self).__init__()
        self.name = "energy_latency_30_60_second"
        self.find = nn.Sequential(
            nn.Linear(30*(30 + 2*node_dim), 512),
            nn.Softplus(),
            nn.Linear(512, 256),
            nn.Softplus(),
            nn.Linear(256, 128), 
            nn.Tanhshrink(),
            nn.Linear(128, 2),
            nn.Sigmoid())
        
    def forward (self, init ):
        xlayers = 0
        for x in init:
            x = x.flatten()
            x = self.find(x)
            if not('train' in argv[0] and 'train' in argv[2]):
                x = Coeff_Energy*x[0] + Coeff_Latency*x[1]
            xlayers += x
        return xlayers