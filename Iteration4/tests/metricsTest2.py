import os.path, sys
sys.path.append(os.path.join(os.path.dirname(os.path.realpath(__file__)), os.pardir))

from Scenario import Scenario
from Coordinate import Coordinate

#tests Scenario.calculateMetrics

#longitude and latitude aren't used in the current implementation, since distances are already calculated and used as input, so they can be set arbitrarily
coreLogPath = list()
coreLogPath.append(Coordinate('230001.550',1,0,0,0,0))
coreLogPath.append(Coordinate('230004.000',4,0,0,0,0))
coreLogPath.append(Coordinate('230444.000',2,0,0,0,0))
coreLogPath.append(Coordinate('230664.000',7,0,0,0,0))
coreLogPath.append(Coordinate('232508.000',4,0,0,0,0))
coreLogPath.append(Coordinate('232522.000',2,0,0,0,0))
coreLogPath.append(Coordinate('232722.000',3,0,0,0,0))
coreLogPath.append(Coordinate('232755.000',4,0,0,0,0))
coreLogPath.append(Coordinate('233122.000',3,0,0,0,0))
coreLogPath.append(Coordinate('233422.000',5,0,0,0,0))

distances = list()
distances.append(1.2)
distances.append(5.3)
distances.append(6.6)
distances.append(3.3)
distances.append(9.7)
distances.append(2.1)
distances.append(7.5)
distances.append(4.3)
distances.append(7.7)
distances.append(5.0)

scenario = Scenario(1, 5.0, '', '', '')
scenario.calculateMetrics(coreLogPath, distances)

print 'Overall Results'
print 'Start Time: ', scenario.totalResult.startTime                                                    #expected: 230000.000
print 'End Time: ', scenario.totalResult.endTime                                                        #expected: 233422.000
print 'Detection percent: ', scenario.totalResult.detectionPercent, '%'                                 #expected: 100%
print 'ID changes: ', scenario.totalResult.idChanges                                                    #expected: 9
print 'Min distance', scenario.totalResult.minPositonalAccuracy                                         #expected: 1.2
print 'Max distance', scenario.totalResult.maxPositionalAccuracy                                        #expected: 9.7
print 'Average postional Accuracy', scenario.totalResult.averagePositionalAccuracy                      #expected: 5.27
print 'Percent within ', scenario.maxRadius, 'm: ', scenario.totalResult.percentWithinMaxRadius, '%'    #expected: 50%

#20 minute segments
print '\nNumber of 20 minute segments: ', len(scenario.twentyMinuteResults)
for i in range(0, len(scenario.twentyMinuteResults)):                                                                   #expected: two 20 minute segments
    print '\nStart Time: ', scenario.twentyMinuteResults[i].startTime                                                   #expected: 230000.000, 232000.000
    print 'End Time: ', scenario.twentyMinuteResults[i].endTime                                                         #expected: 231959.999, 233422.000
    print 'Detection percent: ', scenario.twentyMinuteResults[i].detectionPercent, '%'                                  #expected: 100%,       100%
    print 'Min distance', scenario.twentyMinuteResults[i].minPositonalAccuracy                                          #expected: 1.2,        2.1
    print 'Max distance', scenario.twentyMinuteResults[i].maxPositionalAccuracy                                         #expected: 6.6,        9.7
    print 'Average postional Accuracy', scenario.twentyMinuteResults[i].averagePositionalAccuracy                       #expected: 4.1,        6.05
    print 'ID changes: ', scenario.twentyMinuteResults[i].idChanges                                                     #expected: 3,          5
    print 'Percent within ', scenario.maxRadius, 'm: ', scenario.twentyMinuteResults[i].percentWithinMaxRadius, '%'     #expected: 50%,        50%

