#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Wed Jan 25 16:19:54 2023

@author: mohammad
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
        

    def getPower(self):
        return self.powermodel.power()

    def getPowerFromIPS(self, ips):
        # TODO 
        #return self.powermodel.powerFromCPU(min(100, 100 * (ips / self.ipsCap)))
		
	def getCPU(self):
		
	def getBaseIPS(self):

	def getApparentIPS(self):

	def getIPSAvailable(self):

	def getCurrentRAM(self):
		
	def getRAMAvailable(self):

	def getCurrentDisk(self):
		
	def getDiskAvailable(self):
		