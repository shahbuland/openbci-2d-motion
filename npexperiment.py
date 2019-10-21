import numpy as np

data = np.load("thing.npy")
print(data.shape)
for i in range(60):
	print(data[i])
