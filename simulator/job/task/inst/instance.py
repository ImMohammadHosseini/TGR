
"""

"""
import numpy as np

import torch

class Instance ():
    def __init__ (self, creationId, duration, cpuAvg, cpuMax, memAvg, memMax, 
                  diskMax, graphId = -1, vmId = -1) :
        
        self.creationId = creationId
        self.graphId = graphId
        self.task=None
        self.job=None
        self.duration = duration
        self.completDuration = 0
        self.cpuAvg = cpuAvg
        self.cpuMax = cpuMax
        self.memAvg = memAvg
        self.memMax = memMax
        self.diskMax = diskMax
        self.vmId = vmId
    
    def setGraphId (self, id):
        self.graphId = id
    
    def addCompleteDuration (self, completePart):
        self.completDuration += completePart
        if self.requiredExecTime() == 0:
            self.destroy()
            self.task.addCompleteInstance(self)
        else :
            self.updataNodeInfo()
        
    def getGraphId (self):
        creationIds = self.job.env.graphData['instance'].creationIds.detach().numpy()
        graphId = np.where(creationIds == self.creationId)
        assert len(graphId) == 1
        graphId = graphId[0][0]
        self.setGraphId(graphId)
        return graphId
        
    def requiredExecTime (self):
        return max(0, self.duration - self.completDuration)
    
    def getVmId (self):
        return self.vmId
    
    def getVm (self):
        return self.job.env.getVmById(self.vmId)
    
    def updataNodeInfo (self):
        graphId = self.getGraphId()
        newInfo = [self.duration, self.completDuration, self.cpuMax, 
                   self.memMax, self.diskMax]
        newInfo = torch.tensor(newInfo)
        instNodes = self.job.env.graphData['instance'].x
        instNodes[graphId] = newInfo
        self.job.env.graphData['instance'].x = instNodes
        
    def destroy (self):
        self.destroyAt = self.job.env.interval
        vm = self.getVm()
        vm.deleteInstance(self.creationId)
        self.vmId = -1
        self.destroyInstanceNode()
        
    def destroyInstanceNode (self):
        graphId = self.getGraphId()
        instNodes = self.job.env.graphData['instance'].x
        self.job.env.graphData['instance'].x = torch.cat([instNodes[0:graphId], 
                                                          instNodes[graphId+1:]])
        instIds = self.job.env.graphData['instance'].creationIds
        self.job.env.graphData['instance'].creationIds=torch.cat([instIds[0:graphId], 
                                                          instIds[graphId+1:]])
        
        pEdge0 = self.job.env.graphData['task', 'part_of', 'instance'].edge_index[0]
        pEdge0 = pEdge0.detach().numpy()
        pEdge1 = self.job.env.graphData['task', 'part_of', 'instance'].edge_index[1]
        pEdge1 = pEdge1.detach().numpy()
        indx = np.where(pEdge1 == graphId)
        pEdge0 = np.delete(pEdge0, indx)
        pEdge1 = np.delete(pEdge1, indx)
        pEdge1 = np.where(pEdge1<=graphId, pEdge1, pEdge1-1)
        self.job.env.graphData['task', 'part_of', 'instance'].edge_index = \
            torch.tensor([pEdge0, pEdge1]) 
        
        rEdge0 = self.job.env.graphData['instance', 'run_in', 'vm'].edge_index[0]
        rEdge0 = rEdge0.detach().numpy()
        rEdge1 = self.job.env.graphData['instance', 'run_in', 'vm'].edge_index[1]
        rEdge1 = rEdge1.detach().numpy()
        indx = np.where(rEdge0 == graphId)
        rEdge0 = np.delete(rEdge0, indx)
        rEdge1 = np.delete(rEdge1, indx)
        rEdge0 = np.where(rEdge0<=graphId, rEdge0, rEdge0-1)
        self.job.env.graphData['instance', 'run_in', 'vm'].edge_index = \
            torch.tensor([rEdge0, rEdge1]) 