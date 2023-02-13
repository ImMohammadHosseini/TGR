
"""

"""

class VM ():
    def __init__(self, 
                 core_lim, 
                 ram_lim, 
                 disk_lim,
                 bw_lim,
                 datacenter, 
                 hostId = -1):
        self.ID = -1
        self.coreNum = core_lim
        self.ramCap = ram_lim
        self.diskCap = disk_lim
        self.bwCap = bw_lim
        
        self.datacenter = datacenter
        self.hostId = hostId
        
        self.totalExecTime = 0
        self.totalMigrationTime = 0
        self.active = True
        
    def getFreeCores (self):
        pass
    
    def getFreeRam (self):
        pass
    
    def getFreeDisk (self):
        pass
    
    def possibleToAddInstance (self, instance):
        return (self.getFreeCores() <= instance.cpuMax &&
                self.getFreeRam() <= instance.memMax &&
                self.getFreeDisk() <= instance.diskMax)