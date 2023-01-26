#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Wed Jan 25 15:48:06 2023

@author: mohammad
"""
from simulator.datacenter import AzureFog

from simulator.datacenter.host.Disk import Disk
from simulator.datacenter.host.Bandwidth import Bandwidth
from simulator.datacenter.host.RAM import RAM
from simulator.datacenter.host.Host import Host


class Datacenter (AzureFog) :
    def __init__ (self, ID, num_hosts, num_VMs, Environment) :
        super(num_hosts, num_VMs)
        self.id = ID
        self.env = Environment

        
        self.hostList = []
        self.VMList = []
        
        self.generateHosts()
        self.generateVMs()
        
        
    def generateHosts(self):
        self.hostList = []
        types = ['B2s', 'B2s', 'B2s', 'B2s', 'B4ms', 'B4ms', 'B4ms', 'B4ms', \
           'B8ms', 'B8ms'] * 1
        for i in range(self.num_hosts):
            typeID = types[i]
            IPS = self.types[typeID]['IPS']
            Ram = RAM(self.types[typeID]['RAMSize'], self.types[typeID]['RAMRead']*5, self.types[typeID]['RAMWrite']*5)
            Disk_ = Disk(self.types[typeID]['DiskSize'], self.types[typeID]['DiskRead']*5, self.types[typeID]['DiskWrite']*10)
            Bw = Bandwidth(self.types[typeID]['BwUp'], self.types[typeID]['BwDown'])
            Power = eval(self.types[typeID]['Power']+'()')
            Latency = 0.003 if i < self.edge_hosts else 0.076
            host = Host(len(self.hostlist), IPS, Ram, Disk, Bw, Latency, 
                        Power, self)
            self.hostList.append(host)
    
    def generateVMs(self):
        self.VMs = []
        types = ['Extra-small', 'Extra-small', 'Extra-small', 
                 'small','small','small',
                 'medium','medium','medium',
                 'large','large','large'] * 1
        for i in range(self.num_VMs):
            pass
        #TODO the same method with Azurefog generate host

        