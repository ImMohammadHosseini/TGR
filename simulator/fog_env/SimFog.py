#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Sun Jan 22 09:23:32 2023

@author: mohammad
"""

from .simulator.data.DataPrepration import PrepareData
from os import path

class SimFog () :
    def __init__ (self, num_hosts : int) :
        self.num_hosts = num_hosts
        self.machines_dataset_path = 'simulator/data/datasets/machine_meta/'
        self.containers_dataset_path = 'simulator/data/datasets/container_meta/'
        if not path.exists(self.machines_dataset_path):
            PrepareData()
            
    def generateMachines (self) :
        pass
    
    def generateContainers (self) :
        pass