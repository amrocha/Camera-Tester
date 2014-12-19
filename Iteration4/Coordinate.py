class Coordinate:
	"""Class containing the required information for each tracked vehicle for every second.
	time is the date and time of the recorded tracking log
	tn is the tracking number
	x is the longitude
	y is the latitude"""
	def __init__ (self, tod, tracknum, long, lat):
		self.time = tod
		self.tn = tracknum
		self.longitude = long
		self.latitude = lat

	def __str__(self):
		return "Longitude: " + str(self.longitude) + " Latitude: " + str(self.latitude)

	def __repr__(self):
		return "Time: " + str(self.time) + " Tracknum: " + str(self.tn) + " Longitude: " + str(self.longitude) + " Latitude: " + str(self.latitude) + "\n"