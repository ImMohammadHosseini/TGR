




class CDJB (Workload) :
    def __init__ (self, arrival_rate, sigmaNumJobs) :
        self.arrival_rate = arrival_rate
        self.sigma = sigmaNumJobs
        self.jobs_dataset_path = 'simulator/data/datasets/batch_task/'
        if not path.exists(self.machines_dataset_path):
            PrepareData()
    
    def generateNewJobs(self, interval):