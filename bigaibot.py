from time import sleep, time
import traceback
import g
import bgbSocketNode
import sys

# Initialize the LCD and Buttons
try:
    g.funInitRobot()

    # fun.StartProgram()
    bgbSocketNode.StartProgram()
except:
    # If there is any error, it will be stored in the log file in the same directory
    logtime = str(time())
    f=open("log" + logtime + ".txt",'a')  
    traceback.print_exc(file=f)  
    f.flush()  
    f.close()

#alice = aiml.Kernel()
#alice.learn("std-startup.xml")
#alice.respond('load aiml b')

#while True:
#	print(alice.respond(input("Enter your message >> ")))
