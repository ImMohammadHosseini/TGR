
"""

"""
from enum import Enum
 
class Status(Enum):
    READY = 1
    WAITING = 2
    RUNNING = 3
    TERMINATER = 4
    
    
class Task () :
    def __init__ (self, taskName : str,
                  planCpu,
                  planMem,
                  planDisk,
                  instanceList,
                  graphId = -1) :
        self.id = graphId
        self.job = None
        self.taskName = taskName
        self.planCpu = planCpu
        self.planMem = planMem
        self.planDisk = planDisk
        self.instanceList = instanceList
        self.completedInstances = []
        self.instance_num = len(instanceList)
        self.destroyAt = -1
        
        if self.task_name[:4] == "task" or self.task_name == 'MergeTask' or \
            '_' not in self.task_name:
            self.status = Status.READY
        else: self.status = Status.WAITING
        
        for instance in self.instance_list:
            instance.task = self
        
        self.instancesId = []
    
    def destroyCompletedInstances (self):
        remainInstances = []
        for instance in self.instanceList:
            if instance.requiredExecTime() > 0:
                remainInstances.append(instance)
            else: 
                instance.destroy()
                self.completedInstances.append(instance)
        self.instanceList = remainInstances
    
    def destroy (self):
        self.destroyAt = self.job.env.interval
        
    def set_status (self) :
        pass
        
    def set_job (self, job):
        self.job = job
        for instance in self.instance_list:
            instance.job = job
            
    def instanceGraph (self, past_task_num, past_inst_num) :
        past_inst = past_inst_num
        x_inst = []
        source = []
        dest = []
        for instance in self.instance_list:
            instance.id = past_inst
            self.instancesId.append(instance.id)
            self.job.instancesId.append(instance.id)
            x_inst.append([instance.seq_no, instance.total_seq_no,
                          instance.cpu_max, instance.mem_max])
            
            source.append(past_task_num)
            dest.append(past_inst)
            past_inst += 1
        return x_inst, [source, dest], past_inst

        
        
        
        
        
        
        