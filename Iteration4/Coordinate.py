class Coordinate:
	"""Class containing the required information for each tracked vehicle for every second.
	time is the date and time of the recorded tracking log
	tn is the tracking number
	x is the x cartesian coordinate
	y is the y cartesian coordinate"""
	def __init__ (self, tod, tracknum, cart_x, cart_y):
		self.time = tod
		self.tn = tracknum
		self.longitude = cart_x
		self.latitude = cart_y

	def __str__(self):
		return "Longitude: " + str(self.longitude) + " Latitude: " + str(self.latitude)