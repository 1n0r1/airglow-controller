cimport andorsdk
from errorcodestable cimport code2msg

from cython.operator import dereference
from libc.stdlib cimport malloc, free
import numpy as np

    
def initialize():
    sta = andorsdk.Initialize(NULL)
    return code2msg(sta)

def getTemperature():
    cdef int * t = <int*> malloc(sizeof(int))
    sta = andorsdk.GetTemperature(t)
    cdef int re = dereference(t)
    return (code2msg(sta), re)

def getTemperatureRange():
    cdef int * t1 = <int*> malloc(sizeof(int))
    cdef int * t2 = <int*> malloc(sizeof(int))
    sta = andorsdk.GetTemperatureRange(t1, t2)
    cdef int re1 = dereference(t1)
    cdef int re2 = dereference(t2)
    return (code2msg(sta), re1, re2)

def setTemperature(int a):
    cdef int t = a
    sta = andorsdk.SetTemperature(t)
    return code2msg(sta)
    
def turnOffCooler():
    sta = andorsdk.CoolerOFF()
    return code2msg(sta)
    

def turnOnCooler():
    sta = andorsdk.CoolerON()
    return code2msg(sta)
    

def shutDown():
    sta = andorsdk.ShutDown()
    return code2msg(sta)

def setReadMode(mode=4):
    sta = andorsdk.SetReadMode(mode)
    return code2msg(sta)


def setExposureTime(time):
    sta = andorsdk.SetExposureTime(time)
    return code2msg(sta)

def setShutter(typ=0, mode=0, closingtime=0, openingtime=0):
    sta = andorsdk.SetShutter(typ, mode, closingtime, openingtime)
    return code2msg(sta)

def setAcquisitionMode(mode=1):
    sta = andorsdk.SetAcquisitionMode(mode)
    return code2msg(sta)

def setImage(hbin=2, vbin=2, hstart=1, hend=1024, vstart=1, vend=1024):
    sta = andorsdk.SetImage(hbin, vbin, hstart, hend, vstart,vend)
    return code2msg(sta)


def startAcquisition():
    sta = andorsdk.StartAcquisition()
    return code2msg(sta)


def getStatus():
    cdef int * t = <int*> malloc(sizeof(int))
    sta = andorsdk.GetStatus(t)
    cdef int re = dereference(t)
    return (code2msg(sta), code2msg(re))


def getImage(hbin=2, vbin=2, hstart=1, hend=1024, vstart=1, vend=1024):
    height = (vend - vstart + 1)/vbin
    width = (hend - hstart + 1)/hbin

    cdef at_u32 size = height*width
    cdef at_32 * t = <at_32*> malloc(sizeof(at_32)*size)
    
    sta = andorsdk.GetMostRecentImage(t, size)
    
    if (code2msg(sta) != "DRV_SUCCESS"):
        return (code2msg(sta), 0)

    re = []
    for i in range(0, height):
        row = []
        for j in range(0, width):
            row.append(t[i*width + j])
        re.append(row)
    
    re = np.array(re)
    re = np.flip(re, 0)

    return (code2msg(sta), re)