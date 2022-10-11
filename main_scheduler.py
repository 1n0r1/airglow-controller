from time import sleep
import ephem
from datetime import datetime, timedelta, timezone
import utilities.time_helper
from config import config
from schedule import observations

timeHelper = utilities.time_helper.TimeHelper()
sunrise = timeHelper.getSunrise()
sunset = timeHelper.getSunset()

# make sure laser_shutter is closed
# TODO

timeHelper.waitUntilHousekeeping()
# housekeeping operations

# TODO
# initialise skyscanned, camera, filterwheel

timeHelper.waitUntilStartTime()

while (datetime.now() <= sunrise):
    # take images
    # TODO
    for observation in observations:
        # perform tasks as specified
        # TODO
        pass
