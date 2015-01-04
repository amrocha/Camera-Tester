import os
import xml.etree.ElementTree as et
from Coordinate import Coordinate
from operator import itemgetter, attrgetter
from xml.etree.ElementTree import ParseError

def parseCoreLogs(folderName, referenceLon, referenceLat):
        try:
                fileList = os.listdir(folderName)
        except OSError:
                print 'Not a directory. Assuming file.'
                fileList = list([folderName])

        asteriskEntries = list()
        for f in fileList:
                asteriskEntries = parseCoreLog(folderName+f, referenceLon, referenceLat, asteriskEntries)

        path = []
        tracknum = None
        pathList = []
        for entry in asteriskEntries:
                if(tracknum != entry.tn):
                        tracknum = entry.tn
                        if(path):
                                pathList.append(path)
                        path = []
                path.append(entry)

        return pathList

def parseCoreLog(fileName, referenceLon, referenceLat, partial_entries=list()):
        print "Opening " + fileName
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
		formattedTime = int(time[12:14])*3600 + int(time[15:17])*60 + float(time[18:20] + '.' + time[21:24]) #put time in the same format as the GPS file (HHMMSS.mmm)
		for cart in core_msg:
			if cart.tag == 'WGS84':
				lat = cart.attrib.get('LAT')
				lon = cart.attrib.get('LONG')
				if tracknum > 0:
					core_entries.append(Coordinate(formattedTime, tracknum, float(lon), float(lat), referenceLon, referenceLat))
	asterisk_entries = []
        core_entries.extend(partial_entries)
	asterisk_entries = sorted(core_entries, key=attrgetter('tn', 'time'))

        return asterisk_entries

def parseGpsLog(fileName):
        try:
                f = open(fileName, 'r')
        except IOError, e:
                print 'An error occurred while reading the GPS log file: ', str(e)
                return -1

	gps_entries = list()
	lines = list(f)
	i = 0
	j = -1

        while i < len(lines):
                try:
                        p = lines[i].split(',')
                        if p[0] == "$GPGGA":
                                j += 1
                                #Longitude
                                lon = None
                                d1 = p[4][:3]
                                m1 = p[4][3:]
                                ew = p[5]
                                if(ew == 'E'):
                                        lon = float(d1) + (float(m1)/60)
                                if(ew == 'W'):
                                        lon = -(float(d1) + (float(m1)/60))
                                #Latitude
                                lat = None
                                d2 = p[2][:2]
                                m2 = p[2][2:]
                                ns = p[3]
                                if(ns == 'N'):
                                        lat = float(d2) + (float(m2)/60)
                                if(ns == 'S'):
                                        lat = -(float(d2) + (float(m2)/60))
                                #Time
                                time = None
                                h = int(p[1][:2])
                                m = int(p[1][2:4])
                                s = float(p[1][4:])
                                time = h*3600+m*60+s
                                #Reference Points to orient all other points
                                if(i == 0):
                                        referenceLon = lon
                                        referenceLat = lat

                                gps_entries.append(Coordinate(time, None, lon, lat, referenceLon, referenceLat))
                        i += 1
                except IndexError:
                        print 'An error occurred while reading the GPS log file: A $GPGGA entry at line', i, 'does not have the correct number of elements'
                        return -1

	return gps_entries