import ephem
import datetime
import config


class Observer:
    site_location = ephem.Obersver()
    sun = ephem.sun()

    def __init__(self) -> None:
        self.site_location.lat = config["latitude"]
        self.site_location.lon = config["longitude"]
        self.site_location.date = datetime.datetime.now()
        self.site_location.elevation = config["elevation"]

    def getSunrise(self):
        ephem.localtime(self.site_location.next_rising(self.sun))

    def getSunset(self):
        ephem.localtime(self.site_location.next_setting(self.sun))
