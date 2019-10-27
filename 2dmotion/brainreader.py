import numpy as np
from streamhandler import StreamHandler
from pyOpenBCI import OpenBCICyton

NUM_CONTROLS = 4

# For this experiment
data = [[] for i in range(NUM_CONTROLS)]
row_to_modify = 0 # set later


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
		user_input = input("Enter edit command:")
		
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
			lower_bound = int(input("Lower bound?"))
			upper_bound = int(input("Upper bound?"))
				
		# Print
		elif(str(user_input) == "p"):
			print("Please specify a range:")
			lower_bound = int(input("Lower bound?"))
			upper_bound = int(input("Upper bound?"))
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
	user_input = str(input("What to do?"))
	
	# quit
	if(user_input == "q"): break
	
	# ping bci
	if(user_input == "p"):
		test = OpenBCICyton(daisy="True")

	# record
	elif(user_input == "r"):
		row_to_modify = int(input("Row to record to? [0 - Left] [1 - Up] [2 - Right] [3 - Down]"))
		frame_input = int(input("Recording how many frames?"))
		mystream = StreamHandler(frame_input, collect_data)
		mystream.start_stream()
		print("Finished recording to", row_to_modify)
	
	# save or save as
	elif(user_input == "s" or user_input == "sa"):
		if(LOADED and user_input == "s"):
			np.save(LOADED_PATH, np.asarray(data))
		else:
			file_name = str(input("File path?"))
			np.save(file_name, np.asarray(data))
	
	# load
	elif(user_input == "l"):
		file_name = str(input("File path?"))
		arrdata = np.load(file_name, allow_pickle=True)
		for i in range(NUM_CONTROLS):
			data[i] = list(arrdata[i])
		LOADED_PATH = file_name
		LOADED = True
	# edit
	elif(user_input == "e"):
		row_input = int(input("Row to edit? [0 - Left] [1 - Up] [2 - Right] [3 - Down]"))
		edit_data(row_input)	

	# general info on data so far
	elif(user_input == "i"):
		print("Data sizes:")
		for i in range(NUM_CONTROLS):
			print(len(data[i]))
	
	# help
	elif(user_input == "h"):
		print("q - quit")
		print("p - ping")
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
