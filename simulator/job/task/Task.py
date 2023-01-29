#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Sun Jan 29 09:30:17 2023

@author: mohammad
"""
from enum import Enum
 
class Status(Enum):
    READY = 1
    WAITING = 2
    RUNNING = 3
    TERMINATER = 4
    
    
class Task () :
    def __init__ (self, task_name : str,
                  plan_cpu,
                  plan_mem,
                  instance_list) :
        self.job = None
        self.task_name = task_name
        self.plan_cpu = plan_cpu
        self.plan_mem = plan_mem
        self.instance_list = instance_list
        self.status = None
        
        for instance in self.instance_list:
            instance.task = self
        
        pass
    
    def set_job (self, job):
        self.job = job
        for instance in self.instance_list:
            instance.job = job
            
    def instanceGraph (self) :
        
        
        
        
        
        
        
        
        
        
        