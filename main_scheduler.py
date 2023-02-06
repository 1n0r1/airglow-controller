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
d = datetime.now()
log_name = config['log_dir'] + config['site'] + \
    d.strftime('_%Y%m%d_%H%M%S.log')
logging.basicConfig(filename=log_name, encoding='utf-8',
                    format='%(asctime)s %(message)s',  level=logging.DEBUG)


timeHelper = utilities.time_helper.TimeHelper()
sunrise = timeHelper.getSunrise()
logging.info('Sunrise time set to ' + str(sunrise))
sunset = timeHelper.getSunset()
logging.info('Sunset time set to ' + str(sunset))

# find location of sun and moon
# JJM NOTE: THIS WON'T WORK. NEED TO SET THE OBSERVER LOCATION. THIS SEEMS TO BE DONE IN THE TIMEHELPER
# PROBABLY WANT TO USE THAT OBSERVER SO WE ONLY HAVE ONE WE ARE KEEPING TRACK OF.
# TODO: location with angle
d = datetime.now()
#sun, moon = ephem.Sun(), ephem.Moon()
#sun_location = sun.compute(d)
#logging.info('Location of the sun is ' + sun_location)
#moon_location = moon.compute(d)
#logging.info('Location of the moon is ' + moon_location)

#logging.info('Housekeeping time is ' + moon_location)


# 30 min before house keeping time
timeHelper.waitUntilHousekeeping(deltaMinutes=-30)

powerControl = PowerControl()
powerControl.turnOn(config['AndorPowerPort'])
powerControl.turnOn(config['SkyScannerPowerPort'])
powerControl.turnOn(config['LaserPowerPort'])
# powerControl.turnOn(config['LaserShutterPowerPort'])


logging.info('Waiting until Housekeeping time: ' +
             str(timeHelper.getHousekeeping()))
timeHelper.waitUntilHousekeeping()


# housekeeping operations
# initialise skyscanner, camera, filterwheel

# Housekeeping
# JJM NOTE, THESE LOG ENTRIES WOULD PROBABLY BETTER LIVE INSIDE THE FUNCTIONS.
logging.info('Initializing LaserShutter')
lasershutter = LaserShutter()
# logging.info('Initializing SkyScanner')
print('Init SkyScanner')
# JJM NOTE, SOME OF THESE PARAMETERS (MAYBE ALL) SHOULD BE IN THE CONFIG FILE. MAYBE
# CREATE ANOTHER DICTIONARY TO STORES THESE? "skyscan_config"?
skyscanner = SkyScanner(skyscan_config['max_steps'], skyscan_config['azi_offset'], skyscan_config['zeni_offset'], skyscan_config['azi_world'], skyscan_config['zeni_world'], skyscan_config['number_of_steps'], skyscan_config['port_location'])
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
# logging.info('Homing Skyscanner')
skyscanner.go_home()

camera.setReadMode()
camera.setImage()  # imporve this logging
camera.setShiftSpeed()


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
# JJM the (2,2) at the end is XBin and YBin. These need to be parameters sent in from the config file and also needs to
# affect the CCD setup
imageTaker = Image_Helper(data_folder_name, camera,
                          config['site'], config['latitude'], config['longitude'], config['instr_name'], 2, 2, SkyAlert())

if datetime.now() < (sunset + timedelta(minutes=10)):
    # take dark, bias, laser image
    # JJM NOTE, AGAIN, THESE LOGGING ENTIRES SHOULD PROBABLY LIVE INSIDE THE FUNCTIONS
    bias_image = imageTaker.take_bias_image(config["bias_expose"], 0, 0)
    dark_image = imageTaker.take_dark_image(config["dark_expose"], 0, 0)
    laser_image = imageTaker.take_laser_image(
        config["laser_expose"], skyscanner, lasershutter, config["azi_laser"], config["zen_laser"])
    if config['laser_timedelta'] is not None:
        # save the time
        config['laser_lasttime'] = datetime.now()
else:
    logging.info(
        'Skipped initial images because we are more than 10 minutes after sunset')
    if config['laser_timedelta'] is not None:
        # save the time
        config['laser_lasttime'] = datetime.now()

