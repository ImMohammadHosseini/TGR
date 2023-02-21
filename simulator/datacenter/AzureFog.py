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
                    'core': 16,
					'mem_size': 8000,
					'DiskSize': 128000,
					'Bw': 5000,
					'Power': 'PMB2s'
				},
			'medium':
				{
                    'core': 32,
                    'mem_size': 32000,
					'DiskSize': 256000,
					'Bw': 5000,
					'Power': 'PMB4ms'
				},
			'large':
				{
                    'core': 64,
                    'mem_size': 64000,
					'DiskSize': 512000,
					'Bw': 5000,
					'Power': 'PMB8ms'
				}
 		}
            
        self.num_VMs = num_VMs
        self.edge_VMs = round(num_VMs * 0.6)
        self.vm_types = {
			'Extra-small':
				{
                    'core': 4,
                    'RAM': 8000,
                    'Disk': 32000,
					'Bw': 4000
				},
            'small':
                {
                    'core': 8,
                    'RAM': 16000,
                    'Disk': 64000,
					'Bw': 4000
                },
            'medium':
                {
                    'core': 16,
                    'RAM': 16000,
                    'Disk': 64000,
					'Bw': 4000
                },
            'large':
                {
                    'core': 32,
                    'RAM': 32000,
                    'Disk': 128000,
					'Bw': 4000
                },
        }
                
        
    