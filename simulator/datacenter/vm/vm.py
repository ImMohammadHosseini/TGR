
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
        self.lastVmSize = 0
    
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
        self.setExpectedFreeCores(self.expectedCoreNum - coreToAdd)
        
    def removeExpectedFreeCores (self, coreToRemove):
        self.setExpectedFreeCores(self.expectedCoreNum - coreToRemove)
        
    def setExpectedFreeCores (self, expectedCores) :
        self.expectedCoreNum = max(0, expectedCores)
    
    def getRequestsCore (self):
        #TODO use first instance for run but we can send them by DAG
        instances = self.getInstancesOfVm()
        instance = instances[self.datacenter.env.interval % len(instances)]
        return instance.cpuAvg
    
    def getFreeRam (self):
        instances = self.getInstancesOfVm()
        usedRam = 0
        for instance in instances:
            usedRam += instance.ramAvg
        return self.ramCap - usedRam
    
    def getExpectedFreeRam (self):
        return self.expectedRamCap
    
    def addExpectedFreeRam (self, ramToAdd):
        self.setExpectedFreeRam (self.expectedRamCap - ramToAdd)
        
    def removeExpectedFreeRam (self, ramToRemove):
        self.setExpectedFreeRam (self.expectedRamCap - ramToRemove)
        
    def setExpectedFreeRam (self, expectedRam):
        self.expectedRamCap = max(0, expectedRam)
        
    def getRequestsRam (self):
        #TODO use first instance for run but we can send them by DAG
        instances = self.getInstancesOfVm()
        instance = instances[self.datacenter.env.interval % len(instances)]
        return instance.memAvg
    
    def getFreeDisk (self):
        instances = self.getInstancesOfVm()
        usedDisk = 0
        for instance in instances:
            usedDisk += instance.diskMax
        return self.diskCap - usedDisk
    
    def getExpectedFreeDisk (self):
        return self.expectedDiskCap
    
    def addExpectedFreeDisk (self, diskToAdd):
        self.setExpectedFreeDisk(self.expectedDiskCap - diskToAdd)
        
    def removeExpectedFreeDIsk (self, diskToRemove):
        self.setExpectedFreeDisk(self.expectedDiskCap - diskToRemove)
    
    def setExpectedFreeDisk (self, expectedDisk):
        self.expectedDiskCap = max(0, expectedDisk)
        
    def getRequestsDisk (self):
        #TODO use first instance for run but we can send them by DAG
        instances = self.getInstancesOfVm()
        instance = instances[self.datacenter.env.interval % len(instances)]
        return instance.diskMax
    
    def possibleToAddInstance (self, instance):
        return (instance.cpuMax <= self.getExpectedFreeCores() and \
                instance.memMax <= self.getExpectedFreeRam() and \
                instance.diskMax <= self.getExpectedFreeDisk())
    
    def getVmSize (self):
        if self.lastVmSize == 0:
            self.lastVmSize = self.getRequestsRam()+self.getRequestsDisk()
        return self.lastVmSize
    
    def allocate (self,host, allocBw):
        lastMigrationTime = 0
        if self.hostid != host.id:
            lastMigrationTime += self.getContainerSize() / allocBw
            lastMigrationTime += abs(self.env.getHostById(self.hostid).latency - host.latency)
        self.hostid = host.id
        return lastMigrationTime
    
    def execute (self, lastMigrationTime):
        assert self.hostid != -1
        self.totalMigrationTime += lastMigrationTime
        execTime = self.env.intervaltime - lastMigrationTime
        #reqCore = self.getRequestsCore()
        instances = self.getInstancesOfVm()
        instance = instances[self.datacenter.env.interval % len(instances)]
        requiredExecTime = instance.requiredExecTime()
        self.totalExecTime += min(execTime, requiredExecTime)
        instance.completDu += min(execTime, requiredExecTime)
        
    def allocateAndExecute (self, host, allocBw) :
        self.execute(self.allocate(host, allocBw))