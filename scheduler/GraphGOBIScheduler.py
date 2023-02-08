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
        #TODO check inflects between two projects
        self.model = eval(data_type+"()")
        self.model, _, _, _ = load_model(data_type, self.model, data_type)
        self.data_type = data_type
        self.hosts = int(data_type.split('_')[-1])
        dtl = data_type.split('_')
        #_, _, self.max_container_ips = eval("load_"+'_'.join(dtl[:-1])+
        #                              "_data("+dtl[-1]+")")
        self.repre_model = GNNEncoder ()
        
    def suitable_init (self, emb_host_x, emb_container_x) :
        pass
    
    def run_GraphGOBI (self) :
        pass
    
    def selection (self) :
        pass
    
    def placement (self, containerIDs) :
        pass