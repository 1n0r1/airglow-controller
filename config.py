from datetime import timedelta

config = {
    'site': 'UAO',
    'latitude': '40.1106',
    'longitude': '-88.2073',
    'elevation': 222,
    'horizon': '-8.0',
    'instr_name': 'minime05',
    'startHousekeeping': 20,
    'sky_offset_el': 0,
    'sky_offset_az': 0,
    'auto_schedule': 1,
    'temp_setpoint': -70,
    'bias_expose': 0.1,
    'dark_expose': 300,
    'laser_expose': 30,
    'azi_laser': 90,
    'zen_laser': 180,
    'data_dir': '/mnt/data/',
    'log_dir': '/home/airglow/airglow/logfiles/',
    'laser_timedelta': timedelta(minutes=15),
    'laser_lasttime': None,


    'maxExposureTime': 600,
    'moonThresholdAngle': 37,

    # scipy.signal.convolve2d
    'i1': 150,
    'j1': 150,
    'i2': 200,
    'j2': 200,
    'N': 5,


    # Power Ports
    'AndorPowerPort': 2,
    'SkyScannerPowerPort': 4,
    'LaserPowerPort': 5,
    'LaserShutterPowerPort': 8
}

skyscan_config = {
    'max_steps': 21600,
    'sun_location_azi': 20,
    'sun_location_zeni': 20,
    'moon_location_azi': 30,
    'moon_location_zeni': 30,
    'azi_offset': 19.31,
    'zeni_offset': 0.45,
    'azi_world': 45,
    'zeni_world': 45,
    'number_of_steps': 50,
    'port_location': '/dev/ttyUSB0'
}


