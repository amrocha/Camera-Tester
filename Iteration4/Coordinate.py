import math

class Coordinate:
	"""Class containing the required information for each tracked vehicle for every second.
	time is the date and time of the recorded tracking log
	tn is the tracking number
	x is the longitude
	y is the latitude"""
	def __init__ (self, tod, tracknum, long, lat, referenceLong, referenceLat):
		self.time = tod
		self.tn = tracknum
		self.longitude = long
		self.latitude = lat
		self.x = self.getXCoordinate(self.longitude, referenceLong, referenceLat)
		self.y = self.getYCoordinate(self.latitude, referenceLong, referenceLat)

	def __str__(self):
		return "Longitude: " + str(self.longitude) + " Latitude: " + str(self.latitude)

	def __repr__(self):
		return "Time: " + str(self.time) + " Tracknum: " + str(self.tn) + " Longitude: " + str(self.longitude) + " Latitude: " + str(self.latitude) + " X: " + str(self.x) + " Y: " + str(self.y) + "\n"

	def getXCoordinate(self, lon1, lon2, lat2):
		R = 6371000 #Radius of Earth in meters

		radLat2 = lat2 * math.pi/180
		latDif = 0
		lonDif = (lon2 - lon1) * math.pi/180


		#get angle on Earth, correct for latitude
		a = math.sin(latDif/2)**2 + math.cos(radLat2)**2 * math.sin(lonDif/2)**2
		c = 2 * math.atan2(math.sqrt(a), math.sqrt(1-a))
		#multiply result by radius of Earth
		x = c*R

		return x

	def getYCoordinate(self, lat1, lon2, lat2):
		R = 6371000 #Radius of Earth in meters

		radLat1 = lat1 * math.pi/180
		radLat2 = lat2 * math.pi/180
		latDif = (lat2 - lat1) * math.pi/180
		lonDif = 0


		a = math.sin(latDif/2)**2 + math.cos(radLat1) * math.cos(radLat2) * math.sin(lonDif/2)**2

		c = 2 * math.atan2(math.sqrt(a), math.sqrt(1-a))
		y = c*R

		return y