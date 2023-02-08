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
from .GraphBaGTI.src.opt import opt


class GraphGOBIScheduler(Scheduler):
    def __init__ (self, data_type) :
        self.graphRepre = GNNEncoder ()

        #TODO check inflects between two projects
        self.model = eval(data_type+"()")
        self.model, _, _, _ = load_model(data_type, self.model, data_type)
        self.data_type = data_type
        self.hosts = int(data_type.split('_')[-1])
        dtl = data_type.split('_')
        #_, _, self.max_container_ips = eval("load_"+'_'.join(dtl[:-1])+
        #                              "_data("+dtl[-1]+")")
        
    def suitable_init (self, emb_host_x, emb_container_x) :
        pass
    
    def run_GraphGOBI (self) :
        pass
    
    def selection (self) :
        return []
    
    def first_step_init (self, vm_emb, instance_emb) :
        vm_emb = vm_emb.detach().numpy()
        instance_emb = instance_emb.detach().numpy()
        
        suitabel_instance_init = np.zeros(vm_emb.shape)
        graph_i_id = self.env.graph_data['instance'].id.numpy().reshape(-1)
        
        
        for i, c in enumerate(self.env.containerlist):#TODO instancelist  id changable
            if c:
                idx = np.where(graph_c_id == c.id)[0][0]
                suitabel_container_init[i] = emb_container_x[idx]
        
        return np.concatenate((emb_host_x, suitabel_container_init), axis=1)
    
    def first_step (self, first_sch = False) :
        if not first_sch: self.env.nodeUpdate()
        _, vm_emb, instance_emb = self.graphRepre(self.env.graph_data)
        
    
    def second_step (self) :
        pass
    
    def placement (self, containerIDs, first_sch = False) :
        self.first_step(first_sch)
        self.second_step()
        #return d1, d2