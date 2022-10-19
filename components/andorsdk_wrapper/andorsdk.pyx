cimport andorsdk
from errorcodestable cimport code2msg

from cython.operator import dereference
from libc.stdlib cimport malloc, free
import numpy as np


cdef class Andorsdk:
    hbin=2
    vbin=2
    hstart=1
    hend=1024
    vstart=1
    vend=1024

    def __cinit__(self):
        sta = andorsdk.Initialize(NULL)
        print(code2msg(sta))
    
    def getTemperature(self):
        cdef int * t = <int*> malloc(sizeof(int))
        sta = andorsdk.GetTemperature(t)
        print(code2msg(sta))
        cdef int re = dereference(t)
        return re
    
    def getTemperatureRange(self):
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
        

    def turnOffCooler(self):
        sta = andorsdk.CoolerOFF()
        print(code2msg(sta))
        

    def turnOnCooler(self):
        sta = andorsdk.CoolerON()
        print(code2msg(sta))
        

    def shutDown(self):
        sta = andorsdk.ShutDown()
        print(code2msg(sta))

    def setReadMode(self, mode=4):
        """Set the read mode
        
        Parameter
        -------
        mode: 4 for image mode
        """
        sta = andorsdk.SetReadMode(mode)
        print(code2msg(sta))


    def setExposureTime(self, time):
        sta = andorsdk.SetExposureTime(time)
        print(code2msg(sta))

    def setShutter(self, typ=0, mode=0, closingtime=0, openingtime=0):
        sta = andorsdk.SetShutter(typ, mode, closingtime, openingtime)
        print(code2msg(sta))

    def setAcquisitionMode(self, mode=1):
        sta = andorsdk.SetAcquisitionMode(mode)
        print(code2msg(sta))

    def setImage(self, hbin=2, vbin=2, hstart=1, hend=1024, vstart=1, vend=1024):
        self.hbin = hbin
        self.vbin = vbin
        self.hstart = hstart
        self.hend = hend
        self.vstart = vstart
        self.vend = vend
        sta = andorsdk.SetImage(hbin, vbin, hstart,hend, vstart,vend)
        print(code2msg(sta))


    def startAcquisition(self):
        sta = andorsdk.StartAcquisition()
        print(code2msg(sta))

    
    def getStatus(self):
        """Get the current status
        """
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
            a np 2d array
        """
        height = (self.vend - self.vstart + 1)/self.vbin
        width = (self.hend - self.hstart + 1)/self.hbin

        cdef at_u32 size = height*width
        cdef at_32 * t = <at_32*> malloc(sizeof(at_32)*size)
        
        sta = andorsdk.GetMostRecentImage(t, size)
        print(code2msg(sta))

        re = []
        for i in range(0, height):
            row = []
            for j in range(0, width):
                row.append(t[i*width + j])
            re.append(row)
        
        re = np.array(re)
        re = np.flip(re, 0)

        return re