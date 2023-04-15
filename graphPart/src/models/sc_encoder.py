import torch
import torch.nn as nn
import numpy as np

from torch_geometric.nn import HeteroConv, GATConv


class inter_att(nn.Module):
    def __init__(self, hidden_dim, attn_drop):
        super(inter_att, self).__init__()
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
        z_mc = 0
        for i in range(len(embeds)):
            z_mc += embeds[i] * beta[i]
        return z_mc
    
class Sc_encoder(nn.Module):
    #TODO check sample_rate
    def __init__(self, hidden_dim, attn_drop, num_layers=2):
        super(Sc_encoder, self).__init__()
        
        self.convs = torch.nn.ModuleList()
        for _ in range(num_layers):
            conv = HeteroConv({
                ('datacenter', 'dsho', 'host'): GATConv((-1,-1), hidden_dim,
                                                        dropout=attn_drop,
                                                        add_self_loops=False),
                ('datacenter', 'dsvm', 'vm'): GATConv((-1,-1), hidden_dim,
                                                      dropout=attn_drop,
                                                      add_self_loops=False),
                ('host', 'hods', 'datacenter'): GATConv((-1,-1), hidden_dim,
                                                        dropout=attn_drop,
                                                        add_self_loops=False),
                ('vm', 'vmds', 'datacenter'): GATConv((-1,-1), hidden_dim,
                                                      dropout=attn_drop,
                                                      add_self_loops=False),
                ('task', 'depend', 'task'): GATConv((-1,-1), hidden_dim,
                                                    dropout=attn_drop,
                                                    add_self_loops=False),
                ('task', 'part_of', 'instance'): GATConv((-1,-1), hidden_dim,
                                                         dropout=attn_drop,
                                                         add_self_loops=False),
                ('instance', 'run_in', 'vm'): GATConv((-1,-1), hidden_dim,
                                                      dropout=attn_drop,
                                                      add_self_loops=False),
                ('vm', 'run_by', 'host'): GATConv((-1,-1), hidden_dim,
                                                  dropout=attn_drop,
                                                  add_self_loops=False),
            }, aggr='sum')
            self.convs.append(conv)
        
        self.host_inter = inter_att(hidden_dim, attn_drop)
        self.vm_inter = inter_att(hidden_dim, attn_drop)
        self.instance_inter = inter_att(hidden_dim, attn_drop)

    def forward (self, graph):
        #TODO SAMPLE
        x_dict = graph.x_dict
        edge_index_dict = graph.edge_index_dict
        
        for conv in self.convs:
            x_dict = conv(x_dict, edge_index_dict)
            x_dict = {key: x.relu() for key, x in x_dict.items()}
        
        hostNode = x_dict['host']
        vmNode = x_dict['vm']
        instanceNode = x_dict['instance']
        
        host_z_mc = self.host_inter([hostNode])
        vm_z_mc = self.vm_inter([vmNode])
        instance_z_mc = self.instance_inter([instanceNode])

        return host_z_mc, vm_z_mc, instance_z_mc

