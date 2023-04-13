import os
import sys
import logging
import signal
import scipy
import numpy
import pickle
from time import sleep
from datetime import datetime, timedelta
import smtplib, ssl
from config import config, skyscan_config
from schedule import observations

import utilities.time_helper
from utilities.image_taker import Image_Helper

from googleapiclient.discovery import build
from google_auth_oauthlib.flow import InstalledAppFlow
from google.auth.transport.requests import Request
# for encoding/decoding messages in base64
from base64 import urlsafe_b64decode, urlsafe_b64encode
# for dealing with attachement MIME types
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from email.mime.image import MIMEImage
from email.mime.audio import MIMEAudio
from email.mime.base import MIMEBase
from mimetypes import guess_type as guess_mime_type

from components.camera import getCamera
from components.lasershutter.shutter import LaserShutter
from components.sky_scanner import SkyScanner
from components.skyalert import SkyAlert
from components.powercontrol import PowerControl

try:
    # logger file
    log_name = config['log_dir'] + config['site'] + datetime.now().strftime('_%Y%m%d_%H%M%S.log')
    logging.basicConfig(filename=log_name, encoding='utf-8',
                        format='%(asctime)s %(message)s',  level=logging.DEBUG)


    timeHelper = utilities.time_helper.TimeHelper()
    sunrise = timeHelper.getSunrise()
    logging.info('Sunrise time set to ' + str(sunrise))
    sunset = timeHelper.getSunset()
    logging.info('Sunset time set to ' + str(sunset))

    # 30 min before house keeping time
    timeHelper.waitUntilHousekeeping(deltaMinutes=-30)

    # Turn on power
    powerControl = PowerControl(config['powerSwitchAddress'], config['powerSwitchUser'], config['powerSwitchPassword'])
    powerControl.turnOn(config['AndorPowerPort'])
    powerControl.turnOn(config['SkyScannerPowerPort'])
    powerControl.turnOn(config['LaserPowerPort'])


    logging.info('Waiting until Housekeeping time: ' +
                str(timeHelper.getHousekeeping()))
    timeHelper.waitUntilHousekeeping()


    # Housekeeping
    lasershutter = LaserShutter()
    skyscanner = SkyScanner(skyscan_config['max_steps'], skyscan_config['azi_offset'], skyscan_config['zeni_offset'], skyscan_config['azi_world'], skyscan_config['zeni_world'], skyscan_config['number_of_steps'], skyscan_config['port_location'])
    camera = getCamera("Andor")

    # Signal to response to interupt/kill signal
    def signal_handler(sig, frame):
        skyscanner.go_home()
        camera.turnOffCooler()
        camera.shutDown()
        logging.info('Exiting')
        sys.exit(0)
    signal.signal(signal.SIGINT, signal_handler)


    skyscanner.go_home()

    # Setup camera
    camera.setReadMode()
    camera.setImage(hbin=config['hbin'], vbin=config['vbin'])
    camera.setShiftSpeed()
    camera.setTemperature(config["temp_setpoint"])
    camera.turnOnCooler()
    logging.info('Set camera temperature to %.2f C' % config["temp_setpoint"])


    logging.info("Waiting for sunset: " + str(sunset))
    timeHelper.waitUntilStartTime()
    logging.info('Sunset time start')

    # Create data directroy based on the current sunset time
    data_folder_name = config['data_dir'] + sunset.strftime('%Y%m%d')
    logging.info('Creating data directory: ' + data_folder_name)
    isExist = os.path.exists(data_folder_name)
    if not isExist:
        os.makedirs(data_folder_name)

    imageTaker = Image_Helper(data_folder_name, camera,
                            config['site'], config['latitude'], config['longitude'], config['instr_name'], config['hbin'], config['vbin'], SkyAlert(config['skyAlertAddress']))

    # Take initial images
    if datetime.now() < (sunset + timedelta(minutes=10)):
        bias_image = imageTaker.take_bias_image(config["bias_expose"], 0, 0)
        dark_image = imageTaker.take_dark_image(config["dark_expose"], 0, 0)
        laser_image = imageTaker.take_laser_image(
            config["laser_expose"], skyscanner, lasershutter, config["azi_laser"], config["zen_laser"])
        if config['laser_timedelta'] is not None:
            config['laser_lasttime'] = datetime.now()
    else:
        logging.info('Skipped initial images because we are more than 10 minutes after sunset')
        if config['laser_timedelta'] is not None:
            config['laser_lasttime'] = datetime.now()


    # Main loop
    while (datetime.now() <= sunrise):
        for observation in observations:
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
            world_az, world_zeni = skyscanner.get_world_coords()
            logging.info("The Sky Scanner has moved to azi: %.2f, and zeni: %2f" %(world_az, world_zeni))
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
                                                    observation['skyScannerLocation'][1], skyscanner)

            image_sub = scipy.signal.convolve2d(
                new_image[config['i1']:config['i2'], config['j1']:config['j2']], numpy.ones((config['N'], config['N']))/config['N']**2, mode='valid')
            image_intensity = (numpy.percentile(image_sub, 75) - numpy.percentile(
                image_sub, 25))*numpy.cos(numpy.deg2rad(observation['skyScannerLocation'][1]))

            observation['lastIntensity'] = image_intensity
            observation['lastExpTime'] = observation['exposureTime']

            logging.info('Image intensity: ' + str(image_intensity))

            # Check if we should take a laser image
            logging.info('Time since last laser ' +  str(datetime.now() - config['laser_lasttime']))
            take_laser = (datetime.now() - config['laser_lasttime']) > config['laser_timedelta']
            logging.info('Take_laser is ' + str(take_laser))
            if take_laser:
                world_az, world_zeni = skyscanner.get_world_coords()
                logging.info("The Sky Scanner is pointed at laser position of azi: %.2f and zeni %.2f" %(world_az, world_zeni))
                logging.info('Taking laser image')
                laser_image = imageTaker.take_laser_image(
                    config["laser_expose"], skyscanner, lasershutter, config["azi_laser"], config["zen_laser"])
                config['laser_lasttime'] = datetime.now()



    skyscanner.go_home()

    logging.info('Warming up CCD')
    camera.turnOffCooler()
    while (camera.getTemperature() < -20):
        logging.info('CCD Temperature: ' + str(camera.getTemperature()))
        sleep(10)

    logging.info('Shutting down CCD')
    camera.shutDown()

    powerControl = PowerControl(config['powerSwitchAddress'], config['powerSwitchUser'], config['powerSwitchPassword'])
    powerControl.turnOff(config['AndorPowerPort'])
    powerControl.turnOff(config['SkyScannerPowerPort'])
    powerControl.turnOff(config['LaserPowerPort'])

    logging.info('Executed flawlessly, exitting')

