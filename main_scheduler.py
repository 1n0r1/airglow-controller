import logging
import h5py
from utilities.image_taker import Image_Helper
from time import sleep
import ephem
from datetime import datetime, timedelta, timezone, date
import utilities.time_helper
from config import config
from schedule import observations
import sys
import os
from components.camera import getCamera
from components.lasershutter_i2c.shutter import LaserShutter
from components.sky_scanner import SkyScanner
from pathlib import Path

# logger file

logging.basicConfig(filename='example.log',
                    encoding='utf-8', format='%(asctime)s %(message)s',  level=logging.DEBUG)


# from filterwheel import FilterWheel


timeHelper = utilities.time_helper.TimeHelper()
sunrise = timeHelper.getSunrise()
sunset = timeHelper.getSunset()
logging.info('Sunrise time set to ' + sunrise + 'Sunset time set to ' + sunset)

# find location of sun and moon
d = datetime.utcnow()
sun, moon = ephem.Sun(), ephem.Moon()
sun_location = sun.compute(d)
moon_location = moon.compute(d)
print(sun_location, moon_location)



# TODO: close laser_shutter

timeHelper.waitUntilHousekeeping()
logging.info('Housekeeping time start')

# housekeeping operations


# initialise skyscanned, camera, filterwheel


# Housekeeping
lasershutter = LaserShutter()
skyscanner = SkyScanner()
camera = getCamera("Andor")
skyscanner.go_home()
camera.setReadMode()


# TODO: filterwheel

# sets temperature
camera.setTemperature(config["temp_setpoint"])
camera.turnOnCooler()
logging.info('Set camera temperature')


# Wait until sunset
timeHelper.waitUntilStartTime()
logging.info('Sunset time start')


data_folder_name = date.today()
Path('../data/').mkdir(data_folder_name)
imageTaker = Image_Helper('../data/' + data_folder_name, camera)

# take dark, bias, laser image
bias_image = imageTaker.take_initial_image(config["bias_expose"], 0, 0)
logging.info('bias')
dark_image = imageTaker.take_initial_image(config["dark_expose"], 0, 0)
logging.info('dark')
laser_image = imageTaker.take_laser_image(
    config["laser_expose"], skyscanner, lasershutter, config["azi_laser"], config["zen_laser"])
logging.info('laser')


# Start main loop
image_count = 1
while (datetime.now() <= sunrise):
    # take images
    # TODO
    for observation in observations:
        # perform tasks as specified
        # TODO
        skyscanner.set_pos_real(
            observation["skyScannerLocation"][0], observation["skyScannerLocation"][1])
        new_image = imageTaker.take_normal_image(
            observation["exposureTime"], observation['skyScannerLocation'][0], observation['skyScannerLocation'[1]])
        image_count = image_count + 1
        logging.info('image' + str(image_count))
        # take laser


# Prepare to sleep

# Cool down camera
# Disconnect components
# Send data to server??
