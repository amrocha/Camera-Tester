import os.path, sys
sys.path.append(os.path.join(os.path.dirname(os.path.realpath(__file__)), os.pardir))

from Scenario import Scenario
from MetricsResult import MetricsResult
import FileWriter

totalResult = MetricsResult(23*3600 + 00*60 + 00.000, 00*3600 + 13*60 + 01.000, 60, 4, 2.1, 7.5, 5.35, 33.333)

twentyMinuteResults = list()
twentyMinuteResults.append(MetricsResult(23*3600 + 00*60 + 00.000, 23*3600 + 19*60 + 59.999, 66.666, 5.3, 6.6, 7.5, 5.35, 33.333))
twentyMinuteResults.append(MetricsResult(23*3600 + 20*60 + 00.000, 23*3600 + 39*60 + 59.999, 0, 99999, -1, -1, -1, -1))
twentyMinuteResults.append(MetricsResult(23*3600 + 40*60 + 00.000, 23*3600 + 59*60 + 59.999, 100, 2.1, 7.5, 4.8, 1, 50))
twentyMinuteResults.append(MetricsResult(00*3600 + 13*60 + 01.000, 00*3600 + 13*60 + 01.000, 66.666, 4.3, 6.3, 5.3, 1, 50))

print 'Test1: Valid input'
scenario = Scenario(1, 5.0, sys.path[0], '', 'example_gps.log', 'example_core.log', 4)  
FileWriter.createDataSheet(scenario, totalResult, twentyMinuteResults)
print 'Results file printed successfully\n'

"""
EXPECTED: taken from first successful test

Scenario ID: 1
Date: 2014-10-27 02:44:24.171000
Time taken: 0:00:00
GPS log files used: example_gps.log
Asterisk file used: example_core.log
Time offset: 4
Maximum radius of detection: 5.0 meters

Overall testing results :
Detection percentage: 60%
Positional accuracy (min, max, avg): 2.1, 7.5, 5.35
ID changes: 4
Percentage of points within maximum radius: 33.333%

Results from 23:00:00.000 to 23:19:59.999
Detection percentage: 66.666%
Positional accuracy (min, max, avg): 6.6, 7.5, 5.35
ID changes: 5.3
Percentage of points within maximum radius: 33.333%

Results from 23:20:00.000 to 23:39:59.999
Detection percentage: 0%
Positional accuracy (min, max, avg): -1, -1, -1
ID changes: 99999
Percentage of points within maximum radius: -1%

Results from 23:40:00.000 to 23:59:59.999
Detection percentage: 100%
Positional accuracy (min, max, avg): 7.5, 4.8, 1
ID changes: 2.1
Percentage of points within maximum radius: 50%

Results from 00:13:01.000 to 00:13:01.000
Detection percentage: 66.666%
Positional accuracy (min, max, avg): 6.3, 5.3, 1
ID changes: 4.3
Percentage of points within maximum radius: 50%
"""


print 'Test2: None value scenarios'
try:
    scenario = Scenario(1, 5.0, sys.path[0], '', 'example_gps.log', 'example_core.log', 4) 
    FileWriter.createDataSheet(scenario, totalResult, None)
    print 'Test failed: None value for twentyMinuteResults did not throw error'
except (TypeError), e:
    print 'Error thrown successfully for None value for twentyMinuteResults'
try:
    scenario = Scenario(1, 5.0, sys.path[0], '', 'example_gps.log', 'example_core.log', 4) 
    FileWriter.createDataSheet(scenario, None, twentyMinuteResults)
    print 'Test failed: None value for totalResult did not throw error'
except (TypeError, AttributeError), e:
    print 'Error thrown successfully for None value for totalResult'
try:
    scenario = Scenario(1, 5.0, sys.path[0], '', 'example_gps.log', 'example_core.log', 4) 
    FileWriter.createDataSheet(None, totalResult, twentyMinuteResults)
    print 'Test failed: None value for Scenario object did not throw error'
except (TypeError, AttributeError), e:
    print 'Error thrown successfully for None value for Scenario object'








