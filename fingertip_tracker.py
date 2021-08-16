from collections import deque
import numpy as np

#Class to contain information about the fingertip location
class fingertip_tracker:

	def __init__(self):
		self.points = deque(maxlen=32)
		self.counter = 0
		self.dX = 0
		self.dY = 0

	def track_fingertip(self, location):

		is_clicking = False

		#If the fingertip is not detected, return no click
		if location is None:
			return is_clicking
		
		#Append the current location to the queue of points
		self.points.append(location)

		#Loop over the current queue of points
		for i in np.arange(1, len(self.points)):
			#Skip if there is less than 2 points
			if self.points[i-1] is None or self.points[i] is None:
				continue

			#If we have enough initial points (16) and we are at the start of the queue of points
			#Compare the most recent point with the point 16 frames from the end
			if self.counter >= 16 and i == 1 and self.points[-16] is not None:
				self.dX = self.points[-16][0] - self.points[i][0]
				self.dY = self.points[-16][1] - self.points[1][1]
			
			#If the current point and the point 10 points from the end are witin 10 pixels of each other
			if np.abs(self.dX) < 8 and np.abs(self.dY) < 8:
				is_clicking = True
		
		self.counter+=1
		return is_clicking