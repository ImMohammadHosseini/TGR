
"""
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
ARRIVALRATE = 10

DATACENTERS = 2
HOSTS = 10 #for each datacenter
VMS = 20 # for each datacenter
DATACENTERINFO = [(HOSTS, VMS), (HOSTS, VMS)]#TODO add geographic infos
TOTAL_POWER = 1000
ROUTER_BW = 10000
INTERVAL_TIME = 300 # seconds
logFile = 'COSCO.log'

if len(sys.argv) > 1:
	with open(logFile, 'w'): os.utime(logFile, None)


def initalizeEnvironment (environment, logger):
    
    workload = CDJB(ARRIVALRATE, 2)
    scheduler = GraphGOBIScheduler('energy_latency_'+str(HOSTS)+'_'+str(VMS))
    env = Simulator(DATACENTERS, HOSTS, VMS, TOTAL_POWER, ROUTER_BW, 
                    scheduler, INTERVAL_TIME, DATACENTERINFO)
    #TODO add state stats = Stats(env, workload, datacenter, scheduler)
    newjobinfos = workload.generateNewJobs(env.interval)
    env.addJobsInit(newjobinfos)
    start = time()
    instDecision = scheduler.instancePlacement(first_sch = True)
    firstSchedulingTime = time() - start
    instAllocation = env.instanceAllocateInit(instDecision) 
    env.addRunInEdges(instAllocation)
    
    start = time()
    vmDecision = scheduler.vmPlacement()
    secondSchedulingTime = time() - start
    migration = env.vmAllocateInit(vmDecision)#TODO Vm execute
    env.addRunByEdges(migration)
    
    schedulingTime = firstSchedulingTime + secondSchedulingTime
    
    #TODOworkload.updateDeployedContainers(env.getCreationIDs(migrations, deployed)) 
    print()
    print()
    print()
    #TODOprintDecisionAndMigrations(decision, migrations)

    #TODOstats.saveStats()
    
    return workload, scheduler, env#, stats

def stepSimulation (workload, scheduler, env):
    newjobinfos = workload.generateNewJobs(env.interval)
    deployed, destroyed = env.addJobs(newcontainerinfos)ll#TODO trace, -deployed
    start = time()
    decision = scheduler.filter_placement(scheduler.placement(deployed)) 
    firstSchedulingTime = time() - start
    
    
    
    
    
    
if __name__ == '__main__':
    env, mode = opts.env, int(opts.mode)
    
    workload, scheduler, env = initalizeEnvironment(env, logger)
    
    for step in range(NUM_SIM_STEPS):
        print(color.BOLD+"Simulation Interval:", step, color.ENDC)
        stepSimulation(workload, scheduler, env)#, stats
        #TODOif env != '' and step % 10 == 0: saveStats()
        
    #TODOsaveStats(stats, datacenter, workload, env)
