#Test 1
#Files:
# - gps.log
# - Corefile.log
#Expected Results:
# - To be filled out later
import os.path, sys
sys.path.append(os.path.join(os.path.dirname(os.path.realpath(__file__)), os.pardir))
from Tkinter import Tk
from tkFileDialog import askopenfilename
from tkFileDialog import askdirectory
from Scenario import Scenario

Tk().withdraw() #prevents root window from appearing
print 'Please enter GPS file'
gps = askopenfilename()
print 'Please enter Asterisk file'
core = askopenfilename()
print 'Please enter directory to save .txt'
txtDir = askdirectory()
s = Scenario(1, 8, txtDir, gps, core)
s.run()
#s.export()