import clr
import sys
import os
import zugbruecke
from zugbruecke import CtypesSession
import zugbruecke.ctypes as ctypes
import pythonnet

ctypes64 = CtypesSession(arch='win64')
PiUsb = ctypes64.windll.LoadLibrary('PiUsbNet.dll')

connectShutter = PiUsb.piConnectShutter
