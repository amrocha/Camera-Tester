#Test 1
#Files:
# - gps.log
# - Corefile.log
#Expected Results:
# - To be filled out later
import os.path, sys
sys.path.append(os.path.join(os.path.dirname(os.path.realpath(__file__)), os.pardir))

from Scenario import Scenario

s = Scenario(1, 8, 'gps.log', 'Corefile.log')
s.run()
#s.export()