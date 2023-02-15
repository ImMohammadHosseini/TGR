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
        filtered_decision = []
        for cid, hid in decision:
            if self.env.getContainerByID(cid).getHostID() != hid:
                filtered_decision.append((cid, hid))
        return filtered_decision

    def getMigrationFromHost(self, hostID, decision):
        containerIDs = []
        for (cid, _) in decision:
            hid = self.env.getContainerByID(cid).getHostID()
            if hid == hostID:
                containerIDs.append(cid)
        return containerIDs

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
    