
"""
TODO: ADD Graph representation with dynamic models and train steps in graph
"""
import os, sys, stat

import optparse
import logging as logger
import configparser
import pickle
import shutil
from time import time
from os import system, rename

from simulator.SimulatorGraphData import Simulator
from scheduler.GraphGOBIScheduler import GraphGOBIScheduler
from simulator.workload.ClusterdataWorkload import CDJB
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
DATACENTERINFO = [(HOSTS, VMS), (HOSTS, VMS), (HOSTS, VMS)]#TODO add geographic infos
TOTAL_POWER = 1000
ROUTER_BW = 10000
INTERVAL_TIME = 300 # seconds
logFile = 'COSCO.log'

if len(sys.argv) > 1:
	with open(logFile, 'w'): os.utime(logFile, None)


def initalizeEnvironment (environment, logger):
    
    workload = CDJB(ARRIVALRATE, 2)
    scheduler = GraphGOBIScheduler('energy_latency_'+str(DATACENTERS*HOSTS)+\
                                   '_'+str(DATACENTERS*VMS))
    env = Simulator(DATACENTERS, HOSTS, VMS, TOTAL_POWER, ROUTER_BW, 
                    scheduler, INTERVAL_TIME, DATACENTERINFO)
    #TODO add state stats = Stats(env, workload, datacenter, scheduler)
    newjobinfos = workload.generateNewJobs(env.interval, env)
    env.addJobsInit(newjobinfos)
    start = time()
    instDecision = scheduler.instancePlacement()
    firstSchedulingTime = time() - start
    instAllocation = env.instanceAllocate(instDecision) 
    print(len(instAllocation[0]))
    print(len(env.graphData['instance', 'run_in', 'vm'].edge_index[1]))
    env.addRunInEdges(instAllocation)
    print(len(env.graphData['instance', 'run_in', 'vm'].edge_index[1]))

    start = time()
    vmDecision = scheduler.vmPlacement()
    secondSchedulingTime = time() - start
    allocats = env.vmAllocateInit(vmDecision)#TODO Vm execute
    
    schedulingTime = firstSchedulingTime + secondSchedulingTime
    
    #TODOworkload.updateDeployedContainers(env.getCreationIDs(migrations, deployed)) 
    print("All jobs' IDs:", env.getjobIds())
    print("Num Instances in vms {(vmId, numInstance)}:", env.getNumInstancsInVms())
    print("VMs in host (vmId, hostId):", env.getVmsInHosts())
    
    #TODOprintDecisionAndMigrations(decision, migrations)

    #TODOstats.saveStats()
    
    return workload, scheduler, env#, stats

def stepSimulation (workload, scheduler, env):
    newjobinfos = workload.generateNewJobs(env.interval, env)
    destroyed = env.addJobs(newjobinfos)
    start = time()
    instDecision = scheduler.instancePlacement()
    firstSchedulingTime = time() - start
    instAllocation = env.instanceAllocate(instDecision) 
    env.addRunInEdges(instAllocation)

    start = time()
    vmDecision = scheduler.filter_placement(scheduler.vmPlacement()) 
    secondSchedulingTime = time() - start
    migrations = env.simulationStep(vmDecision)
    schedulingTime = firstSchedulingTime + secondSchedulingTime

    #TODOworkload.updateDeployedContainers(
    
    print("All jobs' IDs:", env.getjobIds())
    print("Destroyed:", destroyed)
    print("Num Instances in vms {(vmId, numInstance)}:", env.getNumInstancsInVms())
    print("VMs in host (vmId, hostId):", env.getVmsInHosts())
    #printDecisionAndMigrations(decision, migrations)
    #TODOstats.saveStats()
    
if __name__ == '__main__':
    env, mode = opts.env, int(opts.mode)
    
    workload, scheduler, env = initalizeEnvironment(env, logger)
    
    for step in range(NUM_SIM_STEPS):
        print(color.BOLD+"Simulation Interval:", step, color.ENDC)
        stepSimulation(workload, scheduler, env)#, stats
        #TODOif env != '' and step % 10 == 0: saveStats()
        
    #TODOsaveStats(stats, datacenter, workload, env)
