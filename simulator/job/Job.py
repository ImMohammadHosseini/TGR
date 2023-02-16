
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
        
        for task in self.task_list:
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
        x_task = [None] * len(self.task_list)
        creasionId_task = [None] * len(self.task_list)
        part_of_source = []
        part_of_dest = []
        source = []
        dest = []
        sorted_task_list = [None] * len(self.task_list)
        for task in self.task_list:
            task.setGraphId(past_task)
            self.tasksId.append(task.graphId)
            if task.task_name[:4] == "task" or task.task_name == 'MergeTask':
                x_task[past_task - past_task_num] = [task.plan_cpu,
                                                     task.plan_mem,
                                                     len(task.instance_list),
                                                     task.status.value]
                creasionId_task[past_task - past_task_num] = task.creatioId
                sorted_task_list[past_task - past_task_num] = task
                
            elif '_' not in task.task_name:
                x_task[int(task.task_name[1:])] = [task.plan_cpu,
                                                   task.plan_mem,
                                                   len(task.instance_list),
                                                   task.status.value]
                creasionId_task[int(task.task_name[1:])] = task.creatioId
                sorted_task_list[int(task.task_name[1:])] = task
                
            else:
                edges = task.task_name.split('_')
                x_task[int(edges[0][1:])] = [task.plan_cpu,
                                             task.plan_mem,
                                             len(task.instance_list),
                                             task.status.value]
                creasionId_task[int(edges[0][1:])] = task.creatioId
                sorted_task_list[int(edges[0][1:])] = task
                dest.append(past_task_num+int(edges[0][1:]))
                for i in edges[1:]:
                    source.append(past_task_num+int(i))
                
                
            x_instance, creationId_instance, part_of, \
                past_inst_num=task.instanceGraph(past_task, past_inst_num)
            part_of_source += part_of[0]
            part_of_dest += part_of[1]
            past_task += 1
        return x_task, creasionId_task, x_instance, creationId_instance, \
            [source,dest], [part_of_source, part_of_dest], past_task,\
                past_inst_num
        
        