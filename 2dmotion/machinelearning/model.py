import torch
from torch import nn
import torch.nn.functional as F

# Input size (vector)
# n_h_layers, number of hidden layers
# h_size, number of hidden neurons in each hidden layer
# output_size (vector)
class Net(nn.Module):
	def __init__(self, input_size, output_size, n_h_layers=0, h_size=128):
		super(Net, self).__init__()
		
		self.input_size = input_size
		self.n_layers = n_h_layers + 2
		self.n_h_layers = n_h_layers
		self.h_size = h_size
		self.output_size = output_size
		
		# List for layers
		self.fc_layers = nn.ModuleList()
		
		node_count = []
		# Add input layer (output size ternary in case theres no h layers)
		node_count.append(input_size)	
		
		# Add hidden layers
		for i in range(self.n_h_layers - 2):
			node_count.append(h_size)

		# Add output layers
		node_count.append(output_size)

		# Build actual layers
		for i in range(len(node_count) - 1):
			self.fc_layers.append(nn.Linear(node_count[i], node_count[i+1]))

	def forward(self, x):
		for i, layer in enumerate(self.fc_layers):
			x = layer(x)
			# Let last layer output be sigmoid
			if i != self.n_layers - 1: x = F.relu(x)
		
		# Note: since the task is classification, 
		#		we probably want to use sigmoid and CE loss
		x = F.sigmoid(x)
		return x
			
		
		
