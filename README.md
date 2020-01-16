# openbci-2dmotion

Using a fully connected neural network, a data collector and an OpenBCI electrode cap, this program learns to read brain waves and classify them as being a 2d motion (Left, Up, Right, Down), then allows the user to control a circle in 2d with their thoughts.

#Dependancies:

Pytorch
pyOpenBCI
OpenBCI electrode cap + Cyton Board + Daisy (16 channels)

This only works on linux and programs using the cyton must be run with sudo to be able to access ports. 
