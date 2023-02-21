
"""

"""
import torch
import numpy as np
from enum import Enum

class Status(Enum):
    READY = 1
    WAITING = 2
    RUNNING = 3
    TERMINATER = 4
    
    
class Task () :
    def __init__ (self, taskName, creationId, planCpu, planMem, planDisk,
                  instanceList, graphId = -1) :
        
        self.creationId = creationId
        self.graphId = graphId
        self.job = None
        self.taskName = taskName
        self.planCpu = planCpu
        self.planMem = planMem
        self.planDisk = planDisk
        self.instanceList = instanceList
        self.completedInstances = []
        self.instance_num = len(instanceList)
        self.destroyAt = -1
        
        '''if self.task_name[:4] == "task" or self.task_name == 'MergeTask' or \
            '_' not in self.task_name:
            self.status = Status.READY
        else: self.status = Status.WAITING'''
        self.status = Status.READY
        
        for instance in self.instanceList:
            instance.task = self
        
        self.instancesId = []
        
    def setGraphId (self, id):
        self.graphId = id
        
    def getGraphId (self):
        creationIds = self.job.env.graphData['task'].creationIds.detach().numpy()
        graphId = np.where(creationIds == self.creationId)
        assert len(graphId) == 1
        graphId = graphId[0][0]
        self.setGraphId(graphId)
        return graphId
    
    def destroyCompletedInstances (self):
        remainInstances = []
        for instance in self.instanceList:
            if instance.requiredExecTime() > 0:
                remainInstances.append(instance)
            else: 
                instance.destroy()
                self.completedInstances.append(instance)
        self.instanceList = remainInstances
    
    
    def set_status (self) :
        pass
        
    def set_job (self, job):
        self.job = job
        for instance in self.instanceList:
            instance.job = job
            
    def instanceGraph (self, past_task_num, past_inst_num) :
        past_inst = past_inst_num
        x_inst = []; creationId_instance = []
        source = []; dest = []
        for instance in self.instanceList:
            instance.setGraphId(past_inst)
            self.instancesId.append(instance.graphId)
            self.job.instancesId.append(instance.graphId)
            x_inst.append([instance.duration, instance.completDu,
                          instance.cpuMax, instance.memMax, instance.diskMax])
            creationId_instance.append(instance.creationId)
            
            source.append(past_task_num)
            dest.append(past_inst)
            past_inst += 1
        return x_inst, creationId_instance, [source, dest], past_inst
 
    def destroy (self):
        self.destroyAt = self.job.env.interval
        self.destroyTaskNode()
    
    def destroyTaskNode (self):
        graphId = self.getGraphId()
        tasksNodes = self.job.env.graphData['task'].x
        self.job.env.graphData['task'].x = torch.cat([tasksNodes[0:graphId], 
                                                      tasksNodes[graphId+1:]])
        taskIds = self.job.env.graphData['task'].creationIds
        self.job.env.graphData['task'].creationIds=torch.cat([taskIds[0:graphId], 
                                                          taskIds[graphId+1:]])
        
        dEdge0 = self.job.env.graphData['task', 'depend', 'task'].edge_index[0]
        dEdge0 = dEdge0.detach().numpy()
        dEdge1 = self.job.env.graphData['task', 'depend', 'task'].edge_index[1]
        dEdge1 = dEdge1.detach().numpy()
        indx = np.where(dEdge0 == graphId)
        dEdge0 = np.delete(dEdge0, indx)
        dEdge1 = np.delete(dEdge1, indx)
        dEdge0 = np.where(dEdge0<=graphId, dEdge0, dEdge0-1)

        indx = np.where(dEdge1 == graphId)
        dEdge0 = np.delete(dEdge0, indx)
        dEdge1 = np.delete(dEdge1, indx)
        dEdge1 = np.where(dEdge1<=graphId, dEdge1, dEdge1-1)
        self.job.env.graphData['task', 'depend', 'task'].edge_index = \
            torch.tensor([dEdge0, dEdge1]) 
        
        
        