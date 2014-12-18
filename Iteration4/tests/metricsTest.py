import os.path, sys
sys.path.append(os.path.join(os.path.dirname(os.path.realpath(__file__)), os.pardir))

from Scenario import Scenario
from Coordinate import Coordinate

#tests Scenario.calculateMetrics

#longitude and latitude aren't used in the current implementation, since distances are already calculated and used as input, so they can be set arbitrarily
coreLogPath = list()
coreLogPath.append(Coordinate('230001.550',-1,0,0))
coreLogPath.append(Coordinate('230001.000',1,0,0))
coreLogPath.append(Coordinate('231959.999',1,0,0))
coreLogPath.append(Coordinate('232005.000',-1,0,0))
coreLogPath.append(Coordinate('233908.000',-1,0,0))
coreLogPath.append(Coordinate('234211.000',2,0,0))
coreLogPath.append(Coordinate('235601.000',3,0,0))
coreLogPath.append(Coordinate('000101.000',4,0,0))
coreLogPath.append(Coordinate('000601.000',-1,0,0))
coreLogPath.append(Coordinate('001301.000',5,0,0))

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
print 'Start Time: ', scenario.totalResult.startTime                                                    #expected: 230000.000
print 'End Time: ', scenario.totalResult.endTime                                                        #expected: 001301.000
print 'Detection percent: ', scenario.totalResult.detectionPercent, '%'                                 #expected: 60%
print 'ID changes: ', scenario.totalResult.idChanges                                                    #expected: 4
print 'Min distance', scenario.totalResult.minPositonalAccuracy                                         #expected: 2.1
print 'Max distance', scenario.totalResult.maxPositionalAccuracy                                        #expected: 7.5
print 'Average postional Accuracy', scenario.totalResult.averagePositionalAccuracy                      #expected: 5.35
print 'Percent within ', scenario.maxRadius, 'm: ', scenario.totalResult.percentWithinMaxRadius, '%'    #expected: 33.333...%

#20 minute segments
print '\nNumber of 20 minute segments: ', len(scenario.twentyMinuteResults)
for i in range(0, len(scenario.twentyMinuteResults)):                                                                   #expected: four 20 minute segments
    print '\nStart Time: ', scenario.twentyMinuteResults[i].startTime                                                   #expected: 230000.000, 232000.000, 234000.000,  000000.000
    print 'End Time: ', scenario.twentyMinuteResults[i].endTime                                                         #expected: 231959.999, 233959.999, 235959.999,  001301.000
    print 'Detection percent: ', scenario.twentyMinuteResults[i].detectionPercent, '%'                                  #expected: 66.666...%, 0%,         100%,        66.666...%
    print 'Min distance', scenario.twentyMinuteResults[i].minPositonalAccuracy                                          #expected: 5.3,        99999,      2.1,         4.3
    print 'Max distance', scenario.twentyMinuteResults[i].maxPositionalAccuracy                                         #expected: 6.6,        -1,         7.5,         6.3
    print 'Average postional Accuracy', scenario.twentyMinuteResults[i].averagePositionalAccuracy                       #expected: 5.95,       -1,         4.8,         5.3
    print 'ID changes: ', scenario.twentyMinuteResults[i].idChanges                                                     #expected: 0,          -1,         1,           1 
    print 'Percent within ', scenario.maxRadius, 'm: ', scenario.twentyMinuteResults[i].percentWithinMaxRadius, '%'     #expected: 0%,         -1%,        50%,         50%

