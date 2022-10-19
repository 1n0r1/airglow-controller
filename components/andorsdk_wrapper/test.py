from time import sleep
import andorsdk
import numpy as np
from PIL import Image

camera = andorsdk.Andorsdk()

camera.setExposureTime(1)
camera.setShutter()
camera.setReadMode()
camera.setAcquisitionMode()
camera.setImage()
camera.startAcquisition()

while (camera.getStatus() != "DRV_IDLE"):
    sleep(1)
    
img = camera.getImage()
print(img)
camera.shutDown()