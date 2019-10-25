import numpy as np
from pyOpenBCI import OpenBCICyton

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
# Set stream_frames to -1 for continuous
# Callback can return true to cancel stream

class StreamHandler:
	def __init__(self, stream_frames, callback):
		#self.board = Mockboard()
		self.board = OpenBCICyton(daisy = True)
		self.frame_counter = 0
		self.stream_frames = stream_frames
		self.callback = callback

	def run_callback(self, sample):
		if self.stream_frames == -1 or self.frame_counter >= self.stream_frames:
			self.board.streaming = False # Cancels streaming
			return
		# In case callback wants to control when stream stops,
		# we can let it abort
		abort = self.callback(sample)
		if(abort is not None and abort):
			self.board.streaming = False # Abort streaming
			return
		self.frame_counter += 1	
		
	def start_stream(self):
		self.frame_counter = 0
		self.board.start_stream(self.run_callback)
