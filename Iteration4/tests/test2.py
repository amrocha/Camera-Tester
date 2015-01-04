import os.path, sys
sys.path.append(os.path.join(os.path.dirname(os.path.realpath(__file__)), os.pardir))

from Scenario import Scenario
from MetricsResult import MetricsResult
import FileWriter

print sys.path[0]
s = Scenario(1, 5.0, sys.path[0], '.', sys.path[0]+'/package/gps/24042014day_rny13.log', sys.path[0]+'/package/core/day/', 4)
s.run()