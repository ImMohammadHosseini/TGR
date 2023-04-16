import torch
import torch.nn as nn
import numpy as np

from typing import Dict
from collections import defaultdict

from torch_geometric.nn import HeteroConv, GCNConv
from torch_geometric.nn.conv import MessagePassing

from torch_geometric.typing import Adj, EdgeType, NodeType


class CustomHeteroConv(HeteroConv):
    def __init__(self, convs: Dict[EdgeType, MessagePassing],):
        super().__init__(convs)
    def forward(
        self,
        x_dict: Dict[NodeType, torch.Tensor],
        edge_index_dict: Dict[EdgeType, Adj],
        *args_dict,
        **kwargs_dict,
    ) -> Dict[NodeType, torch.Tensor]:
        
        out_dict = defaultdict(list)
        for edge_type, edge_index in edge_index_dict.items():
            src, rel, dst = edge_type

            str_edge_type = '__'.join(edge_type)
            if str_edge_type not in self.convs:
                continue

            args = []
            for value_dict in args_dict:
                if edge_type in value_dict:
                    args.append(value_dict[edge_type])
                elif src == dst and src in value_dict:
                    args.append(value_dict[src])
                elif src in value_dict or dst in value_dict:
                    args.append(
                        (value_dict.get(src, None), value_dict.get(dst, None)))

            kwargs = {}
            for arg, value_dict in kwargs_dict.items():
                arg = arg[:-5]  # `{*}_dict`
                if edge_type in value_dict:
                    kwargs[arg] = value_dict[edge_type]
                elif src == dst and src in value_dict:
                    kwargs[arg] = value_dict[src]
                elif src in value_dict or dst in value_dict:
                    kwargs[arg] = (value_dict.get(src, None),
                                   value_dict.get(dst, None))

            conv = self.convs[str_edge_type]

            if src == dst:
                out = conv(x_dict[src], edge_index, *args, **kwargs)
            else:
                out = conv((x_dict[src], x_dict[dst]), edge_index, *args,
                           **kwargs)

            out_dict[dst].append(out)

        return out_dict


class Attention(nn.Module):
    def __init__(self, hidden_dim, attn_drop):
        super(Attention, self).__init__()
        self.fc = nn.Linear(hidden_dim, hidden_dim, bias=True)
        nn.init.xavier_normal_(self.fc.weight, gain=1.414)

        self.tanh = nn.Tanh()
        self.att = nn.Parameter(torch.empty(size=(1, hidden_dim)), requires_grad=True)
        nn.init.xavier_normal_(self.att.data, gain=1.414)

        self.softmax = nn.Softmax()
        if attn_drop:
            self.attn_drop = nn.Dropout(attn_drop)
        else:
            self.attn_drop = lambda x: x

    def forward(self, embeds):
        beta = []
        attn_curr = self.attn_drop(self.att)
        for embed in embeds:
            sp = self.tanh(self.fc(embed)).mean(dim=0)
            beta.append(attn_curr.matmul(sp.t()))
        beta = torch.cat(beta, dim=-1).view(-1)
        beta = self.softmax(beta)
        z_mp = 0
        for i in range(len(embeds)):
            z_mp += embeds[i]*beta[i]
        return z_mp

class Mp_encoder(nn.Module):
    def __init__ (self, P, hidden_dim, attn_drop):
        super(Mp_encoder, self).__init__()
        self.P = P
        
        self.gcn_layers = CustomHeteroConv({
            ('host', 'datacenter', 'host'):GCNConv(-1, hidden_dim, 
                                                   add_self_loops=False),
            ('vm', 'datacenter', 'vm'):GCNConv(-1, hidden_dim,
                                               add_self_loops=False),
            ('vm', 'host', 'vm'):GCNConv(-1,hidden_dim, add_self_loops=False),
            ('instance', 'task', 'instance'):GCNConv(-1, hidden_dim, 
                                                     add_self_loops=False),
            ('instance', 'vm', 'instance'):GCNConv(-1, hidden_dim, 
                                                   add_self_loops=False),
            })
        
        self.prelu = nn.PReLU()
        
        self.hostAttention = Attention(hidden_dim, attn_drop)
        self.vmAttention = Attention(hidden_dim, attn_drop)
        self.instanceAttention = Attention(hidden_dim, attn_drop)

    def forward (self, graph, mps):
        x_dict = graph.x_dict
        x_dict = self.gcn_layers(x_dict, mps)
        x_dict = {key:[self.prelu(x) for x in x_list] for key, x_list in x_dict.items()}
        hostEmbeds = x_dict['host']
        vmEmbeds = x_dict['vm']
        instanceEmbeds = x_dict['instance']
        #print(torch.isnan(instanceEmbeds).any())

        host_z_mp = self.hostAttention(hostEmbeds)
        vm_z_mp = self.vmAttention(vmEmbeds)
        instance_z_mp = self.instanceAttention(instanceEmbeds)

        return host_z_mp, vm_z_mp, instance_z_mp