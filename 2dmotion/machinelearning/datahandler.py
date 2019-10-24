import numpy as np
import torch

# Function to remove an index from a tensor

# Purpose of this program is to get .npy and handle it for training
# It should be able to:
# 1. convert .npy into a tensor
#		- This task will require it to flatten everything on first axis
#		- Dim on first axis is the class label
# 2. get a random batch from the tensor for training
# 3. Randomly partition a given fraction of the data and give it as a test set
class DataHandler:
	def __init__(self, data_path):
		# First load the data from the npy file
		npdata = np.load(data_path, allow_pickle=True)
		
		# Now we begin converting the raw data into a labelled dataset
		num_classes = len(npdata) # Num classes
		vector_size = int(npdata[0][0].size)

		# Get total dataset size
		self.dataset_size = 0
		for i in range(num_classes):
			self.dataset_size += len(npdata[i])

		# Now convert into torch tensor
		self.data = torch.zeros(self.dataset_size, vector_size)

		# Tensor for labels
		self.labels = torch.zeros(self.dataset_size, num_classes)

		# Load data onto tensor for data and labels	
		cnt = 0
		for i in range(num_classes):
			for sample in npdata[i]:
				self.data[cnt] = torch.from_numpy(sample)
				label = torch.zeros(num_classes)
				label[i] = 1
				self.labels[cnt] = label
				cnt += 1

	def get_batch(self, batch_size):
		# Batch must be smaller than dataset
		assert batch_size <= self.dataset_size

		# Get batch_size random indices
		indices = torch.randint(0, self.dataset_size, (batch_size,))

		# get batch from dataset
		return (self.data[indices],self.labels[indices])

	# frac is fraction of training data to partition into test set
	# returns a fraction of the dataset as a training set
	# and removes it from data itself so model isn't trained on it
	def partition_testset(self,frac):
		assert frac <= 1
		testset_size = int(frac * self.dataset_size)
		
		# Get indices that we are putting into test set
		indices = torch.randint(0, self.dataset_size, (testset_size,))
		# Construct testset
		testset = (self.data[indices],self.labels[indices])

		# Remove all those indices from data
		indices, _ = torch.sort(indices)
		for i, ind in enumerate(indices):
			# Every time we remove an element,
			# Indexes are shifted off by one, subtract all by number of removed elements so far to adjust
			modified_ind = ind - i
			self.data = torch.cat((self.data[0:modified_ind], self.data[modified_ind+1:]))
			self.labels = torch.cat((self.labels[0:modified_ind], self.labels[modified_ind+1:]))

		return testset
