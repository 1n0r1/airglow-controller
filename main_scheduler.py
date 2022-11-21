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
import signal





# logger file

d = datetime.utcnow()
log_name = config['log_dir'] + config['site'] + d.strftime('_%Y%m%d_%H%M%S.log')
logging.basicConfig(filename=log_name,
                    encoding='utf-8', format='%(asctime)s %(message)s',  level=logging.DEBUG)


# from filterwheel import FilterWheel


timeHelper = utilities.time_helper.TimeHelper()
sunrise = timeHelper.getSunrise()
sunset = timeHelper.getSunset()
logging.info('Sunset time set to ' + str(sunset))
logging.info('Sunrise time set to ' + str(sunrise))

# find location of sun and moon
### JJM NOTE: THIS WON'T WORK. NEED TO SET THE OBSERVER LOCATION. THIS SEEMS TO BE DONE IN THE TIMEHELPER
### PROBABLY WANT TO USE THAT OBSERVER SO WE ONLY HAVE ONE WE ARE KEEPING TRACK OF.
d = datetime.utcnow()
sun, moon = ephem.Sun(), ephem.Moon()
sun_location = sun.compute(d)
moon_location = moon.compute(d)
print('Sun and moon location:',sun_location, moon_location)

# TODO: close laser_shutter

housekeeping = timeHelper.getHousekeeping()
logging.info('Waiting until Housekeeping time: ' + str(housekeeping))
timeHelper.waitUntilHousekeeping()

# housekeeping operations


# initialise skyscanner, camera, filterwheel


# Housekeeping
### JJM NOTE, THESE LOG ENTRIES WOULD PROBABLY BETTER LIVE INSIDE THE FUNCTIONS.
logging.info('Initializing LaserShutter')
print('Initializing LaserShutter')
lasershutter = LaserShutter()
logging.info('Initializing SkyScanner')
print('Init SkyScanner')
### JJM NOTE, SOME OF THESE PARAMETERS (MAYBE ALL) SHOULD BE IN THE CONFIG FILE. MAYBE
### CREATE ANOTHER DICTIONARY TO STORES THESE? "skyscan_config"?
skyscanner = SkyScanner(21600, 20, 20, 30, 30, 19.31, .45, 45, 45, 50, '/dev/ttyUSB0')
logging.info('Initializing CCD')
print('Init CCD')
camera = getCamera("Andor")

def signal_handler(sig, frame):
    skyscanner.go_home()
    camera.turnOffCooler()
    camera.shutDown()
    print("running the exit")
    logging.info('Exiting')
    sys.exit(0)

signal.signal(signal.SIGINT, signal_handler)
logging.info('Homing Skyscanner')
skyscanner.go_home()
camera.setReadMode()
camera.setImage()

# TODO: filterwheel

# sets temperature
camera.setTemperature(config["temp_setpoint"])
camera.turnOnCooler()
logging.info('Set camera temperature to %.2f C' % config["temp_setpoint"])


# Wait until sunset
logging.info("Waiting for sunset: " + str(sunset))
timeHelper.waitUntilStartTime()
logging.info('Sunset time start')

# Create data directroy based on the current sunset time
data_folder_name = config['data_dir'] + sunset.strftime('%Y%m%d')
logging.info('Creating data directory: ' + data_folder_name)
isExist = os.path.exists(data_folder_name)
if not isExist:
    # Create a new directory
    os.makedirs(data_folder_name)
imageTaker = Image_Helper(data_folder_name, camera)

if (datetime.utcnow() - sunset) < timedelta(minutes = 10):
    # take dark, bias, laser image
    ### JJM NOTE, AGAIN, THESE LOGGING ENTIRES SHOULD PROBABLY LIVE INSIDE THE FUNCTIONS
    logging.info('Taking initial bias image')
    bias_image = imageTaker.take_initial_image(config["bias_expose"], 0, 0)
    logging.info('Taking initial dark image')
    dark_image = imageTaker.take_initial_image(config["dark_expose"], 0, 0)
    logging.info('Taking initial laser image')
    laser_image = imageTaker.take_laser_image(
        config["laser_expose"], skyscanner, lasershutter, config["azi_laser"], config["zen_laser"])
else:
    logging.info('Skipped initial images because we are more than 10 minutes after sunset')

# Start main loop
image_count = 1
while (datetime.now() <= sunrise):
    # take images
    # TODO
    for observation in observations:
        # perform tasks as specified
        # check for sunrise
        # TODO
        if (datetime.now() >= sunrise):
            logging.info('Inside observation loop, but after sunrise! Exiting')
            break
        logging.info('Moving SkyScanner to: %.2f, %.2f' % (observation['skyScannerLocation'][0], observation['skyScannerLocation'][1]))
        skyscanner.set_pos_real(
            observation["skyScannerLocation"][0], observation["skyScannerLocation"][1])
        logging.info('Taking sky exposure')
        new_image = imageTaker.take_normal_image(
            observation["exposureTime"], observation['skyScannerLocation'][0], observation['skyScannerLocation'][1])
        image_count = image_count + 1
        logging.info('Taking laser image')
        laser_image2 = imageTaker.take_laser_image(config["laser_expose"], skyscanner, lasershutter, config["azi_laser"], config["zen_laser"])
        logging.info('image' + str(image_count))
        # take laser


# Prepare to sleep

# Cool down camera
# Disconnect components
# Send data to server??

logging.info('Sending SkyScanner home')
skyscanner.go_home()
logging.info('Warming up CCD')
camera.turnOffCooler()
logging.info('Shutting down CCD')
camera.shutDown()
