
"""

"""
from simulator.datacenter.AzureFog import AzureFog
from metrics.powermodels.PMB2s import PMB2s
from metrics.powermodels.PMB4ms import PMB4ms
from metrics.powermodels.PMB8ms import PMB8ms

from simulator.datacenter.host.Host import Host
from simulator.datacenter.vm.vm import VM 

class Datacenter (AzureFog) :
    def __init__ (self, Id, num_hosts, num_VMs, Environment) :
        super().__init__(num_hosts, num_VMs)
        self.id = Id
        self.env = Environment

        
        self.hostList = []
        self.VMList = []
        
        self.generateHosts()
        self.generateVMs()
        
        self.hostsId = []
        self.vmsId = []
        
    def generateHosts(self):
        self.hostList = []
        types = ['small', 'small', 'small', 'small', \
                 'medium', 'medium', 'medium', 'medium', \
                 'large', 'large'] * 1
        for i in range(self.num_hosts):
            typeID = types[i]
            core = self.host_types[typeID]['core']
            mem_size = self.host_types[typeID]['mem_size']
            disk = self.host_types[typeID]['DiskSize']
            Bw = self.host_types[typeID]['Bw']
            Power = eval(self.host_types[typeID]['Power']+'()')
            Latency = 0.003 if i < self.edge_hosts else 0.076
            host = Host(core, mem_size, disk, Bw, Latency, Power, self)
            self.hostList.append(host)
    
    def generateVMs(self):
        self.VMList = []
        types = ['Extra-small','Extra-small','Extra-small','Extra-small','Extra-small', 
                 'small','small','small','small','small',
                 'medium','medium','medium','medium','medium',
                 'large','large','large','large','large'] * 1
        for i in range(self.num_VMs):
            typeID = types[i]
            coreLim = self.vm_types[typeID]['core']
            ramLim = self.vm_types[typeID]['RAM']
            diskLim = self.vm_types[typeID]['Disk']
            bwLim = self.vm_types[typeID]['Bw']
            vm = VM (coreLim, ramLim, diskLim, bwLim, self)
            
            self.VMList.append(vm)
            
            
    def dsGraphInfo (self, past_host_num, past_vm_num):
        past_hosts = past_host_num; past_vms = past_vm_num
        x_ds = [[self.num_hosts, self.num_VMs]]
        x_host = []; x_vm = []
        dsho_source = []; dsho_dest = []
        dsvm_source = []; dsvm_dest = []
        for host in self.hostList:
            host.id = past_hosts
            self.hostsId.append(host.id)
            x_host.append([host.coreNumCap, host.ramCap, host.diskCap, 
                           host.bwCap])
            dsho_source.append(self.id)
            dsho_dest.append(past_hosts)
            past_hosts += 1
        for vm in self.VMList:
            vm.id = past_vms
            self.vmsId.append(vm.id)
            x_vm.append([vm.coreNum, vm.ramCap, vm.diskCap, vm.bwCap])
            dsvm_source.append(self.id)
            dsvm_dest.append(past_vms)
            past_vms += 1
            
        return x_ds, x_host, x_vm, [dsho_source, dsho_dest], \
            [dsvm_source, dsvm_dest], past_hosts, past_vms
       