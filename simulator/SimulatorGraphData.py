#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Tue Jan 24 09:36:20 2023

@author: mohammad
"""

from torch_geometric.data import HeteroData
from simulator.datacenter.Datacenter import Datacenter


class Simulator () :
    def __init__ (self,
                  num_datacenters,
                  num_hosts, 
                  num_VMs,
                  TotalPower, 
                  RouterBw, 
                  Scheduler,  
                  IntervalTime, 
                  datacenterlistinit):
        
        self.totalpower = TotalPower
        self.totalbw = RouterBw
        self.datacenterlimit = num_datacenters
        self.hostlimit = num_datacenters * num_hosts
        self.vmlimit = num_datacenters * num_VMs     
        self.scheduler = Scheduler
        self.scheduler.setEnvironment(self)
        self.intervaltime = IntervalTime
        self.interval = 0
        
        self.inactiveContainers = []#TODO
        self.stats = None
        
        self.datacenterlist = []
        self.tasklist = [] #or joblist
        
        
        self.graph_data = HeteroData()
        
        self.addDatacenterListInit(datacenterlistinit)
        
    
    def addDatacenterListInit (self, datacenterlist) :
        assert len(datacenterlist) == self.datacenterlimit
        for numHosts, numVMs in datacenterlist:
            self.addDatacenterInit(numHosts, numVMs)
    
    def addDatacenterInit (self, num_hosts, num_VMs) :
        assert len(self.datacenterlist) < self.datacenterlimit
        datacenter = Datacenter(len(self.datacenterlist), num_hosts, num_VMs, self)
        self.datacenterlist.append(datacenter)
    
    def updateGraph (self) :
        pass 
    #TODO Update nodes and edges
    
    def updateDatacentersNode (self) :
        pass
    
    def updateHostsNode (self) :
        pass
    
    def updateVMsNode (self) :
        pass
    
    def updateJobsNode (self) :
        pass
    
    