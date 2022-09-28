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
    
    def getTemperatureRange(self) -> int:
        cdef int * t1 = <int*> malloc(sizeof(int))
        cdef int * t2 = <int*> malloc(sizeof(int))
        sta = andorsdk.GetTemperatureRange(t1, t2)
        print(code2msg(sta))
        cdef int re1 = dereference(t1)
        cdef int re2 = dereference(t2)
        return (re1, re2)

    def setTemperature(self, int a):
        cdef int t = a
        sta = andorsdk.SetTemperature(t)
        print(code2msg(sta))

        sta = andorsdk.CoolerON()
        print(code2msg(sta))
        
        return

    def turnOffCooler(self):
        sta = andorsdk.CoolerOFF()
        print(code2msg(sta))
        
        return

    def turnOnCooler(self):
        sta = andorsdk.CoolerON()
        print(code2msg(sta))
        
        return

    def shutDown(self):
        sta = andorsdk.ShutDown()
        print(code2msg(sta))
        return


    def setParameters(self):
        sta = andorsdk.SetAcquisitionMode(1)
        print(code2msg(sta))

        sta = andorsdk.SetReadMode(4)
        print(code2msg(sta))

        sta = andorsdk.SetExposureTime(10)
        print(code2msg(sta))

        return

    def startAcquisition(self):
        sta = andorsdk.StartAcquisition()
        print(code2msg(sta))

        return
    
    def getStatus(self):
        cdef int * t = <int*> malloc(sizeof(int))
        sta = andorsdk.GetStatus(t)
        print(code2msg(sta))
        cdef int re = dereference(t)

        return code2msg(re)
    
    def getImage(self):
        cdef int * t = <int*> malloc(sizeof(int))
        sta = GetAcquiredData
        print(code2msg(sta))