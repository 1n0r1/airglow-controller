import os
import sys
import logging
import signal
import scipy
import numpy
from time import sleep
from datetime import datetime, timedelta


from config import config, skyscan_config
from schedule import observations

import utilities.time_helper
from utilities.image_taker import Image_Helper

from components.camera import getCamera
from components.lasershutter.shutter import LaserShutter
from components.sky_scanner import SkyScanner
from components.skyalert import SkyAlert
from components.powercontrol import PowerControl
# from filterwheel import FilterWheel



powerControl = PowerControl()
powerControl.turnOn(config['SkyScannerPowerPort'])
print("turned on SkyScanner")
skyscanner = SkyScanner(skyscan_config['max_steps'], skyscan_config['azi_offset'], skyscan_config['zeni_offset'], skyscan_config['azi_world'], skyscan_config['zeni_world'], skyscan_config['number_of_steps'], skyscan_config['port_location'])

skyscanner.go_home()
print("finished going home")
skyscanner.jog(30,30,.3,.3,50)
powerControl.turnOff(config['SkyScannerPowerPort'])