except Exception as e:
    logging.error(e)

    receiver_emails = [
        "khanhn2@illinois.edu",
        "jmakela@illinois.edu"
    ]

    email = "airglowuaotest@gmail.com"
    picklecred = "/home/airglow/airglow/airglow-controller/token.pickle"
    gmailcred = "/home/airglow/airglow/airglow-controller/gmailcredential.json"

    def gmail_authenticate():
        creds = None
        if os.path.exists(picklecred):
            with open(picklecred, "rb") as token:
                creds = pickle.load(token)
        if not creds or not creds.valid:
            if creds and creds.expired and creds.refresh_token:
                creds.refresh(Request())
            else:
                flow = InstalledAppFlow.from_client_secrets_file(gmailcred, SCOPES)
                creds = flow.run_local_server(port=0)
            with open(picklecred, "wb") as token:
                pickle.dump(creds, token)
        return build('gmail', 'v1', credentials=creds)

    def build_message(destination, obj, body):
        message = MIMEText(body)
        message['to'] = destination
        message['from'] = email
        message['subject'] = obj
        return {'raw': urlsafe_b64encode(message.as_bytes()).decode()}

    def send_message(service, destination, obj, body):
        return service.users().messages().send(
            userId="me",
            body=build_message(destination, obj, body)
        ).execute()

    print("sending mail")
    subject = "Airglow UAO Error"
    message = """
This message is sent from UAO FPI site. The program encountered the following error:\

        """
    message = message + str(e)

    SCOPES = ['https://mail.google.com/']
    service = gmail_authenticate()
    for destination in receiver_emails:
        send_message(service, destination, subject, message)