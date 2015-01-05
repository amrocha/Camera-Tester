import os.path, sys
sys.path.append(os.path.join(os.path.dirname(os.path.realpath(__file__)), os.pardir))

from Scenario import Scenario
from Coordinate import Coordinate

#tests Scenario.calculateMetrics

#longitude and latitude aren't used in the current implementation, since distances are already calculated and used as input, so they can be set arbitrarily
coreLogPath = list()
coreLogPath.append(Coordinate(23*3600 + 00*60 + 01.550,1,0,0,0,0)) #23:00:01.550
coreLogPath.append(Coordinate(23*3600 + 00*60 + 04.000,1,0,0,0,0)) #23:00:04.000
coreLogPath.append(Coordinate(23*3600 + 04*60 + 44.000,1,0,0,0,0)) #23:04:44.000
coreLogPath.append(Coordinate(23*3600 + 06*60 + 64.000,1,0,0,0,0)) #23:06:64.000
coreLogPath.append(Coordinate(23*3600 + 07*60 + 08.000,1,0,0,0,0)) #23:07:08.000
coreLogPath.append(Coordinate(23*3600 +  8*60 + 22.000,1,0,0,0,0)) #23:08:22.000
coreLogPath.append(Coordinate(23*3600 + 11*60 + 22.000,1,0,0,0,0)) #23:11:22.000
coreLogPath.append(Coordinate(23*3600 + 11*60 + 55.000,1,0,0,0,0)) #23:11:55.000
coreLogPath.append(Coordinate(23*3600 + 14*60 + 22.000,1,0,0,0,0)) #23:14:22.000
coreLogPath.append(Coordinate(23*3600 + 17*60 + 22.000,1,0,0,0,0)) #23:17:22.000

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


print 'Test 1:'
try:
    scenario = Scenario(1, 5.0, '', '', '')
    scenario.calculateMetrics(list(), distances)
    print 'Test failed. Should throw an error if coreLogPath is empty'
except (IndexError), e:
    print 'Empty coreLogPath error thrown successfully'

print 'Test 2:'
try:
    scenario = Scenario(1, 5.0, '', '', '')
    scenario.calculateMetrics(coreLogPath, list())
    print 'Test failed. Should throw an error if distances is empty'
except (IndexError), e:
    print 'Empty distances error thrown successfully'

print 'Test 3:'
try:
    scenario = Scenario(1, 5.0, '', '', '')
    scenario.calculateMetrics(None, distances)
    print 'Test failed. Should throw an error if coreLogPath has a None value'
except (TypeError), e:
    print 'None value for coreLogPath error thrown successfully'

print 'Test 4:'
try:
    scenario = Scenario(1, 5.0, '', '', '')
    scenario.calculateMetrics(coreLogPath, None)
    print 'Test failed. Should throw an error if distances has a None value'
except (TypeError), e:
    print 'None value for distances error thrown successfully'


