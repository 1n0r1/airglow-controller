from datetime import timedelta

config = {
    'site': 'LOW',
    'latitude': '34.752',
    'longitude': '-111.423',
    'elevation': 2308.0,
    'horizon': '-8.0',
    'instr_name': 'minime11',
    'startHousekeeping': 20,
    'sky_offset_el': 0,
    'sky_offset_az': 0,
    'auto_schedule': 1,
    'temp_setpoint': -70,
    'bias_expose': 0.1,
    'dark_expose': 300,
    'laser_expose': 30,
    'azi_laser': -57.2,
    'zen_laser': -180.0,
    'data_dir': '/home/airglow/airglow/data/',
    'log_dir': '/home/airglow/airglow/logfiles/',
    'laser_timedelta': timedelta(minutes=15),
    'laser_lasttime': None,
    'maxExposureTime': 600,
    'moonThresholdAngle': 37,

    # Camera setting
    'hbin': 2,
    'vbin': 2,

    'skyAlertAddress': 'http://192.168.1.126:81',
    'powerSwitchAddress': '192.168.1.100',
    'powerSwitchUser': 'admin',
    'powerSwitchPassword': 'ionosphere',

    # scipy.signal.convolve2d
    'i1': 150,
    'j1': 150,
    'i2': 200,
    'j2': 200,
    'N': 5,


    # Power Ports
    'AndorPowerPort': 3,
    'SkyScannerPowerPort': 2,
    'LaserPowerPort': 1,
#    'LaserShutterPowerPort': 8,
    'FilterWheelPowerPort': 6, # Need to add this to main_scheduler.py
    'FilterWheelControlPowerPort': 4, # Need to add this to main_scheduler.py
    'CloudSensorPowerPort': 5,
    'NetworkSwitchPowerPort': 7,
    'PCPowerPort': 8,

    # Laser shutter
    'vendorId': 0x0461,
    'productId': 0x0030,

    # Gmaii
    'pickleCred': "/home/airglow/airglow/airglow-controller/token.pickle",
    'gmailCred': "/home/airglow/airglow/airglow-controller/gmailcredential.json",
    'email': "airglowuaotest@gmail.com",
    'receiverEmails': [
        "khanhn2@illinois.edu",
        "jmakela@illinois.edu"
    ]
}

skyscan_config = {
    'max_steps': 21600,
    'sun_location_azi': 20,
    'sun_location_zeni': 20,
    'moon_location_azi': 30,
    'moon_location_zeni': 30,
    'azi_offset': 147.65,
    'zeni_offset': 0.4,
    'azi_world': 45,
    'zeni_world': 45,
    'number_of_steps': 50,
    'port_location': '/dev/ttyKEOSS'
}

filterwheel_config = {
    'port_location': '/dev/ttyRPiFilter',
    'laser_position': 2,
    'park_position': 0
}
