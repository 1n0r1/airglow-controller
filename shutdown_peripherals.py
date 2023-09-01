from components.powercontrol import PowerControl

from config import config

# Code to shutdown the peripherals that need to be off during the day (CCD, Laser, SkyScanner)
# This is a hedge against the code crashing and not going through the power down sequence

try:
    powerControl = PowerControl(config['powerSwitchAddress'], config['powerSwitchUser'], config['powerSwitchPassword'])
    powerControl.turnOff(config['AndorPowerPort'])
    powerControl.turnOff(config['SkyScannerPowerPort'])
    powerControl.turnOff(config['LaserPowerPort'])
    powerControl.turnOff(config['FilterWheelPowerPort'])
except:
    print("Error turning peripherals off")
    
