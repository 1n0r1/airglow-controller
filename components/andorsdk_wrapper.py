import ctypes as ctypes
from telnetlib import STATUS
andorlib = ctypes.CDLL("/usr/local/lib/libandor.so")


def getTemperature():
    # Define return type of GetTemperature
    andorlib.GetTemperature.restype = ctypes.c_uint
    
    temp = ctypes.c_int(0)
    statuss = andorlib.GetTemperature(ctypes.POINTER(temp))
    print(statuss)
    return temp