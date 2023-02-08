#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Wed Jan 25 15:48:06 2023

@author: mohammad
"""
from simulator.datacenter import AzureFog

#from simulator.datacenter.host.Disk import Disk
#from simulator.datacenter.host.Bandwidth import Bandwidth
#from simulator.datacenter.host.RAM import RAM
from simulator.datacenter.host.Host import Host
from simulator.datacenter.vm.vm import VM 

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
        types = ['small', 'small', 'small', 'small', \
                 'medium', 'medium', 'medium', 'medium', \
                 'large', 'large'] * 1
        for i in range(self.num_hosts):
            typeID = types[i]
            core = self.types[typeID]['core']
            mem_size = self.types[typeID]['mem_size']
            disk = self.types[typeID]['DiskSize']
            Bw = self.types[typeID]['Bw']
            Power = eval(self.types[typeID]['Power']+'()')
            Latency = 0.003 if i < self.edge_hosts else 0.076
            host = Host(len(self.hostlist), core, mem_size, disk, Bw, Latency, 
                        Power, self)
            self.hostList.append(host)
    
    def generateVMs(self):
        self.VMList = []
        types = ['Extra-small', 'Extra-small', 'Extra-small', 
                 'small','small','small',
                 'medium','medium','medium',
                 'large','large','large'] * 1
        for i in range(self.num_VMs):
            typeID = types[i]
            core_lim = self.types[typeID]['core']
            ram_lim = self.types[typeID]['RAM']
            disk_lim = self.types[typeID]['Disk']
            vm = VM (len(self.VMList), core_lim, ram_lim, disk_lim, self)
            
            self.VMList.append(vm)
            
            
    def dsGraphInfo (self, past_host_num, past_vm_num):
        past_hosts = past_host_num
        past_vms = past_vm_num
        x_ds = [self.num_hosts, self.num_VMs]
        x_host = []
        x_vm = []
        dsho_source = []
        dsho_dest = []
        dsvm_source = []
        dsvm_dest = []
        for host in self.hostList:
            x_host.append([host.get])
            dsho_source.append(self.id)
            dsho_dest.append(past_hosts)
            past_hosts += 1
        for vm in self.VMList:
            x_vm.append([vm.get])
            dsvm_source.append(self.id)
            dsvm_dest.append(past_vms)
            past_vms += 1
            
        return x_ds, x_host, x_vm, [dsho_source, dsho_dest], \
            [dsvm_source, dsvm_dest], past_hosts, past_vms


x_ds, x_host, x_vm, dsho, dsvm        