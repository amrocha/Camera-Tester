import os.path, sys
sys.path.append(os.path.join(os.path.dirname(os.path.realpath(__file__)), os.pardir))

from Scenario import Scenario
from Coordinate import Coordinate

#tests Scenario.calculateMetrics

#time, longitude and latitude aren't used in the current implementation, so they can be set arbitrarily
coreLogPath = list()
coreLogPath.append(Coordinate(0,-1,0,0))
coreLogPath.append(Coordinate(0,1,0,0))
coreLogPath.append(Coordinate(0,1,0,0))
coreLogPath.append(Coordinate(0,-1,0,0))
coreLogPath.append(Coordinate(0,-1,0,0))
coreLogPath.append(Coordinate(0,2,0,0))
coreLogPath.append(Coordinate(0,2,0,0))
coreLogPath.append(Coordinate(0,3,0,0))
coreLogPath.append(Coordinate(0,-1,0,0))
coreLogPath.append(Coordinate(0,3,0,0))

distances = list()
distances.append(1.2) #ignored
distances.append(5.3)
distances.append(6.6)
distances.append(3.3) #ignored
distances.append(9.7) #ignored
distances.append(2.1)
distances.append(7.5)
distances.append(4.3)
distances.append(5.7) #ignored
distances.append(6.3)

scenario = Scenario(1, 5.0, '', '')
scenario.calculateMetrics(coreLogPath, distances)
print 'Detection percent: ', scenario.detectionPercent, '%'                                 #expected: 60%
print 'ID changes: ', scenario.idChanges                                                    #expected: 2
print 'Min distance', scenario.minPositonalAccuracy                                         #expected: 2.1
print 'Max distance', scenario.maxPositionalAccuracy                                        #expected: 7.5
print 'Average postional Accuracy', scenario.averagePositionalAccuracy                      #expected: 5.35
print 'Percent within ', scenario.maxRadius, 'm: ', scenario.percentWithinMaxRadius, '%'    #expected 33.33%
