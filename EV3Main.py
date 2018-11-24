
#!/usr/bin/env python3
from time import sleep, time
import traceback
import g
import EV3SocketIO

# Initialize the LCD and Buttons
try:
    g.funInitRobot()

    # fun.StartProgram()
    EV3SocketIO.StartProgram()
except:
    # If there is any error, it will be stored in the log file in the same directory
    logtime = str(time())
    f=open("log" + logtime + ".txt",'a')  
    traceback.print_exc(file=f)  
    f.flush()  
    f.close()