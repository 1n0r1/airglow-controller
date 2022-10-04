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
        # Single Scan
        sta = andorsdk.SetAcquisitionMode(1)
        print(code2msg(sta))

        # Readmode image
        sta = andorsdk.SetReadMode(4)
        print(code2msg(sta))

        # Exposure time
        sta = andorsdk.SetExposureTime(10)
        print(code2msg(sta))

        # Trigger
        sta = andorsdk.SetShutter(0, 0, 0, 0)
        print(code2msg(sta))

        # Full resolution
        sta = andorsdk.SetImage(1,1,1,1024,1,256)
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
        """Get the most recent image
        
        Returns
        -------
        img
            a 2d list of longs
        """

        cdef unsigned long size = 1024*256
        cdef long * t = <long*> malloc(sizeof(long)*size)
        
        sta = andorsdk.GetOldestImage(t, size)
        print(code2msg(sta))

        re = []
        for i in range(0, 256):
            row = []
            for j in range(0, 1024):
                row.append(t[i*1024 + j])
            re.append(row)
        
        return re