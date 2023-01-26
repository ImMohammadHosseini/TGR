import numpy as np
from simulator.host.Disk import Disk
from simulator.host.RAM import RAM
from simulator.host.Bandwidth import Bandwidth
from metrics.powermodels.PMRaspberryPi import *
from metrics.powermodels.PMB2s import *
from metrics.powermodels.PMB4ms import *
from metrics.powermodels.PMB8ms import *
from metrics.powermodels.PMXeon_X5570 import *

class AzureFog():
    def __init__(self, num_hosts, num_VMs):
        self.num_hosts = num_hosts
        self.edge_hosts = round(num_hosts * 0.6)
        self.host_types = {
			'B2s':
				{
					'IPS': 4029,
					'RAMSize': 4295,
					'RAMRead': 372.0,
					'RAMWrite': 200.0,
					'DiskSize': 32212,
					'DiskRead': 13.42,
					'DiskWrite': 1.011,
					'BwUp': 5000,
					'BwDown': 5000,
					'Power': 'PMB2s'
				},
			'B4ms':
				{
					'IPS': 4029,
					'RAMSize': 17180,
					'RAMRead': 360.0,
					'RAMWrite': 305.0,
					'DiskSize': 32212,
					'DiskRead': 10.38,
					'DiskWrite': 0.619,
					'BwUp': 5000,
					'BwDown': 5000,
					'Power': 'PMB4ms'
				},
			'B8ms':
				{
					'IPS': 16111,
					'RAMSize': 34360,
					'RAMRead': 376.54,
					'RAMWrite': 266.75,
					'DiskSize': 32212,
					'DiskRead': 11.64,
					'DiskWrite': 1.164,
					'BwUp': 5000,
					'BwDown': 5000,
					'Power': 'PMB8ms'
				}
 		}
            
        self.num_VMs = num_VMs
        self.edge_VMs = round(num_VMs * 0.6)
        self.vm_types = {
			'Extra-small':
				{
                    single-core 1.0 GHz CPU, 
                    'RAM': 768,
                    'Disk':20,
                     
					'IPS': 4029,
					'RAMSize': 4295,
					'RAMRead': 372.0,
					'RAMWrite': 200.0,
					'DiskSize': 32212,
					'DiskRead': 13.42,
					'DiskWrite': 1.011,
					'BwUp': 5000,
					'BwDown': 5000,
					'Power': 'PMB2s'
				},
            'small':
                {
                },
            'medium':
                {
                },
            'large':
                {
                }
        }
                
        
    