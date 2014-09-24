import FileReader
from Coordinate import Coordinate
import subprocess, math
import numpy as np
import matplotlib.pyplot as plt
from scipy.optimize import fmin_cobyla
from decimal import *

class Scenario:
    """
    Class containing information for a test scenario

    variables
    scenarioID: the unique identifier for this scenario
    coreLog: the path and filename for the core log used to generate this scenario
    gpsLog: the path and filename for the gps log used to generate this scenario
    timeOffset: the timestamp difference used to compare points in time between the two log files
    maxRadius: the maximum distance a point from the core log can be from a corresponding gps log point for it to be considered accurate
    """
    def __init__ (self, scenarioID, maxRadius, gpsLog, coreLog=None):
        self.scenarioID = scenarioID
        self.coreLog = coreLog
        self.gpsLog = gpsLog
        self.timeOffset = None
        self.maxRadius = maxRadius

    def run(self):
        if self.coreLog == None:
            self.coreLog = self.runCamSim()
        self.core_entries = FileReader.parseCoreLog(self.coreLog)
        self.gps_entries = FileReader.parseGpsLog(self.gpsLog)
        self.timeOffset = self.calculateTimeOffset()
        distances = self.comparePath()
        print "Minimum Distance"
        print min(distances)
        print "Maximum Distance"
        print max(distances)

        print 'id: ', self.scenarioID
        print 'core log file: ', self.coreLog
        print 'gps log file: ', self.gpsLog
        print 'time offset: ', self.timeOffset
        print 'maximum radius: ', self.maxRadius
        print 'number of core file entries: ', len(self.core_entries)
        print 'number of gps file entries: ', len(self.gps_entries)

    #this method will call camsim, wait until it completes running, and then return the path and filename that was generated by camsim
    def runCamSim(self):
        #call camsim
        CamSimExe = "CamSimDummyApp.exe"
        CamSimArgs = ["aaa", "bbb", "ccc"]
        subprocess.call([CamSimExe] + CamSimArgs)

        #wait

        #obtain and return path and filename of the log file
        return 'Corefile.log'

    """
    Calculates the difference in timestamps between the two files
    The GPS log contains timestamps generated during the time when the video was created
    The Core log contains timestamps generated during the run of camsim
    """
    def calculateTimeOffset(self):
        return 33;

    #this will compare the files and output the result
    def comparePath(self):
        pointList = list()
        for point in self.core_entries:
            pointList.append(self.comparePoints(point));

        return pointList


    def comparePoints(self, c):
        minDist = 99999
        point1 = None
        point2 = None
        point3 = None
        for (i, x) in enumerate(self.gps_entries):
            dist = math.sqrt(pow(c.longitude -  x.longitude, 2) + pow(c.latitude -  x.latitude, 2))
            if(dist < minDist):
                minDist = dist
                point1 = x;
                if(i < len(self.gps_entries)-1):
                    point2 = self.gps_entries[i+1]
                if(i > 0):
                    point3 = self.gps_entries[i-1]

        def Pythagoras (x1, y1, x2, y2):
            return math.sqrt(math.pow((x2 - x1), 2)+ math.pow((y2 - y1), 2))

        def DistancePointLine (px, py, x1, y1, x2, y2):
            if(x1 == x2 and y1 == y2):
                return None
            lineLength = Pythagoras(x1, y1, x2, y2)

            u1 = (((px - x1) * (x2 - x1)) + ((py - y1) * (y2 - y1)))
            u = u1 / (lineLength * lineLength)

            if (u < 0) or (u > 1):
                #// closest point does not fall within the line segment, take the shorter distance
                #// to an endpoint
                ix = Pythagoras(px, py, x1, y1)
                iy = Pythagoras(px, py, x2, y2)
                if ix > iy:
                    DistancePointLine = iy
                else:
                    DistancePointLine = ix
            else:
                # Intersecting point is on the line, use the formula
                ix = x1 + u * (x2 - x1)
                iy = y1 + u * (y2 - y1)
                DistancePointLine = Pythagoras(px, py, ix, iy)

            return DistancePointLine

        if point1 is not None:
            if point2 is None and point3 is not None:
                minDist = DistancePointLine(c.longitude, c.latitude, point1.longitude, point1.latitude, point3.longitude, point3.latitude)

            elif point3 is None and point2 is not None:
                minDist = DistancePointLine(c.longitude, c.latitude, point1.longitude, point1.latitude, point2.longitude, point2.latitude)

            elif point3 is None and point3 is None:
                minDist = Pythagoras(c.longitude, c.latitude, point1.longitude, point1.latitude)

            else:
                minDist =  min(
                    DistancePointLine(c.longitude, c.latitude, point1.longitude, point1.latitude, point2.longitude, point2.latitude),
                    DistancePointLine(c.longitude, c.latitude, point1.longitude, point1.latitude, point3.longitude, point3.latitude)
                )

            return minDist

        else:
            return None


    def export(self):
        f = open('path.kml', 'w')
        i = 0

        kml =   '<?xml version="1.0" encoding="UTF-8"?>\n'
        kml +=  '<kml xmlns="http://www.opengis.net/kml/2.2">\n'
        kml +=      '<Document>\n'
        kml +=          '<name>Paths</name>\n'
        kml +=          '<description>Exported KML file with lines for the GPS and Asterix log files</description>\n'
        kml +=          '<Style id="yellowLineGreenPoly">\n'
        kml +=              '<LineStyle>\n'
        kml +=                  '<color>7f00ffff</color>\n'
        kml +=                  '<width>4</width>\n'
        kml +=              '</LineStyle>\n'
        kml +=              '<PolyStyle>\n'
        kml +=                  '<color>7f00ff00</color>\n'
        kml +=              '</PolyStyle>\n'
        kml +=          '</Style>\n'
        kml +=          '<Style id="redLineGreenPoly">\n'
        kml +=              '<LineStyle>\n'
        kml +=                  '<color>ff0000ff</color>\n'
        kml +=                  '<width>4</width>\n'
        kml +=              '</LineStyle>\n'
        kml +=              '<PolyStyle>\n'
        kml +=                  '<color>7f00ff00</color>\n'
        kml +=              '</PolyStyle>\n'
        kml +=          '</Style>\n'
        kml +=          '<Placemark>'
        kml +=              '<name>GPS Log Path</name>'
        kml +=              '<description>Path generated by the GPS log</description>'
        kml +=              '<styleUrl>#yellowLineGreenPoly</styleUrl>'
        kml +=              '<LineString>'
        kml +=                  '<extrude>1</extrude>'
        kml +=                  '<tessellate>1</tessellate>'
        kml +=                  '<altitudeMode>absolute</altitudeMode>'
        kml +=                  '<coordinates>'
        for entry in self.gps_entries:
            kml += repr(entry.longitude)
            kml += ','
            kml += repr(entry.latitude)
            kml += ',0\n'
        kml +=                  '</coordinates>'
        kml +=              '</LineString>'
        kml +=          '</Placemark>'

		#Iterates over the number of asterisk file entries
        while (i < len(self.core_entries)):
            kml +=          '<Placemark>'
            kml +=              '<name>Core Log TrackNum:'
            kml +=				repr(self.core_entries[i].tn)
            kml +=				'</name>'
            kml +=              '<description>Path generated by the Core log</description>'
            kml +=              '<styleUrl>#redLineGreenPoly</styleUrl>'
            kml +=              '<LineString>'
            kml +=                  '<extrude>1</extrude>'
            kml +=                  '<tessellate>1</tessellate>'
            kml +=                  '<altitudeMode>absolute</altitudeMode>'
            kml +=                  '<coordinates>'
            #Enters the first coordinates of a new track number
            kml += repr(self.core_entries[i].longitude)
            kml += ','
            kml += repr (self.core_entries[i].latitude)
            kml += ',0\n'
            i += 1
            #If the track number changes, stop the loop, and create a new line
            if(i < len(self.core_entries)):
                while (self.core_entries[i-1].tn == self.core_entries[i].tn):
                    print i
                    kml += repr(self.core_entries[i].longitude)
                    kml += ','
                    kml += repr(self.core_entries[i].latitude)
                    kml += ',0\n'
                    i += 1
                    if(i >= len(self.core_entries)):
                        break;
            kml +=                  '</coordinates>'
            kml +=              '</LineString>'
            kml +=          '</Placemark>'
        kml +=      '</Document>\n'
        kml += '</kml>\n'

        f.write(kml)
        f.close()