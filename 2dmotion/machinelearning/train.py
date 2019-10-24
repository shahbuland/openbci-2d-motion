import torch.nn
from model import Net
from datahandler import DataHandler

CUDA = False
ITERATIONS = 3000
BATCH_SIZE = 16

LOAD_CHECKPOINTS = False

LOGGING = True 
LOG_INTERVAL = 100

TESTING = True
TEST_INTERVAL = 1000

SAVE_CHECKPOINTS = False
SAVE_INTERVAL = 1000

# Load and prep data
dh = DataHandler("../datacollection/mytest.npy")
test = dh.partition_testset(0.25)
print("Training set size:")
print(dh.data.shape)
print("Test set size:")
print(test[0].shape)

# Instantiate model
model = Net(16,4,2,128)
if(CUDA) : model.cuda()
opt = torch.nn.optim.Adam(model.parameters(), lr=2e-4)
loss_func = nn.BCELoss()

# Function to test model on test set
# Returns a percent score
def test_model():
	test_size = list(test.shape)[0]
	y = model(test[0])
	score = 0
	test_loss = loss_func(y, test[1])
	for i in range(test_size):
		_,
		if(y[i] == test


# Try to load weights if there are any
if LOAD_CHECKPOINTS:
	try:
		model.load_state_dict(torch.load("checkpoints/params.pt"))
	except:
		print("No prior weights found")

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
		print("
	
	
	

