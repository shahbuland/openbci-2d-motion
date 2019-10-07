import sys
sys.path.append('..')

import unittest
from openbci import cyton as bci
from openbci.plugins import StreamerTCPServer
import time, timeit
from threading import Thread

NB_CHANNELS = 16

# If > 0, interpolate on sample count, 1.024 to 250Hz->256Hz
SAMPLING_FACTOR = -1.024
# If > 0 will interpolate based on time
SAMPLING_RATE = 256

SERVER_PORT = 12345
SERVER_IP = "localhost"

DEBUG = False

last_id = -1
nb_samples_in = -1
nb_samples_out = -1
last_values = [0] * NB_CHANNELS
leftover_duplications = 0
tick = timeit.default_timer()

class Monitor(Thread):
	def __init__(self):
		self.nb_samples_in = -1
		self.nb_samples_out = -1
		self.tick = timeit.default_timer()
		self.start_tick = self.tick
	def run(self):
		while True:
			# Check FPS
			new_tick = timeit.default_timer()
			elapsed_time = new_tick - self.tick
			current_samples_in = nb_samples_in
			current_samples_out = nb_samples_in

			print("--- at t: ", (new_tick - self.start_tick), " ---")
			print("Elapsed time: ", elapsed_time)
			print("nb_samples_in: ", current_samples_in - self.nb_samples_in)
			print("nb_sampels_out: ", current_samples_out - self.nb_samples_out)
			self.tick = new_tick
			self.nb_samples_in = nb_samples_in
			self.nb_samples_out = nb_samples_out
			
			# Watch for connection
			server.check_connections()
			time.sleep(1)

def streamData(sample):
		global last_values

		global tick
		
		if sample.id != last_id + 1:
			print("time", tick, ": packet skipped!")
		if sample.id == 255:
			last_id = -1
		else:
			last_id = sample.id

