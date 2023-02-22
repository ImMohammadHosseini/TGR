
"""

"""
import pandas as pd

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
        
        self.instances = pd.DataFrame({'creationId':[], 'core':[], 'ram':[], 
                                       'disk':[]})
        
        self.datacenter = datacenter
        self.hostId = hostId
        
        self.totalExecTime = 0
        self.totalMigrationTime = 0
        self.active = True
        self.lastVmSize = 0
    
    def getInstancesOfVm (self):
        return self.instances['creationId'].to_list()
    
    def addInstance (self, instCreationId, instCore, instRam, instDisk):
        indx = 0 if pd.isnull(self.instances.index.max()) else self.instances.index.max() + 1
        self.instances.loc[indx]=[instCreationId, instCore, instRam, instDisk]
        self.removeExpectedFreeCores(instCore)
        self.removeExpectedFreeRam(instRam)
        self.removeExpectedFreeDisk(instDisk)
    
    def deleteInstance (self, instCreationId):
        indx = self.instances[(self.instances.creationId==instCreationId)].index
        self.addExpectedFreeCores(self.instances['core'][indx[0]])
        self.addExpectedFreeRam(self.instances['ram'][indx[0]])
        self.addExpectedFreeDisk(self.instances['disk'][indx[0]])
        self.instances = self.instances.drop(indx)
        
    def getInstanceForRun (self):
        pass
    
    def getExpectedFreeCores (self):
        return self.expectedCoreNum
    
    def addExpectedFreeCores (self, coreToAdd):
        self.setExpectedFreeCores(self.expectedCoreNum - coreToAdd)
        
    def removeExpectedFreeCores (self, coreToRemove):
        self.setExpectedFreeCores(self.expectedCoreNum - coreToRemove)
        
    def setExpectedFreeCores (self, expectedCores) :
        self.expectedCoreNum = max(0, expectedCores)
    
    def getRequestsCore (self):
        try:
            return max(self.instances['core'].to_list())
        except:
            print('rid',self.id)
        
    def getExpectedFreeRam (self):
        return self.expectedRamCap
    
    def addExpectedFreeRam (self, ramToAdd):
        self.setExpectedFreeRam (self.expectedRamCap - ramToAdd)
        
    def removeExpectedFreeRam (self, ramToRemove):
        self.setExpectedFreeRam (self.expectedRamCap - ramToRemove)
        
    def setExpectedFreeRam (self, expectedRam):
        self.expectedRamCap = max(0, expectedRam)
        
    def getRequestsRam (self):
        return max(self.instances['ram'].to_list())
    
    def getExpectedFreeDisk (self):
        return self.expectedDiskCap
    
    def addExpectedFreeDisk (self, diskToAdd):
        self.setExpectedFreeDisk(self.expectedDiskCap - diskToAdd)
        
    def removeExpectedFreeDisk (self, diskToRemove):
        self.setExpectedFreeDisk(self.expectedDiskCap - diskToRemove)
    
    def setExpectedFreeDisk (self, expectedDisk):
        self.expectedDiskCap = max(0, expectedDisk)
        
    def getRequestsDisk (self):
        return max(self.instances['disk'].to_list())

    def possibleToAddInstance (self, instance):
        return (instance.cpuMax <= self.getExpectedFreeCores() and \
                instance.memMax <= self.getExpectedFreeRam() and \
                instance.diskMax <= self.getExpectedFreeDisk())
    
    def getVmSize (self):
        if self.lastVmSize == 0:
            self.lastVmSize = self.getRequestsRam()+self.getRequestsDisk()
        return self.lastVmSize
    
    def allocate (self, host, allocBw):
        lastMigrationTime = 0
        if self.hostId != host.id:
            lastMigrationTime += self.getVmSize() / allocBw
            firstLatency = self.datacenter.env.getHostById(self.hostId).latency if self.hostId!=-1 else 0.076
            lastMigrationTime += abs(firstLatency - host.latency)
        self.hostId = host.id
        return lastMigrationTime
    
    def execute (self, lastMigrationTime):
        assert self.hostId != -1
        self.totalMigrationTime += lastMigrationTime
        execTime = self.datacenter.env.intervaltime - lastMigrationTime
        #TODO change for loop for get best instance line
        for instanceCreationId in self.instances['creationId']:
            instance = self.datacenter.env.getInstanceById(instanceCreationId)
            requiredExecTime = instance.requiredExecTime()
            self.totalExecTime += min(execTime, requiredExecTime)
            execTime -= min(execTime, requiredExecTime)
            instance.completDu += min(execTime, requiredExecTime)
            if execTime == 0:
                break
        
    def allocateAndExecute (self, host, allocBw) :
        self.execute(self.allocate(host, allocBw))