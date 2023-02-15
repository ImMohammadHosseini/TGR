
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


def initalizeEnvironment(environment, logger):
    
    workload = CDJB(ARRIVALRATE, 2)
    scheduler = GraphGOBIScheduler('energy_latency_'+str(HOSTS)+'_'+str(VMS))
    env = Simulator(DATACENTERS, HOSTS, VMS, TOTAL_POWER, ROUTER_BW, 
                    scheduler, INTERVAL_TIME, DATACENTERINFO)
    #TODO add state stats = Stats(env, workload, datacenter, scheduler)
    newjobinfos = workload.generateNewContainers(env.interval)



if __name__ == '__main__':
    env, mode = opts.env, int(opts.mode)
    
    datacenter, workload, scheduler, env, stats = initalizeEnvironment(env, 
                                                                       logger)