
"""

"""

class Instance ():
    def __init__ (self, instance_name, duration, cpuAvg, cpuMax, memAvg, 
                  memMax, diskMax, graphId = -1, vmId = -1) :
        
        self.id = graphId
        self.task=None
        self.job=None
        self.duration = duration
        self.completDu = 0
        self.cpuAvg = cpuAvg
        self.cpuMax = cpuMax
        self.memAvg = memAvg
        self.memMax = memMax
        self.diskMax = diskMax
        self.vmId = vmId
        
    def requiredExecTime (self):
        return self.duration - self.completDu
        
    def destroy (self):
        self.destroyAt = self.job.env.interval
        self.vmId = -1
    
    def getVmId (self):
        return self.vmId
    
    def getVm (self):
        return self.job.env.getVmByID(self.vmId)
    