import xml.etree.ElementTree as et
from Coordinate import Coordinate
from operator import itemgetter, attrgetter
from xml.etree.ElementTree import ParseError

def parseCoreLog(fileName):

        try:
                with open(fileName, 'rt') as file:
					xml = '<XML>'
					xml += file.read()
					xml += '</XML>'
					tree = et.fromstring(xml)
        except (ParseError, IOError), e:
                print 'An error occurred while reading the core log file: ', str(e)
                return -1

	core_entries = []

	for core_msg in tree.iterfind('CORE_MSG'):
		tracknum = core_msg.findtext('TrackNum')
		time = core_msg.attrib.get('UTC')
		formattedTime = time[12:14] + time[15:17] + time[18:20] + '.' + time[21:24] #put time in the same format as the GPS file (HHMMSS.mmm)
		for cart in core_msg:
			if cart.tag == 'WGS84':
				lat = cart.attrib.get('LAT')
				lon = cart.attrib.get('LONG')
				if tracknum > 0:
					core_entries.append(Coordinate(formattedTime, tracknum, float(lon), float(lat)))
	asterisk_entries = []
	asterisk_entries = sorted(core_entries, key=attrgetter('tn', 'time'))
	return asterisk_entries

def parseGpsLog(fileName):
        try:
                f = open(fileName, 'r')
        except IOError, e:
                print 'An error occurred while reading the core log file: ', str(e)
                return -1
        
	gps_entries = list()
	lines = list(f)
	i = 0
	j = -1
	start = False

        while i < len(lines):
                try:
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
                except IndexError:
                        print 'An error occurred while reading the GPS file: A $GPGGA entry at line', i, 'does not have the correct number of elements'
                        return -1

	return gps_entries

