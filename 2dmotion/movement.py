from model import Net
import torch
from torch import nn
from streamhandler import StreamHandler
import matplotlib.pyplot as plt
import numpy as np

model = Net(16,4,3,128)

try:
	model.load_state_dict(torch.load("checkpoints/params.pt"))
except:
	print("No prior weights found")

fig = plt.figure()
ax = fig.add_subplot(111)
fig.show()

pos_x = 0
pos_y = 0

scale_factor = 0.01
bound = 4

# First we define the callback function for the stream
def update(data):
	global pos_x
	global pos_y
	data = data.channels_data
	move = model(torch.from_numpy(data).float())
	v = scale_factor * np.asarray([float(move[2] - move[0]), float(move[1] - move[3])])
	pos_x +=  v[0]
	pos_y += v[1]
	# truncate
	pos_x = max(min(bound,pos_x),-1*bound)
	pos_y = max(min(bound,pos_y),-1*bound)
	# plot boundaries
	ax.cla()
	ax.plot([-1*bound,bound,bound,-1*bound,-1*bound],[-1*bound,-1*bound,bound,bound,-1*bound])
	# Draw circle at interpreted coordinates
	ax.add_artist(plt.Circle((pos_x,pos_y), 0.1, color='blue'))
	fig.canvas.draw()

	
# Start the stream	
stream = StreamHandler(-1, update)
stream.start_stream()
