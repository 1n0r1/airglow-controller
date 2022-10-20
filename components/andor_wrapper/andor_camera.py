
import sys
import os
sys.path.append

# This import only works if andor_camera.py is imported from outside components (see main_scheduler.py for import)
# Will not work if import inside components
from .andorsdk_wrapper import andorsdk

class AndorCamera:

    def __init__(self):
        print(andorsdk.initialize())

    def getTemperature(self):
        re = andorsdk.getTemperature()
        print(re[0])
        return re[1]

    def getTemperatureRange(self):
        re = andorsdk.getTemperatureRange()
        print(re[0])
        return (re[1], re[2])

    def setTemperature(self, t):
        re = andorsdk.setTemperature(t)
        print(re)
        
    def turnOffCooler(self):
        re = andorsdk.turnOffCooler()
        print(re)
        
    def turnOnCooler(self):
        re = andorsdk.turnOnCooler()
        print(re)
        
    def shutDown(self):
        re = andorsdk.shutDown()
        print(re)

    def setReadMode(self, mode=4):
        """Set the read mode
        
        Parameter
        -------
        mode: 4 for image mode
        """
        re = andorsdk.setReadMode(mode)
        print(re)


    def setExposureTime(self, time):
        re = andorsdk.setExposureTime(time)
        print(re)

    def setShutter(self, typ=0, mode=0, closingtime=0, openingtime=0):
        re = andorsdk.setShutter(typ, mode, closingtime, openingtime)
        print(re)

    def setAcquisitionMode(self, mode=1):
        re = andorsdk.setAcquisitionMode(mode)
        print(re)

    def setImage(self, hbin=2, vbin=2, hstart=1, hend=1024, vstart=1, vend=1024):
        self.hbin = hbin
        self.vbin = vbin
        self.hstart = hstart
        self.hend = hend
        self.vstart = vstart
        self.vend = vend
        re = andorsdk.setImage(hbin, vbin, hstart, hend, vstart,vend)
        print(re)


    def startAcquisition(self):
        re = andorsdk.startAcquisition()
        print(re)


    def getStatus(self):
        """Get the current status
        """
        re = andorsdk.getStatus()
        print(re[0])
        return re[1]


    def getImage(self):
        """Get the most recent image
        
        Returns
        -------
        img
            a np 2d array
        """
        
        re = andorsdk.getImage(self.hbin, self.vbin, self.hstart, self.hend, self.vstart, self.vend)
        print(re[0])

        return re[1]