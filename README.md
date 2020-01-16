# openbci-2dmotion

Using a fully connected neural network, a data collector and an OpenBCI electrode cap, this program learns to read brain waves and classify them as being a 2d motion (Left, Up, Right, Down), then allows the user to control a circle in 2d with their thoughts.  

# Usage:  
brainreader.py can be used to record and save data  
train.py will train model on saved data  
movement.py will use model to convert brain waves directly to motion  
 
# Dependancies:

Pytorch
pyOpenBCI
OpenBCI electrode cap + Cyton Board + Daisy (16 channels)

This only works on linux and programs using the cyton must be run with sudo to be able to access ports. 
