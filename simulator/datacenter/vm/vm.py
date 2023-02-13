
"""

"""

class VM ():
    def __init__(self, coreLim, ramLim, diskLim, bwLim, datacenter, 
                 hostId = -1):
        
        self.id = -1
        self.coreNum = coreLim
        self.ramCap = ramLim
        self.diskCap = diskLim
        self.bwCap = bwLim
        
        self.expectedCoreNum = self.coreNum
        self.expectedRamCap = self.ramCap
        self.expectedDiskCap = self.diskCap
        
        self.datacenter = datacenter
        self.hostId = hostId
        
        self.totalExecTime = 0
        self.totalMigrationTime = 0
        self.active = True
    
    def getInstancesOfVm (self):
        graphData = self.datacenter.env.graphData
        allEdges = graphData['instance', 'run_in', 'vm'].edge_inde
        allEdges = allEdges.detach().numpy()
        instances = []
        for i, vid in enumerate(allEdges[1]):
            if vid == self.id:
                instances.append(self.datacenter.env.getInstanceById(allEdges[0][i]))
        return instances
    
    def getFreeCores (self):
        instances = self.getInstancesOfVm()
        usedCore = 0
        for instance in instances:
            usedCore += instance.cpuAvg
        return self.coreNum - usedCore
    
    def getExpectedFreeCores (self):
        return self.expectedCoreNum
    
    def addExpectedFreeCores (self, coreToAdd):
        self.expectedCoreNum += coreToAdd
        
    def removeExpectedFreeCores (self, coreToRemove):
        self.expectedCoreNum -= coreToRemove
    
    def getRequestsCore (self):
        pass
    
    def getFreeRam (self):
        instances = self.getInstancesOfVm()
        usedRam = 0
        for instance in instances:
            usedRam += instance.ramAvg
        return self.ramCap - usedRam
    
    def getExpectedFreeRam (self):
        return self.expectedRamCap
    
    def addExpectedFreeRam (self, ramToAdd):
        self.expectedRamCap += ramToAdd
        
    def removeExpectedFreeRam (self, ramToRemove):
        self.expectedRamCap -= ramToRemove
    
    def getRequestsRam (self):
        pass
    
    def getFreeDisk (self):
        instances = self.getInstancesOfVm()
        usedDisk = 0
        for instance in instances:
            usedDisk += instance.diskMax
        return self.diskCap - usedDisk
    
    def getExpectedFreeDisk (self):
        return self.expectedDiskCap
    
    def addExpectedFreeDisk (self, diskToAdd):
        self.expectedDiskCap += diskToAdd
        
    def removeExpectedFreeDIsk (self, diskToRemove):
        self.expectedDiskCap -= diskToRemove
    
    def getRequestsDisk (self):
        pass
    
    def possibleToAddInstance (self, instance):
        return (self.getExpectedFreeCores() <= instance.cpuMax and \
                self.getExpectedFreeRam() <= instance.memMax and \
                self.getExpectedFreeDisk() <= instance.diskMax)