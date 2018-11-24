from time import sleep, time
from importlib import *
import g
import traceback

class ROBOT:
    
    def __init__(self):
        global module
        module = __import__(g.module)
