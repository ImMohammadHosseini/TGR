
from utils.ColorUtils import color

from os import path, makedirs, listdir
from typing import List
import wget
import tarfile


class PrepareData () :    
    def __init__ (self,
                  download_path: str = 'simulator/data/datasets/all_datasets/',
                  dataset_path:str = 'simulator/data/datasets/') :
        
        self.download_path = download_path
        self.dataset_path = dataset_path
        
        self.url='http://clusterdata2018pubcn.oss-cn-beijing.aliyuncs.com/'
        self.url_alternate = 'http://clusterdata2018pubus.oss-us-west-1.aliyuncs.com/'
        
        if not path.exists(download_path): self.download ()
        else: self.extract()
    
        
    def download_names (self) -> List[str] :
        return [
            'container_meta.tar.gz', 
            'batch_task.tar.gz', 
            'batch_instance.tar.gz'
        ]
    
    def file_names (self) -> List[str] :
        return [
            'container_meta.csv', 
            'batch_task.csv', 
            'batch_instance.csv'
        ]
    
    def extract (self) :
        for dataset in listdir(self.dataset_path):
            file = tarfile.open(self.download_path + dataset)
            makedirs(self.dataset_path+dataset[:-7])
            file.extractall(self.dataset_path+dataset[:-7])
            file.close()
            
        
    def download (self) :
        print(color.RED+"THE PROCESS OF DAWNLOADING DATA IS VERY TIME_CONSUMING /n \
               you can download all dataset and put them into \
               TGR/simulator/data/datasets/all_datasets directory"+color.RED)
        
        makedirs(self.download_path)
        print('Downloading clusterdata2018 Dataset')
        
        for dataset in self.download_names():
            part_url = self.url + dataset
            try: filename = wget.download(part_url)
            except: 
                part_url = self.url + dataset
                filename = wget.download(self.url_alternate)
            file = tarfile.open(filename)
            makedirs(self.dataset_path+dataset[:-7])
            file.extractall(self.dataset_path+dataset[:-7])
            file.close()
        
        
        
        