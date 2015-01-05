import os.path, sys
sys.path.append(os.path.join(os.path.dirname(os.path.realpath(__file__)), os.pardir))

from Scenario import Scenario
from Coordinate import Coordinate

#tests Scenario.calculateMetrics

#longitude and latitude aren't used in the current implementation, since distances are already calculated and used as input, so they can be set arbitrarily
coreLogPath = list()
coreLogPath.append(Coordinate(23*3600 + 00*60 + 01.550,-1,0,0,0,0)) #23:00:01.550
coreLogPath.append(Coordinate(23*3600 + 00*60 + 01.000, 1,0,0,0,0)) #23:00:01.000
coreLogPath.append(Coordinate(23*3600 + 19*60 + 59.999, 1,0,0,0,0)) #23:19:59.999
coreLogPath.append(Coordinate(23*3600 + 20*60 + 05.000,-1,0,0,0,0)) #23:20:05.000
coreLogPath.append(Coordinate(23*3600 + 39*60 + 08.000,-1,0,0,0,0)) #23:39:08.000
coreLogPath.append(Coordinate(23*3600 + 42*60 + 11.000, 2,0,0,0,0)) #23:42:11.000
coreLogPath.append(Coordinate(23*3600 + 56*60 + 01.000, 3,0,0,0,0)) #23:56:01.000
coreLogPath.append(Coordinate(00*3600 + 01*60 + 01.000, 4,0,0,0,0)) #00:01:01.000
coreLogPath.append(Coordinate(00*3600 + 06*60 + 01.000,-1,0,0,0,0)) #00:06:01.000
coreLogPath.append(Coordinate(00*3600 + 13*60 + 01.000, 5,0,0,0,0)) #00:13:01.000

distances = list()
distances.append(1.2) #ignored
distances.append(5.3)
distances.append(6.6)
distances.append(3.3) #ignored
distances.append(9.7) #ignored
distances.append(2.1)
distances.append(7.5)
distances.append(4.3)
distances.append(7.7) #ignored
distances.append(6.3)

scenario = Scenario(1, 5.0, '', '', '')
scenario.calculateMetrics(coreLogPath, distances)

print 'Overall Results'
print 'Start Time: ', scenario.timeToString(scenario.totalResult.startTime)                             #expected: 230000.000
print 'End Time: ', scenario.timeToString(scenario.totalResult.endTime)                                 #expected: 001301.000
print 'Detection percent: ', scenario.totalResult.detectionPercent, '%'                                 #expected: 60%
print 'ID changes: ', scenario.totalResult.idChanges                                                    #expected: 4
print 'Min distance', scenario.totalResult.minPositonalAccuracy                                         #expected: 2.1
print 'Max distance', scenario.totalResult.maxPositionalAccuracy                                        #expected: 7.5
print 'Average postional Accuracy', scenario.totalResult.averagePositionalAccuracy                      #expected: 5.35
print 'Percent within ', scenario.maxRadius, 'm: ', scenario.totalResult.percentWithinMaxRadius, '%'    #expected: 33.333...%

#20 minute segments
print '\nNumber of 20 minute segments: ', len(scenario.twentyMinuteResults)
for i in range(0, len(scenario.twentyMinuteResults)):                                                                   #expected: four 20 minute segments
    print '\nStart Time: ', scenario.timeToString(scenario.twentyMinuteResults[i].startTime)                            #expected: 230000.000, 232000.000, 234000.000,  000000.000
    print 'End Time: ', scenario.timeToString(scenario.twentyMinuteResults[i].endTime)                                  #expected: 231959.999, 233959.999, 235959.999,  001301.000
    print 'Detection percent: ', scenario.twentyMinuteResults[i].detectionPercent, '%'                                  #expected: 66.666...%, 0%,         100%,        66.666...%
    print 'Min distance', scenario.twentyMinuteResults[i].minPositonalAccuracy                                          #expected: 5.3,        99999,      2.1,         4.3
    print 'Max distance', scenario.twentyMinuteResults[i].maxPositionalAccuracy                                         #expected: 6.6,        -1,         7.5,         6.3
    print 'Average postional Accuracy', scenario.twentyMinuteResults[i].averagePositionalAccuracy                       #expected: 5.95,       -1,         4.8,         5.3
    print 'ID changes: ', scenario.twentyMinuteResults[i].idChanges                                                     #expected: 0,          -1,         1,           1 
    print 'Percent within ', scenario.maxRadius, 'm: ', scenario.twentyMinuteResults[i].percentWithinMaxRadius, '%'     #expected: 0%,         -1%,        50%,         50%

