import os.path, sys
sys.path.append(os.path.join(os.path.dirname(os.path.realpath(__file__)), os.pardir))

from Coordinate import Coordinate
from Scenario import Scenario
import FileReader
import FileWriter

scenario = Scenario(1, 5.0, '', sys.path[0], '')
gps_entries = FileReader.parseGpsLog('kmlPrintTestGpsFile.log')
core_entries = FileReader.parseCoreLog('kmlPrintTestCoreFile.log')
FileWriter.export(scenario, gps_entries, core_entries)
