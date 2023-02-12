#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Wed Feb  8 09:47:08 2023

@author: mohammad
"""

class VM ():
    def __init__(self, 
                 core_lim, 
                 ram_lim, 
                 disk_lim, 
                 datacenter, 
                 hostId = -1):
        self.ID = -1
        self.core_lim = core_lim
        self.ram_lim = ram_lim
        self.disk_lim = disk_lim
        
        self.datacenter = datacenter
        self.hostId = hostId
        
        self.totalExecTime = 0
        self.totalMigrationTime = 0
        self.active = True
        
    def 
    