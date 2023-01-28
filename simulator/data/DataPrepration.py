
from utils.ColorUtils import color

import pandas as pd
import os 
from os import path, makedirs, listdir
from typing import List
import wget
import tarfile
import random

class PrepareData () :    
    def __init__ (self,
                  download_path: str = 'datasets/all_datasets/',
                  dataset_path:str = 'datasets/') :
        
        self.download_path = download_path
        self.dataset_path = dataset_path
        
        self.url='http://clusterdata2018pubcn.oss-cn-beijing.aliyuncs.com/'
        self.url_alternate = 'http://clusterdata2018pubus.oss-us-west-1.aliyuncs.com/'
        
        if not path.exists(download_path): self.download ()
        elif not path.exists(dataset_path+'/batch_instance' or 
                             dataset_path+'/batch_task'): 
            self.extract()
        else: self.sampling()
        
    def download_names (self) -> List[str] :
        return [
            'batch_task.tar.gz', 
            'batch_instance.tar.gz'
        ]
    
    def file_names (self) -> List[str] :
        return [
            'batch_task.csv', 
            'batch_instance.csv'
        ]
    
    def extract (self) :
        print(color.RED+"THE PROCESS OF EXTRACT DATA IS VERY TIME_CONSUMING /n \
               you can extract batch_task.tar.gz and batch_instance.tar.gz \
               dataset and put them into \
               TGR/simulator/data/datasets/batch_instance directory and \
               TGR/simulator/data/datasets/batch_task directory"+color.RED)
        path = os.getcwd()+'/'+self.download_path
        for dataset in listdir(path):
            file = tarfile.open(path+dataset)
            makedirs(self.dataset_path+dataset[:-7])
            file.extractall(self.dataset_path+dataset[:-7])
            file.close()
            
        
    def download (self) :
        print(color.RED+"THE PROCESS OF DAWNLOADING DATA IS VERY TIME_CONSUMING /n \
               you can download batch_task.tar.gz and batch_instance.tar.gz \
               dataset and put them into \
               TGR/simulator/data/datasets/all_datasets directory"+color.RED)
        
        makedirs(self.download_path)
        print('Downloading clusterdata2018 Dataset')
        
        for dataset in self.download_names():
            part_url = self.url + dataset
            try: filename = wget.download(part_url)
            except: 
                part_url = self.url_alternate + dataset
                filename = wget.download(part_url)
            file = tarfile.open(filename)
            makedirs(self.dataset_path+dataset[:-7])
            file.extractall(self.dataset_path+dataset[:-7])
            file.close()
        
    def sampling (self) :
        task_path = self.dataset_path + 'batch_task/batch_task.csv'
        instance_path = self.dataset_path + 'batch_instance/batch_instance.csv'
        n = 14295731 #all datas in batch_task
        s = 1000
        skip = sorted(random.sample(range(n),n-s))
        #get sample of unique jobs name  
        sample_jobs = pd.read_csv(task_path, header=None, usecols=[2], 
                          skiprows=skip).drop_duplicates()
        
        sample_task = pd.read_csv(task_path, header=None, nrows=0)
        
        chunksize = 20000
        with pd.read_csv(task_path, chunksize=chunksize, header=None) as reader:
            for chunk in reader:
                merged_cunck = chunk.merge(sample_jobs, on=2)
                sample_task = pd.concat([sample_task, merged_cunck])
        
        makedirs(self.dataset_path+'sampling/tasks/')
        sample_task.to_csv(self.dataset_path+'sampling/tasks/sample_task.csv', 
                           header=False, index=False)
        
        sample_instance = pd.read_csv(instance_path, header=None, nrows=0)
        
        with pd.read_csv(instance_path, chunksize=chunksize, header=None) as reader:
            for chunk in reader:
                merged_cunck = chunk.merge(sample_jobs, on=2)
                sample_instance = pd.concat([sample_instance, merged_cunck])

        makedirs(self.dataset_path+'sampling/instance/')        
        sample_instance.to_csv(self.dataset_path+'sampling/instance/sample_instance.csv', 
                           header=False, index=False)
        
        sample_jobs.to_csv(self.dataset_path+'sampling/sample_jobs.csv', 
                           header=False, index=False)

        
        
        
        