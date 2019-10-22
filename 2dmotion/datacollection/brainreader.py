import numpy as np

NUM_CONTROLS = 4

# For this experiment
data = [[] for i in range(NUM_CONTROLS)]
row_to_modify = 0 # set later

# Mock sample for mock board
class Mocksample:
	def __init__(self, channels_data):
		self.channels_data = channels_data

# Mock board for experimenting data stuff without actual board
class Mockboard:
	def __init__(self):
		self.streaming = False

	def start_stream(self, callback):
		self.streaming = True
		while(self.streaming):
			sample = Mocksample(np.random.randn(16))
			callback(sample)

# Handles stream from the board
class StreamHandler:
	def __init__(self, stream_frames, callback):
		self.board = Mockboard()
		self.frame_counter = 0
		self.stream_frames = stream_frames
		self.callback = callback

	def run_callback(self, sample):
		if self.frame_counter >= self.stream_frames:
			self.board.streaming = False # Cancels streaming
			return
		self.callback(sample)
		self.frame_counter += 1	
	
	def start_stream(self):
		self.frame_counter = 0
		self.board.start_stream(self.run_callback)

# Function that collects raw data and appends to data
def collect_data(sample):
	global data
	x = sample.channels_data
	data[row_to_modify].append(np.asarray(x))

# Edits row of data
def edit_data(row):
	global data
	print("Now editing! Type 'h' for help")
	while True:
		user_input = raw_input("Enter edit command:")
		
		# Help
		if(str(user_input) == "h"):
			print("h - help")
			print("q - quit edit")
			print("r - remove")
			print("p - print")
		
		# Quit
		elif(str(user_input) == "q"): break
		
		# Get info
		elif(str(user_input) == "i"):
			print("Size:", np.asarray(data[row]).shape)
			print("Mean:", np.mean(np.asarray(data[row])))
			print("Standard Deviation:", np.std(np.asarray(data[row])))
			print("Minimum value:", np.amin(np.asarray(data[row])))
			print("Maximum value:", np.amax(np.asarray(data[row])))
		
		# Remove
		elif(str(user_input) == "r"):	
			print("Please specify a range:")
			lower_bound = int(raw_input("Lower bound?"))
			upper_bound = int(raw_input("Upper bound?"))
				
		# Print
		elif(str(user_input) == "p"):
			print("Please specify a range:")
			lower_bound = int(raw_input("Lower bound?"))
			upper_bound = int(raw_input("Upper bound?"))
			for i in range(lower_bound, upper_bound):
				print(data[row][i])
		
		# Invalid input 		
		else:
			print("Invalid input. Type 'h' for help")

	print("Now done editing!")	


LOADED = False # Did user load a recording?
LOADED_PATH = ""

# Main loop
while True:
	user_input = str(raw_input("What to do?"))
	
	# quit
	if(user_input == "q"): break
	
	# record
	if(user_input == "r"):
		row_to_modify = int(raw_input("Row to record to? [0 - Left] [1 - Up] [2 - Right] [3 - Down]"))
		frame_input = int(raw_input("Recording how many frames?"))
		mystream = StreamHandler(frame_input, collect_data)
		mystream.start_stream()
		print("Finished recording to", row_to_modify)
	
	# save or save as
	elif(user_input == "s" or user_input == "sa"):
		if(LOADED and user_input == "s"):
			np.save(LOADED_PATH, np.asarray(data))
		else:
			file_name = str(raw_input("File path?"))
			np.save(file_name, np.asarray(data))
	
	# load
	elif(user_input == "l"):
		file_name = str(raw_input("File path?"))
		arrdata = np.load(file_name, allow_pickle=True)
		for i in range(NUM_CONTROLS):
			data[i] = list(arrdata[i])
		LOADED_PATH = file_name
		LOADED = True
	# edit
	elif(user_input == "e"):
		row_input = int(raw_input("Row to edit? [0 - Left] [1 - Up] [2 - Right] [3 - Down]"))
		edit_data(row_input)	

	# general info on data so far
	elif(user_input == "i"):
		print("Data sizes:")
		for i in range(NUM_CONTROLS):
			print(len(data[i]))
	
	# help
	elif(user_input == "h"):
		print("q - quit")
		print("r - record data")
		print("s - save data")
		print("sa - save as")
		print("l - load data from file")
		print("e - edit data")
		print("i - info")
		print("h - help")
		
	# invalid input
	else:
		print("Invalid input, please try again.")
		print("Type 'h' if you are unfamiliar with commands.")
