
import torch
from torch import nn

class ContrastiveLoss(nn.Module):
    def __init__(self,  lam, tau):
        super(ContrastiveLoss, self).__init__()
        self.lam = lam
        self.tau = tau
        self.log = torch.nn.LogSigmoid()
        
    def sim(self, z1, z2):
        z1_norm = torch.norm(z1, dim=-1, keepdim=True)
        z2_norm = torch.norm(z2, dim=-1, keepdim=True)
        dot_numerator = torch.mm(z1, z2.t())
        dot_denominator = torch.mm(z1_norm, z2_norm.t())
        sim_matrix = torch.exp(dot_numerator / dot_denominator / self.tau)
        return sim_matrix
    
    def forward (self, z_mps, z_scs, pos_parts, weights=[.9,.9,1]):
        contrastValues = []
        for z_mp, z_sc, pos in zip(z_mps, z_scs, pos_parts):
            matrix_mp2sc = self.sim(z_mp, z_sc)
            matrix_sc2mp = matrix_mp2sc.t()
    
            matrix_mp2sc = matrix_mp2sc/(torch.sum(
                matrix_mp2sc, dim=1).view(-1, 1) + 1e-8)
            
            lori_mp = -self.log(matrix_mp2sc.mul(pos.to_dense()).sum(dim=-1)).mean()

            matrix_sc2mp = matrix_sc2mp / (torch.sum(matrix_sc2mp, 
                                                     dim=1).view(-1, 1) + 1e-8)
            lori_sc = -self.log(matrix_sc2mp.mul(pos.to_dense()).sum(dim=-1)).mean()

            contrastValues.append(self.lam * lori_mp + (1 - self.lam) * lori_sc)
            #print(self.lam * lori_mp + (1 - self.lam) * lori_sc)
            
        return sum(value * w for value, w in zip(contrastValues, weights) if not torch.isnan(value).all()) / sum(weights)



