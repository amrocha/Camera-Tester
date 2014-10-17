import xml.etree.ElementTree as et
from Coordinate import Coordinate
from operator import itemgetter, attrgetter

def parseCoreLog(fileName):

	with open(fileName, 'rt') as file:
		tree = et.parse(file)

	core_entries = []

	for core_msg in tree.iterfind('CORE_MSG'):
		tracknum = core_msg.findtext('TrackNum')
		time = core_msg.attrib.get('UTC')
		for cart in core_msg:
			if cart.tag == 'WGS84':
				lat = cart.attrib.get('LAT')
				lon = cart.attrib.get('LONG')
				if tracknum > 0:
					core_entries.append(Coordinate(time, tracknum, float(lon), float(lat)))
	asterisk_entries = []
	asterisk_entries = sorted(core_entries, key=attrgetter('tn', 'time'))
	return asterisk_entries

def parseGpsLog(fileName):
	f = open('gps.log', 'r')
	gps_entries = list()
	lines = list(f)
	i = 0
	j = -1
	start = False
	while i < len(lines):
		p = lines[i].split(',')
		if p[0] == "$GPGGA":
			start = True
			j += 1
			d1 = p[4][:3]
			m1 = p[4][3:]
			d2 = p[2][:2]
			m2 = p[2][2:]
			gps_entries.append(Coordinate(p[1], None, float(d1) + (float(m1)/60), float(d2) + (float(m2)/60)))
		i += 1
	return gps_entries

