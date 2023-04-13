import requests
from time import sleep
import logging
from requests.adapters import HTTPAdapter, Retry

# Ambient temp 
# Sky Temperature 
# Dampness
# Darkness
# Humidity (absolute percentage)
# Wind Speed
# Power check (Boolean)
# Barometric Pressure (hPa * 100)

class SkyAlert():
    def __init__(self, address) -> None:
        self.address = address

    def getList(self):
        arr = []

        count = 5
        while count != 0:
            try:
                arr = requests.get(url=self.address, timeout=10).text.split()
                count = 0
            except:
                count = count - 1
                sleep(5)
        if len(arr) == 0:
            arr = [0, 0, 0, 0, 0, 0, 0, 0, 0, 0]
            logging.error('Cannot communicate with SkyAlert')
        while len(arr) < 9:
            arr.append(0)
        return arr

    def getAmbientTemperature(self) -> float:
        # Unit: Degree C
        x = self.getList()
        return float(x[1])
    
    def getSkyTemperature(self) -> float:
        # Unit: Degree C
        x = self.getList()
        return float(x[2])

    def getDampnessValue(self) -> float:
        # x > 990 : dry
        # 990 > x > 970 : damp
        # 970 > x : wet
        x = self.getList()
        return float(x[3])

    def getBrightnessValue(self) -> float:
        # x > 500 : day
        # 500 > x > 250 : dim
        # 250 > x : dark
        x = self.getList()
        return float(x[4])

    def getHumidity(self) -> float:
        # Unit: %
        x = self.getList()
        return float(x[5])
        
    def getWindSpeed(self) -> float:
        # Unit: unknown, need complex math to get value
        x = self.getList()
        return float(x[6])
        
    def getPowerCheck(self) -> float:
        # 1: power is good, 0: power has failed (wait, if power failed how can it send this signal)
        x = self.getList()
        return float(x[7])

    def getPressure(self) -> float:
        # Unit: 10^2 Pa
        x = self.getList()
        return float(x[8])