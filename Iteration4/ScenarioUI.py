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


def runUI():
    print 'Please enter GPS file'
    gps = askopenfilename()
    if gps == '':
        print 'Cancelling: No GPS file was selected'
        return
    
    print 'Please enter Asterisk file'
    core = askopenfilename()
    if core == '':
        print 'Cancelling: No Core file was selected'
        return
    
    print 'Please enter directory to save .txt'
    txtDir = askdirectory()
    if txtDir == '':
        print 'Cancelling: No path was selected for the Results file'
        return
    
    print 'Please enter directory to save .kml'
    kmlDir = askdirectory()
    if kmlDir == '':
        print 'Cancelling: No path was selected for the .kml file'
        return

    s = Scenario(1, 8, txtDir, kmlDir, gps, core)
    s.run()
    

runUI()
    
