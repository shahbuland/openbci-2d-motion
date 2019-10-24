import torch.nn
from model import Net
from datahandler import DataHandler

dh = DataHandler("../datacollection/mytest.npy")
test = dh.partition_testset(0.25)
print("Training set size:")
print(dh.data.shape)
print("Test set size:")
print(test[0].shape)
