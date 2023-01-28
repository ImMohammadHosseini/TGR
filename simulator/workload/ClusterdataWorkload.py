
import os 
from os import path

from simulator.data.DataPrepration import PrepareData
from simulator.workload.JobsWorkload import Workload

class CDJB (Workload) :
    def __init__ (self, 
                  arrival_rate, 
                  sigmaNumJobs,
                  sample_data :str = 'simulator/data/datasets/sampling') :
        self.arrival_rate = arrival_rate
        self.sigma = sigmaNumJobs
        self.sample_data = sample_data
        self.jobs_dataset_path = 'simulator/data/datasets/batch_task/'
        if not path.exists(self.sample_data):
            PrepareData()
    
    def generateNewJobs(self, interval):
        pass