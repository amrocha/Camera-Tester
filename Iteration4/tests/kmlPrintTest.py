import os.path, sys
sys.path.append(os.path.join(os.path.dirname(os.path.realpath(__file__)), os.pardir))

from Coordinate import Coordinate
from Scenario import Scenario
import FileReader
import FileWriter
import time

gps_entries = FileReader.parseGpsLog('kmlPrintTestGpsFile.log')
core_entries = FileReader.parseCoreLog('kmlPrintTestCoreFile.log')

print 'Test1: valid input'
scenario = Scenario(1, 5.0, '', sys.path[0], '')
FileWriter.export(scenario, gps_entries, core_entries)
print 'kml file printed successfully\n'

print 'Test2: no core data'
scenario = Scenario(1, 5.0, '', sys.path[0], '')
FileWriter.export(scenario, gps_entries, list())
print 'kml file printed successfully\n'

print 'Test3: no GPS data'
scenario = Scenario(1, 5.0, '', sys.path[0], '')
FileWriter.export(scenario, list(), core_entries)
print 'kml file printed successfully\n'

print 'Test4: no core or GPS data'
scenario = Scenario(1, 5.0, '', sys.path[0], '')
FileWriter.export(scenario, list(), list())
print 'kml file printed successfully\n'

print 'Test5: None value scenarios'
try:
    scenario = Scenario(1, 5.0, '', sys.path[0], '')
    FileWriter.export(scenario, None, core_entries)
    print 'Test failed: None value for GPS data did not throw error'
except (TypeError), e:
    print 'Error thrown successfully for None value for GPS data'
try:
    scenario = Scenario(1, 5.0, '', sys.path[0], '')
    FileWriter.export(scenario, gps_entries, None)
    print 'Test failed: None value for core file did not throw error'
except (TypeError), e:
    print 'Error thrown successfully for None value for core data'
try:
    scenario = Scenario(1, 5.0, '', sys.path[0], '')
    FileWriter.export(None, gps_entries, core_entries)
    print 'Test failed: None value for Scenario object did not throw error'
except (TypeError, AttributeError), e:
    print 'Error thrown successfully for None value for Scenario object'

