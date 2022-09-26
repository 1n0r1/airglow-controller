cimport andorsdk
from errorcodestable cimport code2msg

from cython.operator import dereference
from libc.stdlib cimport malloc, free


cdef class Andorsdk:
    
    def __cinit__(self):
        sta = andorsdk.Initialize(NULL)
        print(code2msg(sta))
    
    def getTemperature(self) -> int:
        cdef int * t = <int*> malloc(sizeof(int))
        sta = andorsdk.GetTemperature(t)
        print(code2msg(sta))
        cdef int re = dereference(t)
        return re
    
    def setTemperature(self, int a):
        sta = andorsdk.SetTemperature(a)
        print(code2msg(sta))

        sta = andorsdk.CoolerON()
        print(code2msg(sta))
        
        return

    def turnOffCooler(self):
        sta = andorsdk.CoolerOFF()
        print(code2msg(sta))
        
        return

    def shutDown(self):
        sta = andorsdk.ShutDown()
        print(code2msg(sta))
        return