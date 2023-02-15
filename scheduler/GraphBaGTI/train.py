
"""

"""
import os
import torch
from src.constants import MODEL_SAVE_PATH
import src.utils
from src.utils import color

def save_graph_model ():
    #TODO
    pass

def load_graph_model ():
    #TODO
    pass
 
def save_model (model, optimizer, epoch, accuracy_list):
	file_path = MODEL_SAVE_PATH + "/" + model.name + "_" + str(epoch) + ".ckpt"
	torch.save({
        'epoch': epoch,
        'model_state_dict': model.state_dict(),
        'optimizer_state_dict': optimizer.state_dict(),
        'accuracy_list': accuracy_list}, file_path)

def load_model (filename, model, data_type):
    optimizer = torch.optim.Adam(model.parameters(), lr=0.0001, 
                                 weight_decay=1e-5)
    
    file_path1 = MODEL_SAVE_PATH + "/" + filename + "_Trained.ckpt"
    file_path2 = 'scheduler/BaGTI/' + file_path1
    file_path = file_path1 if os.path.exists(file_path1) else file_path2
    if os.path.exists(file_path):
        print(color.GREEN+"Loading pre-trained model: "+filename+color.ENDC)
        checkpoint = torch.load(file_path)
        model.load_state_dict(checkpoint['model_state_dict'])
        optimizer.load_state_dict(checkpoint['optimizer_state_dict'])
        epoch = checkpoint['epoch']
        accuracy_list = checkpoint['accuracy_list']
    else:
        epoch = -1; accuracy_list = []
        print(color.GREEN+"Creating new model: "+model.name+color.ENDC)
    return model, optimizer, epoch, accuracy_list

