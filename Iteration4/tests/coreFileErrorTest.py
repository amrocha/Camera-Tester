import os.path, sys
sys.path.append(os.path.join(os.path.dirname(os.path.realpath(__file__)), os.pardir))

import FileReader


goodFileCoordinates = FileReader.parseCoreLog('coreFileErrorTestGoodFile.log', 0, 0)
print 'Test 1:', '\n', 'core file successfully parsed. number of entries: ', len(goodFileCoordinates), '\n'

print 'Test 2:'
FileReader.parseCoreLog('coreFileErrorTestBadFile.log', 0, 0)

print '\nTest 3:'
FileReader.parseCoreLog('this_is_not_a_file.log', 0, 0)

print '\nTest 4:'
try:
    FileReader.parseCoreLog(None, 0, 0)
except (TypeError), e:
    print 'None value error handled successfully' 
try:
    FileReader.parseCoreLog(3, 0, 0)
except (TypeError), e:
    print 'int value error handled successfully' 
