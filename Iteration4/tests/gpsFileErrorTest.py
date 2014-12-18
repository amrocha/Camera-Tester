import os.path, sys
sys.path.append(os.path.join(os.path.dirname(os.path.realpath(__file__)), os.pardir))

import FileReader

goodFileCoordinates = FileReader.parseGpsLog('gpsFileErrorTestGoodFile.log')
print 'Test 1:', '\n', 'gps file successfully parsed. number of entries: ', len(goodFileCoordinates), '\n'

print 'Test 2:'
FileReader.parseGpsLog('gpsFileErrorTestBadFile.log')

print '\nTest 3:'
FileReader.parseGpsLog('this_is_not_a_file.log')

print '\nTest 4:'
try:
    FileReader.parseGpsLog(None)
except (TypeError), e:
    print 'None value error handled successfully' 
try:
    FileReader.parseGpsLog(3)
except (TypeError), e:
    print 'int value error handled successfully' 
