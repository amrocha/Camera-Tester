import os.path, sys
sys.path.append(os.path.join(os.path.dirname(os.path.realpath(__file__)), os.pardir))

import FileReader

FileReader.parseGpsLog('this_is_not_a_file.log')
FileReader.parseGpsLog('formatErrorTestGpsFile.log')