# Start main loop
image_count = 1
while (datetime.now() <= sunrise):
    # take images
    # TODO
    for observation in observations:
        # perform tasks as specified
        # check for sunrise
        if (datetime.now() >= sunrise):
            logging.info('Inside observation loop, but after sunrise! Exiting')
            break
        
        currThresholdMoonAngle = skyscanner.get_moon_angle(config['latitude'], config['longitude'], observation['skyScannerLocation'][0], observation['skyScannerLocation'][1])
        logging.info('The current Moon angle Threshold is: %.2f' % currThresholdMoonAngle)
        if (currThresholdMoonAngle <= config['moonThresholdAngle']):
            logging.info('The moonThreshold angle was too small. The current threshold moon angle is:  %.2f' % currThresholdMoonAngle + 
            ' the current direction of telescope is az: %.2f ze: %.2f' % (
                observation['skyScannerLocation'][0], observation['skyScannerLocation'][1]))   
            continue

        logging.info('Moving SkyScanner to: %.2f, %.2f' % (
            observation['skyScannerLocation'][0], observation['skyScannerLocation'][1]))
        skyscanner.set_pos_real(
            observation["skyScannerLocation"][0], observation['skyScannerLocation'][1])
        logging.info('Taking sky exposure')

        if (observation['lastIntensity'] == 0 or observation['lastExpTime'] == 0):
            observation['exposureTime'] = 300
        else:
            observation['exposureTime'] = min(0.5*observation['lastExpTime']*(1 + observation['desiredIntensity']/observation['lastIntensity']),
                                              config['maxExposureTime'])

        logging.info('Calculated exposure time: ' +
                     str(observation['exposureTime']))

        # Take image
        new_image = imageTaker.take_normal_image(observation['imageTag'],
                                                 observation['exposureTime'],
                                                 observation['skyScannerLocation'][0],
                                                 observation['skyScannerLocation'][1])

        # TODO: Will need to put into config
        image_sub = scipy.signal.convolve2d(
            new_image[config['i1']:config['i2'], config['j1']:config['j2']], numpy.ones((config['N'], config['N']))/config['N']**2, mode='valid')
        image_intensity = (numpy.percentile(image_sub, 75) - numpy.percentile(
            image_sub, 25))*numpy.cos(numpy.deg2rad(observation['skyScannerLocation'][1]))

        observation['lastIntensity'] = image_intensity
        observation['lastExpTime'] = observation['exposureTime']

        logging.info('Image intensity: ' + str(image_intensity))

        image_count = image_count + 1

        # Check if we should take a laser image
        take_laser = False
        logging.info('Time since last laser ' +
                     str(datetime.now() - config['laser_lasttime']))
        logging.info(str(datetime.now()))
        logging.info(str(config['laser_lasttime']))
        logging.info(str(config['laser_timedelta']))
        logging.info(
            (datetime.now() - config['laser_lasttime']) > config['laser_timedelta'])
#        if config['laser_timedelta'] is None:
#            print('None')
#            take_laser = True
#        elif (datetime.now() - config['laser_lasttime']) > config['laser_timedelta']:
        take_laser = (datetime.now() -
                      config['laser_lasttime']) > config['laser_timedelta']
        if ((datetime.now() - config['laser_lasttime']) > config['laser_timedelta']):
            print('Here')
            take_laser = True
        logging.info('take_laser is ' + str(take_laser))

        if take_laser:
            logging.info('Taking laser image')
            laser_image2 = imageTaker.take_laser_image(
                config["laser_expose"], skyscanner, lasershutter, config["azi_laser"], config["zen_laser"])
            logging.info('image' + str(image_count))
            config['laser_lasttime'] = datetime.now()

# Prepare to sleep

# Cool down camera
# Disconnect components
# Send data to server??

logging.info('Sending SkyScanner home')
skyscanner.go_home()

logging.info('Warming up CCD')
camera.turnOffCooler()
while (camera.getTemperature() < -20):
    logging.info('CCD Temperature: ' + str(camera.getTemperature()))
    sleep(10)

logging.info('Shutting down CCD')
camera.shutDown()

powerControl.turnOff(config['AndorPowerPort'])
powerControl.turnOff(config['SkyScannerPowerPort'])
powerControl.turnOff(config['LaserPowerPort'])
# powerControl.turnOff(config['LaserShutterPowerPort'])

logging.info('Executed flawlessly, exitting')
