import pythonnet

import clr
import sys
import os
import numpy as np

clr.AddReference('PiUsbNet')

from PiUsbNet import *
class LaserShutter:
    def __init__(self, serial=527):
        shutter: PiUsbNet.Shutter = Shutter()
        shutter.Open(527)
        
    # def find(self):
        # piFindShutters(int* DeviceCount, int* SerialNumberArray, int ArraySize)
        # PiUsb.piFindShutters.argtypes = [ctypes.POINTER(ctypes.c_int), ctypes.POINTER(ctypes.c_int), ctypes.c_int] 
        # PiUsb.piFindShutters.restype = ctypes.c_int
        # a = ctypes.c_int(2)
        # b = ctypes.c_int(2)
        
        # c = PiUsb.piFindShutters(ctypes.byref(a), ctypes.byref(b), ctypes.c_int(1))
        # print(c)
        # print(a)
        # print(b)


    # def setState(self, serial=1):
        # i = c_int()
        # b = PiUsb.piSetShutterState(1, 527)
        # print(a)