#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Tue Jan 24 09:09:44 2023

@author: mohammad
"""
import sys
sys.path.append('scheduler/GraphBaGTI/')
import torch
import numpy as np 

from .Scheduler import Scheduler
from .GraphBaGTI.train import load_model
from .GraphBaGTI.src.graph_representation import GNNEncoder
from .GraphBaGTI.src.models import energy_latency_50
from .GraphBaGTI.src.utils import *
from .GraphBaGTI.src.opt import first_step_opt, second_step_opt


class GraphGOBIScheduler(Scheduler):
    def __init__ (self, data_type) :
        self.graphRepre = GNNEncoder ()
        self.model = eval(data_type+"()")
        self.data_type = data_type
        self.hosts = int(data_type.split('_')[-2])
        self.vms = int(data_type.split('_')[-1])
        
        
        
        #TODO check to add the rest
        self.model, _, _, _ = load_model(data_type, self.model, data_type)
        
        dtl = data_type.split('_')
        #_, _, self.max_container_ips = eval("load_"+'_'.join(dtl[:-1])+
        #                              "_data("+dtl[-1]+")")
        
    
    def selection (self) :
        return []
    
    def first_step_init (self, vm_emb, instance_emb, inst_schedueled) :
        vm_emb = vm_emb.detach().numpy()
        instance_emb = instance_emb.detach().numpy()
        schedueled_instances = schedueled_instances.detach().numpy()
        
        inits = []
        ins_ids_init = []; ins_id_init = []; ins_prep = []; oneHots = [];
        for i, inst_emb in enumerate(instance_emb):
            if i not in inst_schedueled:
                ins_id_init.append(i)
                ins_prep.append(inst_emb)
                oneHot = [0] * len(vm_emb)
                oneHot[np.random.randint(0,len(vm_emb))] = 1
                oneHots.append(oneHot)
                if len(ins_prep) == len(vm_emb):
                    two_emb = np.concatenate((vm_emb, ins_prep), axis=1)
                    inits.append(np.concatenate((two_emb, oneHots), axis=1))
                    ins_ids_init.append(ins_id_init)
                    ins_id_init=[]; ins_prep = []; oneHots = []
        
        return inits, ins_ids_init
    
    def first_step (self, first_sch = False) :
        if not first_sch: self.env.nodeUpdate()
        schedueled_instances = self.env.graphData['instance', 'run_in', 'vm'].edge_index[0]
        _, vm_emb, instance_emb = self.graphRepre(self.env.graph_data)
        init, instance_ids_init = self.first_step_init(vm_emb, 
                                                       instance_emb, 
                                                       schedueled_instances)
        init = torch.tensor(init, dtype=torch.float, requires_grad=True)
        result, iteration, fitness = first_step_opt(init, 
                                                    self.model, 
                                                    self.data_type)
        decision = []
        #TODO add suitable decision
        return decision
    
    def first_step_init (self) :
        pass
    def second_step (self) :
        pass
    
    def instancePlacement (self, containerIDs, first_sch = False) :
        d1 = self.first_step(first_sch)
        d2 = self.second_step()
        return d1, d2
    
    def vmPlacement (self):
        pass