
import os 
from os import path
import pandas as pd
from random import gauss

from simulator.data.DataPrepration import PrepareData
from simulator.job.Job import Job
from simulator.job.task.Task import Task
from simulator.job.task.instance.instance import Instanse
from simulator.workload.JobsWorkload import Workload

class CDJB (Workload) :
    def __init__ (self, 
                  arrival_rate, 
                  sigmaNumJobs,
                  sample_data :str = 'simulator/data/datasets/sampling') :
        
        self.arrival_rate = arrival_rate
        self.sigma = sigmaNumJobs
        
        self.sample_data = sample_data
        if not path.exists(self.sample_data):
            PrepareData()
        
        self.jobs_sample_path = 'simulator/data/datasets/sampling/sample_jobs.csv'
        self.arrived_jobs = 0
        
        self.creation_id = 0
        
    def generateNewJobs(self, interval):
        num = int(gauss(self.arrival_rate, self.sigma))
        
        workloadjobs = pd.read_csv(self.sample_data+'/sample_jobs.csv', 
                                   header=None, 
                                   skiprows= self.arrived_jobs,
                                   nrows=num)
        self.arrived_jobs =+ num
        
        workloadtasks = pd.read_csv(self.sample_data+'/tasks/sample_task.csv',
                                    header=None)
        workloadtasks = workloadtasks.merge(workloadjobs, on=2)
        
        workloadinstances = pd.read_csv(self.sample_data+'/instance/sample_instance.csv',
                                    header=None)
        workloadinstances = workloadinstances.merge(workloadjobs, on=2)
        
        job_list = []
        for i, job_idx in workloadjobs.iterrows():
            job_id = job_idx.values[0][2:]
            task_list=[]
            jobs_tasks = workloadtasks.merge(job_idx.rename(2), on=2)
            jobs_instances = workloadinstances.merge(job_idx.rename(2), on=2)
            task_list=[]
            for j, task_info in jobs_tasks.iterrows():
                task_name = task_info[0]
                plan_cpu = task_info[7]
                plan_mem = task_info[8]
                tasks_instances = jobs_instances.merge(pd.Series(task_name).rename(2),
                                                       on=2)
                instance_list=[]
                for k, instance_info in tasks_instances.iterrows():
                    instance_name = instance_info[0]
                    seq_no = instance_info[8]
                    total_seq_no = instance_info[9]
                    cpu_max = instance_info[11]
                    mem_max = instance_info[13]
                    instance_list.append(Instanse (instance_name, 
                                                   seq_no, 
                                                   total_seq_no,
                                                   cpu_max,
                                                   mem_max))
                task_list.append(Task (task_name,
                                       plan_cpu,
                                       plan_mem,
                                       instance_list))
            job_list.append(Job (job_id, task_list))
        
        self.createdJobs += job_list
        self.deployedJobs += [False] * len(job_list)
        return self.getUndeployedJobs()