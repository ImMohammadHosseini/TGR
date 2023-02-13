
"""

"""
#from simulator.datacenter.host.Disk import Disk
#from simulator.datacenter.host.RAM import RAM
#from simulator.datacenter.host.Bandwidth import Bandwidth

class Host ():
    def __init__(self, cores, ram, disk, bw, Latency, Powermodel, Datacenter):
        self.id = -1
        self.coreNumCap = cores
        self.ramCap = ram
        self.diskCap = disk
        self.bwCap = bw
        
        
        self.latency = Latency
        self.powermodel = Powermodel
        self.powermodel.allocHost(self)
        self.powermodel.host = self
        self.datacenter = Datacenter
        
    
    def getVmsOfHost (self):
        graphData = self.datacenter.env.graphData
        allEdges = graphData['vm', 'run_by', 'host'].edge_inde
        allEdges = allEdges.detach().numpy()
        vms = []
        for i, hid in enumerate(allEdges[1]):
            if hid == self.id:
                vms.append(self.datacenter.env.getVmById(allEdges[0][i]))
        return vms
    
    def getPower(self):
        return self.powermodel.power()

    def getPowerFromIPS(self, ips):
        # TODO 
        #return self.powermodel.powerFromCPU(min(100, 100 * (ips / self.ipsCap)))
        pass
    
    def getCPU(self):
        pass
    
    def getBaseIPS(self):
        pass
    
    def getCurrentCores(self):
        vms = self.getVmsOfHost()
        cores = 0
        for vm in vms:
            cores += vm.getRequestsCore()
        return cores 
    
    def getCoresAvailable(self):
        return self.coreNumCap - self.getCurrentCores()
    
    def getCurrentRAM(self):
        vms = self.getVmsOfHost()
        ramSize = 0
        for vm in vms:
            ramSize += vm.getRequestsRam()
        return ramSize 
		
    def getRAMAvailable(self):
        return self.ramCap - self.getCurrentRAM()
    
    def getCurrentDisk(self):
        vms = self.getVmsOfHost()
        diskSize = 0
        for vm in vms:
            diskSize += vm.getRequestsDisk()
        return diskSize 
    
    def getDiskAvailable(self):
        return self.diskCap - self.getCurrentDisk()
        
		