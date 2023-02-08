#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Wed Feb  8 09:47:08 2023

@author: mohammad
"""

class VM ():
    def __init__(self, 
                 ID, 
                 core_lim, 
                 ram_lim, 
                 disk_lim, 
                 datacenter, 
                 hostId = -1):
        self.ID = ID
        self.core_lim = core_lim
        self.ram_lim = ram_lim
        self.disk_lim = disk_lim
        
        self.datacenter = datacenter
        self.hostId = hostId
        
        