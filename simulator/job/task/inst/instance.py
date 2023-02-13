
"""

"""

class Instance ():
    def __init__ (self, instance_name, 
                  duration,
                  cpu_avg,
                  cpu_max,
                  mem_avg,
                  mem_max,
                  disk_max,
                  graphId = -1,
                  vmId = -1) :
        self.id = graphId
        self.task=None
        self.job=None
        self.duration = duration
        self.cpu_avg = cpu_avg
        self.cpu_max = cpu_max
        self.mem_avg = mem_avg
        self.mem_max = mem_max
        self.disk_max = disk_max
        self.vmId = vmId
        
        
        
        
        
        
    def getVmId (self):
        return self.vmId
    
    def getVm (self):
        return self.job.env.getVmByID(self.vmId)
    