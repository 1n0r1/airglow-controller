import logging
from utilities.image_taker import Image_Helper
from time import sleep
from datetime import datetime, timedelta, timezone, date
import utilities.time_helper
import sys
import os
import signal
import scipy
import numpy



from config import config
from schedule import observations

from components.camera import getCamera
from components.lasershutter.shutter import LaserShutter
from components.sky_scanner import SkyScanner
from components.skyalert import SkyAlert
from components.powercontrol import PowerControl
# from filterwheel import FilterWheel




# logger file
d = datetime.utcnow()
log_name = config['log_dir'] + config['site'] + \
    d.strftime('_%Y%m%d_%H%M%S.log')
logging.basicConfig(filename=log_name,
                    encoding='utf-8', format='%(asctime)s %(message)s',  level=logging.DEBUG)



timeHelper = utilities.time_helper.TimeHelper()
sunrise = timeHelper.getSunrise()
logging.info('Sunrise time set to ' + str(sunrise))
sunset = timeHelper.getSunset()
logging.info('Sunset time set to ' + str(sunset))

# find location of sun and moon
# JJM NOTE: THIS WON'T WORK. NEED TO SET THE OBSERVER LOCATION. THIS SEEMS TO BE DONE IN THE TIMEHELPER
# PROBABLY WANT TO USE THAT OBSERVER SO WE ONLY HAVE ONE WE ARE KEEPING TRACK OF.
# TODO: location with angle
d = datetime.utcnow()
#sun, moon = ephem.Sun(), ephem.Moon()
#sun_location = sun.compute(d)
#logging.info('Location of the sun is ' + sun_location)
#moon_location = moon.compute(d)
#logging.info('Location of the moon is ' + moon_location)

#logging.info('Housekeeping time is ' + moon_location)



timeHelper.waitUntilHousekeeping(deltaMinutes = -30) # 30 min before house keeping time

powerControl = PowerControl()
powerControl.turnOn(config['AndorPowerPort'])
powerControl.turnOn(config['SkyScannerPowerPort'])
powerControl.turnOn(config['LaserPowerPort'])
# powerControl.turnOn(config['LaserShutterPowerPort'])


logging.info('Waiting until Housekeeping time: ' + str(timeHelper.getHousekeeping()))
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
skyscanner = SkyScanner(21600, 20, 20, 30, 30,
                        19.31, .45, 45, 45, 50, '/dev/ttyUSB0')
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
### JJM the (2,2) at the end is XBin and YBin. These need to be parameters sent in from the config file and also needs to
### affect the CCD setup
imageTaker = Image_Helper(data_folder_name, camera,
                          config['site'], config['latitude'], config['longitude'], config['instr_name'], 2, 2, SkyAlert())

if datetime.utcnow() < (sunset + timedelta(minutes=10)):
    # take dark, bias, laser image
    # JJM NOTE, AGAIN, THESE LOGGING ENTIRES SHOULD PROBABLY LIVE INSIDE THE FUNCTIONS
    bias_image = imageTaker.take_bias_image(config["bias_expose"], 0, 0)
    dark_image = imageTaker.take_dark_image(config["dark_expose"], 0, 0)
    laser_image = imageTaker.take_laser_image(
        config["laser_expose"], skyscanner, lasershutter, config["azi_laser"], config["zen_laser"])
    if config['laser_timedelta'] is not None:
        # save the time
        config['laser_lasttime'] = datetime.utcnow()
else:
    logging.info(
        'Skipped initial images because we are more than 10 minutes after sunset')
    if config['laser_timedelta'] is not None:
        # save the time
        config['laser_lasttime'] = datetime.utcnow()

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

        
        logging.info('Moving SkyScanner to: %.2f, %.2f' % (
            observation['skyScannerLocation'][0], observation['skyScannerLocation'][1]))
        skyscanner.set_pos_real(
            observation["skyScannerLocation"][0], observation['skyScannerLocation'][1])
        logging.info('Taking sky exposure')


        if (observation['lastIntensity'] == 0 or observation['lastExpTime'] == 0):
            observation['exposureTime'] = 300
        else:
            observation['exposureTime'] = observation['desiredIntensity']*observation['lastExpTime']/observation['lastIntensity']

        logging.info('Calculated exposure time: ' + str(observation['exposureTime']))

        new_image = imageTaker.take_normal_image(observation['imageTag'],
                                                 observation['exposureTime'],
                                                 observation['skyScannerLocation'][0],
                                                 observation['skyScannerLocation'][1])


        # TODO: Will need to put into config
        i1 = 150
        j1 = 150
        i2 = 200
        j2 = 200
        N = 5
        image_sub = scipy.signal.convolve2d(new_image[i1:i2,j1:j2], numpy.ones((N,N))/N**2, mode='valid')
        image_intensity = numpy.percentile(image_sub, 75) - numpy.percentile(image_sub, 25)

        observation['lastIntensity'] = image_intensity
        observation['lastExpTime'] = observation['exposureTime']

        logging.info('Image intensity: ' + str(image_intensity))




        image_count = image_count + 1

        # Check if we should take a laser image
        take_laser = False
        logging.info('Time since last laser ' + str(datetime.utcnow() - config['laser_lasttime']))
        logging.info(str(datetime.utcnow()))
        logging.info(str(config['laser_lasttime']))
        logging.info(str(config['laser_timedelta']))
        logging.info((datetime.utcnow() - config['laser_lasttime']) > config['laser_timedelta'])
#        if config['laser_timedelta'] is None:
#            print('None')
#            take_laser = True
#        elif (datetime.utcnow() - config['laser_lasttime']) > config['laser_timedelta']:
        take_laser = (datetime.utcnow() - config['laser_lasttime']) > config['laser_timedelta']
        if ((datetime.utcnow() - config['laser_lasttime']) > config['laser_timedelta']):
            print('Here')
            take_laser = True
        logging.info('take_laser is ' + str(take_laser))

        if take_laser:
            logging.info('Taking laser image')
            laser_image2 = imageTaker.take_laser_image(
                config["laser_expose"], skyscanner, lasershutter, config["azi_laser"], config["zen_laser"])
            logging.info('image' + str(image_count))
            config['laser_lasttime'] = datetime.utcnow()

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
