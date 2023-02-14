import numpy as np
#from simulator.host.Disk import Disk
#from simulator.host.RAM import RAM
#from simulator.host.Bandwidth import Bandwidth


class AzureFog():
    def __init__(self, num_hosts, num_VMs):
        self.num_hosts = num_hosts
        self.edge_hosts = round(num_hosts * 0.6)
        self.host_types = {
			'small':
				{
                    'core': 200,
					'mem_size': .4,
					'DiskSize': 16000,
					'Bw': 5000,
					'Power': 'PMB2s'
				},
			'medium':
				{
                    'core': 400,
                    'mem_size': .8,
					'DiskSize': 32000,
					'Bw': 5000,
					'Power': 'PMB4ms'
				},
			'large':
				{
                    'core': 800,
                    'mem_size': 1.8,
					'DiskSize': 64000,
					'Bw': 5000,
					'Power': 'PMB8ms'
				}
 		}
            
        self.num_VMs = num_VMs
        self.edge_VMs = round(num_VMs * 0.6)
        self.vm_types = {
			'Extra-small':
				{
                    'core': 100,
                    'RAM': 768,
                    'Disk': 4000,
					'Bw': 2000
				},
            'small':
                {
                    'core': 100,
                    'RAM':1750,
                    'Disk': 8000,
					'Bw': 2000
                },
            'medium':
                {
                    'core': 200,
                    'RAM':3500,
                    'Disk': 16000,
					'Bw': 4000
                },
            'large':
                {
                    'core': 400,
                    'RAM':7000,
                    'Disk': 32000,
					'Bw': 4000
                },
        }
                
        
    