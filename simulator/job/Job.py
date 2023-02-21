
"""
"""

class Job () :
    def __init__ (self, job_id, taskList, creationInterval, envirionment) :
        self.job_id = job_id
        self.taskList = taskList
        self.completedTasks = []
        self.createAt = creationInterval
        self.env = envirionment
        self.startAt = self.env.interval
        self.destroyAt = -1
        
        for task in self.taskList:
            task.set_job(self)
            
        self.tasksId = []
        self.instancesId = []
    
    def destroyCompletedTasks (self):
        remainTasks = []
        for task in self.taskList:
            task.destroyCompletedInstances()
            if len(task.instanceList) != 0:
                remainTasks.append(task)
            else:
                task.destroy()
                self.completedTasks.append(task)
        self.taskList = remainTasks
                
    def destroy (self):
        self.destroyAt = self.env.interval
    
    def jobGraphInfo (self, past_task_num, past_inst_num):
        past_task = past_task_num
        x_task = [None] * len(self.taskList)
        creasionId_task = [None] * len(self.taskList)
        x_instance = []
        creationId_instance = []
        part_of_source = []
        part_of_dest = []
        source = []
        dest = []
        sorted_task_list = [None] * len(self.taskList)
        for task in self.taskList:
            task.setGraphId(past_task)
            self.tasksId.append(task.graphId)
            if task.taskName[:4] == "task" or task.taskName == 'MergeTask':
                x_task[past_task - past_task_num] = [task.planCpu,
                                                     task.planMem,
                                                     task.planDisk,
                                                     len(task.instanceList),
                                                     task.status.value]
                creasionId_task[past_task - past_task_num] = task.creationId
                sorted_task_list[past_task - past_task_num] = task
                
            elif '_' not in task.taskName:
                x_task[int(task.taskName[1:])-1] = [task.planCpu,
                                                   task.planMem,
                                                   task.planDisk,
                                                   len(task.instanceList),
                                                   task.status.value]
                creasionId_task[int(task.taskName[1:])-1] = task.creationId
                sorted_task_list[int(task.taskName[1:])-1] = task
                
            else:
                edges = task.taskName.split('_')
                x_task[int(edges[0][1:])-1] = [task.planCpu,
                                             task.planMem,
                                             task.planDisk,
                                             len(task.instanceList),
                                             task.status.value]
                creasionId_task[int(edges[0][1:])-1] = task.creationId
                sorted_task_list[int(edges[0][1:])-1] = task
                for i in edges[1:]:
                    source.append(past_task_num+int(i)-1)
                    dest.append(past_task_num+int(edges[0][1:])-1)
                
            x_instance_task, creationId_inst_task, part_of, \
                past_inst_num=task.instanceGraph(past_task, past_inst_num)
            x_instance += x_instance_task
            creationId_instance += creationId_inst_task
            part_of_source += part_of[0]
            part_of_dest += part_of[1]
            past_task += 1
        return x_task, creasionId_task, x_instance, creationId_instance, \
            [source,dest], [part_of_source, part_of_dest], past_task,\
                past_inst_num
        
        