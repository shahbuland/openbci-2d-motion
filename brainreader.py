import numpy as np

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
	def __init__(self, stream_name, stream_frames, callback):
		self.board = Mockboard()
		self.frame_counter = 0
		self.stream_frames = stream_frames
		self.stream_name = stream_name
		self.callback = callback

	def run_callback(self, sample):
		if self.frame_counter >= self.stream_frames:
			self.board.streaming = False # Cancels streaming
		self.callback(sample)
		self.frame_counter += 1	
	
	def start_stream(self):
		self.frame_counter = 0
		self.board.start_stream(self.run_callback)

data = []
def collect_data(sample):
	global data
	x = sample.channels_data
	data.append(np.asarray(x))

while True:
	user_input = str(raw_input("What to do? [q/r]"))
	if(user_input == "q"): break
	if(user_input == "r"):
		name_input = str(raw_input("Recording name?"))
		frame_input = int(raw_input("Recording frames?"))
		mystream = StreamHandler(name_input, frame_input, collect_data)
		mystream.start_stream()
		print("Saving file...")
		np.save(name_input, np.asarray(data))
		data = []
		print("Finished recording and saved file")
	else:
		print("Invalid input, please try again.")
