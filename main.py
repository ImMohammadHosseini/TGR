
"""
"""
import os, sys

import torch
import optparse
import logging as logger
import multiprocessing
from time import time
from copy import deepcopy

from simulator.SimulatorGraphData import Simulator
from scheduler.GraphGOBIScheduler import GraphGOBIScheduler
from simulator.workload.ClusterdataWorkload import CDJB
from graphPart.train import GraphEmbedding

from utils.ColorUtils import color

usage = "usage: python main.py -e <environment> -m <mode> # empty environment run simulator"

parser = optparse.OptionParser(usage=usage)
parser.add_option("-e", "--environment", action="store", dest="env", default="", 
					help="In first version, just use simulator(default)")
parser.add_option("-m", "--mode", action="store", dest="mode", default="0", 
					help="In first version, just use default")
opts, args = parser.parse_args()

NUM_SIM_STEPS = 100
ARRIVALRATE = 5

DATACENTERS = 3
HOSTS = 10 #for each datacenter
VMS = 20 # for each datacenter
DATA_TYPE = 'energy_latency_'+str(DATACENTERS*HOSTS)+'_'+str(DATACENTERS*VMS)
DATACENTERINFO = [(HOSTS, VMS), (HOSTS, VMS), (HOSTS, VMS)]#TODO add geographic infos
TOTAL_POWER = 1000
ROUTER_BW = 10000
INTERVAL_TIME = 300 # seconds

#graph embedding part
EMB_DIM = 5
DEVICE = torch.device("cuda" if torch.cuda.is_available() else "cpu")
FEAT_DROP = 0.2
ATTN_DROP = 0.1
LR = 0.0001
LAM = 0.5
TAU = 0.7
NB_EPOCHS = 100
PATIENCE = 20
GRAPH_FEAT_DIM = [2,4,4,5,5]#[DATACENTER,HOST,VM,TASK,INSTANCE]

logFile = 'COSCO.log'

if len(sys.argv) > 1:
	with open(logFile, 'w'): os.utime(logFile, None)
gggraph=[]    
def graphModelTrainerProcess (trainer, graph):
    global gggraph 
    gggraph = graph
    cnt_wait = 0
    best = 1e9
    best_t = 0
    
    for epoch in range(NB_EPOCHS):
        loss = trainer.train_step(deepcopy(graph))
        print(f'Epoch: {epoch:03d}, Loss: {loss:.4f}')
        if loss < best:
            print(f'best: {best:.4f}, Loss: {loss:.4f}###')
            best = loss
            best_t = epoch
            cnt_wait = 0
            print(cnt_wait)
            trainer.save_model()
        
        else:
            cnt_wait += 1

        if cnt_wait == PATIENCE:
            print('Early stopping!')
            break
        #break

def secondProcess (env, trainer, scheduler):
    _, vm_embed, instance_embed = trainer.embedding_step(
        deepcopy(env.graphData))
    
    start = time()
    instDecision = scheduler.instancePlacement(vm_embed, instance_embed)
    firstSchedulingTime = time() - start
    instAllocation = env.instanceAllocate(instDecision) 
    env.addRunInEdges(instAllocation)

    print("Num Instances in vms {(vmId, numInstance)}:", env.getNumInstancsInVms())
    
    host_embed, vm_embed, _ = trainer.embedding_step(
        deepcopy(env.graphData))
    
    start = time()
    scheduler.vmPlacement(host_embed, vm_embed)#vmDecision = 
    secondSchedulingTime = time() - start
    schedulingTime = firstSchedulingTime + secondSchedulingTime

def executeProcess (init='false'):
    pass

