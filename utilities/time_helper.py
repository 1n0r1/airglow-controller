from time import sleep
import ephem
from datetime import date, datetime, timedelta
# import utilities.config as config
from config import config


class TimeHelper:
    site_location = ephem.Observer()

    def __init__(self):
        print(config)
        self.site_location.lat = config["latitude"]
        self.site_location.lon = config["longitude"]
        self.site_location.date = datetime.now()
        self.site_location.elevation = config["elevation"]
        self.sun = ephem.Sun()

    def getSunrise(self):
        return ephem.localtime(self.site_location.next_rising(self.sun))

    def getSunset(self):
        return ephem.localtime(self.site_location.next_setting(self.sun))

    def getHousekeeping(self):
        return self.getSunset() - timedelta(minutes=config["startHousekeeping"])

    def waitUntilHousekeeping(self):
        while (datetime.now() < self.getHousekeeping()):
            sleep(5)
        return

    def waitUntilStartTime(self):
        while (datetime.now() < self.getSunset()):
            sleep(5)
        return
