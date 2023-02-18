
"""

"""
import numpy as np
import torch
from torch_geometric.data import HeteroData
from simulator.datacenter.Datacenter import Datacenter


class Simulator () :
    def __init__ (self, numDatacenters, numHosts, numVMs, totalPower, 
                  routerBw, scheduler, intervalTime, datacenterlistinit):
        
        self.totalpower = totalPower
        self.totalbw = routerBw
        self.datacenterlimit = numDatacenters
        self.hostLimit = numDatacenters * numHosts
        self.vmLimit = numDatacenters * numVMs     
        self.scheduler = scheduler
        self.scheduler.setEnvironment(self)
        self.intervaltime = intervalTime
        self.interval = 0
        
        #self.inactiveContainers = []
        self.stats = None
        
        self.datacenterlist = []
        self.jobList = []
        self.completedJobs = []
        
        self.graphData = HeteroData()
        self.graphInit()
        
        self.addDatacenterListInit(datacenterlistinit)
        
    def graphInit (self):
        self.graphData['datacenter'].x = torch.tensor([])
        self.graphData['host'].x = torch.tensor([])
        self.graphData['vm'].x = torch.tensor([])
        self.graphData['task'].x = torch.tensor([])
        self.graphData['task'].creationIds = torch.tensor([])
        self.graphData['instance'].x = torch.tensor([])
        self.graphData['instance'].creationIds = torch.tensor([])
        
        self.graphData['datacenter', 'dsho', 'host'] = torch.tensor([[],[]])
        self.graphData['datacenter', 'dsvm', 'vm'].edge_index = torch.tensor(
                                                                        [[],[]])
        self.graphData['vm', 'run_by', 'host'].edge_index = torch.tensor(
                                                                        [[], []])
        self.graphData['task', 'depend', 'task'].edge_index = torch.tensor(
                                                                        [[], []])
        self.graphData['task', 'part_of', 'instance'].edge_index = torch.tensor(
                                                                        [[], []])
        self.graphData['instance', 'run_in', 'vm'].edge_index = torch.tensor(
                                                                        [[], []])
        
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
    
    def destroyCompletedJobs (self):
        remainJobs = []; destroyed = []
        for job in self.jobList:
            job.destroyCompletedTasks()
            if len(job.taskList) != 0:
                remainJobs.append(job)
            else:
                job.destroy()
                destroyed.append(job)
        self.jobList = remainJobs
        self.completedJobs += destroyed
        return destroyed
    
    def addJobs (self, newJobsList):
        self.interval += 1
        destroyed = self.destroyCompletedJobs()
        self.addJobNodes(newJobsList)
        self.jobList += newJobsList
        return destroyed
        
    def addJobsInit (self, jobsInit):
        self.interval += 1
        self.addJobNodes(jobsInit)
        self.jobList = jobsInit
        
    def addJobNodes (self, jobsList):
        all_task_num = len(self.graphData['task'].x)
        all_inst_num = len(self.graphData['instance'].x)
        x_task = []; cid_task = [] 
        x_instance = []; cid_instance = []
        depend_source_node = []; depend_dest_node = [] 
        part_of_source_node = []; part_of_dest_node = []
        for job in jobsList:
            x_task_job, task_cid, x_inst_job,inst_cid, depend, part_of,\
                all_task_num, all_inst_num = \
                job.jobGraphInfo(all_task_num, all_inst_num)
                
            x_task += x_task_job; cid_task += task_cid
            x_instance += x_inst_job; cid_instance += inst_cid
            depend_source_node += depend[0] ; depend_dest_node += depend[1] 
            part_of_source_node += part_of[0]; part_of_dest_node += part_of[1]
            
        self.graphData['task'].x = torch.cat((self.graphData['task'].x, 
                                              torch.tensor(x_task)))
        self.graphData['task'].creationIds = torch.cat((self.graphData['task'].creationIds, 
                                                        torch.tensor(cid_task)))
        
        self.graphData['instance'].x = torch.cat((self.graphData['instance'].x, 
                                                  torch.tensor(x_instance)))
        self.graphData['instance'].creationIds = torch.cat((self.graphData['instance'].creationIds, 
                                                            torch.tensor(cid_instance)))
        
        self.graphData['task', 'depend', 'task'].edge_index = torch.cat((
            self.graphData['task', 'depend', 'task'].edge_index, 
            torch.tensor([depend_source_node, depend_dest_node])), dim = 1)
        self.graphData['task', 'part_of', 'instance'].edge_index = torch.cat((
            self.graphData['task', 'part_of', 'instance'].edge_index, 
            torch.tensor([part_of_source_node, part_of_dest_node])), dim = 1)

    def addRunInEdges (self, allocatedInstances):
        self.graphData['instance', 'run_in', 'vm'].edge_index = torch.cat((
            self.graphData['instance', 'run_in', 'vm'].edge_index,
            torch.tensor(allocatedInstances)), dim = 1)

    def addRunByEdges (self, migrations):
        source = self.graphData['vm', 'run_by', 'host'].edge_index[0]
        source = source.detach().numpy()
        dest = self.graphData['vm', 'run_by', 'host'].edge_index[1]
        dest = dest.detach().numpy()
        for vid in migrations[0]:
            indx = np.where(source == vid)
            source = np.delete(source, indx)
            dest = np.delete(dest, indx)
        
        all_source = list(source) + migrations[0]
        all_dest = list(dest) + migrations[1]
        
        self.graphData['vm', 'run_by', 'host'].edge_index=torch.tensor([all_source, 
                                                                        all_dest])
        
        return source, dest
        
    def getInstanceById (self, instanceId):
        for job in self.jobList:
            if instanceId in job.instancesId:
                for task in job.task_list:
                    if instanceId in task.instancesId:
                        for instance in task.instance_list:
                            if instance.getGraphId() == instanceId:
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
    
    def instanceAllocate (self, decision):
        #add a instance in vm based on the decision if its possible
        allocate_source = []; allocate_dest = []
        #routerBwToEach = self.totalbw / len(decision[0])
        for instanceId, vmId in zip(decision[0], decision[1]):
            instance = self.getInstanceById(instanceId)
            vm = self.getVmById(vmId)
            assert instance.vmId == -1
            numberAllocToVm = len(self.scheduler.getAllocateToVm(vmId,
                                                                 decision))
            #allocbw = min(vm.bwCap/ numberAllocToVm, routerBwToEach)
            #TODO check expected or main values
            if vm.possibleToAddInstance(instance):
                allocate_source.append(instanceId)
                allocate_dest.append(vmId)
                instance.vmId = vmId
                
        return [allocate_source, allocate_dest]
    
    def vmAllocateInit (self, decision):
        allocate_source = []; allocate_dest = []
        routerBwToEach = self.totalbw / len(decision[0])
        for vmId, hostId in zip(decision[0], decision[1]):
            vm = self.getVmById(vmId)
            host = self.getHostById(hostId)
            assert vm.HostId == -1
            numberAllocToHost = len(self.scheduler.getMigrationToHost(hostId,
                                                                      decision))
            allocbw = min(host.bwCap/ numberAllocToHost, routerBwToEach)
            #TODO Host possibleToAddVm
            if host.possibleToAddVm(vm):
                allocate_source.append(vmId)
                allocate_dest.append(hostId)
                vm.allocateAndExecute(host, allocbw)   
        
        _, _ = self.addRunByEdges([allocate_source, allocate_dest])
        
        return [allocate_source, allocate_dest]
                
    def simulationStep (self, decision) :
        routerBwToEach=self.totalbw/len(decision[0]) if len(decision[0]) > 0 \
            else self.totalbw
        migrationsSource = []; migrationDest = []    
        for vid, hid in zip(decision[0], decision[1]):
            vm = self.getVmByID(vid)
            currentHostID = vm.getHostID()
            currentHost = self.getHostByID(currentHostID)
            targetHost = self.getHostByID(hid)
            migrateFromNum = len(self.scheduler.getMigrationFromHost(currentHostID, 
                                                                     decision))
            migrateToNum = len(self.scheduler.getMigrationToHost(hid, decision))
            allocbw = min(targetHost.bwCap / migrateToNum, 
                          currentHost.bwCap / migrateFromNum, 
                          routerBwToEach)
            
            if targetHost.possibleToAddVm(vm):
                migrationsSource.append(vid)
                migrationDest.append(hid)
                vm.allocateAndExecute(targetHost, allocbw)
            
        noMigrationVmIds, _ = self.addRunByEdges([migrationsSource, migrationDest])
        for vmId in noMigrationVmIds:
            vm = self.getVmByID(vmId)
            vm.execute(0)
        
        return [migrationsSource, migrationDest]
        