def init ():
    workload = CDJB(ARRIVALRATE, 2)
    scheduler = GraphGOBIScheduler(DATA_TYPE, EMB_DIM)
    env = Simulator(DATACENTERS, HOSTS, VMS, TOTAL_POWER, ROUTER_BW, 
                    scheduler, INTERVAL_TIME, DATACENTERINFO)
    graphTrainer = GraphEmbedding(DATA_TYPE, env.getNodeTypes(), DEVICE, 
                                  GRAPH_FEAT_DIM, EMB_DIM, FEAT_DROP, 
                                  ATTN_DROP, LR, LAM, TAU)
    
    newjobinfos = workload.generateNewJobs(env.interval, env)
    env.addJobsInit(newjobinfos)
    print("All jobs' IDs:", env.getjobIds())
    
    trainGraph = multiprocessing.Process(target=graphModelTrainerProcess, 
                                         args=(graphTrainer, 
                                               deepcopy(env.graphData),))
    second = multiprocessing.Process(target=secondProcess, args=(graphTrainer,))
    
    trainGraph.start()
    second.start()
    trainGraph.join()
    second.join()
    
    env.vmAllocateInit()
    
    print("num remain instances:", env.getNumInstances())
    print("VMs in host (vmId, hostId):", env.getVmsInHosts())
    
    return workload, scheduler, env, graphTrainer#, stats
    
def initalizeEnvironment (environment, logger):
    
    workload = CDJB(ARRIVALRATE, 2)
    
    scheduler = GraphGOBIScheduler(DATA_TYPE, EMB_DIM)
    env = Simulator(DATACENTERS, HOSTS, VMS, TOTAL_POWER, ROUTER_BW, 
                    scheduler, INTERVAL_TIME, DATACENTERINFO)
    
    graphTrainer = GraphEmbedding(DATA_TYPE, env.getNodeTypes(), DEVICE, 
                                  GRAPH_FEAT_DIM, EMB_DIM, FEAT_DROP, 
                                  ATTN_DROP, LR, LAM, TAU)
    #TODO add state stats = Stats(env, workload, datacenter, scheduler)
    newjobinfos = workload.generateNewJobs(env.interval, env)
    env.addJobsInit(newjobinfos)
    print("All jobs' IDs:", env.getjobIds())
    
    graphModelTrainerProcess(graphTrainer, deepcopy(env.graphData))
    graphTrainer.setEmbedModel()
    secondProcess(env, graphTrainer, scheduler)
    
    env.vmAllocateInit()#TODO Vm execute   # allocats =  #vmDecision
    
    #TODOworkload.updateDeployedContainers(env.getCreationIDs(migrations, deployed)) 
    print("num remain instances:", env.getNumInstances())
    print("VMs in host (vmId, hostId):", env.getVmsInHosts())
    #TODOprintDecisionAndMigrations(decision, migrations)
    #TODOstats.saveStats()
    
    return workload, scheduler, env, graphTrainer#, stats

def step (workload, scheduler, env, graphTrainer):
    pass

def stepSimulation (workload, scheduler, env, graphTrainer):
    newjobinfos = workload.generateNewJobs(env.interval, env)
    destroyed = env.addJobs(newjobinfos)
    print("All jobs' IDs:", env.getjobIds())
    env.returnCompleteVm()
    
    graphModelTrainerProcess(graphTrainer, deepcopy(env.graphData))
    graphTrainer.setEmbedModel()
    secondProcess(env, graphTrainer, scheduler)

    env.simulationStep()#migrations =  #vmDecision

    #TODOworkload.updateDeployedContainers(
    
    print("num remain instances:", env.getNumInstances())
    print("Destroyed:", destroyed)
    print("VMs in host (vmId, hostId):", env.getVmsInHosts())
    #printDecisionAndMigrations(decision, migrations)
    #TODOstats.saveStats()
    
if __name__ == '__main__':
    env, mode = opts.env, int(opts.mode)
    
    workload, scheduler, env, graphTrainer = initalizeEnvironment(env, logger)
    
    for step in range(NUM_SIM_STEPS):
        print(color.BOLD+"Simulation Interval:", step, color.ENDC)
        stepSimulation(workload, scheduler, env, graphTrainer)#, stats
        #TODOif env != '' and step % 10 == 0: saveStats()
        
    #TODOsaveStats(stats, datacenter, workload, env)
