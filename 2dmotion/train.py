import torch
from torch import nn
from model import Net
from datahandler import DataHandler

CUDA = False
ITERATIONS = 10000
BATCH_SIZE = 32

LOAD_CHECKPOINTS = False

LOGGING = True 
LOG_INTERVAL = 100

TESTING = True
TEST_INTERVAL = 1000

SAVE_CHECKPOINTS = False
SAVE_INTERVAL = 1000

# Load and prep data
dh = DataHandler("../datacollection/mytest.npy")
test = dh.partition_testset(0.25) # List: [Input, Output]
print("Training set size:")
print(dh.data.shape)
print("Test set size:")
print(test[0].shape)

# Instantiate model
model = Net(16,4,3,128)
if(CUDA) : model.cuda()
opt = torch.optim.Adam(model.parameters(), lr=2e-3)
loss_func = nn.BCELoss()

# Function to test model on test set
# Returns a list [score, max score]
def test_model():
	test_size = list(test[0].shape)[0]
	y = model(test[0])
	score = 0
	test_loss = loss_func(y, test[1])
	for i in range(test_size):
		_,pred_index = y[i].max(0)
		_,true_index = test[1][i].max(0)
		if pred_index == true_index: score += 1
	return [score, test_size]


# Try to load weights if there are any
if LOAD_CHECKPOINTS:
	try:
		model.load_state_dict(torch.load("checkpoints/params.pt"))
		print("Successfully loaded checkpoint")
	except:
		print("No prior weights found")

# Training loop
model.train()
print("Training...")
for i in range(ITERATIONS):
	# Get batch
	data, labels = dh.get_batch(BATCH_SIZE)
	if CUDA: 
		data = data.cuda()
		labels = labels.cuda()

	opt.zero_grad() # reset optimizer
	y = model(data) # forward
	loss = loss_func(y, labels) # loss calculated
	loss.backward()
	opt.step()
	
	# Logging, saving, etc.
	if LOGGING and i % LOG_INTERVAL == 0:
		print("["+str(i)+"/"+str(ITERATIONS)+"]: "+"Loss: "+str(loss.item()))
	if TESTING and i % TEST_INTERVAL == 0:
		score,max_score = test_model()
		print("Scored: ["+str(score)+" / "+str(max_score)+"] on test set") 
	if SAVE_CHECKPOINTS and i % SAVE_INTERVAL == 0:
		print("Saving checkpoints...")
		try: torch.save(model.state_dict(), "checkpoints/params.pt")
		except: print("Couldn't save pt file")
	
	

