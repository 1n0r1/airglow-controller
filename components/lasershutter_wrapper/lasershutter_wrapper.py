import clr
import sys
import os
import zugbruecke
from zugbruecke import CtypesSession
import zugbruecke.ctypes as ctypes
import pythonnet
import numpy as np

ctypes64 = CtypesSession(arch = 'win64')
PiUsb = ctypes64.windll.LoadLibrary('PiUsb.dll')

class LaserShutter:
    def __init__(self, serial=527):
        a = ctypes.c_int()
        
        PiUsb.piConnectShutter(ctypes.byref(a), ctypes.c_int(serial))
        print(a)
    
    def setState(self, serial=1):
        i = c_int()
        b = PiUsb.piSetShutterState(1, 527)
        print(a)
    