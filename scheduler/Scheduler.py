import math
from utils.MathUtils import *
from utils.MathConstants import *
import pandas as pd
from statistics import median
import numpy as np

class Scheduler():
    def __init__(self):
        self.env = None

    def setEnvironment(self, env):
        self.env = env

    def selection(self):
        pass

    def instancePlacement (self, first_sch = False) :
        pass
    
    def vmPlacement (self):
        pass

    def filter_placement(self, decision):
        filteredDecisionSource = []; filteredDecisionDest = []
        for vid, hid in zip(decision[0], decision[1]):
            if self.env.getVmById(vid).hostId != hid:
                filteredDecisionSource.append(vid)
                filteredDecisionDest.append(hid)
        return [filteredDecisionSource, filteredDecisionDest]

    def getMigrationFromHost(self, hostID, decision):
        vmIDs = []
        for vid in decision[0]:
            hid = self.env.getVmById(vid).hostId
            if hid == hostID:
                vmIDs.append(vid)
        return vmIDs

    def getMigrationToHost(self, hostID, decision):
        vmIDs = []
        for vid, hid in zip(decision[0], decision[1]):
            if hid == hostID:
                vmIDs.append(vid)
        return vmIDs

    def getAllocateToVm (self, vmId, decision):
        instanceIDs = [] 
        for instid, vmid in zip(decision[0], decision[1]):
            if vmid == vmId:
                instanceIDs.append(instid)
        return instanceIDs
    