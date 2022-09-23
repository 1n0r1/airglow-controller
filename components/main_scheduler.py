from components.file_reader import ControlFileRead
from components.log_directory import create_log_file
from components.shutter_laser import Close, isClose
import file_reader
import log_directory
import shutter_laser


# function that reads files
ControlFileRead("XYZ.text")

# create directory to save nights data info
create_log_file("day_date")

# specific variables
logOrder = 312
logOrderShort = 31

# create various log files
create_log_file("XYZ Input")

# define image-type counters // create a struct to make prettier
ImageSequenceL = 0  # L refers to laser images
ImageSequenceB = 0  # B refers to bias images
ImageSequenceX = 0  # X refers to 630 images
ImageSequenceD = 0  # D refers to dark count image in sky mode
ImageSequenceF = 0  # F refers to flat-field images
ImageSequenceK = 0  # K refers to laser dark image

# make sure the shutter is closed

if (not isClose()):
    Close()

# read sunsrise/set file
ControlFileRead("Sunrise/set file")

# if read wasnt successfull or if we are afteer the endNightTime perform functions


# save dates into variables // make a struct to make is prettier
DateStart = str(date_of_beginNightTime)
DateEnd = str(date_of_endNightTime)
TimeStart = str(int(beginNightTime)/1000)
TimeEnd = str(int(endNightTime)/1000)

# log all this info
create_log_file("XYZ")

#  Initialize the iCycle counter which counts the position within the default (Cardinal)
# observing cycle.  Used if we lose communications and have to fall back in to a default
# observing mode.

iCycle = -1

#  Before observations, we need to initialize the camera and sky scanner.  This takes some time, so we will
#   start some of this housekeeping 20 minutes before datataking should commence.
beginHousekeepingTime = beginNightTime - 1200

WAIT_UNTIL beginHousekeepingTime

# below will all be functions that do the following
# Clear quick look graphics in the analyze program
SETUP ANALYZE

# Move the SkyScanner to the home position and wait for this to complete
SETUP FPI SKYSCAN

# Initialize the Andor camera and turn on cooling
SETUP CAMERA FPI
SETUP COOLER FPI

#  Get the current status of the Andora camera after initialization
GET_STATUS CAMERA FPI, TEMPERATURE, temperature
GET_STATUS CAMERA FPI, STATE, CurrentState
