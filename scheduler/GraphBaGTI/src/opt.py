
"""

"""

import torch
from copy import deepcopy



def convertToOneHot(dat, emb_part_old, nums):
    allocs = []
    for i in dat:
        alloc = []
        for j in i:
            oneHot = [0] * nums; alist = j.tolist()[-nums:]
            oneHot[alist.index(max(alist))] = 1; alloc.append(oneHot)
        allocs.append(alloc)
    new_dat_oneHot = torch.cat((emb_part_old, torch.FloatTensor(allocs)), dim=2)
    return new_dat_oneHot


def first_step_opt (init, model, data_type):
    VMS = int(data_type.split('_')[-1])
    optimizer = torch.optim.AdamW([init] , lr=0.8)
    scheduler = torch.optim.lr_scheduler.CosineAnnealingLR(optimizer, T_max=10)
    iteration = 0; equal = 0
    while iteration < 200:
        emb_part_old = deepcopy(init.data[:,:,0:-VMS])
        alloc_old = deepcopy(init.data[:,:,-VMS:])
        z = model(init)
        optimizer.zero_grad(); z.backward(); optimizer.step(); scheduler.step()
        init.data = convertToOneHot(init.data, emb_part_old, VMS)
        equal = equal + 1 if torch.all(alloc_old.eq(init.data[:,-VMS:])) else 0
        if equal > 30: break
        iteration += 1
        init.requires_grad = False 
        return init.data, iteration, model(init)



def second_step_opt(init, model, bounds, data_type):
    HOSTS = int(data_type.split('_')[-2])
    optimizer = torch.optim.AdamW([init] , lr=0.8)
    scheduler = torch.optim.lr_scheduler.CosineAnnealingLR(optimizer, T_max=10)
    iteration = 0; equal = 0
    while iteration < 200:
        cpu_old = deepcopy(init.data[:,0:-HOSTS]); alloc_old = deepcopy(init.data[:,-HOSTS:])
        z = model(init)
        optimizer.zero_grad(); z.backward(); optimizer.step(); scheduler.step()
        init.data = convertToOneHot(init.data, cpu_old, HOSTS)
        equal = equal + 1 if torch.all(alloc_old.eq(init.data[:,-HOSTS:])) else 0
        if equal > 30: break
        iteration += 1
    init.requires_grad = False 
    return init.data, iteration, model(init)