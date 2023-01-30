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
        if self.task_name[:4] == "task" or self.task_name == 'MergeTask' or \
            '_' not in self.task_name:
            self.status = Status.READY
        else: self.status = Status.WAITING
        
        for instance in self.instance_list:
            instance.task = self
        
        pass
    
    def set_status (self) :
        pass
        
    def set_job (self, job):
        self.job = job
        for instance in self.instance_list:
            instance.job = job
            
    def instanceGraph (self, past_task_num, past_inst_num) :
        past_inst = past_inst_num
        x_inst = []
        source = []
        dest = []
        for instance in self.instance_list:
            x_inst.append([instance.seq_no, instance.total_seq_no,
                          instance.cpu_max, instance.mem_max])
            
            source.append(past_task_num)
            dest.append(past_inst)
            past_inst += 1
        return x_inst, [source, dest], past_inst
        
        
        
        x_instance 
        part_of_edge_index
        
        
        
        
        
        
        
        
        