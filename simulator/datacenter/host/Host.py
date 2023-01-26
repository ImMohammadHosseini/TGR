#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Wed Jan 25 16:19:54 2023

@author: mohammad
"""
from simulator.datacenter.host.Disk import Disk
from simulator.datacenter.host.RAM import RAM
from simulator.datacenter.host.Bandwidth import Bandwidth

class Host ():
    def __init__(self, ID, IPS, RAM, Disk, Bw, Latency, Powermodel, Environment):
        self.id = ID
        self.ipsCap = IPS
        self.ramCap = RAM
        self.diskCap = Disk
        self.bwCap = Bw
        
        
        self.latency = Latency
        self.powermodel = Powermodel
        self.powermodel.allocHost(self)
        self.powermodel.host = self
        self.env = Environment
        

    def getPower(self):

	def getPowerFromIPS(self, ips):
		
	def getCPU(self):
		
	def getBaseIPS(self):

	def getApparentIPS(self):

	def getIPSAvailable(self):

	def getCurrentRAM(self):
		
	def getRAMAvailable(self):

	def getCurrentDisk(self):
		
	def getDiskAvailable(self):
		