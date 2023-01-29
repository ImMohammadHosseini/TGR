#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Sun Jan 29 09:34:32 2023

@author: mohammad
"""

class Job () :
    def __init__ (self, job_id, task_list) :
        self.job_id = job_id
        self.task_list = task_list
        
        for task in self.task_list:
            task.set_job(self)
    
    def jobGraphInfo (self, past_num):
        past_task = past_num
        x_task = [None] * len(self.task_list)
        source = []
        dest = []
        sorted_task_list = [None] * len(self.task_list)
        for task in self.task_list:
            if task.task_name[:4] == "task" or task.task_name == 'MergeTask':
                x_task[past_task - past_num] = [task.plan_cpu,
                                                task.plan_mem,
                                                len(task.instance_list)]
                sorted_task_list[past_task - past_num] = task
                past_task += 1
            elif '_' not in task.task_name:
                x_task[int(task.task_name[1:])] = [task.plan_cpu,
                                                   task.plan_mem,
                                                   len(task.instance_list)]
                sorted_task_list[int(task.task_name[1:])] = task
                past_task += 1
            else:
                x_task[int(edges[0][1:])] = [task.plan_cpu,
                                             task.plan_mem,
                                             len(task.instance_list)]
                edges = task.task_name.split('_')
                sorted_task_list[int(edges[0][1:])] = task
                dest.append(past_num+int(edges[0][1:]))
                for i in edges[1:]:
                    source.append(past_num+int(i))
                past_task += 1
                
                
                
                for i in range(1, len(task.task_name), 2):
                    
        
        x_task
        x_instance
        part_of_edge_index
        depend_edge_index
        