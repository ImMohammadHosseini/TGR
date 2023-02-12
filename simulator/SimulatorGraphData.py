#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Tue Jan 24 09:36:20 2023

@author: mohammad
"""
import torch
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
        self.joblist = []
        
        
        self.graphData = HeteroData()
        
        self.addDatacenterListInit(datacenterlistinit)
        
    
    def addDatacenterListInit (self, datacenterlist) :
        assert len(datacenterlist) == self.datacenterlimit
        for numHosts, numVMs in datacenterlist:
            self.addDatacenterInit(numHosts, numVMs)
            
        self.dsNodeInit()
    
    def addDatacenterInit (self, num_hosts, num_VMs) :
        assert len(self.datacenterlist) < self.datacenterlimit
        datacenter = Datacenter(len(self.datacenterlist), num_hosts, num_VMs, self)
        self.datacenterlist.append(datacenter)
        
    def dsNodeInit (self):
        all_host_num = 0; all_vm_num = 0
        x_datacenter = []; x_host = []; x_vm = []
        dsho_source_node = []; dsho_dest_node = []; dsvm_source_node = []
        dsvm_dest_node = []
        for ds in self.datacenterlist:
            x_ds, x_host_ds, x_vm_ds, dsho, dsvm, all_host_num, all_vm_num = \
                ds.dsGraphInfo(all_host_num, all_vm_num)
                
            x_datacenter += x_ds; x_host += x_host_ds; x_vm += x_vm_ds
            dsho_source_node += dsho[0]; dsho_dest_node += dsho[1]
            dsvm_source_node += dsvm[0]; dsvm_dest_node += dsvm[1]
            
        self.graphData['datacenter'].x = torch.tensor(x_datacenter)
        self.graphData['host'].x = torch.tensor(x_host)
        self.graphData['vm'].x = torch.tensor(x_vm)
        self.graphData['datacenter', 'dsho', 'host'].edge_index = torch.tensor(
                                            [dsho_source_node, dsho_dest_node])
        self.graphData['datacenter', 'dsvm', 'vm'].edge_index = torch.tensor(
                                            [dsvm_source_node, dsvm_dest_node])
        self.graphData['vm', 'run_by', 'host'].edge_index = torch.tensor([[], []])

    def nodeUpdate (self) :
        pass
    
    def addJobsInit (self, jobsInit):
        self.interval += 1
        self.joblist = jobsInit
        self.jobsNodeInit()
        
    def jobsNodeInit (self):
        all_task_num = 0; all_inst_num = 0
        x_task = []; x_instance = []
        depend_source_node = []; depend_dest_node = []; part_of_source_node = []
        part_of_dest_node = []
        for job in self.joblist:
            x_task_job, x_inst_job, depend, part_of, all_task_num, all_inst_num = \
                job.jobGraphInfo(all_task_num, all_inst_num)
                
            x_task += x_task_job; x_instance += x_inst_job
            depend_source_node += depend[0] ; depend_dest_node += depend[1] 
            part_of_source_node += part_of[0]; part_of_dest_node += part_of[1]
            
        self.graphData['task'].x = torch.tensor(x_task)
        self.graphData['instance'].x = torch.tensor(x_instance)
        self.graphData['task', 'depend', 'task'].edge_index = torch.tensor(
            [depend_source_node, depend_dest_node])
        self.graphData['task', 'part_of', 'instance'].edge_index = torch.tensor(
            [part_of_source_node, part_of_dest_node])
        self.graphData['instance', 'run_in', 'vm'].edge_index = torch.tensor([[], []])


    def addNewJodsNode (self) :
        pass
        
    def getVMsOfHost (self, dsId, hostId):
        vms = []
        #TODO
        return vms
    
    def getInstanceById (self, instanceId):
        for job in self.joblist:
            if instanceId in job.instancesId:
                for task in job.task_list:
                    if instanceId in task.instancesId:
                        for instance in task.instance_list:
                            if instance.id == instanceId:
                                return instance
                            
    def getVmById (self, vmId):
        for datacenter in self.datacenterlist:
            if vmId in datacenter.vmsId:
                for vm in datacenter.VMList:
                    if vm.id == vmId:
                        return vm
                    
    def getHostById (self, hostId):
        for datacenter in self.datacenterlist:
            if hostId in datacenter.hostsId:
                for host in datacenter.hostList:
                    if host.id == hostId:
                        return host
    
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
    
    
    def simulationStep (self) :
        