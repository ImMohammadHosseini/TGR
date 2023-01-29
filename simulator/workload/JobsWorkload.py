import numpy as np

class Workload () :
	def __init__ (self) :
		self.creation_id = 0
		self.createdJobs = []
		self.deployedJobs = []

	def getUndeployedJobs (self) :
		undeployed = []
		for i,deployed in enumerate (self.deployedJobs) :
			if not deployed:
				undeployed.append(self.createdJobs[i])
		return undeployed


