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


# logger file
log_name = config['log_dir'] + config['site'] + datetime.now().strftime('_%Y%m%d_%H%M%S.log')
logging.basicConfig(filename=log_name, encoding='utf-8',
                    format='%(asctime)s %(message)s',  level=logging.DEBUG)

powerControl = PowerControl()
powerControl.turnOn(config['AndorPowerPort'])
powerControl.turnOn(config['SkyScannerPowerPort'])
powerControl.turnOn(config['LaserPowerPort'])
# powerControl.turnOn(config['LaserShutterPowerPort'])

# Housekeeping
logging.info('Initializing LaserShutter')
lasershutter = LaserShutter()
logging.info('Initializing SkyScanner')
skyscanner = SkyScanner(skyscan_config['max_steps'], skyscan_config['azi_offset'], skyscan_config['zeni_offset'], skyscan_config['azi_world'], skyscan_config['zeni_world'], skyscan_config['number_of_steps'], skyscan_config['port_location'])
logging.info('Initializing CCD')
camera = getCamera("Andor")


def signal_handler(sig, frame):
    skyscanner.go_home()
    camera.turnOffCooler()
    camera.shutDown()
    logging.info('Exiting')
    sys.exit(0)
signal.signal(signal.SIGINT, signal_handler)


camera.setReadMode()
camera.setImage()
camera.setShiftSpeed()
camera.setTemperature(config["temp_setpoint"])
camera.turnOnCooler()
logging.info('Set camera temperature to %.2f C' % config["temp_setpoint"])


# Create data directroy based on the current sunset time
data_folder_name = config['data_dir'] + 'lasertest'
logging.info('Creating data directory: ' + data_folder_name)
isExist = os.path.exists(data_folder_name)
if not isExist:
    os.makedirs(data_folder_name)

imageTaker = Image_Helper(data_folder_name, camera,
                          config['site'], config['latitude'], config['longitude'], config['instr_name'], 2, 2, SkyAlert())

# JJM the (2,2) at the end is XBin and YBin. These need to be parameters sent in from the config file and also needs to
# affect the CCD setup


for i in range(10):
    skyscanner.go_home()
    laser_image = imageTaker.take_laser_image(config["laser_expose"], skyscanner, lasershutter, config["azi_laser"], config["zen_laser"])
    sleep(10)

