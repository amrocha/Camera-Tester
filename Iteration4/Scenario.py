import FileReader
import FileWriter
from Coordinate import Coordinate
from MetricsResult import MetricsResult
import subprocess, math
import time
from datetime import datetime
#import numpy as np
#import matplotlib.pyplot as plt
#from scipy.optimize import fmin_cobyla
#from decimal import *

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
    def __init__ (self, scenarioID, maxRadius, txtDir, kmlDir, gpsLog, coreLog=None, timeOffset=None):
        self.scenarioID = scenarioID
        self.date = datetime.utcnow()
        self.txtDir = txtDir
        self.kmlDir = kmlDir
        self.coreLog = coreLog
        self.gpsLog = gpsLog
        self.timeOffset = timeOffset
        self.maxRadius = maxRadius

    def run(self):
        if self.coreLog == None:
            self.coreLog = self.runCamSim()
        self.core_entries = FileReader.parseCoreLog(self.coreLog)
        if(self.core_entries == -1):
            return
        self.gps_entries = FileReader.parseGpsLog(self.gpsLog)
        if(self.gps_entries == -1):
            return
        
        self.timeOffset = self.calculateTimeOffset()
        distances = self.comparePath()
        self.calculateMetrics(self.core_entries, distances)
        FileWriter.createDataSheet(self, self.totalResult, self.twentyMinuteResults)
        FileWriter.export(self, self.gps_entries, self.core_entries)
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
        return 33

    """
    coreLogPath is the list of Coordinates from the path that has been matched with the GPS file
    pathDistances is the list of calculated distances between each point in coreLogPath and the GPS path. The coordinate coreLogPath[i] has a distance of pathDistances[i].
    
    for now I've assumed that a tracknum of -1 is used in coreLogPath at any point in time when nothing was detected
    this may need to be changed depending on how the path comparison is implemented
    """
    def calculateMetrics(self, coreLogPath, pathDistances):
        #all counters with an array of length two have the twenty minute segment counter at index 0 and the total counter at index 1
        #index 0 resets every twenty minutes of footage
        
        #for calculating the detection percent
        numUndetected = [0,0]
        
        #for calculating id changes
        previousID = [-1,-1]
        numIDChanges = [-1,-1]
        
        #for calculating the positional accuracy metrics
        totalDist = [0,0]
        minDist = [99999, 99999]
        maxDist = [-1,-1]
        numAboveRadius = [0,0]

        #used for 20 minute time segments
        timeSegmentStart = coreLogPath[0].time[:4] + '00.000'
        timeSegmentStartIndex = 0
        self.twentyMinuteResults = []
        
        for i in range(0, len(coreLogPath)):
            # if 20 minutes have passed, create the results. Then start the next twenty minute segment
            if (int(coreLogPath[i].time[2:4]) - int(timeSegmentStart[2:4]))%60 >= 20:
                self.twentyMinuteResults.append(self.createResult(i - timeSegmentStartIndex, timeSegmentStart, self.addTimeStamps(timeSegmentStart, '001959.999'),
                                                         numUndetected[0], numIDChanges[0], minDist[0], maxDist[0], totalDist[0], numAboveRadius[0]))
                timeSegmentStartIndex = i
                timeSegmentStart = self.addTimeStamps(timeSegmentStart, '002000.00')
                
                #reset all twenty minute segment counters
                numUndetected[0] = 0
                previousID[0] = -1
                numIDChanges[0] = -1
                totalDist[0] = 0
                minDist[0] = 99999
                maxDist[0] = -1
                numAboveRadius[0] = 0
            
            if coreLogPath[i].tn < 0:
                numUndetected[0] += 1
                numUndetected[1] += 1
            else:
                if coreLogPath[i].tn != previousID[0]:
                    previousID[0] = coreLogPath[i].tn
                    numIDChanges[0] += 1
                if coreLogPath[i].tn != previousID[1]:
                    previousID[1] = coreLogPath[i].tn
                    numIDChanges[1] += 1
                totalDist[0] += pathDistances[i]
                totalDist[1] += pathDistances[i]
                if pathDistances[i] < minDist[0]:
                    minDist[0] = pathDistances[i]
                if pathDistances[i] < minDist[1]:
                    minDist[1] = pathDistances[i]
                if pathDistances[i] > maxDist[0]:
                    maxDist[0] = pathDistances[i]
                if pathDistances[i] > maxDist[1]:
                    maxDist[1] = pathDistances[i]
                if pathDistances[i] > self.maxRadius:
                    numAboveRadius[0] += 1
                    numAboveRadius[1] += 1

        #add last segment
        self.twentyMinuteResults.append(self.createResult(len(coreLogPath) - timeSegmentStartIndex, timeSegmentStart, coreLogPath[len(coreLogPath) - 1].time,
                                                 numUndetected[0], numIDChanges[0], minDist[0], maxDist[0], totalDist[0], numAboveRadius[0]))
        
        #create the total result
        self.totalResult = self.createResult(len(coreLogPath), coreLogPath[0].time[:4] + '00.000', coreLogPath[len(coreLogPath) - 1].time,
                                         numUndetected[1], numIDChanges[1], minDist[1], maxDist[1], totalDist[1], numAboveRadius[1])


    #helper method for calculateMetrics
    def createResult(self, length, startTime, endTime, numUndetected, numIDChanges, minDist, maxDist, totalDist, numAboveRadius):
        detectionPercent = float(length - numUndetected) / length * 100
        if length - numUndetected > 0:
            averageDist = totalDist / float(length - numUndetected)
            percentWithinMaxRadius = ((length - numUndetected) - numAboveRadius) / float(length - numUndetected) * 100
        else:
            averageDist = -1
            percentWithinMaxRadius = -1
        result = MetricsResult(startTime, endTime, detectionPercent, numIDChanges, minDist, maxDist, averageDist, percentWithinMaxRadius)
        return result
    
    #adds two timestamps of the format 'HHMMSS.mmm' 
    def addTimeStamps(self, time1, time2):
        second = float(time1[4:]) + float(time2[4:])
        minute = int(time1[2:4]) + int(time2[2:4])
        hour = int(time1[:2]) + int(time2[:2])
        if second >= 60:
            second %= 60
            minute += 1
        if minute >= 60:
            minute %= 60
            hour += 1
        hour %= 24

        if second < 10:
            second = '0' + str(second)
        else:
            second = str(second)
        if len(second) == 2:
            second += '.000'
        elif len(second) == 4:
            second += '00'
        elif len(second) == 5:
            second += '0'
        
        minute = str(minute)
        if len(minute) == 1:
            minute = '0' + minute

        hour = str(hour)
        if len(hour) == 1:
            hour = '0' + hour
        
        return hour + minute + second

    #This function goes through all core points and compares them to the closes gps points
    #then puts the results in a list
    #Need to change so it compares by core path and returns a list of lists

    def comparePath(self):
        pointList = list()
        for point in self.core_entries:
            pointList.append(self.comparePoints(point));

        return pointList

    #Let's try to make sense of this clusterfuck since I didn't comment when I wrote it
    #Goal is finding the minimum distance to the GPS path, return that
    def comparePoints(self, c):
        minDist = 99999     #Initial value for minDist has to be maximum value possible, so it always goes down
        point1 = None
        point2 = None
        point3 = None

        def Pythagoras (x1, y1, x2, y2):
            return math.sqrt(math.pow((x2 - x1), 2)+ math.pow((y2 - y1), 2))

        #Compare all points in the GPS logs to the point c given
        #find closest point

        for (i, x) in enumerate(self.gps_entries):

            dist = Pythagoras(x.longitude, x.latitude, c.longitude, c.latitude)
            if(dist < minDist):
                point1 = None
                point2 = None
                point3 = None

                minDist = dist
                point1 = x;
                if(i < len(self.gps_entries)-1):
                    point2 = self.gps_entries[i+1]
                if(i > 0):
                    point3 = self.gps_entries[i-1]


        def DistancePointLine (px, py, x1, y1, x2, y2):
            if(x1 == x2 and y1 == y2):
                return None
            lineLength = Pythagoras(x1, y1, x2, y2)

            u1 = (((px - x1) * (x2 - x1)) + ((py - y1) * (y2 - y1)))
            u = u1 / (lineLength * lineLength)

            if (u < 0) or (u > 1):
                #closest point does not fall within the line segment, take the shorter distance
                #to an endpoint
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

            elif point2 is not None and point3 is None:
                minDist = DistancePointLine(c.longitude, c.latitude, point1.longitude, point1.latitude, point2.longitude, point2.latitude)

            elif point2 is None and point3 is None:
                minDist = Pythagoras(c.longitude, c.latitude, point1.longitude, point1.latitude)

            else:
                minDist =  min(
                    DistancePointLine(c.longitude, c.latitude, point1.longitude, point1.latitude, point2.longitude, point2.latitude),
                    DistancePointLine(c.longitude, c.latitude, point1.longitude, point1.latitude, point3.longitude, point3.latitude)
                )
            return minDist

        else:
            return None
   
