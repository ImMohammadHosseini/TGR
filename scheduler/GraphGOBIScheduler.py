
"""

"""
import sys
sys.path.append('scheduler/GraphBaGTI/')
import torch
import numpy as np 

from .Scheduler import Scheduler
from .GraphBaGTI.train import load_model
from .GraphBaGTI.src.graph_representation import GNNEncoder
from .GraphBaGTI.src.models import energy_latency_20_40_first
from .GraphBaGTI.src.models import energy_latency_20_40_second
#from .GraphBaGTI.src.utils import *
from .GraphBaGTI.src.opt import opt


class GraphGOBIScheduler(Scheduler):
    def __init__ (self, data_type) :
        self.graphRepre = GNNEncoder ()
        self.model1 = eval(data_type+"_first()")
        self.model2 = eval(data_type+"_second()")
        self.data_type = data_type
        self.hosts = int(data_type.split('_')[-2])
        self.vms = int(data_type.split('_')[-1])
        #TODO add self.graphRepre load model and save model
        self.model1, _, _, _ = load_model(data_type, self.model1, data_type)
        self.model2, _, _, _ = load_model(data_type, self.model2, data_type)
        #dtl = data_type.split('_')
        #_, _, self.max_container_ips = eval("load_"+'_'.join(dtl[:-1])+
        #                              "_data("+dtl[-1]+")")
    
    def selection (self) :
        return []
    
    def first_step_init (self, vm_emb, instance_emb, schedueled_instances) :
        vm_emb = vm_emb.detach().numpy()
        instance_emb = instance_emb.detach().numpy()
        schedueled_instances = schedueled_instances.detach().numpy()
        
        inits = []
        ins_ids_init = []; ins_id_init = []; ins_prep = []; oneHots = [];
        for i, inst_emb in enumerate(instance_emb):
            if i not in schedueled_instances:
                ins_id_init.append(i)
                ins_prep.append(inst_emb)
                oneHot = [0] * len(vm_emb)
                oneHot[np.random.randint(0,len(vm_emb))] = 1
                oneHots.append(oneHot)
                if len(ins_prep) == len(vm_emb):
                    two_emb = np.concatenate((vm_emb, ins_prep), axis=1)
                    inits.append(np.concatenate((two_emb, oneHots), axis=1))
                    ins_ids_init.append(ins_id_init)
                    ins_id_init=[]; ins_prep = []; oneHots = []
                
        return inits, ins_ids_init
    
    def first_step (self) :
        #TODO add graphrepresentatio in learning process
        #if not first_sch: self.env.nodeUpdate()
        schedueled_instances = self.env.graphData['instance', 'run_in', 'vm'].edge_index[0]
        _, vm_emb, instance_emb = self.graphRepre(self.env.graph_data)
        init, instance_ids_init = self.first_step_init(vm_emb, 
                                                       instance_emb, 
                                                       schedueled_instances)
        init = torch.tensor(init, dtype=torch.float, requires_grad=True)
        result, iteration, fitness = opt(init, self.model1, 
                                         int(self.data_type.split('_')[-1]))
        decisionSource = []; decisionDest = []
        for partsId, part in zip(instance_ids_init, result):
            for instanceId, decision in zip(partsId, part):
                decisionSource.append(instanceId)
                decision = decision[-self.vms:].tolist()
                decisionDest.append(decision.index(max(decision)))
                
        return [decisionSource, decisionDest]
    
    def second_step_init (self, host_emb, vm_emb) :
        host_emb = host_emb.detach().numpy()
        vm_emb = vm_emb.detach().numpy()
        
        inits = []
        vm_ids_init = []; vm_id_init = []; vm_prep = []; oneHots = [];
        for i, vemb in enumerate(vm_emb):
            vm_id_init.append(i)
            vm_prep.append(vemb)
            oneHot = [0] * len(host_emb)
            oneHot[np.random.randint(0,len(host_emb))] = 1
            oneHots.append(oneHot)
            if len(vm_prep) == len(host_emb):
                two_emb = np.concatenate((host_emb, vm_emb), axis=1)
                inits.append(np.concatenate((two_emb, oneHots), axis=1))
                vm_ids_init.append(vm_id_init)
                vm_id_init=[]; vm_prep = []; oneHots = []
        return inits, vm_ids_init
    
    def second_step (self) :
        #TODO if not first_sch: self.env.nodeUpdate()
        #TODO add graphrepresentatio in learning process
        host_emb, vm_emb, _ = self.graphRepre(self.env.graph_data)
        init, vm_ids_init = self.second_step_init(vm_emb, host_emb)
        init = torch.tensor(init, dtype=torch.float, requires_grad=True)
        result, iteration, fitness = opt(init, self.model2, 
                                         int(self.data_type.split('_')[-2]))
        
        decisionSource = []; decisionDest = []
        for partsId, part in zip(vm_ids_init, result):
            for vmId, decision in zip(partsId, part):
                decisionSource.append(vmId)
                decision = decision[-self.hosts:].tolist()
                decisionDest.append(decision.index(max(decision)))
                
        return [decisionSource, decisionDest]
        
        
    def instancePlacement (self) :
        decision = self.first_step()
        return decision
    
    def vmPlacement (self):
        decision = self.second_step()
        return decision